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

Application layer group data management

Implements
==========

 - B{A_GroupDataService}

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


class A_GDSValueError(PKNyXValueError):
    """
    """


class A_GroupDataService(object):
    """ A_GroupDataService class
    """
    def __init__(self):
        """

        raise A_GDSValueError:
        """
        super(A_GroupDataService, self).__init__()

    def groupValueWriteReq(self, src, gad, priority, data):
        """
        """
        Logger().debug("A_GroupDataService.groupValueWriteReq(): src=%s, gad=%s, priority=%s, data=%s" % \
                       (repr(src), repr(gad), repr(priority), repr(data)))

    def groupValueReadReq(self, src, gad, priority):
        """
        """
        Logger().debug("A_GroupDataService.groupValueReadReq(): src=%s, gad=%s, priority=%s" % \
                       (repr(src), repr(gad), repr(priority)))

    def groupValueReadRes(self, src, gad, priority, data):
        """
        """
        Logger().debug("A_GroupDataService.groupValueReadRes(): src=%s, gad=%s, priority=%s, data=%s" % \
                       (repr(src), repr(gad), repr(priority), repr(data)))


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class A_GDSTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
