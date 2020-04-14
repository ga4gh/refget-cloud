# -*- coding: utf-8 -*-
"""Unit tests for RefgetServer class"""

import pytest
from ga4gh.refget.config.exceptions import RefgetException
from ga4gh.refget.server.server import RefgetServer, GetServiceInfoHandler, \
    GetMetadataHandler, GetSequenceHandler

props_dir = "test/common/properties/"

testdata_setup = [
    (
        props_dir + "application.properties",
        False,
        3,
        "properties file not found: " + props_dir + "application.properties"
    ),
    (
        props_dir + "application.properties.0",
        True,
        None,
        ""
    ),
    (
        props_dir + "application.properties.1",
        False,
        4,
        "Could not parse properties file"
    ),
    (
        None,
        True,
        None,
        ""
    ),
]

testdata_handlers = [
    (
        GetServiceInfoHandler,
        props_dir + "application.properties.0"
    )

]

@pytest.mark.parametrize("props_file,e_success,e_code,e_msg", testdata_setup)
def test_server_setup(props_file, e_success, e_code, e_msg):

    try:
        server = RefgetServer(props_file)
        assert e_success == True
    except RefgetException as e:
        assert e_success == False
        assert e.get_exit_code() == e_code
        assert e.get_message() == e_msg
