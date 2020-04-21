# -*- coding: utf-8 -*-
"""Container for modifiable runtime properties"""

import copy
import os
from ga4gh.refget.config.defaults import \
    DEFAULT_PROPERTIES, DEFAULT_ALLOWED_PROPERTY_KEYS
from ga4gh.refget.config.exceptions import RefgetInvalidPropertyException

class Properties(object):
    """Container for modifiable runtime properties

    The Properties class contains modifiable runtime properties, which are 
    specified via the properties file or environment variables. Modifiable 
    properties include the base url to the cloud-based data source, and url
    paths to sequence and metadata objects.

    Attributes:
        properties (dict): loaded runtime properties
    """
    
    def __init__(self, new_props):
        """Properties constructor

        The properties dictionary is initialized as all defaults. Each 
        element in the passed dictionary overwrites the corresponding default
        property.

        Arguments:
            new_props (dict): dictionary of new properties
        """

        self.properties = copy.deepcopy(DEFAULT_PROPERTIES)
        self.__setup(new_props)
    
    def __setup(self, new_props):
        """Setup new properties

        Overwrites the default properties with whatever properties are passed in
        the new properties dictionary.

        Arguments:
            new_props (dict): dictionary of new properties
        
        Raises:
            RefgetInvalidPropertyException: when an unrecognized property key
                is passed in the new properties dictionary
        """

        for key in new_props.keys():
            if key not in DEFAULT_ALLOWED_PROPERTY_KEYS:
                raise RefgetInvalidPropertyException(
                    "unrecognized property: " + key)
            self.properties[key] = new_props[key]
    
    def get(self, key):
        """Get a specific property value

        Arguments:
            key (str): the specific property key
        
        Returns:
            (str): property's value based on the key
        """

        return self.properties[key]
