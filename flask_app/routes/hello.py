
from flask_restful import Resource


class HealthCheck(Resource):
    '''
        Sample endpoint created to check if flask app is running
    '''
    def get(self):
        try:
            response = {
                "message": "Hello from Flask Movie Database"
            }
            print(response)
            return response, 200, {"Content-Type": "application/json"}
        except Exception as e:
            response = {
                "message": "flask app has issue"
            }
            print(e)
            return response, 500, {"Content-Type": "application/json"}
