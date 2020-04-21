# -*- coding: utf-8 -*-
"""Unit tests for Request class"""

import pytest
from ga4gh.refget.http.request import Request

testdata_header = [
    ("Content-Type", "appliciation/json"),
    ("Content-Type", "text/plain"),
    ("Range", "bytes=25-100")
]

testdata_path = [
    ("seqid", "ga4gh:SQ.HKyMuwwEWbdUDXfk5o1EGxGeqBmon6Sp"),
    ("seqid", "1cac8cbb0c0459b7540d77e4e68d441b119ea819a89fa4a9"),
    ("seqid", "000000ca1658e86c7439f5b4f1c1341c")
]

testdata_query = [
    ("start", "20"),
    ("start", "600"),
    ("end", "999")
]

@pytest.mark.parametrize("key,value", testdata_header)
def test_header(key, value):
    
    request = Request()
    request.add_header(key, value)
    assert request.get_header(key) == value
    assert request.get_headers()[key] == value

@pytest.mark.parametrize("key,value", testdata_path)
def test_path(key, value):
    
    request = Request()
    request.add_path_param(key, value)
    assert request.get_path_param(key) == value
    assert request.get_path_params()[key] == value

@pytest.mark.parametrize("key,value", testdata_query)
def test_query(key, value):
    
    request = Request()
    request.add_query_param(key, value)
    assert request.get_query_param(key) == value
    assert request.get_query_params()[key] == value
