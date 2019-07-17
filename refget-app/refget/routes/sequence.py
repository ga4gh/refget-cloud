import json
import requests
from config.sequences import *
from config.constants import *
from config.service_info import *
from middleware.functions import *
from middleware.media_type import MediaTypeMidware
from middleware.query_parameters import QueryParametersMidware
from middleware.sequence_id import SequenceIdMidware
from middleware.start import StartMidware

def get_sequence(event, context):

    @StartMidware(event, context)
    @MediaTypeMidware(event, context, 
                      supported_media_types=[DEFAULT_CONTENT_TYPE_TEXT])
    @SequenceIdMidware(event, context)
    @QueryParametersMidware(event, context)
    def worker(partial_response):

        response = partial_response
        d = response["data"]
        trunc512_id, start, end, subseq_type = \
            d["trunc512_id"], d["start"], d["end"], d["subseq_type"]
        
        uri = S3_BASE_URL + trunc512_id
        s3_response = requests.get(uri)
        seq = s3_response.text
        
        start_idx = int(start) if start else 0
        end_idx = int(end) if end else len(seq)
        end_idx = end_idx + 1 if subseq_type == "range" else end_idx
        seq = seq[start_idx:end_idx]
        
        if subseq_type == "range":
            response["statusCode"] = 206
        response["headers"]["Content-Length"] = len(seq)
        response["body"] = seq
                
        return response

    return finalize_response(worker())

def get_metadata(event, context):

    @StartMidware(event, context)
    @MediaTypeMidware(event, context)
    @SequenceIdMidware(event, context)
    def worker(partial_response):
        
        response = partial_response
        trunc512_id = response["data"]["trunc512_id"]
        response["body"] = json.dumps({"metadata": METADATA[trunc512_id]})
        
        return response
    return finalize_response(worker())

def get_service_info(event, context):
    
    @StartMidware(event, context)
    @MediaTypeMidware(event, context)
    def worker(partial_response):
        response = partial_response
        response["body"] = json.dumps({
            "service": SERVICE_INFO
        })
        return response
    return finalize_response(worker())
