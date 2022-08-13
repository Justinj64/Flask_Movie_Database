
from sqlalchemy import (Column, Integer, ForeignKey,  Float, String)
from models import db


class MovieDetails(db.Model):
    __tablename__ = 'movie_details'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    popularity = Column(Float)
    director = Column(String)
    imdb_score = Column(Float, index=True)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class MovieGenres(db.Model):
    __tablename__ = 'movie_genres'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey(MovieDetails.id))
    genre = Column(String)