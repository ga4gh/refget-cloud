# -*- coding: utf-8 -*-
"""Generic Http Response representation returned from Refget functions

The Response class represents the genericized HTTP response returned from all
Refget functions. The generic response is used to create a 
Vendor/Platform-specific response (e.g. Tornado Server Response,
AWS lambda response dictionary) based on the deployment context, which is then
passed to the deployment framework's downstream processes.
"""

import json
from ga4gh.refget.http.status_codes import StatusCodes as SC
from ga4gh.refget.config.constants import CONTENT_TYPE_JSON_REFGET_VND

class Response(object):
    """Generic representation of HTTP response returned from Refget functions

    Attributes:
        status_code (int): HTTP status code
        headers (dict): key-value mapping of HTTP response headers
        body (str): response body
        data (dict): common data-dictionary to pass resources between functions
    """

    def __init__(self):
        """Response constructor"""

        self.status_code = SC.BAD_REQUEST
        self.headers = {}
        self.body = ""
        self.data = {}

    ##################################################
    # SETTERS / GETTERS
    ##################################################
    
    def set_body(self, body):
        """Set response body

        Arguments:
            body (str): string to set to response body
        """

        self.body = body
    
    def get_body(self):
        """Get response body

        Returns:
            (str): response body
        """

        return self.body
    
    def set_status_code(self, status_code):
        """Set HTTP status code

        Arguments:
            status_code (int): HTTP status code to associate with response
        """

        self.status_code = status_code
    
    def get_status_code(self):
        """Get HTTP status code

        Returns:
            (int): HTTP status code associated with response
        """

        return self.status_code
    
    def put_header(self, key, value):
        """Add or update a key-value pair to response headers

        Arguments:
            key (str): response header key/name
            value (str): value for this header
        """

        self.headers[key] = value
    
    def update_headers(self, new_dict):
        """Add or update multiple header keys and values

        Accepts a dictionary of new headers, and will update the existing
        header dictionary with the new keys and values.

        Arguments:
            new_dict (dict): key-value mapping of new headers
        """

        self.headers.update(new_dict)
    
    def get_header(self, key):
        """Get the value of a particular header

        Arguments:
            key (str): header key/name

        Returns:
            value of specified header
        """

        return self.headers[key]
    
    def get_headers(self):
        """Get complete header dictionary

        Returns:
            (dict): header dictionary
        """

        return self.headers
    
    def put_data(self, key, value):
        """Add or update a key-value pair to data dictionary

        Arguments:
            key (str): data key/name
            value (str): value to store under key
        """

        self.data[key] = value
    
    def update_data(self, new_dict):
        """Add or update multiple keys and values to data dictionary

        This method accepts a dictionary of new data, and will update the
        existing data dictionary with the new keys and values.

        Arguments:
            new_dict (dict): dictionary to update data dictionary with
        """

        self.data.update(new_dict)

    def get_datum(self, key):
        """Get the value under the specified key in data dictionary

        Arguments:
            key (str): data key/name
        
        Returns:
            (str): value under specified key in data dictionary
        """

        return self.data[key]
    
    def get_data(self):
        """Get complete data dictionary

        Returns:
            (dict): data dictionary
        """

        return self.data
    
    def set_redirect_found(self, url):
        """Set the response to redirect client to specified url

        Arguments:
            url (str): redirection location url
        """

        self.set_status_code(SC.REDIRECT_FOUND)
        self.put_header("Location", url)
    
    def set_error(self, code, message):
        """Set the generic response to an error

        Arguments:
            code (int): HTTP status code representing error encountered
            message (str): error message in response body
        """

        self.set_status_code(code)
        self.put_header("Content-Type", CONTENT_TYPE_JSON_REFGET_VND)
        self.set_body(json.dumps({"message": message}))
