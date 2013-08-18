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

The Device is the top-level object. It runs as a process. It mainly encapsulate some initialisation, and provide all
objects needed to create a device.

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id: multicast.py 319 2013-08-15 11:11:25Z fma $"

import sys
import argparse

from pknyx.common.exception import PKNyXValueError
from pknyx.services.logger import Logger

from pknyx.core.ets import ETS
from pknyx.stack.individualAddress import IndividualAddress
from pknyx.stack.stack import Stack


class DeviceValueError(PKNyXValueError):
    """
    """


class Device(object):
    """ Device object.
    """
    def __init__(self, name="None", indAddr="0.0.0"):
        """ Init Device object.
        """
        super(Device, self).__init__()

        # Init logger
        self._logger = Logger("%s-%s" % (name, indAddr))
        #self._logger.setLevel(debugLevel)

        self._name = name
        if not isinstance(indAddr, IndividualAddress):
            indAddr = IndividualAddress(indAddr)
        self._indAddr = indAddr

        self._stack = None
        self._ets = None

        # Common options
        parser = argparse.ArgumentParser(prog="Device",
                                         description="This tool is used to execute a pKNyX device as process.",
                                         epilog="Under developement...")
        parser.add_argument("-l", "--logger",
                            choices=["trace", "debug", "info", "warning", "error", "exception", "critical"],
                            action="store", dest="debugLevel", default="info", metavar="LEVEL",
                            help="logger level")
        parser.add_argument("-n", "--name", action="store", type=str, dest="name",
                             help="name of the device")
        parser.add_argument("-i", "--indAddr", action="store", type=str, dest="indAddr",
                            help="individual address of the device")

        # Create sub-parsers
        subparsers = parser.add_subparsers(title="subcommands", description="valid subcommands",
                                           help="sub-command help")

        # Run parser
        parserRun = subparsers.add_parser("run",
                                          #parents=[parser2],
                                          help="Run device")
        parserRun.set_defaults(func=self._run)

        # Check parser
        parserCheck = subparsers.add_parser("check",
                                            #parents=[parser2],
                                            help="Check device")
        parserCheck.set_defaults(func=self._check)

        ## Simul parser
        #parserSimul = subparsers.add_parser("simul",
                                            #parents=[parser2],
                                            #help="Simulate process")
        #parserSimul.set_defaults(func=simul)
        #parserSimul.add_argument("gad", type=str,
                                 #help="group address")
        #parserSimul.add_argument("value", type=str,
                                 #help="value to send")

        ## Monitor parser
        #parserMonitor = subparsers.add_parser("monitor",
                                              #help="monitor bus")
        #parserMonitor.set_defaults(func=monitor)

        # Parse args
        args = parser.parse_args()

        # Retreive name
        try:
            name = self.NAME
        except AttributeError:
            name = args.name
        if name is None:
            name = "Dummy"

        # Retreive individual address
        try:
            indAddr = self.IND_ADDR
        except AttributeError:
            indAddr = args.indAddr
            if indAddr is None:
                indAddr = "0.0.0"
        if not isinstance(indAddr,  IndividualAddress):
            indAddr = IndividualAddress(indAddr)

        # Init device
        self._init_(indAddr)

        if indAddr.isNull:
            self._logger.warning("Device has a null individual address")

        # Purge args
        options = dict(vars(args))
        options.pop("func")
        options.pop("name")
        options.pop("indAddr")
        options.pop("debugLevel")

        # Call func
        args.func(**options)

    def _init_(self, indAddr="0.0.0"):
        """
        """
        self._stack = Stack(indAddr)
        self._ets = ETS(self._stack)


    def _register(self):
        """
        """
        #raise NotImplementedError
        self._logger.trace("Device._register()")
        for key, value in self.__dict__.iteritems():
            if key.startswith("FB_"):
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
        #raise NotImplementedError
        self._logger.trace("Device._weave()")
        for key, value in self.__dict__.iteritems():
            if key.startswith("LNK_"):
                self._logger.debug("Device._weave(): weave %s (%)" % (key, repr(value)))
                self._ets.weave(**value)

    @property
    def name(self):
        return self._name

    @property
    def indAddr(self):
        return self._indAddr

    @property
    def logger(self):
        return self._logger

    #@property
    #def stack(self):
        #return self.stack

    #@property
    #def ets(self):
        #return self._ets

    #@property
    #def scheduler(self):
        #return self._scheduler

    #@property
    #def notifier(self):
        #return self._notifier

    def _run(self):
        """ Run the stack main loop (blocking call)
        """
        self._register()
        self._weave()
        self._stack.mainLoop()

    def _check(self):
        """
        """
        self._register()
        self._weave()

    #def simul(self):
        #"""
        #"""

    #def printGrOAT(self):
        #"""
        #"""
        #print
        #self._ets.printGroat("gad")
        #print
        #self._ets.printGroat("go")
        #print
        #self._schedule.printJobs()
        #print

    def main(self):

        # Common options
        parser = argparse.ArgumentParser(prog="process.py",
                                         description="This tool is used to launch pKNyX processes.",
                                         epilog="Under developement...")
        parser.add_argument("-l", "--logger",
                            choices=["trace", "debug", "info", "warning", "error", "exception", "critical"],
                            action="store", dest="debugLevel", default="info", metavar="LEVEL",
                            help="logger level")
        parser.add_argument("-n", "--name", action="store", type=str, dest="name",
                             help="name of the device")
        parser.add_argument("-i", "--indAddr", action="store", type=str, dest="indAddr",
                            help="individual address of the device")

        # Create sub-parsers
        subparsers = parser.add_subparsers(title="subcommands", description="valid subcommands",
                                           help="sub-command help")

        # Run parser
        parserRun = subparsers.add_parser("run",
                                          #parents=[parser2],
                                          help="Run device")
        parserRun.set_defaults(func=self._run)

        # Check parser
        parserCheck = subparsers.add_parser("check",
                                            #parents=[parser2],
                                            help="Check device")
        parserCheck.set_defaults(func=self._check)

        ## Simul parser
        #parserSimul = subparsers.add_parser("simul",
                                            #parents=[parser2],
                                            #help="Simulate process")
        #parserSimul.set_defaults(func=simul)
        #parserSimul.add_argument("gad", type=str,
                                 #help="group address")
        #parserSimul.add_argument("value", type=str,
                                 #help="value to send")

        ## Monitor parser
        #parserMonitor = subparsers.add_parser("monitor",
                                              #help="monitor bus")
        #parserMonitor.set_defaults(func=monitor)

        # Parse args
        args = parser.parse_args()

        # Retreive name
        try:
            name = self.NAME
        except AttributeError:
            name = args.name
        if name is None:
            name = "Dummy"

        # Retreive individual address
        try:
            indAddr = self.IND_ADDR
        except AttributeError:
            indAddr = args.indAddr
            if indAddr is None:
                indAddr = "0.0.0"
        if not isinstance(indAddr,  IndividualAddress):
            indAddr = IndividualAddress(indAddr)

        # Init device
        self._init(name, indAddr, args.debugLevel)

        if indAddr.isNull:
            self._logger.warning("Device has a null individual address")

        # Purge args
        options = dict(vars(args))
        options.pop("func")
        options.pop("name")
        options.pop("indAddr")
        options.pop("debugLevel")

        # Call func
        args.func(**options)


if __name__ == "__main__":
    device = Device()
    device.main()
