#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{pKNyX} (U{http://www.pknyx.org}) is Copyright:
  - (C) 2013 Frédéric Mantegazza

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
or see:

 - U{http://www.gnu.org/licenses/gpl.html}

Module purpose
==============

Device (process) management.

Implements
==========

 - B{Device}

Documentation
=============

The Device is the top-level object. It runs as a process. It mainly encapsulates some initialisations.

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common import config
from pknyx.common.exception import PKNyXValueError
from pknyx.services.logger import Logger
from pknyx.services.scheduler import Scheduler
from pknyx.core.ets import ETS
from pknyx.stack.stack import Stack

# Import device config
# This loads the 'config' module beside the custom 'device' module under execution
import config as deviceConfig


class DeviceValueError(PKNyXValueError):
    """
    """


class Device(object):
    """ Device class definition.
    """
    def __init__(self):
        """ Init Device object.
        """
        super(Device, self).__init__()

        self._stack = None
        self._ets = None
        self._stack = Stack(deviceConfig.DEVICE_IND_ADDR)
        self._ets = ETS(self._stack)

        self._register()
        self._weave()

        self._init()

    def _init(self):
        """ Additionnal user init
        """
        pass

    def _register(self):
        """
        """
        Logger().trace("Device._register()")

        for key, value in self.__class__.__dict__.iteritems():
            if key.startswith("FB_"):
                Logger().debug("Device._register(): %s=(%s)" % (key, repr(value)))
                cls = value["cls"]

                # Remove 'cls' key from FB_xxx dict
                # Use a copy to let original untouched
                value_ = {}
                value_.update(value)
                value_.pop('cls')
                self._ets.register(cls, **value_)

    def _weave(self):
        """
        """
        Logger().trace("Device._weave()")

        for key, value in self.__class__.__dict__.iteritems():
            if key.startswith("LNK_"):
                Logger().debug("Device._weave(): %s=(%s)" % (key, repr(value)))
                self._ets.weave(**value)

    def run(self):
        """
        """
        Logger().trace("Device.run()")

        Scheduler().start()
        self._stack.mainLoop()
