
from sqlalchemy import (Column, Integer, ForeignKey,  Float, String)
from models import db


class MovieDetails(db.Model):
    '''
        Main table to store information regarding the following ;
        - id             | integer | primary key which be referenced in the `MovieGenres` table
        - movie name     | string  | index
        - popularity     | float
        - directors name | string
        - imdb_score     | float   | index
    '''
    __tablename__ = 'movie_details'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    popularity = Column(Float)
    director = Column(String)
    imdb_score = Column(Float, index=True)

    # converts the model object to json equivalent
    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class MovieGenres(db.Model):
    '''
        This table is used to store genres for the movies from the main table
        Columns include ;
        - id       | integer  | primary key
        - movie id | integer  | referencing id from `Movie Details` table
        - genres   | string
    '''
    __tablename__ = 'movie_genres'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey(MovieDetails.id))
    genre = Column(String)
