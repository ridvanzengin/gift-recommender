from flask import Flask
from dotenv import load_dotenv
import os
from flask_session import Session

load_dotenv()  # Load environment variables from .env file

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)


    from .routes import main
    app.register_blueprint(main)

    return app
