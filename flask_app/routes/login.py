
from flask import request
from utils.token import Token
from flask_restful import Resource
from resource_bindings.redis_bindings import FlaskRedis
from schemas.payload_schemas import TokenSchema


class Login(Resource):
    '''
        Login class to generate token once user has been created
        Short lived token generated with a specific TTL
        and inserted onto redis for further Movie crud endpoints
    '''
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.success_code = 200
        self.exception_code = 500

    def post(self):
        '''
            Token used is of typt `JWT`.
            Token would be invalidated after the expiry of the given ttl
            In which case, a new token should be generated
        '''
        try:
            request_body = request.get_json()
            # Schema validation - username and ttl mandatory
            request_body_schema = TokenSchema()
            request_body_schema.load(request_body)

            token = Token.generate_token(request_body['username'],
                                         request_body['token_ttl'])
            FlaskRedis.insert_token_in_redis(request_body['username'],
                                             request_body['token_ttl'], token)
            response = {
                "message": "success",
                "token": str(token)
            }
            return response, self.success_code, {"Content-Type": "application/json"}
        except Exception as e:
            response = {
                "message": "flask app has issue",
                "reason": str(e)
            }
            print(e)
            return response, self.exception_code, {"Content-Type": "application/json"}
