import requests
from ga4gh.refget.http.status_codes import StatusCodes as SC
from ga4gh.refget.http.response import Response
from ga4gh.refget.middleware.media_type import MediaTypeMidware
from ga4gh.refget.middleware.query_parameters import QueryParametersMidware
from ga4gh.refget.util.resolve_url import resolve_sequence_url

def get_sequence(properties, request, response):
    
    @MediaTypeMidware(properties, request, response)
    @QueryParametersMidware(properties, request, response)
    def worker(properties, request, response):
        # get start, end subsequence positions from middleware,
        # as well as if subsequence was requested by start/end or by Range
        start, end, subseq_type = [response.get_datum(a) for a \
                                   in ["start", "end", "subseq-type"]]
        
        # get sequence id from request and prepare URL    
        seqid = request.get_path_param("seqid")
        url = resolve_sequence_url(properties, seqid)

        # if the full sequence has been requested OR subequence has been 
        # specified by 'Range' header, then redirect client to datasource
        # (assuming source can handle partial content response)
        if subseq_type == None or subseq_type == "range": 
            response.set_redirect_found(url)

        elif subseq_type == "start-end": # if subsequence has been specified by
                                         # start/end query parameters, then
                                         # handle parsing subsequence here
            datasource_response = requests.get(url)
            # if datasource resource was successfully retrieved, continue to
            # subsequence, otherwise redirect client to datasource url
            if SC.is_successful_code(datasource_response.status_code):
                seq = datasource_response.text
                start_idx = int(start) if start else 0
                end_idx = int(end) if end else len(seq)
                seq = seq[start_idx:end_idx]
                response.put_header("Content-Length", len(seq))
                response.set_body(seq)
            else:
                response.set_redirect_found(url)
    worker(properties, request, response)
