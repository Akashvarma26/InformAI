# Importing required libraries
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from utils.rag import get_answer_and_docs
from utils.faiss_maker import docs_to_vdb
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Initiating app
app=FastAPI(
    title="InformAI",
    description="Web based RAG question answering Assistant",
    version="0.1.0"
)

# Setting up middle ware to communicate with react frontend
origins = [
    #"http://localhost:3000",  # React default port
    #"http://127.0.0.1:3000",
    "http://127.0.0.1:5500"     # Html local server port
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
)

class Message(BaseModel):
    message:str


# RAG App chat API
@app.post("/chat",description="Response from InformAI")
def chat(message:Message):
    response=get_answer_and_docs(message.message)
    response_content={
        "question":message.message,
        "answer":response["answer"],
        "documents":[doc.dict() for doc in response['context']]
    }
    return JSONResponse(content=response_content,status_code=200)

# RAG App input link API
@app.post("/link",description="Web link input method API for InformAI context section.")
def link(url:str):
    try:
        db,val_len=docs_to_vdb(url=url)
        db.save_local("utils/vectordatabase/faiss_index")
        return JSONResponse(content={"response":f"{val_len} documents from url {url} added to InformAI's Vector DB successfully. ✅"},status_code=200)
    except Exception as e:
        return JSONResponse(content=f"Error: Enter correct URL that can be uploaded to Vector DB. ❌    EXCEPTION : {str(e)}", status_code=500)