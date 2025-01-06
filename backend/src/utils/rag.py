# Importing Libraries, methods and setting up APIs
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['USER_AGENT'] = 'myagent'
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough,RunnableParallel
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from operator import itemgetter
from utils.faiss_maker import docs_to_vdb,embeddings

# Setting the Embedding model all-MiniLM-L6-v2(384 dimensions) and GROQ Llama3.3 70b versatile model
model=ChatGroq(model="llama-3.3-70b-versatile",temperature=0.3)

# Prompt temp for our RAG LLM
prompt_tempt="""
You are 'InformAI' an Assistant for answering questions asked.
Answer the question based on the context, in a concise manner and use bullet points when applicable.

Context:{context}
Question:{question}
Answer:
"""

# Prompt template
prompt= ChatPromptTemplate.from_template(prompt_tempt)
db,val_len=docs_to_vdb()
retriever=db.as_retriever()

# Function of RAG Chain
def rag_chain():
    db=FAISS.load_local("utils/vectordatabase/faiss_index",embeddings=embeddings, allow_dangerous_deserialization=True)
    retriever=db.as_retriever()
    chain=({"context":retriever.with_config(top_k=4),
            "question":RunnablePassthrough()
            }
            | RunnableParallel({
                "response":prompt|model,
                "context":itemgetter("context")
            })
            )
    return chain

# function to get responses
def get_answer_and_docs(question:str):
    chain=rag_chain()
    response=chain.invoke(question)
    answer=response['response'].content
    context=response['context']
    return {
        "answer":answer,
        "context":context
    }

#test_response=get_answer_and_docs("What is LangGraph?")
#print(test_response)