import openai
import pinecone
import pandas as pd
import re
import json

# Load dataset
df = pd.read_csv('add_gseet_data.csv_filepath')
df.head()

# Initialize Pinecone
pinecone.init(api_key="pcsk_gBbQu_FPvCVmX9BNxyHAjZZ1oHLvFXYvo5T3z8JezwNLxvSAjvwCZQ4Wvawe3aGUiaQC7")

# Connect to an existing index or create a new one
index_name = "example-index"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine"
    )
index = pinecone.Index(index_name)

# Initialize Generative AI model
import google.generativeai as genai
genai.configure(api_key="AIzaSyAOq6bzppdHPJSNLP2HYrNJJ_P9Md6lOCA")
model = genai.GenerativeModel("gemini-pro")


def extract_issue_details(title, body):
    """
    Extract product and issue details from user input.
    """
    prompt = f"""Extract the product name and issue from the following:
    Title: {title}
    Body: {body}
    Provide JSON output with keys 'product_name' and 'issue_sentence'."""

    response = model.generate_content(prompt)
    cleaned_data = re.sub(r"```[a-zA-Z]*\n|\n```", "", response.text.strip())

    try:
        extracted_json = json.loads(cleaned_data)
        return extracted_json.get('product_name', 'Unknown'), extracted_json.get('issue_sentence', 'Unknown')
    except json.JSONDecodeError:
        raise ValueError(f"Error parsing JSON response:\n{cleaned_data}")


def find_similar_issues(issue_sentence, top_k=3):
    """
    Retrieve similar issues from the Pinecone index.
    """
    embedding_response = genai.embed_content(
        model="models/embedding-001",
        content=issue_sentence,
        task_type="retrieval_document"
    )
    embedding = embedding_response['embedding']
    result = index.query(vector=embedding, top_k=top_k, include_metadata=True)

    return result['matches']


def generate_response(product_name, issue_sentence, similar_issues):
    """
    Create a personalized response using the provided details.
    """
    # Ensure we have enough similar issues
    while len(similar_issues) < 3:
        similar_issues.append({'metadata': {'issue': 'No similar issue found', 'response': 'No response available'}})

    prompt = f"""
    Product: {product_name}
    User Issue: {issue_sentence}

    Similar issues and responses:
    1. {similar_issues[0]['metadata']['issue']} - {similar_issues[0]['metadata']['response']}
    2. {similar_issues[1]['metadata']['issue']} - {similar_issues[1]['metadata']['response']}
    3. {similar_issues[2]['metadata']['issue']} - {similar_issues[2]['metadata']['response']}

    Generate a subject and body for a helpful response in JSON format.
    """
    response = model.generate_content(prompt)
    cleaned_data = re.sub(r"```[a-zA-Z]*\n|\n```", "", response.text.strip())

    try:
        extracted_json = json.loads(cleaned_data)
        return extracted_json.get('subject', 'No subject'), extracted_json.get('body', 'No body')
    except json.JSONDecodeError:
        raise ValueError(f"Error parsing JSON response:\n{cleaned_data}")


def handle_issue(title, body):
    """
    End-to-end workflow for resolving user issues.
    """
    # Extract details
    product_name, issue_sentence = extract_issue_details(title, body)

    # Retrieve similar issues
    similar_issues = find_similar_issues(issue_sentence)

    # Generate response
    subject, response_body = generate_response(product_name, issue_sentence, similar_issues)

    return {
        "subject": subject,
        "response": response_body
    }


# Example usage
title = "App crashes on startup"
body = "Whenever I open the app, it just crashes without any error message. Please help!"

try:
    result = handle_issue(title, body)
    print("Generated Response:")
    print("Subject:", result["subject"])
    print("Body:", result["response"])
except ValueError as e:
    print("Error:", e)
