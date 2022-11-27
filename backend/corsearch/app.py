from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from .urlcounts.routes import urlcounts_blueprint

load_dotenv()

app = Flask(__name__)

# Enable Cross Origin Resource Sharing (CORS), make cross-origin AJAX possible.
# By default allowing CORS for all domains on all routes.
# See - https://flask-cors.readthedocs.io/en/latest/
CORS(app)

app.register_blueprint(urlcounts_blueprint)
