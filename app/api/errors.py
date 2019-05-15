from flask import jsonify
from app.exceptions import PropertyNotFoundError
from . import api


def bad_request(message):
    response = jsonify({
        'error': 'bad request',
        'message': message
    })
    response.status_code = 400
    return response


@api.errorhandler(PropertyNotFoundError)
def validation_error(e):
    return bad_request(e.args[0])
