# Importing required libraries
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from utils.rag import get_answer_and_docs
from utils.faiss_maker import docs_to_vdb

# Initiating app
app=FastAPI(
    title="InformAI",
    description="Web based RAG question answering Assistant",
    version="0.1.0"
)

# Sample get method API
@app.get("/",description="Test method to display message")
def test1():
    return {"message":"Hello! User"}

# Sample post method API
@app.post("/test",description="Test to display custom user input string message")
def test2(message:str):
    return JSONResponse(content={"Your message":message},status_code=200)

# RAG App chat API
@app.post("/chat",description="Response from InformAI")
def get_response(message:str):
    response=get_answer_and_docs(message)
    response_content={
        "Question":message,
        "Answer":response["answer"],
        "All Documents":[doc.dict() for doc in response['context']]
    }
    return JSONResponse(content=response_content,status_code=200)

# RAG App input link API
@app.post("/get_input_link",description="Web link input method API for InformAI context section.")
def get_link(url:str):
    try:
        db,val_len=docs_to_vdb(url=url)
        db.save_local("utils/vectordatabase/faiss_index")
        return JSONResponse(content={"response":f"{val_len} documents from url {url} added to InformAI's Vector DB successfully. ✅"},status_code=200)
    except Exception as e:
        return JSONResponse(content=f"Error: Enter correct URL that can be uploaded to Vector DB. ❌    EXCEPTION : {str(e)}", status_code=500)