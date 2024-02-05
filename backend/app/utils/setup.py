from pinecone import Pinecone
from langchain_openai import ChatOpenAI

def setup_pinecone(index_name, pinecone_key):
    pc = Pinecone(api_key=pinecone_key)
    index = pc.Index(index_name)

    return index

def setup_llm(model_name, openai_key):
    llm = ChatOpenAI(
        openai_api_key=openai_key,
        model_name= model_name,
        temperature=0.7
    )
    return llm