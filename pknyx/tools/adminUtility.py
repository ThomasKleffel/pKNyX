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

The main goal of this utility is to start/stop a device, and to create a fresh device from a template.
Ths usage of this utility is not mandatory, but handles some annoying logger init suffs.

Usage
=====

Should be used from an executable script. See scripts/pknyx-admin.py.

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import shutil
#import imp
import sys
import stat
import string
import os.path
import argparse

from pknyx.common import config
from pknyx.common.exception import PKNyXValueError
from pknyx.services.logger import Logger
from pknyx.tools.templateGenerator import TemplateGenerator
from pknyx.tools.templates.deviceTemplate import ADMIN, INIT, CONFIG, DEVICE, FB
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

    def _createDevice(self, args):
        """
        """
        Logger().setLevel("info")
        Logger().info("Generate '%s' structure from template..." % args.name)  # must be a simple name, not a path

        topDir = args.name
        deviceDir = os.path.join(topDir, args.name)
        fbDir = os.path.join(deviceDir, "fb")
        pluginsDir = os.path.join(deviceDir, "plugins")

        if args.className is None:
            deviceClass = args.name.capitalize()
        else:
            deviceClass = args.className
        deviceName = args.name
        replace = dict(deviceName=deviceName, deviceClass=deviceClass)

        # Top dir
        TemplateGenerator.createDir(topDir)
        Logger().info("'%s' dir created" % topDir)

        adminGen = TemplateGenerator(ADMIN)
        dest = os.path.join(topDir, "admin.py")
        adminGen.generateToFile(dest, replaceDict=replace, script=True)
        Logger().info("'%s' file generated" % dest)

        # Device dir
        TemplateGenerator.createDir(deviceDir)
        Logger().info("'%s' dir created" % deviceDir)

        initGen = TemplateGenerator(INIT)
        dest = os.path.join(deviceDir, "__init__.py")
        initGen.generateToFile(dest, {}, script=False)
        Logger().info("'%s' file generated" % dest)

        configGen = TemplateGenerator(CONFIG)
        dest = os.path.join(deviceDir, "config.py")
        configGen.generateToFile(dest, replaceDict=replace, script=False)
        Logger().info("'%s' file generated" % dest)

        deviceGen = TemplateGenerator(DEVICE)
        dest = os.path.join(deviceDir, "device.py")
        deviceGen.generateToFile(dest, replaceDict=replace, script=False)
        Logger().info("'%s' file generated" % dest)

        # 'fb' dir
        TemplateGenerator.createDir(fbDir)
        Logger().info("'%s' dir created" % fbDir)

        initGen = TemplateGenerator(INIT)
        dest = os.path.join(fbDir, "__init__.py")
        initGen.generateToFile(dest, {}, script=False)
        Logger().info("'%s' file generated" % dest)

        fbGen = TemplateGenerator(FB)
        dest = os.path.join(fbDir, "%sFB.py" % deviceName)
        fbGen.generateToFile(dest, replaceDict=replace, script=False)
        Logger().info("'%s' file generated" % dest)

        # 'plugins' dir
        TemplateGenerator.createDir(pluginsDir)
        Logger().info("'%s' dir created" % pluginsDir)

        initGen = TemplateGenerator(INIT)
        dest = os.path.join(pluginsDir, "__init__.py")
        initGen.generateToFile(dest, {}, script=False)
        Logger().info("'%s' file generated" % dest)

        Logger().info("'%s' structure done" % deviceName)

    def _checkRunDevice(self, args):
        """
        """

        # Retreive device config path
        PKNYX_DEVICE_PATH = args.configPath
        if PKNYX_DEVICE_PATH == "$PKNYX_DEVICE_PATH":
            raise AdminUtilityValueError("$PKNYX_DEVICE_PATH not set")

        sys.path.insert(0, PKNYX_DEVICE_PATH)

        # Load specific device 'config' module which must exists in PKNYX_DEVICE_PATH dir
        import config as deviceConfigModule
        #try:
            #fp, pathname, description = imp.find_module("config", [PKNYX_DEVICE_PATH])
        #except ImportError:
            #raise AdminUtilityValueError("can't find any 'config' module in $PKNYX_DEVICE_PATH path (%s)" % PKNYX_DEVICE_PATH)
        #try:
            #deviceConfigModule = imp.load_module("config", fp, pathname, description)
        #finally:
            #if fp:
                #fp.close()

        # Retreive device config
        if args.deviceIndAddr is not None:
            deviceConfigModule.DEVICE_IND_ADDR = args.deviceIndAddr

        # Init the logger
        # DO NOT USE LOGGER BEFORE THIS POINT!
        if args.loggerLevel is not None:
            config.LOGGER_LEVEL = args.loggerLevel
        Logger("%s-%s" % (deviceConfigModule.DEVICE_NAME, deviceConfigModule.DEVICE_IND_ADDR), config.LOGGER_LEVEL)

        Logger().debug("AdminUtility._checkRunDevice(): args=%s" % repr(args))

        Logger().info("Logger level is '%s'" % config.LOGGER_LEVEL)
        Logger().info("Config path is '%s'" % PKNYX_DEVICE_PATH)
        Logger().info("Device name is '%s'" % deviceConfigModule.DEVICE_NAME)
        Logger().info("Device Individual Address is '%s'" % deviceConfigModule.DEVICE_IND_ADDR)

        deviceIndAddr = deviceConfigModule.DEVICE_IND_ADDR
        if not isinstance(deviceIndAddr, IndividualAddress):
            deviceIndAddr = IndividualAddress(deviceIndAddr)
        if deviceIndAddr.isNull:
            Logger().warning("device individual address is null")

        # Import user device
        import device as deviceModule
        #try:
            #fp, pathname, description = imp.find_module("device", [PKNYX_DEVICE_PATH])
        #except ImportError:
            #raise AdminUtilityValueError("can't find any 'device' module in $PKNYX_DEVICE_PATH path (%s)" % PKNYX_DEVICE_PATH)
        #try:
            #deviceModule = imp.load_module("device", fp, pathname, description)
        #finally:
            #if fp:
                #fp.close()

        # Instantiate device
        device = deviceModule.DEVICE()

        return device

    def _checkDevice(self, args):
        """
        """
        device = self._checkRunDevice(args)

        Logger().info("No error found")

    def _runDevice(self, args):
        """
        """
        device = self._checkRunDevice(args)

        Logger().info("Detaching is '%s'" % args.detach)

        device.run()

    def execute(self):

        # Main parser
        mainParser = argparse.ArgumentParser(prog="pknyx-admin.py",
                                             description="This tool is used to manage pKNyX devices.",
                                             epilog="Under developement...")

        # Create sub-parsers
        subparsers = mainParser.add_subparsers(title="subcommands", description="valid subcommands",
                                               help="sub-command help")

        # Create device parser
        createDeviceParser = subparsers.add_parser("createdevice",
                                                   help="create device from template")
        createDeviceParser.add_argument("-c", "--class", type=str, dest="className",
                                        help="name of the device class")
        createDeviceParser.add_argument("name", type=str,
                                        help="name of the device")
        createDeviceParser.set_defaults(func=self._createDevice)

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

        # Check device parser
        checkDeviceParser = subparsers.add_parser("checkdevice",
                                                  parents=[checkRunDeviceParser],
                                                  help="check device (does not launch the stack main loop)")
        checkDeviceParser.set_defaults(func=self._checkDevice)

        # Run device parser
        runDeviceParser = subparsers.add_parser("rundevice",
                                                parents=[checkRunDeviceParser],
                                                help="run device")
        runDeviceParser.add_argument("-d", "--detach", action="store_true", default=False,
                                     help="detach the process (run in background)")
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
