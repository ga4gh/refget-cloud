import json
from config.constants import *

class MediaTypeMW(object):

    @staticmethod
    def middleware_func(event, partial_response, supported_media_types):

        client_media_types = \
            MediaTypeMW._MediaTypeMW__assign_default_media_type(event)
        response = MediaTypeMW._MediaTypeMW__check_unsupported_media_type(
            partial_response,
            client_media_types,
            supported_media_types
        )
        return response

    @staticmethod
    def __assign_default_media_type(event):

        media_types = []

        if "Accept" not in event["headers"]:
            media_types = [DEFAULT_CONTENT_TYPE_JSON,
                           DEFAULT_CONTENT_TYPE_TEXT]
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
    def __check_unsupported_media_type(partial_response, client_types,
        supported_types):

        partial_response["statusCode"] = 406
        partial_response["body"] = json.dumps({
                "message": "requested media type(s) not supported"
        })

        for client_type in client_types:
            if partial_response["statusCode"] != 200:
                if client_type in set(supported_types):
                    partial_response = {
                        "statusCode": 200,
                        "headers": {
                            "Content-Type": client_type
                        },
                        "body": ""
                    }

        return partial_response

def MediaTypeMidware(event, context,
                     supported_media_types=[DEFAULT_CONTENT_TYPE_JSON]):

    def decorator_function(func):
        def wrapper(partial_response):
            # print("Partial Response is")
            # print(partial_response)

            midware_response = MediaTypeMW.middleware_func(
                event, partial_response, supported_media_types)
            if midware_response["statusCode"] == 200:
                return func(midware_response)
            else:
                return midware_response
        return wrapper

    return decorator_function
