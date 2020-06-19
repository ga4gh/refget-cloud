# -*- coding: utf-8 -*-
"""Application-wide logging utility"""

import logging
import sys

logger = logging.getLogger("refget-service")
"""Application-wide logger"""

logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
