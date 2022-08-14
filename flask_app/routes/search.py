from flask import request
from sqlalchemy import func
from models.app_models import db
from flask_restful import Resource
from utils.common_functions import tuple_to_dict
from models.app_models import MovieDetails, MovieGenres


class Search(Resource):
    '''
        Search class implemented for search movies based on various parameters ;
        - by movie name
        - by director's name
        - by rating (eg: 7+ : return all movies with an imdb score of > 7)
        - results are paginated with default size of 10
        - page size and page number can be passed as a param as well
    '''
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.success_code = 200
        self.exception_code = 500

    def fetch_result(self, queries, page_number, page_size):
        '''
            Function to query database based on the queries constructed earlier
        '''
        movie_details = db.session.query(MovieDetails.id,
                                         MovieDetails.name,
                                         MovieDetails.popularity,
                                         MovieDetails.director,
                                         MovieDetails.imdb_score,
                                         func.group_concat(MovieGenres.genre))\
                                    .join(MovieGenres, MovieDetails.id == MovieGenres.movie_id)\
                                    .group_by(MovieDetails.id)\
                                    .filter(*queries)\
                                    .order_by(MovieDetails.popularity.desc())\
                                    .paginate(page_number, page_size, False)\

        headers = ['id', 'name', 'popularity', 'director', 'imdb_score', 'genres']
        formatted_result = tuple_to_dict(headers, movie_details)
        return formatted_result

    def get(self):
        try:
            queries = []
            args = request.args
            page_number = int(args.get("page_number", 1))
            page_size = int(args.get("page_size", 10))
            if args.get('movie_name'):
                queries.append(MovieDetails.name == args.get('movie_name'))
            if args.get('director_name'):
                queries.append(MovieDetails.director == args.get('director_name'))
            if args.get('rating'):
                rating = args.get('rating')[:-1]
                queries.append(MovieDetails.imdb_score >= float(rating))
            result = self.fetch_result(queries, page_number, page_size)
            return result, self.success_code, {"Content-Type": "application/json"}
        except Exception as e:
            response = {
                "message": "flask app has issue",
                "reason": str(e)
            }
            print(e)
            return response, self.exception_code, {"Content-Type": "application/json"}
