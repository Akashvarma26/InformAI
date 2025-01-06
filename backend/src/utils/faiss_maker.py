# Importing Required Libraries
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['USER_AGENT'] = 'myagent'
os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Embedding model
embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Function to split documents for RAG App
def docs_to_vdb(chunk_size=1000,chunk_overlap=100,url="https://python.langchain.com/docs/introduction/"):
    docs=WebBaseLoader(url).load()
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    final_docs=text_splitter.split_documents(docs)
    val_len=len(final_docs)
    db=FAISS.from_documents(final_docs,embeddings)
    return db,val_len