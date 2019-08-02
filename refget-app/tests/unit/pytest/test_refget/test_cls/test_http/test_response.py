# -*- coding: utf-8 -*-
"""Module pytest.test_refget.test_cls.test_http.test_response.py
Unit tests for the Response class
"""

from cls.http.response import Response
from cls.http.status_codes import StatusCodes as SC

def test_constructor():

    resp = Response()
    assert resp.get_status_code() == SC.BAD_REQUEST
    assert hasattr(resp, 'headers')
    assert hasattr(resp, 'body')
    assert hasattr(resp, 'data')

