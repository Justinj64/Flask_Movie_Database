import os
from app import create_app


'''
    Entrypoint of the Flask application.
    If a specific `env` is not defined,
    we take the `development` config as default.
'''


config_name = os.getenv('ENV', 'development')
api, app = create_app(config_name)


if __name__ == '__main__':
    app.run(host=app.config.get('HOST'),
            port=app.config.get('PORT'),
            debug=app.config.get('DEBUG'))
