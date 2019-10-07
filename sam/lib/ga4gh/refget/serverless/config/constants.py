# -*- coding: utf-8 -*-
"""Constants to be used in various modules throughout the application"""

DEFAULT_CONTENT_TYPE_TEXT = "text/vnd.ga4gh.refget.v1.0.0+plain"
"""Default MIME type string for text-based responses"""
DEFAULT_CONTENT_TYPE_JSON = "application/vnd.ga4gh.refget.v1.0.0+json"
"""Default MIME type string for JSON-based responses"""
CHARSET = "charset=us-ascii"
"""Default charset for use in Content-Type response header"""
S3_BASE_URL = "http://refget-test.s3-website.eu-west-2.amazonaws.com/"
"""Base URL to S3 Bucket containing sequences and metadata"""
S3_SEQUENCE_URL = S3_BASE_URL + "sequence/"
"""Base URL to S3 Bucket's sequence directory"""
S3_METADATA_URL = S3_BASE_URL + "metadata/json/"
"""Base URL to S3 Bucket's metadata directory"""

__all__ = [
    "DEFAULT_CONTENT_TYPE_TEXT",
    "DEFAULT_CONTENT_TYPE_JSON",
    "CHARSET",
    "S3_BASE_URL",
    "S3_SEQUENCE_URL",
    "S3_METADATA_URL"
]