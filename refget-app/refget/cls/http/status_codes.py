# -*- coding: utf-8 -*-
"""Module cls.http.status_codes.py
This module contains the StatusCodes class, which references http status code
numbers by name
"""

class StatusCodes(object):
    """References http status code numbers by name"""

    OK = 200
    PARTIAL_CONTENT = 206
    REDIRECT_FOUND = 302
    BAD_REQUEST = 400
    NOT_FOUND = 404
    NOT_ACCEPTABLE = 406
    REQUESTED_RANGE_NOT_SATISFIABLE = 416
    NOT_IMPLEMENTED = 501

    def is_successful_code(status_code):
        """Checks whether a status code is one of several successful codes

        Arguments:
            status_code (int): status code to check
        
        Returns:
            (bool): True if code is in successful code set, otherwise False
        """

        success_set = set([
            StatusCodes.OK,
            StatusCodes.PARTIAL_CONTENT
        ])

        return status_code in success_set

