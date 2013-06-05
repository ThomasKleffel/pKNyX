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

Implements
==========

 - B{}

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
from pknyx.stack.layer7.a_groupDataListener import A_groupDataListener


class GDServiceValueError(PKNyXValueError):
    """
    """


class GroupDataService(A_GroupDataListener):
    """ Xxx class

    @ivar _agds: Application group data service object
    @type _agds: L{A_GroupDataService}
    """
    def __init__(self, agds):
        """

        @param agds: Application group data service object
        @type agds: L{A_GroupDataService}

        raise GDServiceValueError:
        """
        super(GroupDataService, self).__init__()

        self._agds = A_GroupDataService()


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class GDServiceTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
