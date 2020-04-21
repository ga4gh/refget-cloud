# -*- coding: utf-8 -*-
"""Unit tests for Response class"""

import pytest
from ga4gh.refget.http.response import Response
from ga4gh.refget.http.status_codes import StatusCodes as SC
from ga4gh.refget.config.constants import CONTENT_TYPE_JSON_REFGET_VND, \
    CONTENT_TYPE_TEXT_REFGET_VND

testdata_body = [
    ("ACGT"),
    ('{"message": "NOTFOUND"}'),
    ('''{"service": {"circular_supported": false}}''')
]

testdata_status_code = [
    (SC.OK),
    (SC.PARTIAL_CONTENT),
    (SC.NOT_ACCEPTABLE)
]

testdata_header = [
    ("Content-Type", CONTENT_TYPE_JSON_REFGET_VND),
    ("Content-Type", CONTENT_TYPE_TEXT_REFGET_VND),
    ("Content-Type", "application/json")
]

testdata_data = [
    ("seqid", "ga4gh:SQ.HKyMuwwEWbdUDXfk5o1EGxGeqBmon6Sp"),
    ("subseq-type", "start-end"),
    ("subseq-type", "range")
]

testdata_redirect = [
    ("https://ga4gh.org"),
    ("https://example.com"),
    ("https://anotherexample.com")
]

@pytest.mark.parametrize("body", testdata_body)
def test_body(body):
    response = Response()
    response.set_body(body)
    assert response.get_body() == body

@pytest.mark.parametrize("status_code", testdata_status_code)
def test_status_code(status_code):
    response = Response()
    response.set_status_code(status_code)
    assert response.get_status_code() == status_code

@pytest.mark.parametrize("key,value", testdata_header)
def test_header(key, value):
    response = Response()
    response.put_header(key, value)
    assert response.get_header(key) == value
    assert response.get_headers()[key] == value
    
    new_dict = {"headerA": "valueA", "headerB": "valueB"}
    response.update_headers(new_dict)
    assert response.get_header(key) == value
    assert response.get_headers()[key] == value

@pytest.mark.parametrize("key,value", testdata_data)
def test_data(key, value):
    response = Response()
    response.put_data(key, value)
    assert response.get_datum(key) == value
    assert response.get_data()[key] == value
    
    new_dict = {"dataA": "valueA", "dataB": "valueB"}
    response.update_data(new_dict)
    assert response.get_datum(key) == value
    assert response.get_data()[key] == value

@pytest.mark.parametrize("url", testdata_redirect)
def test_redirect(url):
    response = Response()
    response.set_redirect_found(url)
    assert response.get_status_code() == SC.REDIRECT_FOUND
    assert response.get_header("Location") == url
