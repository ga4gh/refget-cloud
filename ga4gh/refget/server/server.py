# -*- coding: utf-8 -*-
"""Wraps refget functions into Tornado framework web server"""

import click
import os
import sys
import tornado.ioloop
import tornado.web
from ga4gh.refget.config.logger import logger
from ga4gh.refget.config.exceptions import \
    RefgetException, RefgetPropertiesFileNotFoundException, \
    RefgetPropertiesParseException, RefgetOpenApiNotFoundException
from ga4gh.refget.config.properties import Properties
from ga4gh.refget.http.request import Request
from ga4gh.refget.http.response import Response
from ga4gh.refget.routes.sequence.get_metadata import get_metadata
from ga4gh.refget.routes.sequence.get_service_info import get_service_info
from ga4gh.refget.routes.sequence.get_sequence import get_sequence

class RefgetServer(object):
    """Tornado framework web server application serving all refget routes

    Attributes:
        properties_file (str): path to application .properties file
        properties (Properties): loaded runtime properties from file
        application (tornado.web.Application): web app serving all refget routes
    """
    
    def __init__(self, properties_file):
        """RefgetServer constructor

        Arguments:
            properties_file (str): path to properties file, overwrites defaults
        """
        
        self.properties_file = properties_file
        self.swagger_ui_dir = "./web/swagger-ui"
        self.properties = None
        self.application = None
        self.__setup()

    def run(self):
        """Run refget server on specified (or default) port"""

        port = self.properties.get("server.port")
        logger.info("running server on port " + str(port))
        self.application.listen(port)
        tornado.ioloop.IOLoop.current().start()

    def __setup(self):
        """Load properties from properties file and application routes"""
        
        logger.info("setting server properties")
        self.__setup_properties()
        logger.info("setting OpenAPI routes")
        self.__setup_openapi()
        logger.info("setting server api routes")
        self.__setup_application()
        logger.info("setup complete")

    def __setup_properties(self):
        """Loads Properties object from properties file

        The application's properties object is initialized with having all
        default properties. Valid properties in the properties file will 
        overwrite their corresponding defaults

        Raises:
            RefgetPropertiesFileNotFoundException: when specified properties
                file was not found
            RefgetPropertiesParseException: when one or more entries in the
                properties file was malformed
        """

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
    
    def __setup_openapi(self):
        
        openapi_file = self.properties.get("local.openapi_file")

        if not openapi_file:
            logger.info("no OpenAPI file provided. Swagger UI will not be available")
        else:
            logger.info("moving %s to Swagger UI directory" % openapi_file)
            if not os.path.exists(openapi_file):
                raise RefgetOpenApiNotFoundException(
                    "OpenAPI file: %s not found" % openapi_file)

            openapi_output_file = self.swagger_ui_dir + "/openapi.yaml"
            openapi_content = open(openapi_file, "r").read()
            open(openapi_output_file, "w").write(openapi_content)
    
    def __setup_application(self):
        """Setup server routes by assigning function handlers to api routes"""

        refget_routes = [
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
        ]

        swaggerui_routes = [
            (r"/(.*)", tornado.web.StaticFileHandler, {'path': self.swagger_ui_dir})
        ]

        routes = refget_routes + swaggerui_routes \
                 if self.properties.get("local.openapi_file") \
                 else refget_routes
        self.application = tornado.web.Application(routes)

class RefgetRequestHandler(tornado.web.RequestHandler):
    """Generic request handler for all refget-related requests

    All refget request handlers must be initialized with the runtime properties,
    a generic request object modified from the Tornado-specific request object,
    and an empty refget response object that will be modified by the method.

    Attributes:
        properties (Properties): runtime properties imported from server
        g_request (Request): generic refget request created from Tornado request
        g_response (Response): generic refget response modified by route methods
    """

    def initialize(self, properties):
        """Initialize the request handler by loading server Properties"""

        self.properties = properties
        self.g_request = None
        self.g_response = None

    def prepare(self):
        """Instantiate the generic request and response passed to refget func

        the generic request is instantiated by converting the Tornado-specific
        request object, so that it will be compatible with refget functions
        """

        self.g_request = self.get_generic_request()
        self.g_response = Response()
    
    def get_generic_request(self):
        """Instantiate a generic refget request from Tornado request object

        Returns:
            (Request): generic refget request, compatible with refget functions
        """

        g_request = Request()
        for key in self.path_kwargs.keys():
            g_request.add_path_param(key, self.path_kwargs[key])
        for key in self.request.query_arguments:
            g_request.add_query_param(key, self.get_query_argument(key))
        for key, value in self.request.headers.get_all():
            g_request.add_header(key, value)
        return g_request
    
    def finalize_response(self):
        """Converts the completed generic response to Tornado-specific response

        The generic response is updated by the refget functions. This method
        writes the generic response as a Tornado-specific response, so that the
        server will return valid responses in the Tornado runtime context.
        """
        
        self.set_status(self.g_response.get_status_code())
        headers = self.g_response.get_headers()
        for key in headers.keys():
            self.set_header(key, headers[key])
        self.write(self.g_response.get_body())

class GetServiceInfoHandler(RefgetRequestHandler):
    """Request handler for get service info refget function"""

    def get(self):
        """Get service info HTTP response"""

        get_service_info(self.properties, self.g_request, self.g_response)
        self.finalize_response()

class GetSequenceHandler(RefgetRequestHandler):
    """Request handler for get sequence refget function"""

    def get(self, seqid):
        """Get sequence HTTP response"""

        get_sequence(self.properties, self.g_request, self.g_response)
        self.finalize_response()

class GetMetadataHandler(RefgetRequestHandler):
    """Request handler for get metadata refget function"""

    def get(self, seqid):
        """Get metadata HTTP response"""

        get_metadata(self.properties, self.g_request, self.g_response)
        self.finalize_response()

class SwaggerUIHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.write("There's an openapi specified")

@click.command()
@click.option('--properties-file', help='Path to server properties file')
def run_server(**kwargs):
    """Run refget tornado web server

    Arguments:
        kwargs (dict): dictionary of commandline properties
    """

    logger.info("program started")
    try:
        server = RefgetServer(kwargs['properties_file'])
        server.run()
    except RefgetException as ex:
        msg_template = "exiting program: exit_code: {}, message: {}"
        msg = msg_template.format(str(ex.get_exit_code()), str(ex.get_message()))
        logger.info(msg)
        sys.exit(ex.get_exit_code())
