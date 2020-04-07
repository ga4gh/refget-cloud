class RefgetException(Exception):

    def __init__(self, message):
        super(RefgetException, self).__init__(message)
        self.exit_code = 1
        self.message = message
    
    def get_exit_code(self):
        return self.exit_code
    
    def get_message(self):
        return self.message
    
    def __str__(self):
        return self.m

class RefgetInvalidPropertyException(RefgetException):
    
    def __init__(self, msg):
        super(RefgetInvalidPropertyException, self).__init__(msg)
        self.exit_code = 2

class RefgetPropertiesFileNotFoundException(RefgetException):

    def __init__(self, msg):
        super(RefgetPropertiesFileNotFoundException, self).__init__(msg)
        self.exit_code = 3

class RefgetPropertiesParseException(RefgetException):

    def __init__(self, msg):
        super(RefgetPropertiesParseException, self).__init__(msg)
        self.exit_code = 4