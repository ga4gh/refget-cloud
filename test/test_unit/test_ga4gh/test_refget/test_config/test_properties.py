# -*- coding: utf-8 -*-
"""Unit tests for Properties class"""

import pytest
from ga4gh.refget.config.defaults import \
    DEFAULT_PROPERTIES, DEFAULT_ALLOWED_PROPERTY_KEYS
from ga4gh.refget.config.properties import Properties
from ga4gh.refget.config.exceptions import RefgetInvalidPropertyException

testdata = [
    (
        {
            "source.base_url": "https://datasource.com",
            "server.port": "7878"
        },
        False
    ),
    (
        {
            "source.base_url": "https://example.com",
            "source.sequence_path": "/seq/{seqid}",
            "source.metadata_path": "/metadata/{seqid}",
            "server.port": "9998"
        },
        False
    ),
    (
        {
            "source.base_url": "https://example.com",
            "invalid.property": "anyValue"
        },
        True
    )
]

@pytest.mark.parametrize("props_dict,raises_exception", testdata)
def test_properties(props_dict, raises_exception):
    
    try:
        properties = Properties(props_dict)
        for key in DEFAULT_ALLOWED_PROPERTY_KEYS:
            if key in props_dict.keys():
                assert properties.get(key) == props_dict[key]
            else:
                assert properties.get(key) == DEFAULT_PROPERTIES[key]
        assert raises_exception == False
    except RefgetInvalidPropertyException as e:
        assert raises_exception == True
