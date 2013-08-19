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

 - B{AdminUtilityValueError}
 - B{AdminUtility}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import imp
import os.path
import argparse

from pknyx.common import config
from pknyx.common.exception import PKNyXValueError
from pknyx.services.logger import Logger
from pknyx.stack.individualAddress import IndividualAddress


class AdminUtilityValueError(PKNyXValueError):
    """
    """


class AdminUtility(object):
    """
    """
    def __init__(self):
        """
        """
        super(AdminUtility, self).__init__()


    def _checkRunDevice(self, args):
        """
        """

        # Retreive device config path
        PKNYX_DEVICE_PATH = args.configPath
        if PKNYX_DEVICE_PATH == "$PKNYX_DEVICE_PATH":
            raise AdminUtilityValueError("$PKNYX_DEVICE_PATH not set")

        # Load device specific 'config' module which must exists in PKNYX_DEVICE_PATH dir
        try:
            fp, pathname, description = imp.find_module("config", [PKNYX_DEVICE_PATH])
        except ImportError:
            raise AdminUtilityValueError("can't find any 'config' module in $PKNYX_DEVICE_PATH path (%s)" % PKNYX_DEVICE_PATH)
        try:
            deviceConfigModule = imp.load_module("config", fp, pathname, description)
        finally:
            if fp:
                fp.close()

        # Retreive device config
        if args.deviceIndAddr is not None:
            deviceConfigModule.DEVICE_IND_ADDR = args.deviceIndAddr

        # Init the logger
        # DO NOT USE LOGGER BEFORE THIS POINT!
        if args.loggerLevel is not None:
            config.LOGGER_LEVEL = args.loggerLevel
        Logger("%s-%s" % (deviceConfigModule.DEVICE_NAME, deviceConfigModule.DEVICE_IND_ADDR), config.LOGGER_LEVEL)

        Logger().debug("main(): args=%s" % repr(args))

        Logger().info("main(): config path is '%s'" % PKNYX_DEVICE_PATH)
        Logger().info("main(): device name is '%s'" % deviceConfigModule.DEVICE_NAME)
        Logger().info("main(): device individual address is '%s'" % deviceConfigModule.DEVICE_IND_ADDR)

        deviceIndAddr = deviceConfigModule.DEVICE_IND_ADDR
        if not isinstance(deviceIndAddr, IndividualAddress):
            deviceIndAddr = IndividualAddress(deviceIndAddr)
        if deviceIndAddr.isNull:
            Logger().warning("device individual address is null")

        # Import device
        try:
            fp, pathname, description = imp.find_module("device", [PKNYX_DEVICE_PATH])
        except ImportError:
            raise AdminUtilityValueError("can't find any 'device' module in $PKNYX_DEVICE_PATH path (%s)" % PKNYX_DEVICE_PATH)
        try:
            deviceModule = imp.load_module("device", fp, pathname, description)
        finally:
            if fp:
                fp.close()

        device = deviceModule.device

        return device


    def _createDevice(self, args):
        """
        """
        print args.name  # must be a simple name, not a complex path


    def _checkDevice(self, args):
        """
        """
        device = self._checkRunDevice(args)


    def _runDevice(self, args):
        """
        """
        device = self._checkRunDevice(args)
        device.run()


    def execute(self):

        # Main parent parser
        mainParser = argparse.ArgumentParser(prog="pknyx-admin.py",
                                             description="This tool is used to manage pKNyX devices.",
                                             epilog="Under developement...")

        # Check/run device parent parser
        checkRunDeviceParser = argparse.ArgumentParser(add_help=False)
        checkRunDeviceParser.add_argument("-l", "--logger",
                                          choices=["trace", "debug", "info", "warning", "error", "exception", "critical"],
                                          action="store", dest="loggerLevel", metavar="LEVEL",
                                          help="override logger level")
        checkRunDeviceParser.add_argument("-i", "--indAddr", action="store", type=str, dest="deviceIndAddr",
                                          help="override individual address")
        checkRunDeviceParser.add_argument("-p", "--path", action="store", type=str, dest="configPath", default=os.path.expandvars("$PKNYX_DEVICE_PATH"),
                                          help="set/override $PKNYX_DEVICE_PATH path")

        # Create sub-parsers
        subparsers = mainParser.add_subparsers(title="subcommands", description="valid subcommands",
                                               help="sub-command help")

        # Create device parser
        createDeviceParser = subparsers.add_parser("createdevice",
                                                   help="Create device from template")
        createDeviceParser.add_argument("name", type=str,
                                        help="name of the device")
        createDeviceParser.set_defaults(func=self._createDevice)

        # Check device parser
        checkDeviceParser = subparsers.add_parser("checkdevice",
                                                  parents=[checkRunDeviceParser],
                                                  help="Check device")
        checkDeviceParser.set_defaults(func=self._checkDevice)

        # Run device parser
        runDeviceParser = subparsers.add_parser("rundevice",
                                                parents=[checkRunDeviceParser],
                                                help="Run device")
        runDeviceParser.set_defaults(func=self._runDevice)

        # Parse args
        args = mainParser.parse_args()
        args.func(args)


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class AdminUtilityTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()


