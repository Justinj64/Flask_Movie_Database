from flask_restful import Resource
from flask import request
from utils.token import Token
from resource_bindings.redis_bindings import FlaskRedis
from schemas.payload_schemas import TokenSchema


class Login(Resource):
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.success_code = 200
        self.processing_code = 202
        self.bad_code = 400
        self.auth_code = 401
        self.process_error_code = 422
        self.exception_code = 500

    def post(self):
        try:
            request_body = request.get_json()
            request_body_schema = TokenSchema()
            request_body_schema.load(request_body)
            token = Token.generate_token(request_body['username'], request_body['token_ttl'])
            FlaskRedis.insert_token_in_redis(request_body['username'], request_body['token_ttl'], token)
            response = {
                "message": "success",
                "token": str(token)
            }
            return response, 200, {"Content-Type": "application/json"}
        except Exception as e:
            response = {
                "message": "flask app has issue",
                "reason": str(e)
            }
            print(e)
            return response, 500, {"Content-Type": "application/json"}