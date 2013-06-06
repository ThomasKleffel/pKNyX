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

Group data service management

Implements
==========

 - B{GroupDataService}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger
from pknyx.stack.group import Group
from pknyx.core.groupAddress import GroupAddress
from pknyx.core.layer7.a_groupDataListener import A_GroupDataListener


class GDSValueError(PKNyXValueError):
    """
    """


class GroupDataService(A_GroupDataListener):
    """ GroupDataService class

    @ivar _agds: Application group data service object
    @type _agds: L{A_GroupDataService}

    @ivar _groups: Groups managed
    @type _groups: set of L{Group}
    """
    def __init__(self, agds):
        """

        @param agds: Application group data service object
        @type agds: L{A_GroupDataService}

        raise GDSValueError:
        """
        super(GroupDataService, self).__init__()

        self._agds = agds
        self._groups = {}

    def groupValueWriteInd(self, src, gad, data, priority):
        """
        """
        Logger().debug("GroupDataService.groupValueWriteInd(): src=%s, gad=%s, data=%s, priority=%s" % \
                       (repr(src), repr(gad), repr(data), repr(priority)))
        try:
            group = self._group[gad]
            group.onGroupValueWrite(src, data)
        except KeyError:
            Logger().exception("GroupDataService.groupValueWriteInd()", debug=True)
            Logger().debug("GroupDataService.groupValueWriteInd(): no registered group for that GAD (%s)" % repr(gad))

    def groupValueReadInd(self, src, gad, priority):
        """
        """
        Logger().debug("GroupDataService.groupValueReadInd(): src=%s, gad=%s, priority=%s" % \
                       (repr(src), repr(gad), repr(priority)))
        try:
            group = self._group[gad]
            group.onGroupValueRead(src)
        except KeyError:
            Logger().exception("GroupDataService.groupValueReadInd()", debug=True)
            Logger().debug("GroupDataService.groupValueReadInd(): no registered group for that GAD (%s)" % repr(gad))

    def groupValueReadCon(self, src, gad, data, priority):
        """
        """
        Logger().debug("GroupDataService.groupValue_ReadCon(): src=%s, gad=%s, data=%s, priority=%s" % \
                       (repr(src), repr(gad), repr(data), repr(priority)))
        try:
            group = self._group[gad]
            group.onGroupValueResponse(src, data)
        except KeyError:
            Logger().exception("GroupDataService.groupValueReadCon()", debug=True)
            Logger().debug("GroupDataService.groupValueReadCon(): no registered group for that GAD (%s)" % repr(gad))

    @property
    def agds(self):
        return self._agds

    @property
    def groups(self):
        return self._groups

    def subscribe(self, gad, listener):
        """

        @param gad: Group address the listener wants to subscribe to
        @type gad : L{GroupAddress}

        @param listener: object to link to the GAD
        @type listener: L{GroupDataListener}
        """
        if not isinstance(GroupAddress, gad):
            gad = GroupAddress(gad)

        if not self._groups.has_key(gad):
            self._group[gad] = Group(gad, self)
        accesspoint = self._groups[gad].createAP(listener)

        return accesspoint


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class GDSTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
