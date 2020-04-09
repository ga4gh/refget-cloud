# -*- coding: utf-8 -*-
"""Unit tests for StatusCodes class"""

import pytest
from ga4gh.refget.http.status_codes import StatusCodes as SC

testdata_is_successful = [
    (SC.OK, True),
    (SC.PARTIAL_CONTENT, True),
    (SC.REDIRECT_FOUND, False),
    (SC.BAD_REQUEST, False),
    (SC.NOT_FOUND, False),
    (SC.NOT_ACCEPTABLE, False),
    (SC.REQUESTED_RANGE_NOT_SATISFIABLE, False),
    (SC.NOT_IMPLEMENTED, False)
]

@pytest.mark.parametrize("code,successful", testdata_is_successful)
def test_is_successful_code(code, successful):

    assert SC.is_successful_code(code) == successful
