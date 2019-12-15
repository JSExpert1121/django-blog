from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)
    error_types = {
        'ValidationError': _custom_exception_handler
    }

    exc_class = exc.__class__.__name__
    if exc_class in error_types:
        response = error_types[exc_class](exc, context, response)

    return response


def _custom_exception_handler(exc, context, response):

    response.data = {
        'errors': response.data
    }

    return response
