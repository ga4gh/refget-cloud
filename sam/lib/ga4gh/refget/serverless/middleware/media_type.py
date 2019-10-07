# -*- coding: utf-8 -*-
"""Checks request headers for correct/appropriate media types"""

import json
from ga4gh.refget.serverless.cls.http.status_codes import StatusCodes as SC
from ga4gh.refget.serverless.config.constants import *

class MediaTypeMW(object):
    """Middleware, checks request for appropriate media types

    MediaTypeMW middleware checks the "Accept" header of the request. If the
    request only accepts MIME types that the refget app cannot satisfy, it sets
    the response status code to NOT ACCEPTABLE
    """

    @staticmethod
    def middleware_func(event, resp, supported_media_types):
        """performs all media type validation submethods

        :param event: AWS SAM event (incl. headers, path params, query params)
        :type event: dict[str, object]
        :param resp: response object to modify
        :type resp: class:`ga4gh.refget.serverless.cls.http.response.Response`
        :param supported_media_types: MIME types supported by server route
        :type supported_media_types: list[str]
        """

        # get a list of client's accepted media types according to its
        # Accept header
        client_media_types = \
            MediaTypeMW._MediaTypeMW__assign_default_media_type(event)
        
        # check if there is overlap between client's accept media types,
        # and the media types the server supports
        # if not, set response status code to NOT ACCEPTABLE 
        MediaTypeMW._MediaTypeMW__check_unsupported_media_type(
            resp,
            client_media_types,
            supported_media_types
        )

    @staticmethod
    def __assign_default_media_type(event):
        """set default media types if no request "Accept" header

        If the request doesn't contain an "Accept" header, then assume the
        client will accept refget's MIME types

        :param event: AWS SAM event (incl. headers, path params, query params)
        :type event: dict[str, object]
        """

        media_types = []
        # add defaults if no Accept header
        if "Accept" not in event["headers"]:
            media_types = [DEFAULT_CONTENT_TYPE_JSON,
                           DEFAULT_CONTENT_TYPE_TEXT]
        # if accept header is present, create a list of types from the Accept
        # header string. If '*/*' is present, also add in the default refget
        # types
        else:
            media_types = [
                e.strip() for e in 
                event["headers"]["Accept"].split(";")[0].split(",")
            ]

            if "*/*" in set(media_types):
                media_types += [DEFAULT_CONTENT_TYPE_JSON, 
                                DEFAULT_CONTENT_TYPE_TEXT]

        return media_types

    @staticmethod
    def __check_unsupported_media_type(resp, client_types,
        supported_types):
        """Check if server can fulfill request accepted media types

        :param resp: response object to modify
        :type resp: class:`ga4gh.refget.serverless.cls.http.response.Response`
        :param client_types: accepted MIME types from client 'Accept' header
        :type client_types: list[str]
        :param supported_types: MIME types this API route allows
        :type supported_types: list[str]
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

def MediaTypeMidware(event, context,
                     supported_media_types=[DEFAULT_CONTENT_TYPE_JSON]):
    """Creates the media type middleware decorator function

    :param event: AWS SAM event (incl. headers, path params, query params)
    :type event: dict[str, object]
    :param context: AWS SAM context
    :type context: dict[str, str]
    :param supported_media_types: supported MIME types for this api route
    :type supported_media_types: list[str]
    :return: media type middleware decorator function
    :rtype: function
    """

    def decorator_function(func):
        def wrapper(resp):
            # perform media type middleware function, which modifies
            # the response status code/headers/body as necessary
            # if status code is still OK at end of function, then execute the
            # inner function
            MediaTypeMW.middleware_func(event, resp, supported_media_types)
            if resp.get_status_code() == SC.OK:
                return func(resp)
            else:
                return resp
        return wrapper
    return decorator_function
