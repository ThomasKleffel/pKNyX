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

__revision__ = "$Id: template.py 61 2013-05-30 06:17:47Z fma $"

from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger
from pknyx.stack.groupDataListener import GroupDataListener


class GroupValueError(PKNyXValueError):
    """
    """


class Group(object):
    """ Group class

    @ivar _gad: Group address (GAD) identifying this group
    @type _gad: L{GroupAddress}

    @ivar _listeners: Listeners linked (binded) to the GAD
    @type _listeners: list of L{GroupDataListener}
    """
    def __init__(self):
        """ Init the Group object

        @param gad: Group address identifying this group
        @type gad: L{GroupAddress}

        raise GroupValueError:
        """
        super(Group, self).__init__()

    def groupValue_writeInd(self, srcGad, data):
        for listener in self._listeners:
            listener.onGroupWrite(srcGad, data)

    def groupValue_readInd(self, srcGad):
        for listener in self._listeners:
            data = listener.onGroupRead(srcGad)
            if data is not None:
                ags.groupValue_ReadRes(self._gad, data, listener.priority)

    def groupValue_readCon(self, srcGad, data):
        for listener in self._listeners:
            listener.onGroupResponse(srcGad, data)

    def createAP(self, listener):
        """ Create an accesspoint

        The given listener is also added to the listenders binded with the GAD handled by this group.

        @param listener: Listener
        @type listener: L{GroupDataListener}
        """
        if not issubclass(GroupDataListener, listener):
            raise GroupValueError("invalid listener (%s)" % repr(listener))

        return Acesspoint(listener)


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
