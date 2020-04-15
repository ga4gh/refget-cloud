# -*- coding: utf-8 -*-
"""Update response to contain redirect to sequence metadata"""

import requests
from ga4gh.refget.middleware.media_type import MediaTypeMidware
from ga4gh.refget.util.resolve_url import resolve_metadata_url

def get_metadata(properties, request, response):
    """Refget function, get requested sequence metadata

    The get_metadata function corresponds to the /sequence/{seqid}/metadata
    endpoint described in the refget API specification. First performs media
    type validation, then returns redirect to object metadata location 

    Arguments:
        properties (Properties): runtime properties
        request (Request): generic refget request
        response (Response): modifiable, generic refget response
    """

    @MediaTypeMidware(properties, request, response)
    def worker(properties, request, response):

        seqid = request.get_path_param("seqid")
        url = resolve_metadata_url(properties, seqid)
        value = requests.get(url).text
        response.set_redirect_found(url)

    worker(properties, request, response)
