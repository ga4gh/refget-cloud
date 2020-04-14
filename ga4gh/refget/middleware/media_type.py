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
    """

    @staticmethod
    def middleware_func(request, response, supported_media_types):
        """Performs all media type validations

        Arguments:
            request (Request): refget generic request
            response (Response): modifiable, refget generic response
            supported_media_types (list): list of supported MIME media type
                strings for a given endpoint
        """

        # get a list of client's accepted media types according to its
        # Accept header
        client_media_types = \
            MediaTypeMW._MediaTypeMW__assign_default_media_type(request)
        
        # check if there is overlap between client's accept media types,
        # and the media types the server supports
        # if not, set response status code to NOT ACCEPTABLE 
        MediaTypeMW._MediaTypeMW__check_unsupported_media_type(
            response,
            client_media_types,
            supported_media_types
        )

    @staticmethod
    def __assign_default_media_type(request):
        """Set default media types if no request "Accept" header

        If the request doesn't contain an "Accept" header, then assume the
        client will accept refget's MIME types

        Arguments:
            request (Request): Refget generic request
        """

        media_types = []
        # add defaults if no Accept header
        if not request.get_header("Accept"):
            media_types = [CONTENT_TYPE_JSON,
                           CONTENT_TYPE_TEXT]
        # if accept header is present, create a list of types from the Accept
        # header string. If '*/*' is present, also add in the default refget
        # types
        else:
            media_types = [
                e.strip() for e in 
                request.get_header("Accept").split(";")[0].split(",")
            ]

            if "*/*" in set(media_types):
                media_types += [CONTENT_TYPE_JSON, 
                                CONTENT_TYPE_TEXT]

        return media_types

    @staticmethod
    def __check_unsupported_media_type(resp, client_types,
        supported_types):
        """Check if server can fulfill request accepted media types

        Arguments:
            resp (Response): Modifiable, Refget generic response
            client_types (list): accepted MIME types from client Accept header
            supported_types (list): MIME types supported by web service endpoint
        """

        # first, set status code to NOT ACCEPTABLE, in case we do not find
        # any client/server media type overlap  
        resp.set_status_code(SC.NOT_ACCEPTABLE)
        resp.set_body(json.dumps({
                "message": "requested media type(s) not supported"
        }))

        # for each client accepted media type, check if it's in the server
        # supported media types. if so, status code is OK, and the response
        # Content-Type header is the first overlapping media type
        for client_type in client_types:
            if resp.get_status_code()!= SC.OK:
                if client_type in set(supported_types):
                    resp.set_status_code(SC.OK)
                    resp.put_header("Content-Type", client_type)
                    resp.set_body("")

def MediaTypeMidware(properties, request, response,
                     supported_media_types=[CONTENT_TYPE_JSON]):
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
            # perform media type middleware function, which modifies
            # the response status code/headers/body as necessary
            # if status code is still OK at end of function, then execute the
            # inner function
            MediaTypeMW.middleware_func(request, response, supported_media_types)
            if response.get_status_code() == SC.OK:
                return func(properties, request, response)
            else:
                return response
        return wrapper
    return decorator_function
