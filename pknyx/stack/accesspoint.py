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

 - B{Accesspoint}

Documentation
=============

B{Accesspoint} are used by L{Datapoint<pknyx.core.datapoint>} to communicate over the bus using group data service.

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


class AccesspointValueError(PKNyXValueError):
    """
    """


class Accesspoint(object):
    """ Accesspoint class

    @ivar _group: group that access poit belong to
    @type _group: L{Group}
    """
    def __init__(self, group):
        """

        @param group: group that access poit belong to
        @type group: L{Group}

        raise AccesspointValueError:
        """
        super(Accesspoint, self).__init__()

        if not isinstance(Group, group):
            raise("invalid group (%r)" % repr(group))
        self._group = group

    def groupValueWrite(self, src, priority, data):
        """ Write data request on the GAD associated with this group
        """
        self._group.groupValueWrite(src, priority, data)

    def groupValueRead(self, src, priority):
        """ Read data request on the GAD associated with this group
        """
        self._group.groupValueRead(src, priority)

    def groupValueResponse(self, src, priority):
        """ Read data response on the GAD associated with this group
        """
        self._group.groupValueResponse(src, priority)


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class AccesspointTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
