import os
from app import create_app

config_name = os.getenv('ENV', 'development')
api, app = create_app(config_name)

# Run App:
if __name__ == '__main__':
    app.run(host=app.config.get('HOST'),
            port=app.config.get('PORT'),
            debug=app.config.get('DEBUG'))