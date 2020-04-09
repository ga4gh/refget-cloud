# -*- coding: utf-8 -*-
"""Unit tests for QueryParameters Middleware class"""

import json
import pytest
from ga4gh.refget.http.status_codes import StatusCodes as SC
from ga4gh.refget.middleware.query_parameters import QueryParametersMidware
from test.common.constants import TRUNC512_PHAGE, TRUNC512_NONEXISTENT, \
    FILESERVER_PROPS_DICT
from test.common.methods import setup_properties_request_response

props_dict = FILESERVER_PROPS_DICT

testdata = [
    # valid, no params
    (
        {"path": {"seqid": TRUNC512_PHAGE}},
        SC.OK,
        ""
    ),
    # invalid, both start/end and range provided
    (
        {
            "header": {"Range": "bytes=25-50"},
            "path": {"seqid": TRUNC512_PHAGE},
            "query": {"start": "25", "end": "50"},
        },
        SC.BAD_REQUEST,
        json.dumps({
            "message": "Cannot provide both sequence start/end AND Range"
        })
    ),
    # invalid, malformed Range header
    (
        {
            "header": {"Range": "TwentyFiveToFifty"},
            "path": {"seqid": TRUNC512_PHAGE}
        },
        SC.BAD_REQUEST,
        json.dumps({
            "message": "Invalid 'Range' header"
        })
    ),
    # valid start/end parameter
    (
        {"path": {"seqid": TRUNC512_PHAGE}, "query": {"start": "25"}},
        SC.OK,
        ""
    ),
    # valid range header
    (
        {"path": {"seqid": TRUNC512_PHAGE}, "header": {"Range": "bytes=25-50"}},
        SC.OK,
        ""
    ),
    # invalid, start is not an unsigned int
    (
        {"path": {"seqid": TRUNC512_PHAGE}, "query": {"start": "TwentyFive"}},
        SC.BAD_REQUEST,
        json.dumps({"message": "start/end must be unsigned int"})
    ),
    # invalid, start is negative
    (
        {"path": {"seqid": TRUNC512_PHAGE}, "query": {"start": "-25"}},
        SC.BAD_REQUEST,
        json.dumps({"message": "start/end must be unsigned int"})
    ),
    # invalid, unsatisfiable range
    (
        {
            "path": {"seqid": TRUNC512_PHAGE},
            "query": {"start": "25", "end": "50000000"}
        },
        SC.REQUESTED_RANGE_NOT_SATISFIABLE,
        json.dumps({"message": "Invalid sequence range provided"})
    ),
    # invalid, unsupported circular request
    (
        {
            "path": {"seqid": TRUNC512_PHAGE},
            "query": {"start": "25", "end": "20"}
        },
        SC.NOT_IMPLEMENTED,
        json.dumps({
            "message": "server DOES NOT support circular sequences, end MUST "
                       + "be higher than start"})
    ),
    # invalid, metadata could not be found for object
    (
        {"path": {"seqid": TRUNC512_NONEXISTENT}, "query": {"start": "25"}},
        SC.NOT_FOUND,
        json.dumps({
            "message": "sequence " + TRUNC512_NONEXISTENT + " not found"})
    )
]

@pytest.mark.parametrize("request_dict,exp_sc,exp_body", testdata)
def test_query_parameters_middleware(request_dict, exp_sc, exp_body):
    properties, request, response = setup_properties_request_response(
        props_dict, request_dict)
    response.set_status_code(SC.OK)
    
    @QueryParametersMidware(properties, request, response)
    def dummy_function(properties, request, response):
        return None
    dummy_function(properties, request, response)
    
    assert response.get_status_code() == exp_sc
    assert response.get_body() == exp_body
