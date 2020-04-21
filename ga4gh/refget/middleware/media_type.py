# -*- coding: utf-8 -*-
"""Checks request headers for correct and appropriate media types"""

import json
from ga4gh.refget.http.status_codes import StatusCodes as SC
from ga4gh.refget.config.constants import *

class MediaTypeMW(object):
    """Middleware, checks request for correct and appropriate media types

    MediaTypeMW middleware checks the "Accept" header of the request. If the
    request only accepts MIME types that the refget service cannot satisfy, it
    sets the response status code to NOT ACCEPTABLE

    Attributes:
        request (Request): refget generic request
        response (Response): modifiable, refget generic response
        supported_media_types (list): list of supported MIME media type
            strings for a given endpoint
    """

    def __init__(self, request, response, supported_media_types):
        """MediaTypeMW constructor

        Arguments:
            request (Request): refget generic request
            response (Response): modifiable, refget generic response
            supported_media_types (list): list of supported MIME media type
                strings for a given endpoint
        """

        self.request = request
        self.response = response
        self.supported_media_types = supported_media_types
        self.acceptable_media_types = []
    
    def validate(self):
        """Perform all media type validation"""

        self.__assign_acceptable_media_types()        
        self.__check_unsupported_media_type()

    def __assign_acceptable_media_types(self):
        """Set default media types if no request "Accept" header

        If the request doesn't contain an "Accept" header, then assume the
        client will accept refget's MIME types
        """

        media_types = []
        # add defaults if no Accept header
        if not self.request.get_header("Accept"):
            media_types = [mime for mime in self.supported_media_types]
        # if accept header is present, create a list of types from the Accept
        # header string. If '*/*' is present, also add in the default refget
        # types
        else:
            media_types = [
                e.strip() for e in 
                self.request.get_header("Accept").split(";")[0].split(",")
            ]

            if "*/*" in set(media_types):
                media_types += [mime for mime in self.supported_media_types]

        self.acceptable_media_types = media_types

    def __check_unsupported_media_type(self):
        """Check if server can fulfill request accepted media types

        Checks for overlap between acceptable media types and the media types
        the server and endpoint supports. If not, set response status code to
        NOT ACCEPTABLE
        """

        # first, set status code to NOT ACCEPTABLE, in case we do not find
        # any client/server media type overlap 
        self.response.set_error(
            SC.NOT_ACCEPTABLE,
            "requested media type(s) not supported"
        ) 

        # for each client accepted media type, check if it's in the server
        # supported media types. if so, status code is OK, and the response
        # Content-Type header is the first overlapping media type
        for client_type in self.acceptable_media_types:
            if self.response.get_status_code()!= SC.OK:
                if client_type in set(self.supported_media_types):
                    self.response.set_status_code(SC.OK)
                    self.response.put_header("Content-Type", client_type)
                    self.response.set_body("")

def MediaTypeMidware(properties, request, response,
                     supported_media_types=[CONTENT_TYPE_JSON_REFGET_VND,
                                            CONTENT_TYPE_JSON_VND_NEUTRAL]):
    """Creates the media type middleware decorator function

    Arguments:
        properties (Properties): runtime properties
        request (Request): generic refget request
        response (Response): modifiable, generic refget response
        supported_media_types (list): supported MIME types

    Returns:
        (function): media type middleware decorator function
    """

    def decorator_function(func):
        def wrapper(properties, request, response):
            # perform media type validation, which modifies response status
            # code/headers/body. if status code is OK at end of function,
            # execute inner function
            middleware = MediaTypeMW(request, response, supported_media_types)
            middleware.validate()
            if response.get_status_code() == SC.OK:
                return func(properties, request, response)
            else:
                return response
        return wrapper
    return decorator_function
