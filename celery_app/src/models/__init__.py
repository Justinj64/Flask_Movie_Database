from sqlalchemy import (
    Column, Integer, Float, String, ForeignKey, ARRAY, create_engine)

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from config import get_config

env = os.getenv('ENV')

config = get_config(env)
db_url = config.get('DB_URL')

Base = declarative_base()
engine = create_engine(db_url)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class MovieDetails(Base):
    __tablename__ = 'movie_details'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    popularity = Column(Float)
    director = Column(String)
    imdb_score = Column(Float, index=True)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class MovieGenres(Base):
    __tablename__ = 'movie_genres'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey(MovieDetails.id))
    genre = Column(String)

