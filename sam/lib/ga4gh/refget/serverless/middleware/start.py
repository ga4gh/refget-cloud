# -*- coding: utf-8 -*-
"""Start of middleware, creates an initial response object

The start middleware function creates an initial response object and passes it
to subsequent middleware functions and/or api route worker function
"""

from ga4gh.refget.serverless.cls.http.response import Response

def StartMidware(event, context):
    """Creates the start middleware decorator function

    :param event: AWS SAM event (incl. headers, path params, query params)
    :type event: dict[str, object]
    :param context: AWS SAM context
    :type context: dict[str, str]
    :return: higher order decorator function
    :rtype: function
    """

    def decorator_function(func):
        def wrapper():
            return func(Response())
        return wrapper
    return decorator_function

__all__ = [
    'StartMidware'
]