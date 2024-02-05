from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_openai import OpenAIEmbeddings
from uuid import uuid4
from dotenv import load_dotenv
import sys
import os

load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.setup import setup_pinecone
import app.config as config



PATH_DIRECTORY = 'data'
BATCH_LIMIT = 20

index = setup_pinecone(config.Config.INDEX_NAME, os.environ.get('PINECONE_KEY', False))

def load_docs(directory):
    loader = DirectoryLoader(directory, loader_cls=TextLoader)
    documents = loader.load()
    return documents

def split_docs(documents):

    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
        
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

    docs_splitted = []
    for doc in documents:
        text_splitted = markdown_splitter.split_text(doc.page_content)
        for elem in text_splitted:
            docs_splitted.append(str(elem))

    return docs_splitted 

def embedding_loader(docs, model_name, batch_limit):
    embed = OpenAIEmbeddings(model=model_name)

    texts = []
    metadatas = []
    for i, doc in enumerate(docs):
        doc = str(doc)
        texts.append(doc)
        metadatas.append({"chunk":i,"text":doc})
        if len(texts) >= batch_limit:
            ids = [str(uuid4()) for _ in range(len(texts))]
            embeds = embed.embed_documents(texts)
            print('longitud',len(embeds))
            index.upsert(vectors=zip(ids, embeds,metadatas))
            texts = []
            metadatas= []
    
    if len(texts) > 0:
        ids = [str(uuid4()) for _ in range(len(texts))]
        embeds = embed.embed_documents(texts)
        index.upsert(vectors=zip(ids, embeds, metadatas))

    

documents = load_docs(PATH_DIRECTORY)
docs = split_docs(documents)
embedding_loader(docs, config.Config.EMBEDDING_MODEL, BATCH_LIMIT)

# print(len(docs))
# print(docs[0])
# print(len(docs[0]))



