from flask import request
from flask_restful import Resource
from resource_bindings.redis_bindings import FlaskRedis
from schemas.payload_schemas import UserSchema
from middleware.decorators import login_required


class User(Resource):
    '''
        User class would be the first endpoint.
        Creates a user based on basic auth and inserts record onto redis.
        Basic auth and `user_type` parameter are mandatory
    '''
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.success_code = 200
        self.exception_code = 500

    @login_required
    def post(self):
        '''
            User can be of two types - `user` and `admin`
            - `user` can only search for movies
            - `admin` can create, edit and delete movie records
            `user_type` parameter in the request body should be set accordingly
        '''
        try:
            auth = request.authorization
            username = auth.username
            request_body = request.get_json()
            # Schema validation - user_type(admin/user) mandatory
            request_body_schema = UserSchema()
            request_body_schema.load(request_body)
            FlaskRedis.insert_user_details(username, request_body['user_type'])
            response = {"message": f"user {username} successfully created"}
            return response, self.success_code, {"Content-Type": "application/json"}
        except Exception as e:
            response = {
                "status": "failed",
                "reason": str(e)
            }
            print(e)
            return response, self.exception_code, {"Content-Type": "application/json"}
