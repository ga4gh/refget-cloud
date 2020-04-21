# -*- coding: utf-8 -*-
"""Unit tests for get_service_info method"""

import json
import pytest
from ga4gh.refget.config.service_info import SERVICE_INFO
from ga4gh.refget.http.status_codes import StatusCodes as SC
from ga4gh.refget.routes.sequence.get_service_info import get_service_info
from test.common.methods import setup_properties_request_response

props_dict = {}

testdata = [
    ({}, SC.OK, json.dumps({"service": SERVICE_INFO})),
    (
        {"header": {"Accept": "text/strange-encoding"}},
        SC.NOT_ACCEPTABLE,
        json.dumps({"message": "requested media type(s) not supported"})
    )
]

@pytest.mark.parametrize("request_dict,exp_sc,exp_body", testdata)
def test_get_service_info(request_dict, exp_sc, exp_body):
    properties, request, response = setup_properties_request_response(
        props_dict, request_dict)
    get_service_info(properties, request, response)
    assert response.get_status_code() == exp_sc
    assert response.get_body() == exp_body
