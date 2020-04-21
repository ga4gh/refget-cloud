# -*- coding: utf-8 -*-
"""Unit tests for MediaType Middleware class"""

import pytest
from ga4gh.refget.config.constants import *
from ga4gh.refget.config.properties import Properties
from ga4gh.refget.http.request import Request
from ga4gh.refget.http.response import Response
from ga4gh.refget.http.status_codes import StatusCodes as SC
from ga4gh.refget.middleware.media_type import MediaTypeMW, MediaTypeMidware
from test.common.methods import setup_request

testdata = [
    ({}, SC.OK),
    ({"header": {"Accept": "text/strange-encoding"}}, SC.NOT_ACCEPTABLE),
    ({"header": {"Accept": "*/*"}}, SC.OK)
]

@pytest.mark.parametrize("request_dict,exp_status_code", testdata)
def test_media_type_middleware(request_dict, exp_status_code):
    properties = Properties({})
    request = setup_request(request_dict)
    response = Response()

    @MediaTypeMidware(properties, request, response)
    def dummy_function(properties, request, response):
        return None
    dummy_function(properties, request, response)

    assert response.get_status_code() == exp_status_code
