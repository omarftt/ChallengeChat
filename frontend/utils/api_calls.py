import streamlit as st
import requests
import json
import time


# @st.cache_data(show_spinner="Generating an answer based on your documentation ...")
def generate_text_llm(host:str, question: str, token_api: str):

    url = f"{host}/api/v0/generate_text"

    payload = json.dumps({
    "question": f"{question}"
    })

    headers = {
        'Authorization': f"{token_api}",
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()["text"]["result"]

# @st.cache_data(show_spinner="Generating followup questions ...")
def generate_questions_cached():
    time.sleep(2)
    return ["API answer to: cached"]

