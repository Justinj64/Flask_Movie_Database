
import redis

from flask import current_app as c_app
from datetime import datetime, timedelta


class FlaskRedis:

    def __init__(self, app=None, config_prefix="FLASK_REDIS", **kwargs):    
        self.config_prefix = config_prefix

        if app is not None:
            self.init_app(app)

    def init_app(self, app, **kwargs):
        try:
            redis_host = app.config.get('REDIS_HOST')
            redis_port = app.config.get('REDIS_PORT')
            redis_db = app.config.get('REDIS_DB')
            redis_password = app.config.get('REDIS_PASSWORD') if app.config.get('REDIS_PASSWORD') else None
            redis_ssl = app.config.get('REDIS_SSL')

            redis_connection = redis.StrictRedis(host=redis_host, port=redis_port,
                                        db=redis_db, password=redis_password,
                                        ssl=redis_ssl, decode_responses=True)
            app.config['REDIS_CONNECTION'] = redis_connection
            print("Redis app created")
        except Exception as e:
            raise e

    @staticmethod
    def insert_user_details(username, usertype, verify=True):
        try:
            redis_connection = c_app.config.get('REDIS_CONNECTION')
            key = f"USER_DETAILS:{username}"
            if verify:
                username_exists = redis_connection.exists(key)
                if username_exists:
                    raise ValueError('username already taken')
            user_details = {
                "username": username,
                "type": usertype,
                "token": "",
                "created_timestamp": datetime.utcnow().isoformat(),
                "expiry_timestamp": ""
            }
            user_details = redis_connection.hmset(key, user_details)
            return user_details
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def insert_token_in_redis(username, ttl, token):
        try:
            '''
                Insert token in redis when new token is generated
            '''
            redis_connection = c_app.config.get('REDIS_CONNECTION')
            key = f"USER_DETAILS:{username}"
            username_exists = redis_connection.exists(key)
            if not username_exists:
                raise ValueError('username is not present, kindly create')
            data = {
                "token": token,
                "expiry_timestamp": (datetime.utcnow() + timedelta(minutes=ttl)).strftime("%Y-%m-%d %H:%M:%S")
            }
            redis_connection.hmset(f"USER_DETAILS:{username}", data)
        except Exception as e:
            print(e)
            raise e
