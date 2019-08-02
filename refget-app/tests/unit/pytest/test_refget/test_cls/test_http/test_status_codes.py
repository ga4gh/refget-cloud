# -*- coding: utf-8 -*-
"""Module pytest.test_refget.test_cls.test_http.test_status_codes.py
Unit tests for the StatusCodes class
"""

from cls.http.status_codes import StatusCodes as SC

def test_correct_status_codes():

    assertions = [
        [SC.OK, 200],
        [SC.PARTIAL_CONTENT, 206],
        [SC.REDIRECT_FOUND, 302],
        [SC.BAD_REQUEST, 400],
        [SC.NOT_FOUND, 404],
        [SC.NOT_ACCEPTABLE, 406],
        [SC.REQUESTED_RANGE_NOT_SATISFIABLE, 416],
        [SC.NOT_IMPLEMENTED, 501]
    ]

    for code in assertions:
        assert code[0] == code[1]

def test_is_successful_code():

    assertions = [
        [SC.OK, True],
        [SC.PARTIAL_CONTENT, True],
        [SC.REDIRECT_FOUND, False],
        [SC.BAD_REQUEST, False],
        [SC.NOT_FOUND, False],
        [SC.NOT_ACCEPTABLE, False],
        [SC.REQUESTED_RANGE_NOT_SATISFIABLE, False],
        [SC.NOT_IMPLEMENTED, False]
    ]

    for code in assertions:
        assert SC.is_successful_code(code[0]) == code[1]