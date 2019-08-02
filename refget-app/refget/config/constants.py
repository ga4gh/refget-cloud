# -*- coding: utf-8 -*-
"""Module config.constants.py
Constants to be used in various modules throughout the application

Attributes:
    DEFAULT_CONTENT_TYPE_TEXT (str): MIME type for text-based responses
    DEFAULT_CONTENT_TYPE_JSON (str): MIME type for json-based response
    CHARSET (str): charset to be used in response Content-Type header
    S3_BASE_URL (str): base URL to AWS S3 bucket holding sequences and metadata 
    S3_SEQUENCE_URL (str): URL to sequence directory of S3 bucket
    S3_METADATA_URL (str): URL to metadata directory of S3 bucket
"""

DEFAULT_CONTENT_TYPE_TEXT = "text/vnd.ga4gh.refget.v1.0.0+plain"
DEFAULT_CONTENT_TYPE_JSON = "application/vnd.ga4gh.refget.v1.0.0+json"
CHARSET = "charset=us-ascii"
S3_BASE_URL = "http://refget-test.s3-website.eu-west-2.amazonaws.com/"
S3_SEQUENCE_URL = S3_BASE_URL + "sequence/"
S3_METADATA_URL = S3_BASE_URL + "metadata/json/"