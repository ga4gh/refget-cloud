# -*- coding: utf-8 -*-
"""Module cls.http.response.py
This module contains the Response class, which contains properties that can
be modified to modulate the http response sent back to the client.
"""

from cls.http.status_codes import StatusCodes as SC

class Response(object):
    """an HTTP response, sends back appropriate response to client

    For each web api route, a Response object is created and modified through
    a chain of middleware checks. If, at the end of a middleware function, the
    response status code is OK (200), the next function will execute. If ever
    the status code is modified to an error, the response will be sent back to
    client without executing further processing steps.

    Attributes:
        status_code (int): response status code
        headers (dict): http headers
        body (str): response body
        data (dict): data dict accessible throughout all middleware functions
    """

    def __init__(self):
        """instantiates a Response object"""

        self.status_code = SC.BAD_REQUEST
        self.headers = {}
        self.body = ""
        self.data = {}

    def finalize(self):
        """Format response according to AWS lambda/API Gateway expected format

        For each API route declared in an AWS SAM stack, the response must be 
        sent back as a dict with the appropriate keys and data structures. This
        method formats the response object according to that format.

        Returns:
            (dict): response information formatted according to AWS SAM
        """

        return {
            "statusCode": self.get_status_code(),
            "headers": self.get_headers(),
            "body": self.get_body()
        }

    ##################################################
    # SETTERS / GETTERS
    ##################################################
    
    def set_body(self, body):
        """set response body

        Arguments:
            body (str): string to set to response body
        """

        self.body = body
    
    def get_body(self):
        """get response body

        Returns:
            (str): response body
        """

        return self.body
    
    def set_status_code(self, status_code):
        """set status code

        Arguments:
            status_code (int): int to set to status code
        """

        self.status_code = status_code
    
    def get_status_code(self):
        """get status code

        Returns:
            (int): response status code
        """

        return self.status_code
    
    def put_header(self, key, value):
        """add or update a key-value pair to response headers

        Arguments:
            key (str): header key/name
            value (str): value for this header
        """

        self.headers[key] = value
    
    def update_headers(self, new_dict):
        """add or update multiple header keys and values

        This method accepts a dictionary of new headers, and will update the 
        existing header dictionary with the new keys and values. 

        Arguments:
            new_dict (dict): dictionary to update headers with
        """

        self.headers.update(new_dict)
    
    def get_header(self, key):
        """get the value of a particular header

        Arguments:
            key (str): header key/name
        
        Returns:
            (str): value of specified header
        """

        return self.headers[key]
    
    def get_headers(self):
        """get complete header dictionary

        Returns:
            (dict): header dictionary
        """

        return self.headers
    
    def put_data(self, key, value):
        """add or update a key-value pair to data dictionary

        Arguments:
            key (str): data key/name
            value (str): value to store under key
        """

        self.data[key] = value
    
    def update_data(self, new_dict):
        """add or update multiple keys and values to data dictionary

        This method accepts a dictionary of new data, and will update the
        existing data dictionary with the new keys and values. 

        Arguments:
            new_dict (dict): dictionary to update data dictionary with
        """

        self.data.update(new_dict)

    def get_datum(self, key):
        """get the value under the specified key in data dictionary

        Arguments:
            key (str): data key/name
        
        Returns:
            (str): value under specified key in data dictionary
        """

        return self.data[key]
    
    def get_data(self):
        """get complete data dictionary

        Returns:
            (dict): data dictionary
        """

        return self.data
    
    def set_redirect_found(self, url):
        """Set the response to redirect client to specified url

        Arguments:
            url (str): redirect url
        """

        self.set_status_code(SC.REDIRECT_FOUND)
        self.put_header("Location", url)
