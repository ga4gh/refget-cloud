import copy
import os

from ga4gh.refget.config.defaults import \
    DEFAULT_PROPERTIES, DEFAULT_ALLOWED_PROPERTY_KEYS
from ga4gh.refget.config.exceptions import RefgetInvalidPropertyException

class Properties(object):
    
    def __init__(self, new_props):

        self.properties = copy.deepcopy(DEFAULT_PROPERTIES)
        self.__setup(new_props)
    
    def __setup(self, new_props):

        for key in new_props.keys():

            if key not in DEFAULT_ALLOWED_PROPERTY_KEYS:
                raise RefgetInvalidPropertyException(
                    "unrecognized property: " + key)

            self.properties[key] = new_props[key]
    
    def get(self, key):
        return self.properties[key]