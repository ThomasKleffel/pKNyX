# -*- coding: utf-8 -*-

"""

License
=======

Module purpose
==============

Graphical toolkit extensions

Implements
==========

- HtmlDefaultFormatter
- HtmlColorFormatter
- HtmlSpaceFormatter
- HtmlSpaceColorFormatter

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import logging
import time

from pknyx.common import config
from pknyx.common.loggingFormatter import DefaultFormatter


class HtmlDefaultFormatter(DefaultFormatter):
    """ Formatage par défaut pour Qt.
    """
    def _toHtml(self, msg):
        """ Convert for html.
        """
        msg = msg.replace('<', "&lt;")
        msg = msg.replace('>', "&gt;")
        msg = msg.replace(' ', "&nbsp;")
        msg = msg.replace('\n', "<br />")
        return msg

    def format(self, record):
        msg = DefaultFormatter.format(self, record)
        return self._toHtml(msg)


class HtmlColorFormatter(HtmlDefaultFormatter):
    """ Formatage avec couleurs.
    """
    colors = {'trace': "<font color=blue>",
              'debug': "<font color=lightblue>",
              'info': "<font color=white>",
              'warning': "<font color=yellow>",
              'error': "<font color=red>",
              'exception': "<font color=violet>",
              'critical': "<font color=white bgcolor=red>",
              'default': "<font color=white>"
              }

    def _toColor(self, msg, levelname):
        """ Colorize.
        """
        if levelname == 'TRACE':
            color = HtmlColorFormatter.colors['trace']
        elif levelname == 'DEBUG':
            color = HtmlColorFormatter.colors['debug']
        elif levelname == 'INFO':
            color = HtmlColorFormatter.colors['info']
        elif levelname == 'WARNING':
            color = HtmlColorFormatter.colors['warning']
        elif levelname == 'ERROR':
            color = HtmlColorFormatter.colors['error']
        elif levelname == 'EXCEPTION':
            color = HtmlColorFormatter.colors['exception']
        elif levelname == 'CRITICAL':
            color = HtmlColorFormatter.colors['critical']
        else:
            color = HtmlColorFormatter.colors['default']

        return color + msg + "</font>"

    def format(self, record):
        msg = HtmlDefaultFormatter.format(self, record)
        return self._toColor(msg, record.levelname)


class HtmlSpaceFormatter(HtmlDefaultFormatter):
    """ Formatage avec sauts de lignes.
    """
    _lastLogTime = time.time()

    def _addSpace(self, msg):
        """ Ajoute des lignes vides.

        Le nombre de lignes vide est fonction du temps écoulé depuis
        le dernier enregistrement émis.
        """
        if time.time() - HtmlSpaceFormatter._lastLogTime > 3600:
            space = "<br /><br /><br />"
        elif time.time() - self._lastLogTime > 60:
            space = "<br /><br />"
        elif time.time() - self._lastLogTime > 3:
            space = "<br />"
        else:
           space = ""
        QSpaceFormatter._lastLogTime = time.time()

        return space + msg

    def format(self, record):
        msg = HtmlDefaultFormatter.format(self, record)
        return self._addSpace(msg)


class HtmlSpaceColorFormatter(HtmlSpaceFormatter, HtmlColorFormatter):
    """ Formatter avec couleurs et sauts de lignes.
    """
    def format(self, record):
        msg = HtmlSpaceFormatter.format(self, record)
        return self._toColor(msg, record.levelname)
