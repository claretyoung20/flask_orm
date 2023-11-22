import logging

from flask import request

logging.basicConfig(filename='record.log', level=logging.DEBUG)


def log_error(exception):
    request_url = request.url
    logging.error(f"Error for API: {request_url}, error message: {exception}")
