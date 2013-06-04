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

 - B{GroupDataListenerValueError}
 - B{GroupDataListener}

Documentation
=============

The B{GroupDataListener} class is the base class for group data listeners, which are called when group data
events occurs on KNX bus (real or virtual one).

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger


class GDListenerValueError(PKNyXValueError):
    """
    """


class GroupDataListener(object):
    """ Group data listener class
    """
    def __init__(self, parent):
        """ Init group data listener object
        """
        super(GroupDataListener, self).__init__()

    def onGroupWrite(self, srcGad, data):
        """  Group write callback

        @param srcGAD : source Group Address
        @type srcGAD : L{GroupAddress}

        @param data: data received
        @type data: bytearray
        """
        raise NotImplementedError

    def onGroupRead(self, srcGad):
        """ Group read callback

        @param srcGAD : source Group Address
        @type srcGAD : L{GroupAddress}
        """
        raise NotImplementedError

    def onGroupResponse(self, srcGad, data):
        """ Group response

        @param srcGAD : source Group Address
        @type srcGAD : L{GroupAddress}

        @param data: data received
        @type data: bytearray
        """
        raise NotImplementedError


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class GDListenerTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
