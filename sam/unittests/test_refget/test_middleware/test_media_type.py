# -*- coding: utf-8 -*-
"""Unit tests for the media type midware
"""

import json
from ga4gh.refget.serverless.config.constants import *
from ga4gh.refget.serverless.middleware.start import StartMidware
from ga4gh.refget.serverless.middleware.media_type \
    import MediaTypeMW, MediaTypeMidware

def test_media_type_midware():

    test_cases = [
        # INVALID MEDIA TYPE
        {
            "event": {
                "headers": {
                    "Accept": "text/strange1, text/strange2;"
                }
            },
            "context": {},
            "assertions": {
                "statusCode": 406,
                "headers": {},
                "body": json.dumps({
                    "message": "requested media type(s) not supported"
                })
            }
        },
        # VALID MEDIA TYPE: */*
        {
            "event": {
                "headers": {
                    "Accept": "*/*;"
                }
            },
            "context": {},
            "assertions": {
                "statusCode": 200,
                "headers": {
                    "Content-Type": DEFAULT_CONTENT_TYPE_JSON
                },
                "body": ""
            }
        }
    ]

    for case in test_cases:

        @StartMidware(case["event"], case["context"])
        @MediaTypeMidware(case["event"], case["context"])
        def worker(resp):
            return resp
        r = worker().finalize()
        assert case["assertions"]["statusCode"] == r["statusCode"]
        assert case["assertions"]["body"] == r["body"]
        for hkey in case["assertions"]["headers"].keys():
            assert case["assertions"]["headers"][hkey] == r["headers"][hkey]
