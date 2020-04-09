# -*- coding: utf-8 -*-
"""Unit tests for Exceptions"""

import pytest
from ga4gh.refget.config.exceptions import RefgetException, \
    RefgetInvalidPropertyException, RefgetPropertiesFileNotFoundException, \
    RefgetPropertiesParseException

testdata = [
    (RefgetException, "invalid operation", 1),
    (RefgetInvalidPropertyException, "invalid property", 2),
    (RefgetPropertiesFileNotFoundException, "file not found", 3),
    (RefgetPropertiesParseException, "could not parse file", 4)
]

@pytest.mark.parametrize("exc_class,message,exp_exit_code", testdata)
def test_raise_exception(exc_class, message, exp_exit_code):
    
    try:
        raise exc_class(message)
    except exc_class as e:
        assert e.get_exit_code() == exp_exit_code
        assert e.get_message() == message
        assert str(e) == message
