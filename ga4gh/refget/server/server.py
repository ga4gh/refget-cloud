import click
import os
import sys
import tornado.ioloop
import tornado.web

from ga4gh.refget.config.logger import logger
from ga4gh.refget.config.exceptions import \
    RefgetException, RefgetPropertiesFileNotFoundException, \
    RefgetPropertiesParseException
from ga4gh.refget.config.properties import Properties
from ga4gh.refget.http.request import Request
from ga4gh.refget.http.response import Response
from ga4gh.refget.routes.sequence.get_metadata import get_metadata
from ga4gh.refget.routes.sequence.get_service_info import get_service_info
from ga4gh.refget.routes.sequence.get_sequence import get_sequence

class RefgetServer(object):
    
    def __init__(self, properties_file):
        
        self.properties_file = properties_file
        self.properties = None
        self.application = None
        self.__setup()

    def run(self):

        port = self.properties.get("server.port")
        logger.info("running server on port " + str(port))
        self.application.listen(port)
        tornado.ioloop.IOLoop.current().start()

    def __setup(self):
        
        logger.info("setting server properties")
        self.__setup_properties()
        logger.info("setting server api routes")
        self.__setup_application()
        logger.info("setup complete")

    def __setup_properties(self):

        props = {}
        
        if self.properties_file:
            logger.info("parsing properties file: " + self.properties_file)

            if not os.path.exists(self.properties_file):
                raise RefgetPropertiesFileNotFoundException(
                    "properties file not found: " + self.properties_file)
            
            fh = open(self.properties_file, "r")
            for line in fh:
                ls = line.strip().split("=")
                if len(ls) != 2:
                    raise RefgetPropertiesParseException(
                        "Could not parse properties file")
                props[ls[0]] = ls[1]
        else:
            logger.info("no properties file specified, using all defaults")
        
        self.properties = Properties(props)
    
    def __setup_application(self):
        self.application = tornado.web.Application([
            (
                r"/sequence/service-info",
                GetServiceInfoHandler,
                dict(properties=self.properties)
            ),
            (
                r"/sequence/(?P<seqid>[^/]+)",
                GetSequenceHandler,
                dict(properties=self.properties)
            ),
            (
                r"/sequence/(?P<seqid>[^/]+)/metadata",
                GetMetadataHandler,
                dict(properties=self.properties)
            )
        ])

class RefgetRequestHandler(tornado.web.RequestHandler):

    def initialize(self, properties):
        self.properties = properties
        self.g_request = None
        self.g_response = None

    def prepare(self):
        self.g_request = self.get_generic_request()
        self.g_response = Response()
    
    def get_generic_request(self):
        g_request = Request()
        for key in self.path_kwargs.keys():
            g_request.add_path_param(key, self.path_kwargs[key])
        for key in self.request.query_arguments:
            g_request.add_query_param(key, self.get_query_argument(key))
        for key, value in self.request.headers.get_all():
            g_request.add_header(key, value)
        return g_request
    
    def finalize_response(self):
        
        self.set_status(self.g_response.get_status_code())
        headers = self.g_response.get_headers()
        for key in headers.keys():
            self.set_header(key, headers[key])
        self.write(self.g_response.get_body())

class GetServiceInfoHandler(RefgetRequestHandler):

    def get(self):
        get_service_info(self.properties, self.g_request, self.g_response)
        self.finalize_response()

class GetSequenceHandler(RefgetRequestHandler):
    def get(self, seqid):
        get_sequence(self.properties, self.g_request, self.g_response)
        self.finalize_response()

class GetMetadataHandler(RefgetRequestHandler):
    def get(self, seqid):
        get_metadata(self.properties, self.g_request, self.g_response)
        self.finalize_response()

@click.command()
@click.option('--properties-file', help='Path to server properties file')
def run_server(properties_file):
    
    logger.info("program started")
    try:
        server = RefgetServer(properties_file)
        server.run()
    except RefgetException as ex:
        msg_template = "exiting program: exit_code: {}, message: {}"
        msg = msg_template.format(str(ex.get_exit_code()), str(ex.get_message()))
        logger.info(msg)
        sys.exit(ex.get_exit_code())
