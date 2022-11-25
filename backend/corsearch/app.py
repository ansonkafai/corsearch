from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from .urlcounts.routes import urlcounts_blueprint

load_dotenv()

app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(urlcounts_blueprint)
