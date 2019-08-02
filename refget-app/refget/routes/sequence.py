"""Module routes.sequence.py
Lambda functions associated with '/sequence/' API routes 
"""

import json
import requests
from cls.http.status_codes import StatusCodes as SC
from config.constants import *
from config.service_info import *
from middleware.media_type import MediaTypeMidware
from middleware.query_parameters import QueryParametersMidware
from middleware.start import StartMidware

def get_sequence(event, context):
    """'/sequence/:id' route function, get a sequence/subsequence by its id

    Arguments:
        event (dict): AWS event/request
        context (dict): AWS context
    
    Returns:
        (dict): finalized response according to AWS SAM expected format
    """

    @StartMidware(event, context)
    @MediaTypeMidware(event, context, 
                      supported_media_types=[DEFAULT_CONTENT_TYPE_TEXT])
    @QueryParametersMidware(event, context)
    def worker(resp):
        """post-middleware inner function, get a sequence/subsequence by id

        Arguments:
            resp (Response): Response object
        
        Returns:
            (Response): Response containing sequence/subsequence in body
        """

        # get start, end subsequence positions from middleware,
        # as well as if subsequence was requested by start/end or by Range
        start, end, subseq_type = [resp.get_datum(a) for a \
                                   in ["start", "end", "subseq-type"]]

        # get sequence id from request and prepare S3 URL    
        seqid = event['pathParameters']['id']
        url = S3_SEQUENCE_URL + seqid

        # if the full sequence has been requested OR subequence has been 
        # specified by 'Range' header, then redirect client to s3 bucket
        # (s3 bucket can handle partial content response)
        if subseq_type == None or subseq_type == "range": 
            resp.set_redirect_found(url)

        elif subseq_type == "start-end": # if subsequence has been specified by
                                         # start/end query parameters, then
                                         # handle parsing subsequence here

            s3_response = requests.get(url)
            # if s3 resource was successfully retrieved, continue to
            # subsequence, otherwise redirect client to s3 url
            if SC.is_successful_code(s3_response.status_code):
                seq = s3_response.text
                start_idx = int(start) if start else 0
                end_idx = int(end) if end else len(seq)
                seq = seq[start_idx:end_idx]
                resp.put_header("Content-Length", len(seq))
                resp.set_body(seq)

            else:
                resp.set_redirect_found(url)
                
        return resp
    
    return worker().finalize()

def get_metadata(event, context):
    """'/sequence/:id/metadata' route function, get sequence metadata by id

    Arguments:
        event (dict): AWS event/request
        context (dict): AWS context
    
    Returns:
        (dict): finalized response according to AWS SAM expected format
    """

    @StartMidware(event, context)
    @MediaTypeMidware(event, context)
    def worker(resp):
        """post-middleware inner function, get sequence metadata by its id

        Arguments:
            resp (Response): Response object

        Returns:
            (Response): Response containing sequence metadata in body
        """

        # form url to S3 metadata object based on sequence id in the request,
        # and set the response to redirect to the S3 url
        seqid = event['pathParameters']['id']
        url = S3_METADATA_URL + seqid + ".json"
        resp.set_redirect_found(url)
        
        return resp

    return worker().finalize()

def get_service_info(event, context):
    """'/sequence/service-info' route function, get service info

    Arguments:
        event (dict): AWS event/request
        context (dict): AWS context
    
    Returns:
        (dict): finalized response according to AWS SAM expected format
    """
    
    @StartMidware(event, context)
    @MediaTypeMidware(event, context)
    def worker(resp):
        """post-middleware inner function, get service info

        Arguments:
            resp (Response): Response object
        
        Returns:
            (Response): Response containing service info in body
        """

        resp.set_body(json.dumps({
            "service": SERVICE_INFO
        }))
        return resp

    return worker().finalize()
