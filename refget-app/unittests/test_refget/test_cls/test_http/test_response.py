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

def test_update_headers():

    resp = Response()
    new_headers = {
        "Accept": "text/encoding1",
        "Range": "bytes=5-20"
    }
    resp.update_headers(new_headers)
    assert resp.get_header("Accept") == "text/encoding1"
    assert resp.get_header("Range") == "bytes=5-20"

def test_get_data():
    resp = Response()
    new_data = {
        "subseq-type": "start-end"
    }
    data = resp.get_data()
    resp.update_data(new_data)
    assert resp.get_datum("subseq-type") == "start-end"
