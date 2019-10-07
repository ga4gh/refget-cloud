# -*- coding: utf-8 -*-
"""Lambda functions associated with '/sequence/' API routes"""

import json
import requests
from ga4gh.refget.serverless.cls.http.status_codes import StatusCodes as SC
from ga4gh.refget.serverless.config.constants import *
from ga4gh.refget.serverless.config.service_info import *
from ga4gh.refget.serverless.middleware.media_type import MediaTypeMidware
from ga4gh.refget.serverless.middleware.query_parameters \
    import QueryParametersMidware
from ga4gh.refget.serverless.middleware.start import StartMidware

def get_sequence(event, context):
    """'/sequence/:id' route function, get a sequence/subsequence by its id

    :param event: AWS SAM event (incl. headers, path params, query params)
    :type event: dict[str, object]
    :param context: AWS SAM context
    :type context: dict[str, str]
    :return: AWS SAM-formatted response
    :rtype: dict[str, object]
    """

    @StartMidware(event, context)
    @MediaTypeMidware(event, context, 
                      supported_media_types=[DEFAULT_CONTENT_TYPE_TEXT])
    @QueryParametersMidware(event, context)
    def worker(resp):
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

    :param event: AWS SAM event (incl. headers, path params, query params)
    :type event: dict[str, object]
    :param context: AWS SAM context
    :type context: dict[str, str]
    :return: AWS SAM-formatted response
    :rtype: dict[str, object]
    """

    @StartMidware(event, context)
    @MediaTypeMidware(event, context)
    def worker(resp):
        # form url to S3 metadata object based on sequence id in the request,
        # and set the response to redirect to the S3 url
        seqid = event['pathParameters']['id']
        url = S3_METADATA_URL + seqid + ".json"
        resp.set_redirect_found(url)
        return resp

    return worker().finalize()

def get_service_info(event, context):
    """'/sequence/service-info' route function, get service info

    :param event: AWS SAM event (incl. headers, path params, query params)
    :type event: dict[str, object]
    :param context: AWS SAM context
    :type context: dict[str, str]
    :return: AWS SAM-formatted response
    :rtype: dict[str, object]
    """
    
    @StartMidware(event, context)
    @MediaTypeMidware(event, context)
    def worker(resp):
        resp.set_body(json.dumps({
            "service": SERVICE_INFO
        }))
        return resp

    return worker().finalize()

__all__ = [
    'get_sequence',
    'get_metadata',
    'get_service_info'
]