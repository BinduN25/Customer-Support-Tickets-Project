# Customer Support Ticket Analysis and Prevention System (Infosys Springboard Internship)

This repository contains the implementation of a **Customer Support Ticket Analysis and Prevention System** developed as part of my Infosys Springboard Internship. The project is designed to enhance the efficiency of customer support by leveraging sentiment analysis, automated response generation, and issue escalation handling, integrated seamlessly using FastAPI and Zapier.

## Importance of Customer Support Ticket Analysis
In today's fast-paced world, customer satisfaction is pivotal for any organization. Analyzing customer support tickets helps identify recurring issues, gauge customer sentiment, and streamline response mechanisms. This not only enhances the customer experience but also reduces the workload on support teams, allowing them to focus on critical tasks.

---

## Project Structure

### Initial Data Analysis
The project begins with an exploratory **data analysis** conducted on two datasets located in the `analysis` folder under the `rough` directory. This step was crucial to:
1. Understand the structure and quality of the data.
2. Identify patterns and trends that inform the subsequent machine learning models.

---

### Sentiment Analysis 
This module determines the sentiment of the user based on their ticket. By classifying tickets into positive, neutral, or negative sentiments, the system:
- Prioritizes tickets requiring immediate attention.
- Provides insights into the overall customer satisfaction levels.

Key steps:
1. Preprocessing ticket data.
2. Training and testing a sentiment classification model.
3. Outputting the sentiment score for each ticket.


---

### Issue Escalation
This module identifies tickets requiring escalation based on specific keywords and patterns. If an issue is marked for escalation:
- The ticket is forwarded to a human agent for review.
- Automated responses are bypassed to ensure personalized handling.

Key steps:
1. Keyword-based filtering and rule-based classification.
2. Forwarding flagged tickets for manual intervention.

---

### Response Automation
This module generates automated responses for tickets using two distinct approaches:

1. **Classical Machine Learning and Transformer-based Classification**:
   - Products are classified based on ticket content.
   - Predefined templates generate responses tailored to the classified product category.



2. **Pipeline Using Gemini and Vector Search**:
   - Embeddings are created using the ticket content.
   - Vector search retrieves the most relevant response.
   - A personalized response is generated based on context and user history.

---

### Integration with FastAPI and Zapier
The entire system is integrated using FastAPI to expose API endpoints for each module. These endpoints are connected through Zapier to:
- Automate workflows and email responses.
- Seamlessly handle escalations and response generation.

## Zapier integration (trigger and action)

This integration ensures:
- Scalability of the system.
- A unified platform for executing all functionalities.
- Sent email response (not formatted properly)
  
---

## Requirements
### Data
The `data` folder contains all datasets used in this project. Ensure to download the data for running the modules.

### Keys and Dependencies
To run the system, the following keys and dependencies are required:

1. **JSON Key for Google Sheets**
   - [Generate a Google Sheets API Key](https://developers.google.com/sheets/api/quickstart/python)

2. **Gemini API Key**
   - [Sign up for Gemini API Key](https://ai.google.dev/gemini-api/docs/api-key)

3. **Pinecone API DOCS**
   - [Get a Pinecone API Key](https://docs.pinecone.io/reference/api/introduction)

4. **Dataset**
   - Download from the `data` folder in this repository.

5. **FastAPI and Uvicorn**
   - Install using:
     ```bash
     pip install fastapi uvicorn
     ```

---

## Conclusion
This Customer Support Ticket Analysis and Prevention System is a comprehensive solution for modern customer support challenges. By combining sentiment analysis, issue escalation, and automated responses, the system optimizes ticket handling and ensures customer satisfaction. The seamless integration with FastAPI and Zapier makes it scalable and adaptable to diverse business needs.
