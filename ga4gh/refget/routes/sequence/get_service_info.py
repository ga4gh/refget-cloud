# -*- coding: utf-8 -*-
"""Update response to contain web service info"""

import json
from ga4gh.refget.middleware.media_type import MediaTypeMidware
from ga4gh.refget.config.service_info import SERVICE_INFO

def get_service_info(properties, request, response):
    """Refget function, get web service info

    The get_service_info function corresponds to the /sequence/service-info
    endpoint described in the refget API specification. First performs media
    type validation, then returns service info object

    Arguments:
        properties (Properties): runtime properties
        request (Request): generic refget request
        response (Response): modifiable, generic refget response
    """

    @MediaTypeMidware(properties, request, response)
    def worker(properties, request, response):
        response.set_body(json.dumps({
            "service": SERVICE_INFO
        }))
    worker(properties, request, response)