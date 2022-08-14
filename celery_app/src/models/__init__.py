import os

from config import get_config
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, Float, String,
                        ForeignKey, create_engine)


env = os.getenv('ENV')

config = get_config(env)
db_url = config.get('DB_URL')

'''
    Create a db session and engine according
    to the db url specified in the config file
'''
Base = declarative_base()
engine = create_engine(db_url)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class MovieDetails(Base):
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


class MovieGenres(Base):
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
