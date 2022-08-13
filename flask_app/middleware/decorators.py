from flask import request
from functools import wraps


def login_required(f):
    """ basic auth for api """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return ({'message': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function