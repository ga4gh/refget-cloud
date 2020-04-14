# -*- coding: utf-8 -*-
"""HTTP Status Code integers by name"""

class StatusCodes(object):
    """HTTP Status Code integers by name

    Constants:
        OK (int): code for successful request
        PARTIAL_CONTENT (int): code for successful request, partial response
        REDIRECT_FOUND (int): code for succesful redirect
        BAD_REQUEST (int): code for bad or malformed request
        NOT_FOUND (int): code for requested resource not found
        NOT_ACCEPTABLE (int): code for not acceptable request
        REQUESTED_RANGE_NOT_SATISFIABLE (int): code for not satisfiable request
        NOT_IMPLEMENTED (int): code for not implemented endpoint/feature
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
