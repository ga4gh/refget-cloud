import json
from config.constants import *
from config.sequences import *

class SequenceIdMW(object):

    @staticmethod
    def middleware_func(event, partial_response):
        seqid = event['pathParameters']['id']
        response = SequenceIdMW._SequenceIdMW__get_trunc512_id(partial_response,
            seqid)
        return response

    @staticmethod
    def __get_trunc512_id(partial_response, seqid):
        
        partial_response["statusCode"] = 404
        partial_response["body"] = json.dumps({
            "message": "sequence with id " + seqid + " not found"
        })

        trunc512_id = None    
        if seqid in SEQUENCE_TRUNC512:
            trunc512_id = seqid
        else:
            if seqid in CHECKSUM_MAP.keys():
                trunc512_id = CHECKSUM_MAP[seqid]
    
        if trunc512_id:
            partial_response["statusCode"] = 200
            partial_response["body"] = ""
            partial_response["data"] = {"trunc512_id": trunc512_id}
        
        return partial_response

def SequenceIdMidware(event, context):

    def decorator_function(func):
        def wrapper(partial_response):

            midware_response = SequenceIdMW.middleware_func(event, 
                partial_response)
            if midware_response["statusCode"] == 200:
                return func(midware_response)
            else:
                return midware_response
        return wrapper

    return decorator_function
