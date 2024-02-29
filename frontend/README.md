# Frontend - Document Chat App 

## Description
This repository contains the frontend service implemented for the Document Chat App using Streamlit

## Installation

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

3. Modify config.py :
    ```python
    class Config:
        BACKEND_HOST = '## INSERT VALUE HERE ##' # Backend server host:port
        TOKEN_API = '## INSERT VALUE HERE ##' # Must be the same for backend and frontend
    ```

## Running

Run the Streamlit application:

```bash
streamlit run app.py
