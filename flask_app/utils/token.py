import jwt

from flask import current_app as c_app
from datetime import datetime, timedelta


class Token:
    '''
        Main Class for Token Generation
    '''
    @staticmethod
    def generate_token(user_name, ttl):
        '''
            Generate token
            Args:
                username (str): username
            Returns(Based on username and secret hash):
                str: jwt token
        '''
        try:
            token_payload = {}
            token_payload["username"] = user_name
            token_payload["created_timestamp"] = datetime.utcnow().isoformat()
            token_payload["expiry_timestamp"] = (datetime.utcnow() + timedelta(minutes=ttl)).strftime("%Y-%m-%d %H:%M:%S")
            token = jwt.encode(token_payload, "some_secret")
            return token
        except Exception as e:
            raise e

    @staticmethod
    def is_token_valid(user_name):
        '''
            Check token validitity
        '''
        redis_con = c_app.config.get('REDIS_CONNECTION')
        result_username = redis_con.hgetall(f"USER_DETAILS:{user_name}")
        expiry_timestamp_user = result_username.get("expiry_timestamp", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

        token = result_username.get("token")

        current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if expiry_timestamp_user and expiry_timestamp_user > current_time:
            return True, token

        return False, token

    