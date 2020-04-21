# -*- coding: utf-8 -*-
"""Unit tests for Logger class"""

import pytest
from io import StringIO
from ga4gh.refget.config.logger import logger

def test_logger():

    logger.debug("DEBUG")
    logger.info("INFO")
    logger.warn("WARN")
    logger.error("ERROR")
