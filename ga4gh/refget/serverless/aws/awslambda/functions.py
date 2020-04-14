import os
from ga4gh.refget.config.defaults import DEFAULT_ALLOWED_PROPERTY_KEYS
from ga4gh.refget.config.properties import Properties
from ga4gh.refget.http.request import Request
from ga4gh.refget.http.response import Response
from ga4gh.refget.routes.sequence.get_metadata import get_metadata as gmetadata
from ga4gh.refget.routes.sequence.get_sequence import get_sequence as gsequence
from ga4gh.refget.routes.sequence.get_service_info import get_service_info as \
    gserviceinfo

def get_properties(context):

    new_props = {}
    for property_key in DEFAULT_ALLOWED_PROPERTY_KEYS:
        envvar_name = property_key.replace(".", "_").upper()
        envvar_value = os.getenv(envvar_name)
        if envvar_value:
            new_props[property_key] = envvar_value
    return Properties(new_props)

def get_generic_request(event):

    request = Request()

    build_request = [
        {
            "event_key": "pathParameters",
            "method": request.add_path_param
        },
        {
            "event_key": "queryStringParameters",
            "method": request.add_query_param
        },
        {
            "event_key": "headers",
            "method": request.add_header
        }
    ]

    for build in build_request:
        event_dict = event[build['event_key']]
        add_method = build['method']
        if event_dict:
            for key in event_dict.keys():
                add_method(key, event_dict[key])
    
    return request

def get_response():
    return Response()

def get_properties_request_response(event, context):

    return [
        get_properties(context),
        get_generic_request(event),
        get_response()
    ]

def finalize_response(response):
    
    return {
        "statusCode": response.get_status_code(),
        "headers": response.get_headers(),
        "body": response.get_body()
    }

def get_sequence(event, context):

    props, request, response = get_properties_request_response(event, context)
    gsequence(props, request, response)
    return finalize_response(response)

def get_metadata(event, context):

    props, request, response = get_properties_request_response(event, context)
    gmetadata(props, request, response)
    return finalize_response(response)

def get_service_info(event, context):
    
    props, request, response = get_properties_request_response(event, context)
    gserviceinfo(props, request, response)
    return finalize_response(response)
