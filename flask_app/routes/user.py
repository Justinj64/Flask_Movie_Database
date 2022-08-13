from flask_restful import Resource
from flask import request
from resource_bindings.redis_bindings import FlaskRedis
from schemas.payload_schemas import UserSchema
from middleware.decorators import login_required


class User(Resource):
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

    @login_required
    def post(self):
        try:
            auth = request.authorization
            username = auth.username
            request_body = request.get_json()
            # handle in common funct
            request_body_schema = UserSchema()
            request_body_schema.load(request_body)
            FlaskRedis.insert_user_details(username, request_body['user_type'])
            response = {"message": f"user {username} successfully created"}
            return response, 200, {"Content-Type": "application/json"}
        except Exception as e:
            response = {
                "status": "failed",
                "reason":str(e)
            }
            print(e)
            return response, 500, {"Content-Type": "application/json"}