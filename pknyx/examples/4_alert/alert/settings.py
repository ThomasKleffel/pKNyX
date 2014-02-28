# -*- coding: utf-8 -*-

from pknyx.common import config

DEVICE_NAME = "alert"
DEVICE_IND_ADDR = "1.1.1"
DEVICE_VERSION = "0.1"

# Override default logger level
config.LOGGER_LEVEL = "info"

# Email settings
FROM = "pknyx@localhost"  # From' header field
TO = "pknyx@localhost"  # 'To' header field
SUBJECT = "pKNyX alert"  # 'Subject' header field
SMTP = "localhost"  # SMTP server name

# Temperatures limits
TEMP_LIMITS = {"temp_1": [19., 24.],
               "temp_2": [5., 30.]
              }
