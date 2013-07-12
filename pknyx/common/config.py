# -*- coding: utf-8 -*-

""" Python KNX framework.

License
=======

 - B{pKNyX} (U{http://www.pknyx.org}) is Copyright:
  - (C) 2013 Frédéric Mantegazza

Licensed under the EUPL, Version 1.1 or - as soon they will be approved by
the European Commission - subsequent versions of the EUPL (the "Licence");
You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:

 - U{http://ec.europa.eu/idabc/eupl}

Unless required by applicable law or agreed to in writing, software distributed
under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.

See the Licence for the specific language governing permissions and limitations
under the Licence.

Module purpose
==============

Configuration

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import sys
import os.path


# Name and version
APP_NAME = "pKNyX"
VERSION_MAJOR = 0
VERSION_MINOR = 9  # Odd means dev. release
VERSION_UPDATE = 1
VERSION = "%d.%d.%d" % (VERSION_MAJOR, VERSION_MINOR, VERSION_UPDATE)

# Paths
HOME_DIR = os.path.expanduser("~")
if sys.platform == 'win32':
    USER_CONFIG_DIR = os.path.join(os.path.expandvars("$APPDATA"), APP_NAME.lower())
    DATA_STORAGE_DIR = HOME_DIR  # Find a way to retreive the "My Documents" dir in all languages
    TMP_DIR = os.path.expandvars("$TEMP")
else:
    USER_CONFIG_DIR = os.path.join(HOME_DIR, ".config", APP_NAME.lower())  # OpenDesktop standard
    DATA_STORAGE_DIR = HOME_DIR
    TMP_DIR = "/tmp"
USER_PLUGINS_DIR = os.path.join(USER_CONFIG_DIR, "plugins")

for dir_ in (USER_CONFIG_DIR, USER_PLUGINS_DIR):
    try:
        os.makedirs(dir_)
    except OSError, (errno, errmsg):
        if errno in (17, 183):  # dir already exists
            pass
        else:
            raise

CONFIG_FILE = "%s%sconf" % (APP_NAME.lower(), os.path.extsep)
USER_CONFIG_FILE = os.path.join(USER_CONFIG_DIR, CONFIG_FILE)
if VERSION_MINOR % 2:
    USER_GUIDE_URL = "http://www.pknyx.org/wiki/UserGuideSvn"
else:
    USER_GUIDE_URL = "http://www.pknyx.org/wiki/UserGuide%d.x" % VERSION_MAJOR

# Logger
LOGGER_LONG_FORMAT = "%(asctime)s::%(threadName)s::%(levelname)s::%(message)s"
LOGGER_SHORT_FORMAT = "%(threadName)s::%(message)s"
LOGGER_FORMAT = LOGGER_SHORT_FORMAT
LOGGER_MAX_COUNT_LINE = 1000
LOGGER_FILENAME = "%s%slog" % (APP_NAME.lower(), os.path.extsep)
LOGGER_MAX_BYTES = 100 * 1024
LOGGER_BACKUP_COUNT = 3

# @todo: add automatic load of a gad map if present in config dir
