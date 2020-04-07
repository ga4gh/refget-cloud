# -*- coding: utf-8 -*-
"""Information about the refget service"""

SERVICE_INFO = {
    "circular_supported": False,
    "algorithms": ["md5", "trunc512"],
    "subsequence_limit": 300000,
    "supported_api_versions": ["1.0"]
}
"""Dictionary containing information about refget service"""

__all__ = [
    "SERVICE_INFO"
]
