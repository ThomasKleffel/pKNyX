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

ETS management

Implements
==========

 - B{ETS}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common.exception import PKNyXValueError
from pknyx.common.singleton import Singleton
from pknyx.services.logger import Logger
from pknyx.stack.flags import Flags
from pknyx.stack.groupAddress import GroupAddress
from pknyx.services.scheduler import Scheduler
from pknyx.services.notifier import Notifier
from pknyx.services.groupAddressTableMapper import GroupAddressTableMapper


class ETSValueError(PKNyXValueError):
    """
    """


class ETS(object):
    """ ETS class

    @ivar _stack: KNX stack object
    @type _stack: L{Stack<pknyx.stack.stack>}

    @ivar _functionalBlocks: registered functional blocks
    @type _functionalBlocks: set of L{FunctionalBlocks<pknyx.core.functionalBlocks>}

    raise ETSValueError:
    """
    __metaclass__ = Singleton

    def __init__(self):
        """
        """
        super(ETS, self).__init__()

    @property
    def gadMap(self):
        return self._gadMap

    @property
    def buildingMap(self):
        return self._buildingMap

    def register(self, device, buildingMap='root'):
        """ Register a device

        This method registers pending scheduler/notifier jobs of all FunctionalBlock of the Device.

        @param device: device to register
        @type device: L{Device<pknyx.core.device>}
        """
        for fb in device.fb.values():

            # Register pending scheduler/notifier jobs
            Scheduler().doRegisterJobs(fb)
            Notifier().doRegisterJobs(fb)

    def weave(self, device):
        """ Weave (link, bind...) device datapoints

        @param device: device to weave
        @type device: L{Device<pknyx.core.device>}
        """
        flags = None
        for fb_, dp, gad in device.lnk:

            # Retreive FunctionnalBlock from device
            try:
                fb = device.fb[fb_]

            except KeyError:
                raise ETSValueError("unregistered functional block (%s)" % fb)

            # Retreive GroupObject from FunctionalBlock
            try:
                groupObject = fb.go[dp]

            except KeyError:
                raise ETSValueError("no Group Object associated with this datapoint (%s)" % dp)

            # Override GroupObject flags
            if flags is not None:
                if not isinstance(flags, Flags):
                    flags = Flags(flags)
                groupObject.flags = flags

            # Get GroupAddress
            if not isinstance(gad, GroupAddress):
                gad = GroupAddress(gad)

            # Ask the group data service to subscribe this GroupObject to the given gad
            # In return, get the created group
            group = device.stack.agds.subscribe(gad, groupObject)

            # If not already done, set the GroupObject group. This group will be used when the GroupObject wants to
            # communicate on the bus. This mimics the S flag of ETS real application.
            # @todo: find a better way
            if groupObject.group is None:
                groupObject.group = group

    bind = weave
    link = weave  # nice names too!

    def getGrOAT(self, device, by="gad", outFormatLevel=3):
        """ Build the Group Object Association Table
        """

        # Retreive all bound gad
        gads = []
        for gad in device.stack.agds.groups.keys():
            gads.append(GroupAddress(gad, outFormatLevel))
        gads.sort()  #reverse=True)

        output = "\n"

        if by == "gad":
            gadMapTable = GroupAddressTableMapper().table
            title = "%-34s %-30s %-30s %-10s %-10s %-10s" % ("GAD", "Datapoint", "Functional block", "DPTID", "Flags", "Priority")
            output += title
            output += "\n"
            output += len(title) * "-"
            output += "\n"
            gadMain = gadMiddle = gadSub = -1
            for gad in gads:
                if gadMain != gad.main:
                    index = "%d/-/-" % gad.main
                    if gadMapTable.has_key(index):
                        output +=  u"%2d %-33s" % (gad.main, gadMapTable[index]['desc'].decode("utf-8"))
                        output += "\n"
                    else:
                        output +=  u"%2d %-33s" % (gad.main, "")
                        output += "\n"
                    gadMain = gad.main
                    gadMiddle = gadSub = -1
                if gadMiddle != gad.middle:
                    index = "%d/%d/-" % (gad.main, gad.middle)
                    if gadMapTable.has_key(index):
                        output +=  u" ├── %2d %-27s" % (gad.middle, gadMapTable[index]['desc'].decode("utf-8"))
                        output += "\n"
                    else:
                        output +=  u" ├── %2d %-27s" % (gad.middle, "")
                        output += "\n"
                    gadMiddle = gad.middle
                    gadSub = -1
                if gadSub != gad.sub:
                    index = "%d/%d/%d" % (gad.main, gad.middle, gad.sub)
                    if gadMapTable.has_key(index):
                        output +=  u" │    ├── %3d %-21s" % (gad.sub, gadMapTable[index]['desc'].decode("utf-8"))
                    else:
                        output +=  u" │    ├── %3d %-21s" % (gad.sub, "")
                    gadSub = gad.sub

                for i, go in enumerate(device.stack.agds.groups[gad.address].listeners):
                    dp = go.datapoint
                    fb = dp.owner
                    if not i:
                        output +=  u"%-30s %-30s %-10s %-10s %-10s" % (dp.name, fb.name, dp.dptId, go.flags, go.priority)
                        output += "\n"
                    else:
                        output +=  u" │    │                            %-30s %-30s %-10s %-10s %-10s" % (dp.name, fb.name, dp.dptId, go.flags, go.priority)
                        output += "\n"

                gad_ = gad

        elif by == "go":

            # Retreive all groupObjects, not only bound ones
            # @todo: use buildingMap presentation
            mapByDP = {}
            title = "%-29s %-30s %-10s %-30s %-10s %-10s" % ("Functional block", "Datapoint", "DPTID", "GAD", "Flags", "Priority")
            output +=  title
            output += "\n"
            output +=  len(title) * "-"
            output += "\n"
            for fb in device.fb.values():
                #output +=  "%-30s" % fb.name
                for i, go in enumerate(fb.go.values()):
                    output +=  "%-30s" % fb.name
                    dp = go.datapoint
                    #if i:
                        #output +=  "%-30s" % ""
                    gads_ = []
                    for gad in gads:
                        if go in device.stack.agds.groups[gad.address].listeners:
                            gads_.append(gad.address)
                    if gads_:
                        output +=  "%-30s %-10s %-30s %-10s %-10s" % (go.name, dp.dptId, ", ".join(gads_), go.flags, go.priority)
                        output += "\n"
                    else:
                        output +=  "%-30s %-10s %-30s %-10s %-10s" % (go.name, dp.dptId, "", go.flags, go.priority)
                        output += "\n"

        else:
            raise ETSValueError("by param. must be in ('gad', 'dp')")

        return output


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
