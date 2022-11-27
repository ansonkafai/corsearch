from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from dotenv import load_dotenv

from .urlcounts import UrlcountsAPI

# Load environment variables from .env file.
load_dotenv()

# Initialize Flask app instance.
app = Flask(__name__)

# Enable Cross Origin Resource Sharing (CORS), make cross-origin AJAX possible.
# By default allowing CORS for all domains on all routes.
# See - https://flask-cors.readthedocs.io/en/latest/
CORS(app)

# Flask restful wraps Flask app instance.
api = Api(app)

# Creating APIs through Flask Restful.
api.add_resource(UrlcountsAPI, '/urlcounts')

# Set Swagger configs.
app.config.update({
    "APISPEC_SPEC": APISpec(
        title="Corsearch Technical Challenge",
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version="3.0.2",
    ),
    "APISPEC_SWAGGER_URL": "/swagger/",  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})

# Generate Swagger APIs spec.
docs = FlaskApiSpec(app)
docs.register(UrlcountsAPI)
