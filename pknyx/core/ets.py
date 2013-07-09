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
from pknyx.stack.groupAddress import GroupAddress
from pknyx.services.scheduler import Scheduler


class ETSValueError(PKNyXValueError):
    """
    """


class ETS(object):
    """ ETS class

    @ivar _stack: KNX stack object
    @type _stack: L{Stack<pknyx.stack.stack>}

    @ivar _functionalBlocks: registered functional blocks
    @type _functionalBlocks: set of L{FunctionalBlocks<pknyx.core.functionalBlocks>}

    @ivar _gadMap:

    @ivar _buidlingMap:

    raise ETSValueError:
    """
    def __init__(self, stack, gadMap={}, buildingMap={}):
        """

        @param stack: KNX stack object
        @type stack: L{Stack<pknyx.stack.stack>}

        raise ETSValueError:
        """
        super(ETS, self).__init__()

        self._stack = stack
        self._gadMap = gadMap
        self._buildingMap = buildingMap

        self._functionalBlocks = set()

    @property
    def stack(self):
        return self._stack

    @property
    def functionalBlockNames(self):
        return [fb.name for fb in self._functionalBlocks]

    @property
    def datapoints(self):
        dps = []
        for fb in self._functionalBlocks:
            dps.append(fb.dp.values())

        return dps

    @property
    def gadMap(self):
        return self._gadMap

    @gadMap.setter
    def gadMap(self, gadMap):
        self._gadMap = gadMap

    @property
    def buildingMap(self):
        return self._buildingMap

    @gadMap.setter
    def buildingMap(self, buildingMap):
        self._gadMap = buildingMap

    def register(self, cls, name, desc=None, building='root'):
        """ Register a functional block

        @param cls: class of functional block to register
        @type cls: subclass of L{FunctionalBlocks<pknyx.core.functionalBlocks>}
        """
        for fb in self._functionalBlocks:
            if name == fb.name:
                raise ETSValueError("functional block already registered (%s)" % fb)

        # Instanciate the function block
        fb = cls(name=name, desc=desc)

        self._functionalBlocks.add(fb)

        # Also register pending scheduler jobs
        Scheduler().registerJobs(fb)


    def link(self, fb, dp, gad):
        """ Link a datapoint to a GAD

        @param fb: name of the functional block owning the datapoint
        @type fb: str

        @param dp: name of the datapoint to link
        @type dp: str

        @param gad : group address to link to
        @type gad : str or L{GroupAddress}

        raise ETSValueError:
        """
        for fb_ in self._functionalBlocks:
            if fb == fb_.name:
                break
        else:
            raise ETSValueError("unregistered functional block (%s)" % fb)

        # Retreive GroupObject from FunctionalBlock
        groupObject = fb_.go[dp]

        # Get GroupAddress
        if not isinstance(gad, GroupAddress):
            gad = GroupAddress(gad)

        # Ask the group data service to subscribe this GroupObject to the given gad
        # In return, get the created group
        group = self._stack.gds.subscribe(gad, groupObject)

        # If not already done, set the GroupObject group. This group will be used when the GroupObject wants to
        # communicate on the bus. This mimics the S flag of ETS real application
        # @todo: find a better way
        if groupObject.group is None:
            groupObject.group = group

    weave = link

    def printMapTable(self, by="gad", outFormatLevel=3):
        """
        """

        # Retreive all bound gad
        gads = []
        for gad in self._stack.gds.groups.keys():
            gads.append(GroupAddress(gad, outFormatLevel=outFormatLevel))
        gads.sort()

        if by == "gad":
            print "Ordered by GroupAddress:\n"
            title = "%-35s %-25s %-30s %-10s %-10s %-10s" % ("GAD", "Datapoint", "Functional block", "DPTID", "Flags", "Priority")
            print title
            print len(title) * "-"
            gadMain = gadMiddle = gadSub = -1
            for gad in gads:
                if gadMain != gad.main:
                    index = "%d" % gad.main
                    if self._gadMap.has_key(index):
                        print u"%2d %-33s" % (gad.main, self._gadMap[index]['desc'].decode("utf-8"))
                    else:
                        print u"%2d %-33s" % (gad.main, "")
                    gadMain = gad.main
                    gadMiddle = gadSub = -1
                if gadMiddle != gad.middle:
                    index = "%d/%d" % (gad.main, gad.middle)
                    if self._gadMap.has_key(index):
                        print u" ├── %2d %-27s" % (gad.middle, self._gadMap[index]['desc'].decode("utf-8"))
                    else:
                        print u" ├── %2d %-27s" % (gad.middle, "")
                    gadMiddle = gad.middle
                    gadSub = -1
                if gadSub != gad.sub:
                    index = "%d/%d/%d" % (gad.main, gad.middle, gad.sub)
                    if self._gadMap.has_key(index):
                        print u" │    ├── %3d %-21s" % (gad.sub, self._gadMap[index]['desc'].decode("utf-8")),
                    else:
                        print u" │    ├── %3d %-21s" % (gad.sub, ""),
                    gadSub = gad.sub

                for i, go in enumerate(self._stack.gds.groups[gad.address].listeners):
                    dp = go.datapoint
                    fb = dp.owner
                    if not i:
                        print u"%-25s %-30s %-10s %-10s %-10s" % (dp.name, fb.name, dp.dptId, go.flags, go.priority)
                    else:
                        print u" │    │                             %-25s %-30s %-10s %-10s %-10s" % (dp.name, fb.name, dp.dptId, go.flags, go.priority)

                gad_ = gad

        elif by == "go":

            # Retreive all groupObjects, not only bound ones
            # @todo: use building presentation
            mapByDP = {}
            print "Ordered by GroupObject:\n"
            title = "%-30s %-25s %-10s %-30s %-10s %-10s" % ("Functional block", "Datapoint", "DPTID", "GAD", "Flags", "Priority")
            print title
            print len(title) * "-"
            for fb in self._functionalBlocks:
                #print "%-30s" % fb.name,
                for i, go in enumerate(fb.go.values()):
                    print "%-30s" % fb.name,
                    dp = go.datapoint
                    #if i:
                        #print "%-30s" % "",
                    gads_ = []
                    for gad in gads:
                        if go in self._stack.gds.groups[gad.address].listeners:
                            gads_.append(gad.address)
                    if gads_:
                        print "%-25s %-10s %-30s %-10s %-10s" % (go.name, dp.dptId, ", ".join(gads_), go.flags, go.priority)
                    else:
                        print "%-25s %-10s %-30s %-10s %-10s" % (go.name, dp.dptId, "", go.flags, go.priority)

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
