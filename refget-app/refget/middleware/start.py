# -*- coding: utf-8 -*-
"""Module middleware.start.py
Start of middleware, creates an initial response object

The start middleware module creates an initial response object and passes it
to subsequent middleware functions and/or api route worker function
"""

from cls.http.response import Response

def StartMidware(event, context):
    """Creates the start middleware decorator function

    Arguments:
        event (dict): AWS event/request with closure in middleware chain
        context (dict): AWS context with closure in middleware chain

    Returns:
        (function): start middleware decorator function
    """

    def decorator_function(func):
        """Decorator: creates the response and passes it to next function

        Arguments:
            func (function): inner function that takes the response
        
        Returns:
            (function): wrapped function
        """

        def wrapper():
            """Inner function: creates response and passes to next function

            Returns:
                (Response): Response object
            """

            return func(Response())

        return wrapper

    return decorator_function