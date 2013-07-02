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

ETS management

Implements
==========

 - B{ETS}

Documentation
=============

@todo: subclass and add building/GA tree nodes (as class vars).

class MOB(ETS):

    BUILDINGS =
    GADS =

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common.exception import PKNyXValueError
from pknyx.logging.loggingServices import Logger
from pknyx.core.device import Device
from pknyx.stack.groupAddress import GroupAddress, GroupAddressValueError


class ETSValueError(PKNyXValueError):
    """
    """


class ETS(object):
    """ ETS class

    @ivar _stack: KNX stack object
    @type _stack: L{Stack<pknyx.stack.stack>}

    @ivar _devices: registered devices
    @type _devices: set of L{Device}

    raise ETSValueError:
    """
    def __init__(self, stack):
        """

        @param stack: KNX stack object
        @type stack: L{Stack<pknyx.stack.stack>}

        raise ETSValueError:
        """
        super(ETS, self).__init__()

        self._stack = stack

        self._devices = set()
        self._gadMap = None

    @property
    def stack(self):
        return self._stack

    @property
    def devices(self):
        return [device.name for device in self._devices]

    @property
    def datapoints(self):
        dps = []
        for device in self._devices:
            dps.append(device.dp.values())

        return dps

    @property
    def gadMap(self):
        return self._gadMap

    @gadMap.setter
    def gadMap(self, gadMap):
        self._gadMap = gadMap

    def register(self, device, building='root'):
        """ Register a device

        @param device: device to register
        @type device: L{Device}
        """
        if device in self._devices:
            raise ETSValueError("device already registered (%s)" % repr(device))

        self._devices.add(device)

    def link(self, dev, dp, gad):
        """ Link a datapoint to a GAD

        @param dev: device owning the datapoint
        @type dev: L{Device}

        @param dp: name of the datapoint to link
        @type dp: str

        @param gad : Group address to link to
        @type gad : str or L{GroupAddress} (or sequence of...)

        @todo: check for duplicate individual address

        raise ETSValueError:
        """
        if dev not in self._devices:
            raise ETSValueError("unregistered device (%s)" % dev)

        # Get datapoint
        datapoint = dev.dp[dp]

        # Check if gad is a single GAD or a sequence of GAD
        if isinstance(gad[0], GroupAddress):
            gads = gad
        else:
            try:
                GroupAddress(gad[0])
            except GroupAddressValueError:
                gads = (gad,)
            else:
                gads = gad

        for gad in gads:

            # Ask the group data service to subscribe this datapoint to the given gad
            # In return, get the created accesspoint
            accesspoint = self._stack.gds.subscribe(gad, datapoint)

            # If the datapoint does not already have an accesspoint, set it
            # This accesspoint will be used by the datapoint to send datas to the default GAD
            # This mimics the S flag of ETS real application
            # @todo: find a way to change it later? Or let the datapoint manage this?
            if datapoint.accesspoint is None:
                datapoint.accesspoint = accesspoint

        # Add the device to the known devices
        self._devices.add(dev)

    def computeMapTable(self):
        """
        """
        mapByGAD = {}
        for gad, group in self._stack.gds.groups.iteritems():
            mapByGAD[gad] = []
            for dp in group.listeners:
                mapByGAD[gad].append("%s (%s)" % (dp.name, dp.owner.name))

        # Retreive all datapoints, not only bound ones
        mapByDP = {}
        for device in self._devices:
            for dp in device.dp.values():
                gads = []
                for gad, dps in mapByGAD.iteritems():
                    if "%s (%s)" % (dp.name, device.name) in dps:
                        gads.append(gad)
                mapByDP["%s (%s)" % (dp.name, device.name)] = gads

        return {'byGAD': mapByGAD, 'byDP': mapByDP}

    def printMapTable(self, by="gad", outFormatLevel=3):
        """
        """

        # Retreive all bound gad
        gads = []
        for gad in self._stack.gds.groups.keys():
            gads.append(GroupAddress(gad, outFormatLevel=outFormatLevel))
        gads.sort()

        if by == "gad":
            print "Ordered by GAD:\n"
            print "%-24s %-25s %-20s %-8s %-8s %-8s" % ("GAD", "Datapoint", "Device", "DPTID", "Flags", "Priority")
            gadMain = gadMiddle = gadSub = -1
            for gad in gads:
                if gadMain != gad.main:
                    try:
                        print "%2d %-10s" % (gad.main, self._gadMap[gad.main]['root'])
                    except (TypeError, KeyError):
                        print "%2d %-10s" % (gad.main, "")
                    gadMain = gad.main
                    gadMiddle = gadSub = -1
                if gadMiddle != gad.middle:
                    try:
                        print " ├── %2d %-10s" % (gad.middle, self._gadMap[gad.main][gad.middle]['root'])
                    except (TypeError, KeyError):
                        print " ├── %2d %-10s" % (gad.middle, "")
                    gadMiddle = gad.middle
                if gadSub != gad.sub:
                    try:
                        print " │    ├── %3d %-10s" % (gad.sub, self._gadMap[gad.main][gad.middle][gad.sub]),
                    except (TypeError, KeyError):
                        print " │    ├── %3d %-10s" % (gad.sub, ""),
                    gadSub = gad.sub
                    gadSub = -1

                for i, dp in enumerate(self._stack.gds.groups[gad.address].listeners):
                    if not i:
                        print "%-25s %9s %-10s %-8s %-8s %-8s" % (dp.name, dp.owner.address, dp.owner.name, dp.dptId, dp.flags, dp.priority)
                    else:
                        print " │    │                  %-25s %9s %-10s %-8s %-8s %-8s" % (dp.name, dp.owner.address, dp.owner.name, dp.dptId, dp.flags, dp.priority)

                gad_ = gad

        elif by == "dp":

            # Retreive all datapoints, not only bound ones
            # Use building presentation
            mapByDP = {}
            print "Ordered by Datapoint:\n"
            print "%-20s %-25s %-10s %-27s %-8s %-8s\n" % ("Device", "Datapoint", "DPTID", "GAD", "Flags", "Priority")
            for device in self._devices:
                print "%9s %-10s" % (device.address, device.name),
                for i, dp in enumerate(device.dp.values()):
                    if i:
                        print "%9s %-10s" % ("", ""),
                    gads_ = []
                    for gad in gads:
                        if dp in self._stack.gds.groups[gad.address].listeners:
                            gads_.append(gad.address)
                    if gads_:
                        print "%-25s %-10s %-27s %-8s %-8s" % (dp.name, dp.dptId, ", ".join(gads_), dp.flags, dp.priority)
                    else:
                        print "%-25s %-10s %-27s %-8s %-8s" % (dp.name, dp.dptId, "", dp.flags, dp.priority)

        else:
            raise ETSValueError("by param. must be in ('gad', 'dp')")


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class ETSTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
