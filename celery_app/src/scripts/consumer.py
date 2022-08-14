
import copy
from utils.decorators import handle_exception
from utils.celery_tasks import app
from models import MovieDetails, MovieGenres, Session

'''
    Consumer module which contains task to perform
    operation as messages are consumed from RabbitMq
    Tasks involve - Insert/Update/Delete operations
    to the sqllite operation
'''


@handle_exception
@app.task(name="db_worker:insert_record")
def insert_record(data):
    '''
        Insert records onto both `movie_details` and `movie_genres` tables
    '''
    updated_data = {
        "name": data.get('name'),
        "director": data.get('director'),
        "popularity": data.get('popularity'),
        "imdb_score": data.get('imdb_score'),
    }
    movie_details = MovieDetails(**updated_data)
    Session.add(movie_details)
    Session.commit()
    data_mapping = []
    for genre in data['genres']:
        row_dict = {}
        row_dict['movie_id'] = movie_details.id
        row_dict['genre'] = genre
        data_mapping.append(row_dict)
    Session.bulk_insert_mappings(MovieGenres, data_mapping)
    Session.commit()
    print("data has been inserted")


@handle_exception
@app.task(name="db_worker:update_record")
def update_record(data):
    '''
        We create a copy of the data payload
        and remove `genres` key from it since
        we do no want any operations on it referencing
        the main table
    '''
    updated_data = copy.deepcopy(data)
    if 'genres' in updated_data:
        del updated_data['genres']

    Session.query(MovieDetails).filter(MovieDetails.id == data['id'])\
                               .update(updated_data)
    Session.commit()

    if data.get('genres'):
        Session.query(MovieGenres).filter(MovieGenres.movie_id == data['id'])\
                                  .delete()
        data_mapping = []
        for genre in data['genres']:
            row_dict = {}
            row_dict['movie_id'] = data['id']
            row_dict['genre'] = genre
            data_mapping.append(row_dict)

    Session.bulk_insert_mappings(MovieGenres, data_mapping)
    Session.commit()
    print(f"data with id {data['id']} has been updated")


@handle_exception
@app.task(name="db_worker:delete_record")
def delete_record(data):
    '''
        Delete a spefic record based on the id provided
    '''
    Session.query(MovieGenres).filter(MovieGenres.movie_id == data['id'])\
                              .delete()
    Session.query(MovieDetails).filter(MovieDetails.id == data['id'])\
                               .delete()
    Session.commit()
    print(f"data with id {data['id']} has been deleted")
