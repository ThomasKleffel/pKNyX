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

Logging

Implements
==========

- DefaultFormatter
- ColorFormatter
- Logger

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import logging
import logging.handlers
import StringIO
import traceback
import os.path

from pknyx.common import config
from pknyx.common.loggingFormatter import DefaultFormatter, ColorFormatter, \
                                          SpaceFormatter, SpaceColorFormatter

logger = None


class LoggerObject(object):
    """ Logger object.
    """
    def __init__(self, defaultStreamHandler, defaultFileHandler):
        """ Init object.
        """
        super(LoggerObject, self).__init__()

        logging.TRACE = logging.DEBUG - 5
        logging.EXCEPTION = logging.ERROR + 5
        logging.raiseExceptions = 0
        logging.addLevelName(logging.TRACE, "TRACE")
        logging.addLevelName(logging.EXCEPTION, "EXCEPTION")

        # Formatters
        #defaultFormatter = DefaultFormatter(config.LOGGER_FORMAT)
        spaceFormatter = SpaceFormatter(config.LOGGER_FORMAT)
        #colorFormatter = ColorFormatter(config.LOGGER_FORMAT)
        spaceColorFormatter = SpaceColorFormatter(config.LOGGER_FORMAT)

        # Logger
        self.__logger = logging.getLogger('papywizard')
        self.__logger.setLevel(logging.TRACE)

        # Handlers
        if defaultStreamHandler:
            stdoutStreamHandler = logging.StreamHandler()
            #stdoutStreamHandler.setFormatter(colorFormatter)
            stdoutStreamHandler.setFormatter(spaceColorFormatter)
            self.__logger.addHandler(stdoutStreamHandler)
        if defaultFileHandler:
            loggerFilename = os.path.join(config.TMP_DIR, config.LOGGER_FILENAME)
            fileHandler = logging.handlers.RotatingFileHandler(loggerFilename, 'w',
                                                               config.LOGGER_MAX_BYTES,
                                                               config.LOGGER_BACKUP_COUNT)
            fileHandler.setFormatter(spaceFormatter)
            self.__logger.addHandler(fileHandler)

    def addStreamHandler(self, stream, formatter=DefaultFormatter):
        """ Add a new stream handler.

        Can be used to register a new GUI handler.

        @param stream: open stream where to write logs
        @type stream: file

        @param formatter: associated formatter
        @type formatter: L{DefaultFormatter<pknyx.common.loggingFormatter>}
        """
        handler = logging.StreamHandler(stream)
        handler.setFormatter(formatter(config.LOGGER_FORMAT))
        self.__logger.addHandler(handler)

    def setLevel(self, level):
        """ Change logging level.

        @param level: new level, in ('trace', 'debug', 'info', 'warning', 'error', 'exception', 'critical')
        @type level: str
        """
        loggerLevels = ('trace', 'debug', 'info', 'warning', 'error', 'exception', 'critical')
        if level not in loggerLevels:
            raise ValueError("Logger level must be in %s" % repr(loggerLevels))
        levels = {'trace': logging.TRACE,
                  'debug': logging.DEBUG,
                  'info': logging.INFO,
                  'warning': logging.WARNING,
                  'error': logging.ERROR,
                  'exception': logging.EXCEPTION,
                  'critical': logging.CRITICAL}
        self.__logger.setLevel(levels[level])

    def trace(self, message, *args, **kwargs):
        """ Logs a message with level TRACE.

        @param message: message to log
        @type message: string
        """
        self.__logger.log(logging.TRACE, message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        """ Logs a message with level DEBUG.

        @param message: message to log
        @type message: string
        """
        self.__logger.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        """ Logs a message with level INFO.

        @param message: message to log
        @type message: string
        """
        self.__logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """ Logs a message with level WARNING.

        @param message: message to log
        @type message: string
        """
        self.__logger.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        """ Logs a message with level ERROR.

        @param message: message to log
        @type message: string
        """
        self.__logger.error(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        """ Logs a message with level CRITICAL.

        @param message: message to log
        @type message: string
        """
        self.__logger.critical(message, *args, **kwargs)

    def exception(self, message, debug=False, *args, **kwargs):
        """ Logs a message within an exception.

        @param message: message to log
        @type message: string

        @param debug: flag to log exception on DEBUG level instead of EXCEPTION one
        @type debug: bool
        """
        kwargs['exc_info'] = True
        if debug:
            self.debug(message, *args, **kwargs)
        else:
            self.log(logging.EXCEPTION, message, *args, **kwargs)

    def log(self, level, message, *args, **kwargs):
        """ Logs a message with given level.

        @param level: log level to use
        @type level: int

        @param message: message to log
        @type message: string
        """
        self.__logger.log(level, message, *args, **kwargs)

    def getTraceback(self):
        """ Return the complete traceback.

        Should be called in an except statement.
        """
        tracebackString = StringIO.StringIO()
        traceback.print_exc(file=tracebackString)
        message = tracebackString.getvalue().strip()
        tracebackString.close()
        return message

    def shutdown(self):
        """ Shutdown the logging service.
        """
        logging.shutdown()


# Logger factory
def Logger(defaultStreamHandler=True, defaultFileHandler=True):
    global logger
    if logger is None:
        logger = LoggerObject(defaultStreamHandler, defaultFileHandler)

    return logger
