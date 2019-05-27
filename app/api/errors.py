from flask import jsonify
from app.exceptions import IncompleteFieldError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from . import api


def bad_request(message):
    response = jsonify({
        'error': 'bad request',
        'message': message
    })
    response.status_code = 400
    return response


def resource_not_exist(message):
    response = jsonify({
        'error': 'request resource not exist',
        'message': message
    })
    response.status_code = 404
    return response


def server_error(message):
    response = jsonify({
        'error': 'server error',
        'message': message
    })
    response.status_code = 500
    return response


@api.errorhandler(IncompleteFieldError)
@api.errorhandler(ValueError)
def incomplete_field_error(e):
    return bad_request(e.args[0])


@api.errorhandler(NoResultFound)
def no_result_found(e):
    return resource_not_exist(e.args[0])


@api.errorhandler(MultipleResultsFound)
def multi_results_found(e):
    return server_error(e.args[0])
