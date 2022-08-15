import datetime
from flask import request
from functools import wraps
from utils.common_functions import get_token_fields
from resource_bindings.redis_bindings import FlaskRedis


def login_required(f):
    '''
        basic auth check while using the `user` endpoint
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return ({'message': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


def token_required(f):
    '''
        for crud operations on movie records, token is mandatory
    '''
    def wrapper(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = {
                'message': 'unable to process request',
                'status': 'failed',
                'reason': "no token found"
            }
            return response, 401
        return f(*args, **kwargs)
    return wrapper


def is_admin(f):
    '''
        assert token in the request and check expiry condition for token
        validate if the user triggering the incoming request is of type `admin`
    '''
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        token_details = get_token_fields(auth_token)
        username = token_details.get('username')
        if not token_details.get('username'):
            response = {
                'message': 'unable to process request',
                'status': 'failed',
                'reason': "Please check the integrity of the token sent"
            }
            return response, 401
        user_details = FlaskRedis.fetch_user_details(username)
        if token_details.get('expiry_timestamp'):
            time_format = '%Y-%m-%d %H:%M:%S'  # time format
            token_expiry_date = datetime.datetime.strptime(token_details['expiry_timestamp'], time_format)
            current_timestamp = datetime.datetime.utcnow()
            if current_timestamp > token_expiry_date:
                response = {
                    'message': 'unable to process request',
                    'status': 'failed',
                    'reason': "token expired, kindly create a new token"
                }
                return response, 401
        if user_details.get('type') != 'admin':
            response = {
                'message': 'unable to process request',
                'status': 'failed',
                'reason': "Only admin can add/edit/delete movie records"
            }
            return response, 401
        return f(*args, **kwargs)
    return wrapper
