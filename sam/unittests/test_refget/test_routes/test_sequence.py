# -*- coding: utf-8 -*-
"""Unit tests for the sequence routes
"""

import json
from ga4gh.refget.serverless.config.constants import *
from ga4gh.refget.serverless.routes.sequence import *
from refget_test_constants import *

def test_sequence():
    test_cases = [
        # CASE 0: INVALID ID, NO QUERY STRING PARAMS
        {
            "event": {
                "headers": [],
                "queryStringParameters": None,
                "pathParameters": {
                    "id": INVALID_CHECKSUM
                }
            },
            "context": {},
            "assertions": {
                "statusCode": 302,
                "headers": {
                    "Location": REDIRECT_LOCATION_INVALID_MD5,
                    "Content-Type": DEFAULT_CONTENT_TYPE_TEXT
                },
                "body": ""
            }
        },
        # CASE 1: VALID ID, NO QUERY STRING PARAMS
        {
            "event": {
                "headers": [],
                "queryStringParameters": None,
                "pathParameters": {
                    "id": PHAGE_MD5
                }
            },
            "context": {},
            "assertions": {
                "statusCode": 302,
                "headers": {
                    "Location": REDIRECT_LOCATION_PHAGE_MD5,
                    "Content-Type": DEFAULT_CONTENT_TYPE_TEXT
                },
                "body": ""
            }
        },
        # CASE 2: INVALID ID, START-END SPECIFIED
        {
            "event": {
                "headers": [],
                "queryStringParameters": {
                    "start": 100,
                    "end": 400
                },
                "pathParameters": {
                    "id": INVALID_CHECKSUM
                }
            },
            "context": {},
            "assertions": {
                "statusCode": 404,
                "headers": {
                    "Content-Type": DEFAULT_CONTENT_TYPE_TEXT
                },
                "body": json.dumps({
                        "message": "sequence {} not found".format(
                            INVALID_CHECKSUM)
                        })
            }
        },
        # CASE 3: VALID ID, START-END SPECIFIED
        {
            "event": {
                "headers": [],
                "queryStringParameters": {
                    "start": 100,
                    "end": 400
                },
                "pathParameters": {
                    "id": PHAGE_MD5
                }
            },
            "context": {},
            "assertions": {
                "statusCode": 200,
                "headers": {
                    "Content-Type": DEFAULT_CONTENT_TYPE_TEXT,
                    "Content-Length": 300
                },
                "body": PHAGE_SUBSEQ_100_400
            }
        },
        # CASE 4: INVALID ID, RANGE SPECIFIED
        {
            "event": {
                "headers": {
                    "Range": "bytes=100-400"
                },
                "queryStringParameters": None,
                "pathParameters": {
                    "id": INVALID_CHECKSUM
                }
            },
            "context": {},
            "assertions": {
                "statusCode": 404,
                "headers": {
                    "Content-Type": DEFAULT_CONTENT_TYPE_TEXT,
                },
                "body": json.dumps({
                    "message": "sequence " + INVALID_CHECKSUM + " not found"
                })
            }
        }
        # CASE 5: VALID ID, RANGE SPECIFIED
    ]

    for case in test_cases:
        r = get_sequence(case["event"], case["context"])
        assert case["assertions"]["statusCode"] == r["statusCode"]
        assert case["assertions"]["body"] == r["body"]
        for hkey in case["assertions"]["headers"].keys():
            assert case["assertions"]["headers"][hkey] == r["headers"][hkey]

def test_metadata():

    test_cases = [
        # CASE 0: INVALID ID
        {
            "event": {
                "headers": [],
                "queryStringParameters": None,
                "pathParameters": {
                    "id": INVALID_CHECKSUM
                }
            },
            "context": {},
            "assertions": {
                "statusCode": 302,
                "headers": {
                    "Content-Type": DEFAULT_CONTENT_TYPE_JSON,
                    "Location": REDIRECT_LOCATION_INVALID_MD5_METADATA
                },
                "body": ""
            }
        },
        # CASE 1: VALID ID
        {
            "event": {
                "headers": [],
                "queryStringParameters": None,
                "pathParameters": {
                    "id": PHAGE_MD5
                }
            },
            "context": {},
            "assertions": {
                "statusCode": 302,
                "headers": {
                    "Content-Type": DEFAULT_CONTENT_TYPE_JSON,
                    "Location": REDIRECT_LOCATION_PHAGE_MD5_METADATA
                },
                "body": ""
            }
        }
    ]

    for case in test_cases:
        r = get_metadata(case["event"], case["context"])
        assert case["assertions"]["statusCode"] == r["statusCode"]
        assert case["assertions"]["body"] == r["body"]
        for hkey in case["assertions"]["headers"].keys():
            assert case["assertions"]["headers"][hkey] == r["headers"][hkey]

def test_service_info():
    event = {
        "headers": []
    }
    context = {}
    
    r = get_service_info(event, context)
    body = json.loads(r["body"])
    service = body["service"]
    assert r['statusCode'] == 200
    assert service["circular_supported"] == False
    assert service["subsequence_limit"] == 300000
    assert all(algo in service["algorithms"] for algo in ["md5", "trunc512"])
    assert all(v in service["supported_api_versions"] for v in ["1.0"])

test_sequence()