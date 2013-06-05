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

Group data management

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
from pknyx.stack.groupAddress import GroupAddress
from pknyx.stack.groupDataListener import GroupDataListener


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
    @type _listeners: list of L{GroupDataListener}
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

        if not isinstance(GroupAddress, gad):
            gad = GroupAddress(gad)
        self._gad = gad

        if not isinstance(GroupDataListener, gds):
            raise GroupValueError("invalid group data listener (%s)" % repr(gds))

        self._listeners = set()

    def createAP(self, listener):
        """ Create an accesspoint to communicate with this group

        The given listener is also added to the listenders binded with the GAD handled by this group.

        @param listener: Listener
        @type listener: L{GroupDataListener}
        """
        if not issubclass(GroupDataListener, listener):
            raise GroupValueError("invalid listener (%s)" % repr(listener))

        self._listeners.add(listener)

        return Acesspoint(listener)

    def write(self, src, priority, data):
        """ Write data request on the GAD associated with this group
        """
        gds.agds.groupValue_writeReq(src, self._gad, priority, data)

    def read(self, src, priority):
        """ Read data request on the GAD associated with this group
        """
        gds.agds.groupValue_readReq(src, self._gad, priority)

    def onWrite(self, src, data):
        """ Callback for write requests

        @param src: individual address of the source device which sent the write request
        @type src: L{IndividualAddress}

        @param data: data associated with this request
        @type data: bytearray
        """
        for listener in self._listeners:
            try:
                listener.onGroupWrite(src, self._gad, data)
            except:
                Logger().exception("Group.onWrite()")

    def onRead(self, src):
        """ Callback for read requests

        @param src: individual address of the source device which sent the read request
        @type src: L{IndividualAddress}
        """
        for listener in self._listeners:
            try:
                data = listener.onGroupRead(src, self._gad)
                if data is not None:
                    gds.agds.groupValue_readRes(src, self._gad, listener.priority, data)
            except:
                Logger().exception("Group.onRead()")

    def onResponse(self, src, data):
        """ Callback for read response result

        @param src: individual address of the source device which sent the read result
        @type src: L{IndividualAddress}

        @param data: data associated with this result
        @type data: bytearray
        """
        for listener in self._listeners:
            try:
                listener.onGroupResponse(src, self._gad, data)
            except:
                Logger().exception("Group.onResponse()")


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class GroupTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
