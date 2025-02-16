# InformAI
RAG Application using Frontend and FastAPI.         



InformAI is a web-based Retrieval-Augmented Generation (RAG) question-answering assistant built with FastAPI. It enables users to ask questions and receive contextual responses based on indexed documents. The application supports adding web links to enrich the knowledge base using FAISS for vector storage.


## Features

- FastAPI-based Backend: Provides efficient API endpoints for Q&A and document ingestion.

- Retrieval-Augmented Generation (RAG): Enhances response accuracy with relevant document retrieval.

- FAISS Vector Database: Stores indexed documents for quick search and retrieval.

- CORS Middleware Support: Allows communication with multiple frontend clients.

- Web Link Ingestion: Adds web page content to the knowledge base for better context.

## Installation

#### Prerequisites

- Python 3.8+

- FastAPI

- LangChain

- FAISS

- Pydantic

## Setup

Clone the repository:
```
git clone https://github.com/Akashvarma26/InformAI.git
```
```
cd InformAI
```
Create a virtual environment and activate it:
```
python -m venv venv_name
```
```
venv\Scripts\activate
```
Install dependencies:
```
pip install -r requirements.txt
```         
# Usage

## Running the API Server
To start the FastAPI server,first change directory to src and run:
```
uvicorn app:app --reload
``` 
The API will be accessible at http://127.0.0.1:8000.

# Endpoints

1. Chat API

Endpoint: POST /chat

Description: Processes user queries and returns answers with supporting documents.
```
Request Body:

{
  "message": "What is artificial intelligence?"
}

Response:

{
  "question": "What is artificial intelligence?",
  "answer": "Artificial intelligence (AI) refers to...",
  "documents": [
    {"title": "Intro to AI", "content": "AI is the simulation of human intelligence..."}
  ]
}
```
2. Add Web Link to Knowledge Base

Endpoint: POST /link

Description: Adds content from a URL to the FAISS vector database.
```
Request Body:

{
  "url": "https://example.com/ai-article"
}

Response:

{
  "response": "10 documents from url https://example.com/ai-article added to InformAI's Vector DB successfully. ✅"
}
```
## Frontend Compatibility

InformAI supports multiple frontend implementations. Ensure CORS settings allow communication with your frontend domain.