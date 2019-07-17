import json
import re
from config.constants import *
from config.sequences import *

class QueryParametersMW(object):

    @staticmethod
    def middleware_func(event, partial_response):
        
        checkfuncs = [
            QueryParametersMW._QueryParametersMW__check_datatype,
            QueryParametersMW._QueryParametersMW__check_datarange,
            QueryParametersMW._QueryParametersMW__check_noncircular
        ]
        start, end, subseq_type = [None, None, None]

        e, r = event, partial_response
        r = QueryParametersMW._QueryParametersMW__check_supplied_params(e, r)

        if r["statusCode"] == 200 and r["data"]["subseq-type"] != "none":
            res = QueryParametersMW._QueryParametersMW__get_subseq_coords(e, r)
            start, end, subseq_type = res

            for checkfunc in checkfuncs:
                if r["statusCode"] == 200:
                    r = checkfunc(e, r, start, end, subseq_type)
            
        r["data"]["start"] = start
        r["data"]["end"] = end
        r["data"]["subseq_type"] = subseq_type

        return r
    
    @staticmethod
    def __get_subseq_coords(event, partial_response):
        start = None
        end = None

        subseq_type = partial_response["data"]["subseq-type"]
        if subseq_type == "start-end":
            if event['queryStringParameters']:
                params = event['queryStringParameters']
                if "start" in params.keys():
                    start = params["start"]
                if "end" in params.keys():
                    end = params["end"]

        elif subseq_type == "range":
            range_header = event["headers"]["Range"]
            range_pattern = re.compile("bytes=(\d+)-(\d+)")
            range_match = range_pattern.search(range_header)
            if range_match:
                start = range_match.group(1)
                end = range_match.group(2)
            else:
                partial_response["statusCode"] = 400
                partial_response["body"] = json.dumps({
                    "message": "Invalid 'Range' header"
                })
            
        return [start, end, subseq_type]

    @staticmethod
    def __check_supplied_params(event, partial_response):
        use_start_end = False
        use_range = False
        partial_response["data"]["subseq-type"] = "none"

        if event['queryStringParameters']:
            params = event['queryStringParameters']
            if "start" in params.keys() or "end" in params.keys():
                use_start_end = True
                partial_response["data"]["subseq-type"] = "start-end"
        
        if "Range" in event['headers']:
            use_range = True
            partial_response["data"]["subseq-type"] = "range"
        
        if use_start_end and use_range:
            partial_response["statusCode"] = 400
            partial_response["body"] = json.dumps({
                "message": "Cannot provide both sequence start/end AND Range"
            })
        
        return partial_response
    
    def __check_datatype(event, partial_response, start, end, subseq_type):

        def number_check(val):
            is_valid_number = True
            try:
                val = int(val)
                if val < 0:
                    raise ValueError("Not an unsigned int")
            except ValueError as e:
                is_valid_number = False
            
            return is_valid_number
        
        vals = [start, end]
        for val in vals:
            if val:
                if not number_check(val):
                    partial_response["statusCode"] = 400
                    partial_response["body"] = json.dumps({
                        "message": "start/end must be unsigned int"
                    })
            
        return partial_response
    
    def __check_datarange(event, partial_response, start, end, subseq_type):

        seq_length = METADATA[partial_response["data"]["trunc512_id"]]["length"]
        keys = ["start", "end"]
        val_dict = {"start": start, "end": end}
        # comparator function by:
        # end inclusivity (True/False)
        # Value for range start or end
        comparator_dict = {
            "range": {
                "start": lambda val, seqlen: int(val) >= seqlen,
                "end": lambda val, seqlen: False
            },
            "start-end": {
                "start": lambda val, seqlen: int(val) >= seqlen,
                "end": lambda val, seqlen: int(val) > seqlen
            }
        }
        
        for key in keys:
            val = val_dict[key]
            if val:
                comparator_func = comparator_dict[subseq_type][key]
                if comparator_func(val, seq_length):
                    partial_response["statusCode"] = 416
                    partial_response["body"] = json.dumps({
                        "message": "Invalid sequence range provided"
                    })
            
        return partial_response
    
    def __check_noncircular(event, partial_response, start, end, subseq_type):

        # the status code to return based on whether the subsequence was 
        # specified by start/end , or by range header
        status_codes = {"range": 416, "start-end": 501}
        
        if start and end:
            if int(start) > int(end):
                partial_response["statusCode"] = status_codes[subseq_type]
                partial_response["body"] = json.dumps({
                    "message": "server DOES NOT support circular " +
                                "sequences, end MUST be higher than start"
                })
        return partial_response

def QueryParametersMidware(event, context):

    def decorator_function(func):
        def wrapper(partial_response):

            midware_response = QueryParametersMW.middleware_func(event, 
                partial_response)
            if midware_response["statusCode"] == 200:
                return func(midware_response)
            else:
                return midware_response
        return wrapper

    return decorator_function
