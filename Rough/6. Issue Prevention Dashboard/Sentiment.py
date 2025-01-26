import json
import time
import logging
from google.generativeai import configure, GenerativeModel

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def get_sentiment(title, chat_history):
    configure(api_key="AIzaSyAOq6bzppdHPJSNLP2HYrNJJ_P9Md6lOCA")
    model = GenerativeModel("gemini-pro")

    # Define the function schema for the output
    function_schema = {
        "name": "save_sentiment",
        "description": "Save sentiment related data.",
        "parameters": {
            "type": "object",
            "properties": {
                "thought": {
                    "type": "string",
                    "description": "Your thoughts on sentence and sentiment."
                },
                "sentiment": {
                    "type": "string",
                    "description": "The sentiment of the conversation."
                }
            },
            "required": ["thought", "sentiment"]
        }
    }

    # Create the prompt
    prompt = f"""
    You are a Support Agent. Determine the sentiment of the following ticket based on the title and chat history. 
    Use the JSON schema strictly for your response:
    {json.dumps(function_schema['parameters'], indent=3)}

    Title: "{title}"
    Chat History: "{chat_history}"

    Examples:
    1. ...
    Customer: Hi, I need help with a refund. I returned a product but haven’t received the money.
    Agent: Sorry for the inconvenience. Could you provide your order number?
    ...
    Sentiment: frustrated

    2. ...
    Customer: Thanks for resolving the issue quickly.
    Agent: You're welcome! Let us know if you need further assistance.
    ...
    Sentiment: positive

    3. ...
    Customer: Does this product come in black?
    Agent: Yes, it does. Would you like me to check availability for you?
    ...
    Sentiment: neutral
    """

    try:
        # Add a short delay to prevent API rate limiting
        time.sleep(1)
        
        # Generate the response from the model
        response = model.generate_content(prompt)

        # Log the raw response for debugging
        logging.debug(f"Raw response: {response.text}")

        # Parse the JSON response
        sentiment_data = json.loads(response.text.strip())

        # Validate the sentiment value
        thought = sentiment_data.get("thought", "No thought provided.")
        sentiment = sentiment_data.get("sentiment")

        if sentiment not in ["positive", "negative", "neutral", "frustrated"]:
            raise ValueError("Invalid sentiment value returned by the model.")

        return {
            "sentiment": sentiment,
            "thought": thought
        }

    except json.JSONDecodeError:
        logging.error("Failed to decode JSON response.")
        return {"error": "JSON decoding error."}
    except ValueError as e:
        logging.error(f"Validation error: {e}")
        return {"error": str(e)}
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return {"error": "Unexpected error."}

# Example usage
title = "Cisco router issue"
chat_history = """
Dear Customer Support Team, We are experiencing a complete outage affecting our enterprise network involving Cisco Router ISR4331. 
This disruption is critically impacting our secure WAN connectivity across all domains, urgently requiring your immediate intervention. 
Due to this issue, our company has halted various essential operations, significantly affecting our services and commitments to clients. 
As our technical team has not been able to resolve the problem internally, we need your expert support to diagnose and rectify this issue swiftly. 
Please consider this a high priority and provide us with the necessary technical assistance to restore our network’s functionality. 
Thank you for your prompt attention.
"""
result = get_sentiment(title, chat_history)
print(result)
