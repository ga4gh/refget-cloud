# -*- coding: utf-8 -*-
"""Exception classes for RefgetServer and other functions"""

class RefgetException(Exception):
    """Generic refget exception

    Attributes:
        exit_code (int): exit code from encountered exception
        message (str): explanation message of the exception encountered
    """

    def __init__(self, message):
        """RefgetException constructor

        Arguments:
            message (str): explanation message of the exception encountered
        """

        super(RefgetException, self).__init__(message)
        self.exit_code = 1
        self.message = message
    
    def get_exit_code(self):
        """Get exception exit code

        Returns:
            (int): exit code
        """

        return self.exit_code
    
    def get_message(self):
        """Get exception message

        Returns:
            (str): exception message
        """

        return self.message
    
    def __str__(self):
        """Get string representation of RefgetException

        Returns:
            (str): exception message
        """

        return self.message

class RefgetInvalidPropertyException(RefgetException):
    """Exception for when an invalid property is specified in properties file

    Attributes:
        exit_code (int): exception exit code
    """
    
    def __init__(self, msg):
        """RefgetInvalidPropertyException constructor

        Arguments:
            msg (str): exception message
        """

        super(RefgetInvalidPropertyException, self).__init__(msg)
        self.exit_code = 2

class RefgetPropertiesFileNotFoundException(RefgetException):
    """Exception for when the specified properties file is not found

    Attributes:
        exit_code (int): exception exit code
    """

    def __init__(self, msg):
        """RefgetPropertiesFileNotFoundException constructor

        Arguments:
            msg (str): exception message
        """

        super(RefgetPropertiesFileNotFoundException, self).__init__(msg)
        self.exit_code = 3

class RefgetPropertiesParseException(RefgetException):
    """Exception for when the properties file was improperly formatted

    Attributes:
        exit_code (int): exception exit code
    """

    def __init__(self, msg):
        """RefgetPropertiesParseException constructor

        Arguments:
            msg (str): exception message
        """

        super(RefgetPropertiesParseException, self).__init__(msg)
        self.exit_code = 4
