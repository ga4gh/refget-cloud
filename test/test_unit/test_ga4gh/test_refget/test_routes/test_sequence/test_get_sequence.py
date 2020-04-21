# -*- coding: utf-8 -*-
"""Unit tests for get_sequence method"""

import json
import pytest
from ga4gh.refget.http.status_codes import StatusCodes as SC
from ga4gh.refget.routes.sequence.get_sequence import get_sequence
from test.common.methods import setup_properties_request_response
from test.common.constants import TRUNC512_PHAGE, TRUNC512_CEREVISIAE, \
    TRUNC512_NONEXISTENT, FILESERVER_PROPS_DICT

props_dict = FILESERVER_PROPS_DICT

testdata = [
    # get full sequence via redirect
    ({"path": {"seqid": TRUNC512_PHAGE}}, SC.REDIRECT_FOUND, ""),
    # get subseq by start/end
    (
        {"path": {"seqid": TRUNC512_PHAGE}, "query": {"start": "25", "end": "50"}},
        SC.OK,
        "AAGTTAACACTTTCGGATATTTCTG"
    )
]

@pytest.mark.parametrize("request_dict,exp_sc,exp_body", testdata)
def test_get_sequence(request_dict, exp_sc, exp_body):
    properties, request, response = setup_properties_request_response(
        props_dict, request_dict)
    get_sequence(properties, request, response)
    assert response.get_status_code() == exp_sc
    assert response.get_body() == exp_body
