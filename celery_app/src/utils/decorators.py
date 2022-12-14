from functools import wraps

'''
    Decorator class to handle exceptions
    on the celery tasks
'''


def handle_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        except Exception as e:
            print(f"Exception while running function {func.__name__} as {e}")
            raise Exception
    return wrapper
