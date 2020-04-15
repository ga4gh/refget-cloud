# -*- coding: utf-8 -*-
"""Wraps refget functions into serverless AWS lambda functions"""

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
    """Load Properties object from environment variables

    In the server context, properties are passed via properties file. In the 
    AWS serverless context, properties are passed via environment variables.
    The same properties are allowed, except environment variable property names
    are written in all capitals, and underscores replace periods. For example:

        source.base_url -> SOURCE_BASE_URL
        server.port -> SERVER_PORT
    
    Returns:
        (Properties): loaded properties from environment variables
    """

    new_props = {}
    for property_key in DEFAULT_ALLOWED_PROPERTY_KEYS:
        envvar_name = property_key.replace(".", "_").upper()
        envvar_value = os.getenv(envvar_name)
        if envvar_value:
            new_props[property_key] = envvar_value
    return Properties(new_props)

def get_generic_request(event):
    """Instantiate a generic refget request from AWS serverless event object

    Returns:
        (Request): generic refget request, compatible with refget functions
    """

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
    """Instantiate a generic refget response

    Returns:
        (Response): generic refget response, compatible with refget functions
    """

    return Response()

def get_properties_request_response(event, context):
    """Load all objects required for a refget function

    Returns:
        (list): Properties, Request, and Response objects for single request
    """

    return [
        get_properties(context),
        get_generic_request(event),
        get_response()
    ]

def finalize_response(response):
    """Converts the completed refget response to AWS lambda-specific response

    The generic response is updated by the refget functions. This method writes
    the generic response as an AWS lambda-formatted response, so that the
    overall serverless function will return valid HTTP responses. The AWS
    lambda-formatted response is simply a dictionary with keys for statusCode,
    headers, and body

    Returns:
        (dict): AWS lambda-formatted response dictionary
    """
    
    return {
        "statusCode": response.get_status_code(),
        "headers": response.get_headers(),
        "body": response.get_body()
    }

def get_sequence(event, context):
    """Serverless request handler for get sequence refget function

    Returns:
        (dict): finalized sequence serverless response
    """

    props, request, response = get_properties_request_response(event, context)
    gsequence(props, request, response)
    return finalize_response(response)

def get_metadata(event, context):
    """Serverless request handler for get metadata refget function

    Returns:
        (dict): finalized metadata serverless response
    """

    props, request, response = get_properties_request_response(event, context)
    gmetadata(props, request, response)
    return finalize_response(response)

def get_service_info(event, context):
    """Serverless request handler for get service info refget function

    Returns:
        (dict): finalized service info serverless response
    """
    
    props, request, response = get_properties_request_response(event, context)
    gserviceinfo(props, request, response)
    return finalize_response(response)
