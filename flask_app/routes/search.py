from flask_restful import Resource
from models.app_models import MovieDetails, MovieGenres
from flask import request
from models.app_models import db
from sqlalchemy import literal_column, func
from utils.common_functions import tuple_to_dict


class Search(Resource):
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

    def fetch_result(self, queries, page_number, page_size):
        movie_details = db.session.query(MovieDetails.name,
                                         MovieDetails.popularity,
                                         MovieDetails.director,
                                         MovieDetails.imdb_score,
                                         func.string_agg(MovieGenres.genre, literal_column("','")))\
                                    .join(MovieGenres, MovieDetails.id == MovieGenres.movie_id)\
                                    .group_by(MovieDetails.id)\
                                    .filter(*queries)\
                                    .order_by(MovieDetails.popularity.desc())\
                                    .paginate(page_number, page_size, False)\

        headers = ['name','popularity', 'director', 'imdb_score', 'genres']
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
            return result
        except Exception as e:
            response = {
                "message": "flask app has issue",
                "reason": str(e)
            }
            print(e)
            return response, 500, {"Content-Type": "application/json"}