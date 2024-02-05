from flask import Flask, request, jsonify
from .config import Config
import os


app = Flask(__name__)

SECRET_TOKEN = os.environ.get('TOKEN_API', False)


@app.before_request
def check_token():
    if 'Authorization' not in request.headers:
        return jsonify({"error": "Missing Authorization header"}), 401

    token = request.headers['Authorization']

    if token != f"Bearer {SECRET_TOKEN}":
        return jsonify({"error": "Invalid token"}), 401
    

def create_app():
    app.config.from_object(Config)

    from .routes import routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app
