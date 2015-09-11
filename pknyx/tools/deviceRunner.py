# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{pKNyX} (U{http://www.pknyx.org}) is Copyright:
  - (C) 2013-2015 Frédéric Mantegazza

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

 - B{DeviceRunnerValueError}
 - B{DeviceRunner}

Documentation
=============

The main goal of this utility is to start/stop a device, and to create a fresh device from a template.
Ths usage of this utility is not mandatory, but handles some annoying logger init suffs.

Usage
=====

Should be used from an executable script. See scripts/pknyx-admin.py.

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import os.path
import imp
import sys

from pknyx.common import config
from pknyx.common.exception import PKNyXValueError
from pknyx.services.logger import Logger
from pknyx.services.scheduler import Scheduler
from pknyx.services.groupAddressTableMapper import GroupAddressTableMapper
from pknyx.core.ets import ETS
from pknyx.stack.stack import Stack
from pknyx.stack.individualAddress import IndividualAddress
from pknyx.stack.groupAddress import GroupAddress, GroupAddressValueError


class DeviceRunnerValueError(PKNyXValueError):
    """
    """


class DeviceRunner(object):
    """
    """
    def __init__(self, loggerLevel, devicePath, gadMapPath):
        """
        """
        super(DeviceRunner, self).__init__()

        sys.path.insert(0, devicePath)

        # Load user 'settings' module
        from settings import DEVICE_NAME, DEVICE_IND_ADDR

        # Init the logger
        if loggerLevel is not None:
            config.LOGGER_LEVEL = loggerLevel

        # DO NOT USE LOGGER BEFORE THIS POINT!
        Logger("%s-%s" % (DEVICE_NAME, DEVICE_IND_ADDR))
        Logger().info("Logger level is '%s'" % config.LOGGER_LEVEL)

        Logger().info("Device path is '%s'" % devicePath)
        Logger().info("Device name is '%s'" % DEVICE_NAME)

        deviceIndAddr = DEVICE_IND_ADDR
        if not isinstance(deviceIndAddr, IndividualAddress):
            deviceIndAddr = IndividualAddress(deviceIndAddr)
        if deviceIndAddr.isNull:
            Logger().warning("Device Individual Address is null")
        else:
            Logger().info("Device Individual Address is '%s'" % DEVICE_IND_ADDR)

        # Load GAD map table
        mapper = GroupAddressTableMapper()
        mapper.loadFrom(gadMapPath)

        # Create KNX stack
        self._stack = Stack(DEVICE_IND_ADDR)
        self._ets = ETS(self._stack)

    def check(self, printGroat=False):
        """
        """

        # Create device from user 'device' module
        from device import DEVICE
        self._device = DEVICE()

        self._device.register(self._ets)
        self._device.weave(self._ets)

        if printGroat:
            Logger().info(self._ets.getGrOAT("gad"))
            Logger().info(self._ets.getGrOAT("go"))

        self._device.init()

    def run(self, dameon=False):
        """
        """
        Logger().trace("Device.run()")

        self.check()

        Logger().info("Detaching is '%s'" % detach)

        Scheduler().start()
        self._stack.mainLoop()  # blocking call
        Scheduler().stop()

        self._device.shutdown()


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class DeviceRunnerTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
