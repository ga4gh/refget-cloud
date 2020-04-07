DEFAULT_SOURCE_BASE_URL = "http://insdc-mirror.s3-website-us-west-2.amazonaws.com"
DEFAULT_SOURCE_SEQUENCE_PATH = "/sequence/{seqid}"
DEFAULT_SOURCE_METADATA_PATH = "/metadata/json/{seqid}.json"

DEFAULT_SERVER_PORT = 8888

DEFAULT_ALLOWED_PROPERTY_KEYS = {
    "source.base_url",
    "source.sequence_path",
    "source.metadata_path",
    "server.port"
}

DEFAULT_PROPERTIES = {
    "source.base_url": DEFAULT_SOURCE_BASE_URL,
    "source.sequence_path": DEFAULT_SOURCE_SEQUENCE_PATH,
    "source.metadata_path": DEFAULT_SOURCE_METADATA_PATH,
    "server.port": DEFAULT_SERVER_PORT
}