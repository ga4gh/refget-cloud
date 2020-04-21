# -*- coding: utf-8 -*-
"""Unit tests for get_metadata method"""

import json
import pytest
from ga4gh.refget.http.status_codes import StatusCodes as SC
from ga4gh.refget.routes.sequence.get_metadata import get_metadata
from test.common.methods import setup_properties_request_response
from test.common.constants import TRUNC512_PHAGE, TRUNC512_CEREVISIAE, \
    TRUNC512_NONEXISTENT, FILESERVER_PROPS_DICT

props_dict = FILESERVER_PROPS_DICT

testdata = [
    # get metadata via redirect
    ({"path": {"seqid": TRUNC512_PHAGE}}, SC.REDIRECT_FOUND, "")
]

@pytest.mark.parametrize("request_dict,exp_sc,exp_body", testdata)
def test_get_sequence(request_dict, exp_sc, exp_body):
    properties, request, response = setup_properties_request_response(
        props_dict, request_dict)
    get_metadata(properties, request, response)
    assert response.get_status_code() == exp_sc
    assert response.get_body() == exp_body
