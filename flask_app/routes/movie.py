from models import db
from flask_restful import Resource
from models.app_models import MovieDetails
from flask import request, current_app as c_app
from middleware.decorators import is_admin, token_required
from utils.common_functions import check_record_exists
from schemas.payload_schemas import (InsertMovieSchema,
                                     DeleteMovieSchema,
                                     UpdateMovieSchema)
from utils.celery_tasks import (insert_record,
                                delete_record,
                                update_record)


class Movie(Resource):
    def __init__(self):
        '''
            Movie Class initialized for crud operations ;
            For each action (Post,Put,Delete) : token and admin access is mandatory
            Admin access is given to the user by setting the user_type to 'admin' while creating the user
        '''
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.success_code = 200
        self.processing_code = 202
        self.exception_code = 500

    @token_required
    @is_admin
    def post(self):
        try:
            request_body = request.get_json()
            request_body_schema = InsertMovieSchema()
            request_body_schema.load(request_body)
            rabbitmq_payload = request_body

            # Initial check to validate if a record with
            # movie name under same director exists
            exists = db.session.query(MovieDetails.id)\
                               .filter_by(name=request_body['name'],
                                          director=request_body['director'])\
                               .first()

            # If a record already exists with the above mentioned parameters
            # We return with the following message
            if exists:
                response = {"status": "failed",
                            "reason": "movie with the given name and director already exits"}
                return response, self.exception_code, {"Content-Type": "application/json"}

            # async function call to the celery worker worker for insert operation
            insert_record.apply_async(args=(rabbitmq_payload, ),
                                      queue=c_app.config.get('QUEUE_NAME'))

            response = {"message": "record processing"}
            return response, self.processing_code, {"Content-Type": "application/json"}
        except Exception as e:
            response = {
                "status": "failed",
                "reason": str(e)
            }
            print(e)
            return response, self.exception_code, {"Content-Type": "application/json"}

    @token_required
    @is_admin
    def put(self):
        try:
            request_body = request.get_json()
            request_body_schema = UpdateMovieSchema()
            request_body_schema.load(request_body)
            rabbitmq_payload = request_body

            # Initial check to validate if a record with movie id exists
            exists = check_record_exists(request_body)
            if not exists:
                response = {"status": "failed",
                            "reason": "movie with the given id does not exist"}
                return response, 500, {"Content-Type": "application/json"}

            # async function call to the celery worker worker for update operation
            update_record.apply_async(args=(rabbitmq_payload, ),
                                      queue=c_app.config.get('QUEUE_NAME'))

            response = {"message": "record updation request sent"}
            return response, self.processing_code, {"Content-Type": "application/json"}
        except Exception as e:
            response = {
                "status": "failed",
                "reason": str(e)
            }
            print(e)
            return response, self.exception_code, {"Content-Type": "application/json"}

    @token_required
    @is_admin
    def delete(self):
        try:
            request_body = request.get_json()
            request_body_schema = DeleteMovieSchema()
            request_body_schema.load(request_body)
            rabbitmq_payload = request_body

            # Initial check to validate if a record with movie id exists
            exists = check_record_exists(request_body)
            if not exists:
                response = {"status": "failed",
                            "reason": "movie with the given id does not exist"}
                return response, self.exception_code, {"Content-Type": "application/json"}

            # async function call to the celery worker worker for delete operation
            delete_record.apply_async(args=(rabbitmq_payload, ),
                                      queue=c_app.config.get('QUEUE_NAME'))

            response = {"message": "record deletion request sent"}
            return response, self.processing_code, {"Content-Type": "application/json"}
        except Exception as e:
            response = {
                "status": "failed",
                "reason": str(e)
            }
            print(e)
            return response, self.exception_code, {"Content-Type": "application/json"}
