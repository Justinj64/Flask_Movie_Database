import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from datetime import datetime
from models.app_models import MovieDetails
from models import db

'''
Module to handle methods which may be used commonly
'''


def tuple_to_dict(col_header, tuples):
    '''
        converts a set of tuples to dict with
        the mentioned column headers.
    '''
    result = []
    for k in tuples.items:
        row_dict = dict(zip(col_header, k))
        result.append(row_dict)
    return result


def get_token_fields(auth_token):
    '''
        decodes a particular jwt token
    '''
    try:
        token_details = jwt.decode(auth_token, 'some_secret', algorithms=['HS256'])
        return token_details

    except ExpiredSignatureError as e:
        print({'auth_token': auth_token, 'exception': e, 'timestamp': datetime.utcnow().isoformat()})

    except InvalidSignatureError as e:
        print({'auth_token': auth_token, 'exception': e,'timestamp': datetime.utcnow().isoformat()})

    except Exception as e:
        print({'auth_token': auth_token, 'exception': e,'timestamp': datetime.utcnow().isoformat()})

    return {}


def check_record_exists(request_body):
    '''
        verifies if a particular movie record exists in db by id
    '''
    exists = db.session.query(MovieDetails.id).filter_by(id=request_body['id']).first()
    return exists