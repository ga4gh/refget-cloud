# -*- coding: utf-8 -*-
"""Default values for modifiable server properties"""

DEFAULT_SOURCE_BASE_URL = "http://insdc-mirror.s3-website-us-west-2.amazonaws.com"
"""Refget server points to INSDC AWS S3 bucket by default"""

DEFAULT_SOURCE_SEQUENCE_PATH = "/sequence/{seqid}"
"""Refget server resolves sequence requests to specified dir in S3 bucket"""

DEFAULT_SOURCE_METADATA_PATH = "/metadata/json/{seqid}.json"
"""Refget server resolves metadata requests to specified dir in S3 bucket"""

DEFAULT_SERVER_PORT = 8888
"""Default port server runs on"""

DEFAULT_ALLOWED_PROPERTY_KEYS = {
    "source.base_url",
    "source.sequence_path",
    "source.metadata_path",
    "server.port"
}
"""Allowed modifiable properties in properties file"""

DEFAULT_PROPERTIES = {
    "source.base_url": DEFAULT_SOURCE_BASE_URL,
    "source.sequence_path": DEFAULT_SOURCE_SEQUENCE_PATH,
    "source.metadata_path": DEFAULT_SOURCE_METADATA_PATH,
    "server.port": DEFAULT_SERVER_PORT
}
"""Default properties for each property key"""