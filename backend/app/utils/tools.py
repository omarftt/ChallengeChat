import os
from langchain_community.vectorstores import Pinecone
from langchain.chains import RetrievalQA
import uuid


os.environ["TOKENIZERS_PARALLELISM"] = "false"

def generate_id():
        return str(uuid.uuid4())

def generate_text(question, llm, index, embed):

    vectorstore = Pinecone(
        index, embed, text_key="text"
    )
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    result = qa.invoke(question)
    return result
    


