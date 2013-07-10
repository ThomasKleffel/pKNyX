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
from pknyx.services.loggingServices import Logger


class GDLValueError(PKNyXValueError):
    """
    """


class GroupDataListener(object):
    """ Group data listener class
    """
    def __init__(self):
        """ Init group data listener object
        """
        super(GroupDataListener, self).__init__()

    def onGroupWrite(self, src, data):
        """ Callback for write requests

        @param src: individual address of the source device which sent the write request
        @type src: L{IndividualAddress<pknyx.core.individualAddress>}

        @param data: data associated with this request
        @type data: bytearray
        """
        raise NotImplementedError

    def onGroupRead(self, src):
        """ Callback for read requests

        @param src: individual address of the source device which sent the read request
        @type src: L{IndividualAddress<pknyx.core.individualAddress>}
        """
        raise NotImplementedError

    def onGroupResponse(self, src, data):
        """ Callback for read response indication

        @param src: individual address of the source device which sent the read result
        @type src: L{IndividualAddress<pknyx.core.individualAddress>}

        @param data: data associated with this result
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
