# -*- coding: utf-8 -*-
"""Common helper functions for testing"""

from ga4gh.refget.config.properties import Properties
from ga4gh.refget.http.request import Request
from ga4gh.refget.http.response import Response

def setup_properties(props_dict):
    return Properties(props_dict)

def setup_request(request_dict):
    request = Request()
    info = [
        {"method": request.add_header, "dict_key": "header"},
        {"method": request.add_path_param, "dict_key": "path"},
        {"method": request.add_query_param, "dict_key": "query"}
    ]

    for i in info:
        method = i["method"]
        dict_key = i["dict_key"]
        if dict_key in request_dict.keys():
            for key in request_dict[dict_key].keys():
                method(key, request_dict[dict_key][key])
    return request

def setup_properties_request_response(props_dict, request_dict):
    return [
        setup_properties(props_dict),
        setup_request(request_dict),
        Response()
    ]