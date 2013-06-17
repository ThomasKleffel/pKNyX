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

 - B{Group}

Documentation
=============

A B{Group} object is identified by its L{GroupAddress}. It contains all listeners linked (binded) to this GAD.
Whenever group data events occur, they are sent to Group objects, which then dispatch them to all listeners.

Note that group data events may come from a real KNX bus or not.

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger
from pknyx.core.groupAddress import GroupAddress
from pknyx.core.accesspoint import Accesspoint


class GroupValueError(PKNyXValueError):
    """
    """


class Group(object):
    """ Group class

    @ivar _gad: Group address (GAD) identifying this group
    @type _gad: L{GroupAddress}

    @ivar _gds: Group data service object
    @type _gds: L{GroupDataService}

    @ivar _listeners: Listeners linked (binded) to the GAD
    @type _listeners: set of L{GroupDataListener<pknyx.core.groupDataListener>}
    """
    def __init__(self, gad, gds):
        """ Init the Group object

        @param gad: Group address identifying this group
        @type gad: L{GroupAddress}

        @param gds: Group data service object
        @type gds: L{GroupDataService}

        raise GroupValueError:
        """
        super(Group, self).__init__()

        if not isinstance(gad, GroupAddress):
            gad = GroupAddress(gad)
        self._gad = gad

        self._gds = gds

        self._listeners = set()

    def __repr__(self):
        return "<Group(%r)>" % self._gad

    def __str__(self):
        return "<Group(gad=\"%s\")>" % self._gad

    @property
    def gad(self):
        return self._gad

    @property
    def listeners(self):
        return self._listeners

    def createAP(self, listener):
        """ Create an accesspoint to communicate with this group

        The given listener is also added to the listenders bound with the GAD handled by this group.

        @param listener: Listener
        @type listener: L{GroupDataListener<pknyx.core.groupDataListener>}
        """
        self._listeners.add(listener)

        return Accesspoint(self)

    def groupValueWrite(self, src, data, priority):
        """ Write data request on the GAD associated with this group
        """
        gds.agds.groupValueWriteReq(src, self._gad, data, priority)

    def groupValueRead(self, src, priority):
        """ Read data request on the GAD associated with this group
        """
        gds.agds.groupValueReadReq(src, self._gad, priority)

    def groupValueResponse(self, src, data, priority):
        """ Response data request on the GAD associated with this group
        """
        gds.agds.groupValueReadRes(src, self._gad, data, priority)

    def onGroupValueWrite(self, src, data):
        """ Callback for write requests

        @param src: individual address of the source device which sent the write request
        @type src: L{IndividualAddress<pknyx.core.individualAddress>}

        @param data: data associated with this request
        @type data: bytearray
        """
        for listener in self._listeners:
            try:
                listener.onGroupValueWrite(src, self._gad, data)
            except:
                Logger().exception("Group.onGroupValueWrite()")

    def onGroupValueRead(self, src):
        """ Callback for read requests

        @param src: individual address of the source device which sent the read request
        @type src: L{IndividualAddress<pknyx.core.individualAddress>}
        """
        for listener in self._listeners:
            try:
                data = listener.onGroupValueRead(src, self._gad)
                if data is not None:
                    self._gds.agds.groupValueReadRes(src, self._gad, listener.priority, data)
            except:
                Logger().exception("Group.onGroupValueRead()")

    def onGroupValueResponse(self, src, data):
        """ Callback for read response indication

        @param src: individual address of the source device which sent the read result
        @type src: L{IndividualAddress<pknyx.core.individualAddress>}

        @param data: data associated with this result
        @type data: bytearray
        """
        for listener in self._listeners:
            try:
                listener.onGroupValueResponse(src, self._gad, data)
            except:
                Logger().exception("Group.onGroupValueResponse()")


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class GroupTestCase(unittest.TestCase):

        def setUp(self):
            self.group = Group("1/1/1", None)

        def tearDown(self):
            pass

        def test_display(self):
            print repr(self.group)
            print self.group

        def test_constructor(self):
            pass


    unittest.main()
