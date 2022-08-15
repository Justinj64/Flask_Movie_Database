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
            token_payload["expiry_timestamp"] = (datetime.utcnow() + timedelta(minutes = ttl)).strftime("%Y-%m-%d %H:%M:%S")
            token = jwt.encode(token_payload, "some_secret")
            return token.decode('utf-8')
        except Exception as e:
            raise e

    