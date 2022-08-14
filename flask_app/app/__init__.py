from models import db
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import get_config


def create_app(config_name):
    # Initialize flask app and updated config accordingly
    app = Flask(__name__)
    CORS(app)
    app.config.update(get_config(config_name))

    api = Api(app, catch_all_404s=True)

    from resource_bindings.redis_bindings import FlaskRedis

    # Initialize Sql and Redis
    redis_app = FlaskRedis()
    redis_app.init_app(app)
    db.init_app(app)
    print("Sql app created")

    # API Routes:
    from routes.hello import HealthCheck
    from routes.login import Login
    from routes.user import User
    from routes.search import Search
    from routes.movie import Movie

    # API Endpoints:
    api.add_resource(HealthCheck, '/v1/health_check', methods=['GET'], endpoint='health_check')
    api.add_resource(Login, '/v1/login', methods=['POST'], endpoint='login')
    api.add_resource(User, '/v1/user', methods=['POST'], endpoint='user')
    api.add_resource(Search, '/v1/search', methods=['GET'], endpoint='search')
    api.add_resource(Movie, '/v1/movie', methods=['POST', 'PUT', 'DELETE'], endpoint='movie')

    # Uncomment this out if running for the first time
    # Creates all tables present in models.py file
    # with app.app_context():
    #    db.create_all()
    #    db.session.commit()
    return api, app
