from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import get_config
from models import db


def create_app(config_name):

    app = Flask(__name__)
    CORS(app)
    app.config.update(get_config(config_name))

    api = Api(app, catch_all_404s=True)

    from resource_bindings.redis_bindings import FlaskRedis

    redis_app = FlaskRedis()
    redis_app.init_app(app)

    db.init_app(app)

    # API Routes:
    from routes.hello import Hello
    from routes.login import Login
    from routes.user import User
    from routes.search import Search

    # API Endpoints:
    api.add_resource(Hello, '/v1/hello', methods=['GET'], endpoint='hello')
    api.add_resource(Login, '/v1/login', methods=['POST'], endpoint='login')
    api.add_resource(User, '/v1/user', methods=['POST'], endpoint='user')
    api.add_resource(Search, '/v1/search', methods=['GET'], endpoint='search')

    return api, app
