import json

from ga4gh.refget.middleware.media_type import MediaTypeMidware
from ga4gh.refget.config.service_info import SERVICE_INFO

def get_service_info(properties, request, response):

    @MediaTypeMidware(properties, request, response)
    def worker(properties, request, response):
        response.set_body(json.dumps({
            "service": SERVICE_INFO
        }))
    worker(properties, request, response)