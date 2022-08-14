from app import create_app

ENV = 'development'


# test if application is up by hitting the /health_check endpoint
def test_movie_applications():
    _, flask_app = create_app(ENV)
    with flask_app.test_client() as test_client:
        response = test_client.get('/v1/health_check')
        assert response.status_code == 200


# test redis connection is established
def test_redis_conn():
    import redis
    _, flask_app = create_app(ENV)
    host = flask_app.config['REDIS_HOST']
    port = flask_app.config['REDIS_PORT']
    r = redis.from_url(f'redis://{host}:{port}')
    assert r.ping() is True


# test sqllite3 connection
def test_mysql_connection():
    import sqlite3 as mdb
    _, flask_app = create_app(ENV)
    myconn = mdb.connect(flask_app.config['SQLALCHEMY_DATABASE_URI'])
    assert myconn.cursor()
    myconn.close()


# test `/user` endpoint works as expected and data is inserted onto redis
def test_create_user():
    _, flask_app = create_app(ENV)
    with flask_app.test_client() as test_client:
        import base64
        import redis
        import random

        username = "admin" + str(random.randint(0,1000))
        password = "testpassword"
        user_pass_string = str.encode(username+":"+password)
        valid_credentials = base64.b64encode(user_pass_string).decode("utf-8")
        data = dict(user_type='admin')
        response = test_client.post('/v1/user',
                                    headers={"Authorization": "Basic " + valid_credentials},
                                    json=data)
        assert response.status_code == 200
        host = flask_app.config['REDIS_HOST']
        port = flask_app.config['REDIS_PORT']
        r = redis.from_url(f'redis://{host}:{port}')
        key = f"USER_DETAILS:{username}"
        assert r.exists(key)
