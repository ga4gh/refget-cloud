import requests
from ga4gh.refget.middleware.media_type import MediaTypeMidware
from ga4gh.refget.util.resolve_url import resolve_metadata_url

def get_metadata(properties, request, response):

    @MediaTypeMidware(properties, request, response)
    def worker(properties, request, response):

        seqid = request.get_path_param("seqid")
        url = resolve_metadata_url(properties, seqid)
        value = requests.get(url).text
        response.set_redirect_found(url)

    worker(properties, request, response)
