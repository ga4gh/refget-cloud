# -*- coding: utf-8 -*-
"""Defines the StatusCodes class, which references http status code
numbers by name
"""

class StatusCodes(object):
    """References http status code numbers by name

    Constants:
        OK (int): 200\n
        PARTIAL_CONTENT (int): 206\n
        REDIRECT_FOUND (int): 302\n
        BAD_REQUEST (int): 400\n
        NOT_FOUND (int): 404\n
        NOT_ACCEPTABLE (int): 406\n
        REQUESTED_RANGE_NOT_SATISFIABLE (int): 416\n
        NOT_IMPLEMENTED (int): 501
    """

    OK = 200
    PARTIAL_CONTENT = 206
    REDIRECT_FOUND = 302
    BAD_REQUEST = 400
    NOT_FOUND = 404
    NOT_ACCEPTABLE = 406
    REQUESTED_RANGE_NOT_SATISFIABLE = 416
    NOT_IMPLEMENTED = 501

    @staticmethod
    def is_successful_code(status_code):
        """Checks whether a status code is one of several successful codes

        :param status_code: status code to check
        :type status_code: int
        :return: True if code is in successful code set, otherwise False
        :rtype: bool
        """

        success_set = set([
            StatusCodes.OK,
            StatusCodes.PARTIAL_CONTENT
        ])

        return status_code in success_set
