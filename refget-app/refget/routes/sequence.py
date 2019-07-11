import json
import requests
from config.sequences import *
from config.constants import *
from config.service_info import *
from middleware.media_type import MediaTypeMidware

def get_trunc512_id(seqid):
    trunc512_id = None
    
    if seqid in SEQUENCE_TRUNC512:
        trunc512_id = seqid
    else:
        if seqid in CHECKSUM_MAP.keys():
            trunc512_id = CHECKSUM_MAP[seqid]
    
    return trunc512_id

def get_sequence(e, c):

    log = ""
    seqid = e['pathParameters']['id']
    response_body = "Invalid id, no resource found"
    trunc512_id = get_trunc512_id(seqid)
    
    if trunc512_id:
        uri = S3_BASE_URL + trunc512_id
        s3_response = requests.get(uri)
        log += str(s3_response.status_code) + "; "
        log += str(s3_response.text) + "; "
        response_seq = s3_response.text

        if e['queryStringParameters']:
            q = e['queryStringParameters']
            start = 0 if "start" not in q.keys() else int(q["start"])
            end = len(response_seq) if "end" not in q.keys() else int(q["end"])
            response_seq = response_seq[start:end]
            
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": DEFAULT_CONTENT_TYPE_TEXT + "; " + CHARSET,
            "Content-Length": len(response_seq)
        },
        "body": response_seq
        # "body": json.dumps({
        #     "log": log,
        #     "event": str(e)
        # })
    }

def get_metadata(event, context):

    @MediaTypeMidware(event, context)
    def worker(midware_response):
        response = midware_response

        seqid = event['pathParameters']['id']
        trunc512_id = get_trunc512_id(seqid)
        if trunc512_id:
            response["body"] = json.dumps({"metadata": METADATA[trunc512_id]})
        else:
            response["statusCode"] = 404
            response["body"] = json.dumps({
                "message": "resource not found"
            })

        return response
    return worker()

def get_service_info(event, context):
    
    @MediaTypeMidware(event, context)
    def worker(midware_response):
        response = midware_response
        response["body"] = json.dumps({
            "service": SERVICE_INFO
        })
        return response
    return worker()
