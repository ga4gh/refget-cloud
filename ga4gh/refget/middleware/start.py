# -*- coding: utf-8 -*-
"""Start of middleware, creates an initial response object

The start middleware function creates an initial response object and passes it
to subsequent middleware functions and/or api route worker function
"""

from ga4gh.refget.http.response import Response

def StartMidware(properties, request, response):
    """Creates the start middleware decorator function

    :param event: AWS SAM event (incl. headers, path params, query params)
    :type event: dict[str, object]
    :param context: AWS SAM context
    :type context: dict[str, str]
    :return: higher order decorator function
    :rtype: function
    """

    def decorator_function(func):
        def wrapper(properties, request, response):
            print("inside the Start wrapper")
            return func(properties, request, response)
        return wrapper
    return decorator_function
