from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import get_config


def create_app(config_name):

    app = Flask(__name__)
    CORS(app)
    app.config.update(get_config(config_name))

    api = Api(app, catch_all_404s=True)

    # API Routes:
    from routes.hello import Hello

    # API Endpoints:
    api.add_resource(Hello, '/v1/hello', methods=['GET'], endpoint='hello')

    return api, app
