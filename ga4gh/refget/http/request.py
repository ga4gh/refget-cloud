class Request(object):
    
    def __init__(self):
        
        self.headers = {}
        self.path_params = {}
        self.query_params = {}

    def add_header(self, key, value):
        self.headers[key] = value
    
    def get_header(self, key):
        return None if key not in self.headers else self.headers[key]
    
    def get_headers(self):
        return self.headers
    
    def add_path_param(self, key, value):
        self.path_params[key] = value
    
    def get_path_param(self, key):
        return None if key not in self.path_params else self.path_params[key]
    
    def get_path_params(self):
        return self.path_params
    
    def add_query_param(self, key, value):
        self.query_params[key] = value
    
    def get_query_param(self, key):
        return None if key not in self.query_params else self.query_params[key]
    
    def get_query_params(self):
        return self.query_params
