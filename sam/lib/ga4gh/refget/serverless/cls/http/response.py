# -*- coding: utf-8 -*-
"""Defines the Response class, which can be modified to modulate the http
response sent back to the client. Response is formatted according to expected
AWS SAM format.
"""

from ga4gh.refget.serverless.cls.http.status_codes import StatusCodes as SC

class Response(object):
    """an HTTP response, sends back appropriate response to client

    For each web api route, a Response object is created and modified through
    a chain of middleware checks. If, at the end of a middleware function, the
    response status code is OK (200), the next function will execute. If ever
    the status code is modified to an error, the response will be sent back to
    client without executing further processing steps.

    :param status_code: response status code
    :type status_code: int
    :param headers: http headers
    :type headers: dict[str, str]
    :param body: response body
    :type body: str
    :param data: data dict accessible throughout all middleware functions
    :type data: dict[str, str]
    """

    def __init__(self):
        """Constructor method"""

        self.status_code = SC.BAD_REQUEST
        self.headers = {}
        self.body = ""
        self.data = {}

    def finalize(self):
        """Format response according to AWS lambda/API Gateway expected format

        For each API route declared in an AWS SAM stack, the response must be 
        sent back as a dict with the appropriate keys and data structures. This
        method formats the response object according to that format.

        :return: response information formatted according to AWS SAM
        :rtype: dict[str, object]
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

        :param body: string to set to response body
        :type body: str
        """

        self.body = body
    
    def get_body(self):
        """get response body

        :return: response body
        :rtype: str
        """

        return self.body
    
    def set_status_code(self, status_code):
        """set status code

        :param status_code: int to set to status code
        :type status_code: int
        """

        self.status_code = status_code
    
    def get_status_code(self):
        """get status code

        :return: response status code
        :rtype: int
        """

        return self.status_code
    
    def put_header(self, key, value):
        """add or update a key-value pair to response headers

        :param key: header key/name
        :type key: str
        :param value: value for this header
        :type value: str
        """

        self.headers[key] = value
    
    def update_headers(self, new_dict):
        """add or update multiple header keys and values

        This method accepts a dictionary of new headers, and will update the 
        existing header dictionary with the new keys and values.

        :param new_dict: dictionary to update headers with
        :type new_dict: dict[str, str]
        """

        self.headers.update(new_dict)
    
    def get_header(self, key):
        """get the value of a particular header

        :param key: header key/name
        :type key: str
        :return: value of specified header
        :rtype: str
        """

        return self.headers[key]
    
    def get_headers(self):
        """get complete header dictionary

        :return: header dictionary
        :rtype: dict[str, str]
        """

        return self.headers
    
    def put_data(self, key, value):
        """add or update a key-value pair to data dictionary

        :param key: data key/name
        :type key: str
        :param value: value to store under key
        :type value: str
        """

        self.data[key] = value
    
    def update_data(self, new_dict):
        """add or update multiple keys and values to data dictionary

        This method accepts a dictionary of new data, and will update the
        existing data dictionary with the new keys and values. 

        :param new_dict: dictionary to update data dictionary with
        :type new_dict: dict[str, str]
        """

        self.data.update(new_dict)

    def get_datum(self, key):
        """get the value under the specified key in data dictionary

        :param key: data key/name
        :type key: str
        :return: value under specified key in data dictionary
        :rtype: str
        """

        return self.data[key]
    
    def get_data(self):
        """get complete data dictionary

        :return: data dictionary
        :rtype: dict[str, str]
        """

        return self.data
    
    def set_redirect_found(self, url):
        """set the response to redirect client to specified url

        :param url: redirect url
        :type url: str
        """

        self.set_status_code(SC.REDIRECT_FOUND)
        self.put_header("Location", url)

__all__ = [
    'Response'
]