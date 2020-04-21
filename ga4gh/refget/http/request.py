# -*- coding: utf-8 -*-
"""Generic HTTP Request representation passed to Refget functions

The Request class represents the genericized HTTP request passed to the Refget
service. The generic request is used in all Refget functions.
Vendor/Platform-specific request objects (e.g. Tornado Server Request, AWS 
lambda request) are first converted to this generic request before being passed
to the Refget functions.
"""

class Request(object):
    """Generic representation of HTTP request passed to Refget service

    Attributes:
        headers (dict): key-value mapping of HTTP headers
        path_params (dict): key-value mapping of parameters on url path
        query_params (dict): key-value mapping of parameters on query string
    """
    
    def __init__(self):
        """Request constructor"""
        
        self.headers = {}
        self.path_params = {}
        self.query_params = {}

    def add_header(self, key, value):
        """Add a header to the headers dictionary

        Arguments:
            key (str): header key
            value (str): header value
        """

        self.headers[key] = value
    
    def get_header(self, key):
        """Get a value from header dictionary

        Arguments:
            key (str): header key

        Returns:
            (str): value of header specified by key, or 'None' if key not found
        """

        return None if key not in self.headers else self.headers[key]
    
    def get_headers(self):
        """Get headers dictionary

        Returns:
            (dict): headers dictionary
        """

        return self.headers
    
    def add_path_param(self, key, value):
        """Add a named path parameter to the dictionary

        Arguments:
            key (str): path parameter key/name
            value (str): path parameter value
        """

        self.path_params[key] = value
    
    def get_path_param(self, key):
        """Get a value from path parameters dictionary

        Arguments:
            key (str): path parameter key/name

        Returns:
            (str): value of param specified by key, 'None' if key not found 
        """

        return None if key not in self.path_params else self.path_params[key]
    
    def get_path_params(self):
        """Get path parameters dictionary

        Returns:
            (dict): path parameters dictionary
        """

        return self.path_params
    
    def add_query_param(self, key, value):
        """Add a query string parameter to the dictionary

        Arguments:
            key (str): query string parameter key/name
            value (str): query string parameter value
        """

        self.query_params[key] = value
    
    def get_query_param(self, key):
        """Get a value from query string parameters dictionary

        Arguments:
            key (str): query string parameter key/name
        
        Returns:
            (str): value of param specified by key, 'None' if key not found
        """

        return None if key not in self.query_params else self.query_params[key]
    
    def get_query_params(self):
        """Get query string parameters dictionary

        Returns:
            (dict): query string parameters dictionary
        """

        return self.query_params
