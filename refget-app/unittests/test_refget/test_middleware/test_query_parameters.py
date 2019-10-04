# -*- coding: utf-8 -*-
"""Unit tests for the query parameters midware
"""

import json
from config.constants import *
from middleware.start import StartMidware
from middleware.media_type import MediaTypeMidware
from middleware.query_parameters import QueryParametersMidware
from refget_test_constants import *

def test_query_parameters_midware():

    test_cases = [
        # CASE 0: INVALID, PROVIDE BOTH RANGE AND START/END
        {
            "event": {
                "headers": {
                    "Range": "bytes=100-400"
                },
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
                "statusCode": 400,
                "headers": {
                    "Content-Type": DEFAULT_CONTENT_TYPE_JSON
                },
                "body": json.dumps({
                    "message": "Cannot provide both sequence start/end AND " \
                               + "Range"
                })
            }
        },
        # CASE 1: INVALID, RANGE OUT OF BOUNDS
        {
            "event": {
                "headers": {
                    "Range": "bytes=6000-10000"
                },
                "queryStringParameters": None,
                "pathParameters": {
                    "id": PHAGE_MD5
                }
            },
            "context": {},
            "assertions": {
                "statusCode": 416,
                "headers": {
                    "Content-Type": DEFAULT_CONTENT_TYPE_JSON
                },
                "body": json.dumps({
                    "message": "Invalid sequence range provided"
                })
            }
        },
        # CASE 2: INVALID, RANGE MALFORMED
        {
            "event": {
                "headers": {
                    "Range": "foo=100-400"
                },
                "queryStringParameters": None,
                "pathParameters": {
                    "id": PHAGE_MD5
                }
            },
            "context": {},
            "assertions": {
                "statusCode": 400,
                "headers": {
                    "Content-Type": DEFAULT_CONTENT_TYPE_JSON
                },
                "body": json.dumps({
                    "message": "Invalid 'Range' header"
                })
            }
        },
        # CASE 3: INVALID, START/END DOES NOT CONTAIN UNSIGNED INTS
        {
            "event": {
                "headers": {},
                "queryStringParameters": {
                    "start": "onehundred",
                    "end": "fourhundred"
                },
                "pathParameters": {
                    "id": PHAGE_MD5
                }
            },
            "context": {},
            "assertions": {
                "statusCode": 400,
                "headers": {
                    "Content-Type": DEFAULT_CONTENT_TYPE_JSON
                },
                "body": json.dumps({
                    "message": "start/end must be unsigned int"
                })
            }
        },
        # CASE 4: INVALID, CIRCULAR RANGE PROVIDED
        {
            "event": {
                "headers": {
                    "Range": "bytes=400-100"
                },
                "queryStringParameters": None,
                "pathParameters": {
                    "id": PHAGE_MD5
                }
            },
            "context": {},
            "assertions": {
                "statusCode": 416,
                "headers": {
                    "Content-Type": DEFAULT_CONTENT_TYPE_JSON
                },
                "body": json.dumps({
                    "message": "server DOES NOT support circular sequences, "
                               "end MUST be higher than start"
                })
            }
        },
    ]

    for case in test_cases:

        @StartMidware(case["event"], case["context"])
        @MediaTypeMidware(case["event"], case["context"])
        @QueryParametersMidware(case["event"], case["context"])
        def worker(resp):
            return resp
        r = worker().finalize()
        print(r)
        print("***")
        assert case["assertions"]["statusCode"] == r["statusCode"]
        assert case["assertions"]["body"] == r["body"]
        for hkey in case["assertions"]["headers"].keys():
            assert case["assertions"]["headers"][hkey] == r["headers"][hkey]
    

test_query_parameters_midware()
