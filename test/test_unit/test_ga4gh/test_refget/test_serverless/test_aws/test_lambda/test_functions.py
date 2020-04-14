# -*- coding: utf-8 -*-
"""Unit tests for AWS Lambda functions"""

import json
import pytest
from ga4gh.refget.config.service_info import SERVICE_INFO
from ga4gh.refget.http.status_codes import StatusCodes as SC
from ga4gh.refget.serverless.aws.awslambda.functions import \
    get_sequence, get_metadata, get_service_info
from test.common.constants import TRUNC512_PHAGE, FILESERVER_PROPS_DICT as PROPS

context = None

testdata = [
    # get_sequence tests
    (
        get_sequence,
        {
            "pathParameters": {"seqid": TRUNC512_PHAGE},
            "queryStringParameters": {"start": "25", "end": "50"},
            "headers": {}
        },
        SC.OK,
        "AAGTTAACACTTTCGGATATTTCTG",
        {}
    ),
    # get_metadata tests
    (
        get_metadata,
        {
            "pathParameters": {"seqid": TRUNC512_PHAGE},
            "queryStringParameters": {},
            "headers": {}
        },
        SC.REDIRECT_FOUND,
        "",
        {
            "Location": "http://localhost:8080/sequence/%s/metadata" % TRUNC512_PHAGE
        }
    ),
    # get_service_info tests
    (
        get_service_info,
        {
            "pathParameters": {},
            "queryStringParameters": {},
            "headers": {'Accept': 'text/strange-encoding'}
        },
        SC.NOT_ACCEPTABLE,
        json.dumps({"message": "requested media type(s) not supported"}),
        {}
    )
]

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("SOURCE_BASE_URL", PROPS["source.base_url"])
    monkeypatch.setenv("SOURCE_METADATA_PATH", PROPS["source.metadata_path"])

@pytest.mark.parametrize("function,event,exp_sc,exp_body,exp_headers", testdata)
def test_aws_lambda_function(function, event, exp_sc, exp_body, exp_headers,
    mock_env):

    response = function(event, context)
    assert response["statusCode"] == exp_sc
    assert response["body"] == exp_body
    for key in exp_headers.keys():
        assert response["headers"][key] == exp_headers[key]
