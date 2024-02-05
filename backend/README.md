# Backend - Challenge Chat App 

## Description
This repository contains the backend API implemented for the Challenge Chat App using Flask.

## Configuration Pinecone

1. In Pinecone platform, create a vector database (index)
    ```txt
    Follow this configuration according to you LLM:
        - 3072 dimensions (if you are using text-embedding-3-large)
        - 1536 dimensions (if you are using text-embedding-3-small)
    ```
## Installation python

1. Create and activate a Python virtual environment:
    ```bash
    pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    ```
2. Install packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Modify app/config.py :
    ```python
    class Config:
        INDEX_NAME = 'ai-assistant' # Change according to your Pinecone database name
        LLM_NAME = 'gpt-3.5-turbo' # Change according to your OpenAI LLM
        EMBEDDING_MODEL = 'text-embedding-3-large' # Change according to your OpenAI LLM
    ```

3. Create/Modify .env :
    ```txt
    OPENAI_API_KEY = '## Insert your OpenAI key ##'
    PINECONE_KEY = '## Insert you Pinecone key ##'
    TOKEN_API = "## Insert your token here ##"  # Must be the same for backend and frontend
    ```

## Before running

This step is required only once to load your documents into Pinecone and convert them into vectors.

1. Create /data folder
    ```bash
    cd /install
    mkdir data
    ```
2. Load your .md documents in /data directory:

3. Run the document loader code. This process may take some time depending on the number of documents you have :
    ```bash
    python load_data.py
    ```

## Running

Run the Flask API:

```bash
python run.py
