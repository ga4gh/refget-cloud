# -*- coding: utf-8 -*-
"""Module config.service_info.py
Information about the refget service

Attributes:
    SERVICE_INFO (dict): dictionary containing information about refget service
"""

SERVICE_INFO = {
    "circular_supported": False,
    "algorithms": ["md5", "trunc512"],
    "subsequence_limit": 300000,
    "supported_api_versions": ["1.0"]
}
