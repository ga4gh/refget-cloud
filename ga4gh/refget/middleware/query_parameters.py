# -*- coding: utf-8 -*-
"""Checks that query string parameters and/or headers are set correctly"""

import json
import re
import requests
from ga4gh.refget.config.constants import *
from ga4gh.refget.http.status_codes import StatusCodes as SC
from ga4gh.refget.util.resolve_url import resolve_metadata_url

class QueryParametersMW(object):
    """Middleware, checks request for appropriate query parameters

    QueryParametersMW checks "start" and/or "end" query parameters, or the
    "Range" header, which all deal with requesting subsequences. If any of 
    these request parameters/headers are malformed, it sets the response status
    code to an appropriate error code
    """

    @staticmethod
    def middleware_func(properties, request, response):
        """performs all subsequence param validation submethods

        :param event: AWS SAM event (incl. headers, path params, query params)
        :type event: dict[str, object]
        :param resp: response object to modify
        :type resp: class:`ga4gh.refget.serverless.cls.http.response.Response`
        """
        
        # a series of functions to perform on the request, if any subseq
        # params have been provided 
        checkfuncs = [
            QueryParametersMW._QueryParametersMW__get_subseq_coords,
            QueryParametersMW._QueryParametersMW__check_datatype,
            QueryParametersMW._QueryParametersMW__check_datarange,
            QueryParametersMW._QueryParametersMW__check_noncircular
        ]

        # the response data dict is annotated with 3 parameters:
        # 1. start: indicating subseq start
        # 2. end: indicating subseq end
        # 3. subseq-type: indicating whether the subsequence was specified via
        #                 start/end query parameters, or via the Range header

        # initially, set all to None in case no subsequence requested
        response.update_data({"start": None, "end": None, "subseq-type": None})

        # check how subsequence parameters have been specified, if at all
        QueryParametersMW._QueryParametersMW__check_supplied_params(
            properties, request, response)

        # if subseq parameters have been specified (and are so far OK), iterate
        # through the various check functions, modifying response as necessary 
        if response.get_status_code() == SC.OK and response.get_datum("subseq-type"):
            for checkfunc in checkfuncs:
                if response.get_status_code() == SC.OK:
                    checkfunc(properties, request, response)
    
    @staticmethod
    def __check_supplied_params(properties, request, response):
        """check if subsequence parameters are supplied and specified correctly

        Updates the response data dictionary with start/end positions, and the
        subseq-type. ONLY ONE of start/end query params and Range header can
        be supplied. If BOTH subseq methods are provided, response is modified
        to indicate this is a BAD REQUEST

        :param event: AWS SAM event (incl. headers, path params, query params)
        :type event: dict[str, object]
        :param resp: response object to modify
        :type resp: class:`ga4gh.refget.serverless.cls.http.response.Response`
        """

        use_start_end = False
        use_range = False

        # check if start/end was provided in the request, 
        # indicate subseq-type is 'start-end' in response data dict

        start = request.get_query_param("start")
        end = request.get_query_param("end")
        range_header = request.get_header("Range")

        if start or end:
            use_start_end = True
            response.put_data("subseq-type", "start-end")
        
        # check if Range header was provided in the request,
        # indicate subseq-type is 'Range' in response data dict
        if range_header:
            use_range = True
            response.put_data("subseq-type", "range")
        
        # if both start/end and AND Range header, this is a BAD REQUEST
        if use_start_end and use_range:
            response.set_status_code(SC.BAD_REQUEST)
            response.set_body(json.dumps({
                "message": "Cannot provide both sequence start/end AND Range"
            }))
    
    @staticmethod
    def __get_subseq_coords(properties, request, response):
        """parse start/end bases according to subsequence specification format

        Sets 'start' and 'end' bases in data dictionary, based on how the
        subsequence was provided ('range' or 'start-end'). If the Range header
        does not follow the expected format, this is a BAD REQUEST

        :param event: AWS SAM event (incl. headers, path params, query params)
        :type event: dict[str, object]
        :param resp: response object to modify
        :type resp: class:`ga4gh.refget.serverless.cls.http.response.Response`
        """

        start = None
        end = None

        # if subseq-type is 'start-end', then set base start and end according
        # to values of query parameters (if either start or end is not 
        # specified, then keep that value as None)
        subseq_type = response.get_datum("subseq-type")
        if subseq_type == "start-end":
            start = request.get_query_param("start")
            end = request.get_query_param("end")

        # if subseq-type is 'range', then set base start and end according to
        # values in Range header. If Range header does not match expected 
        # format/regex, this is a BAD REQUEST
        elif subseq_type == "range":
            range_header = request.get_header("Range")
            range_pattern = re.compile("bytes=(\d+)-(\d+)")
            range_match = range_pattern.search(range_header)
            if range_match:
                start = range_match.group(1)
                end = range_match.group(2)
            else:
                response.set_status_code(SC.BAD_REQUEST)
                response.set_body(json.dumps({
                    "message": "Invalid 'Range' header"
                }))
        
        # update the response data dictionary
        response.update_data({"start": start, "end": end})
    
    @staticmethod
    def __check_datatype(properties, request, response):
        """checks the start/end parameters are valid positive integers

        If either start or end base provided by request are not integers, this
        is a BAD REQUEST 

        :param event: AWS SAM event (incl. headers, path params, query params)
        :type event: dict[str, object]
        :param resp: response object to modify
        :type resp: class:`ga4gh.refget.serverless.cls.http.response.Response`
        """

        def unsigned_int_check(val):
            is_valid_number = True
            try:
                val = int(val)
                if val < 0:
                    raise ValueError("Not an unsigned int")
            except ValueError as e:
                is_valid_number = False
            
            return is_valid_number
        
        # for start and end base, if not None, perform the number check
        # if either is not an unsigned int, this is a BAD REQUEST
        vals = [response.get_datum("start"), response.get_datum("end")]
        for val in vals:
            if val:
                if not unsigned_int_check(val):
                    response.set_status_code(SC.BAD_REQUEST)
                    response.set_body(json.dumps({
                        "message": "start/end must be unsigned int"
                    }))
    
    @staticmethod
    def __check_datarange(properties, request, response):
        """check that start/end bases fall within accepted range

        start/end accepted range is slightly different based on whether subseq
        was request by query parameters or Range header. If the requested subseq
        violates constraints then the response status code will be set to
        REQUESTED RANGE NOT SATIFIABLE

        :param event: AWS SAM event (incl. headers, path params, query params)
        :type event: dict[str, object]
        :param resp: response object to modify
        :type resp: class:`ga4gh.refget.serverless.cls.http.response.Response`
        """

        try:
            # get sequence length from metadata object stored on S3
            seqid = request.get_path_param("seqid")
            metadata_url = resolve_metadata_url(properties, seqid)
            metadata_response = requests.get(metadata_url)
            if not SC.is_successful_code(metadata_response.status_code):
                response.set_status_code(metadata_response.status_code)
                response.set_body(json.dumps({
                    "message": "sequence %s not found" % seqid
                }))
                raise Exception("Metadata for object not found")

            metadata_json = metadata_response.json()
            seq_length = int(metadata_json["metadata"]["length"])

            # perform range checking on both start (if specified) 
            # and end (if specified)
            keys = ["start", "end"]
            val_dict = {"start": response.get_datum("start"), 
                        "end": response.get_datum("end")}
            
            # comparator functions by subseq-type and whether it is start or end
            # base. for each comparator function, if True is returned, then that
            # parameter violates the acceptable range, and response status code
            # set to REQUEST RANGE NOT SATISFIABLE
            comparator_dict = {
                "range": { # if subseq specified by 'Range' header, then
                    "start": lambda val, seqlen: int(val) >= seqlen,
                        # start base MUST be LESS THAN sequence length
                    "end": lambda val, seqlen: False
                        # any end base is acceptable
                },
                "start-end": { # if subseq specified by start/end parameters, 
                               # then
                    "start": lambda val, seqlen: int(val) >= seqlen,
                        # start base MUST be LESS THAN sequence length
                    "end": lambda val, seqlen: int(val) > seqlen
                        # end base MUST be LESS THAN OR EQUAL TO sequence length
                }
            }

            subseq_type = response.get_datum("subseq-type")
            for key in keys:
                val = val_dict[key]
                if val:
                    comparator_func = comparator_dict[subseq_type][key]
                    if comparator_func(val, seq_length):
                        response.set_status_code(SC.REQUESTED_RANGE_NOT_SATISFIABLE)
                        response.set_body(json.dumps({
                            "message": "Invalid sequence range provided"
                        }))
        except Exception as e:
            pass
    
    @staticmethod
    def __check_noncircular(properties, event, resp):
        """check requested subsequence is not circular

        circular sequence requests are not currently supported on this server.
        if the start base is higher than the end base, this will give the 
        response an error status code (exact code based on subeq specification
        type)

        :param event: AWS SAM event (incl. headers, path params, query params)
        :type event: dict[str, object]
        :param resp: response object to modify
        :type resp: class:`ga4gh.refget.serverless.cls.http.response.Response`
        """

        # the status code to return based on whether the subsequence was 
        # specified by start/end, or by range header
        status_codes = {"range": SC.REQUESTED_RANGE_NOT_SATISFIABLE,
                        "start-end": SC.NOT_IMPLEMENTED}

        start, end, subseq_type = \
            [resp.get_datum(a) for a in ["start", "end", "subseq-type"]]
        
        # if request start is greater than end, set the response status code
        # to an error code
        if start and end:
            if int(start) > int(end):
                resp.set_status_code(status_codes[subseq_type])
                resp.set_body(json.dumps({
                    "message": "server DOES NOT support circular " +
                                "sequences, end MUST be higher than start"
                }))

def QueryParametersMidware(properties, request, response):
    """Creates the query parameter middleware decorator function

    :param event: AWS SAM event (incl. headers, path params, query params)
    :type event: dict[str, object]
    :param context: AWS SAM context
    :type context: dict[str, str]
    :return: query parameters middleware decorator function
    :rtype: function
    """

    def decorator_function(func):
        def wrapper(properties, request, response):
            # perform query param middleware function, which modifies the 
            # response status code/headers/body as necessary
            # if status code is still OK at end of function, then execute the
            # inner function
            QueryParametersMW.middleware_func(properties, request, response)
            if response.get_status_code() == SC.OK:
                return func(properties, request, response)
            else:
                return response
        return wrapper
    return decorator_function
