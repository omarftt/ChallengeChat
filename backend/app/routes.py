from flask import Blueprint,  jsonify,  request
from langchain_openai import OpenAIEmbeddings
from app.utils import setup_pinecone, setup_llm, generate_text, generate_id
from app.config import Config
import os


routes_blueprint = Blueprint('routes', __name__)

index = setup_pinecone(Config.INDEX_NAME, os.environ.get('PINECONE_KEY', False))
llm = setup_llm(Config.LLM_NAME, os.environ.get('OPENAI_API_KEY', False))
embed = OpenAIEmbeddings(model=Config.EMBEDDING_MODEL)


@routes_blueprint.route('/api/v0/generate_text', methods=['GET'])
def generate_texto_route():

    request_data = request.get_json()
    
    if 'question' not in request_data:
        return jsonify({"type": "error", "error": "No question provided"})

    question = request_data['question']

    text_output = generate_text(question,llm, index, embed)

    return jsonify(
        {
            "type": "text", 
            "id": generate_id(),
            "text": text_output,
        })


