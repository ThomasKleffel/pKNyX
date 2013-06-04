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

Device management

Implements
==========

 - B{Device}

Documentation
=============

B{Device} is one of the most important object of B{pKNyX} framework, after L{Datapoint}.
A device contains one or more Datapoints, to form a high level entity. It can represents a real device, and act as
a KNX gateway for that device, or

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id: template.py 61 2013-05-30 06:17:47Z fma $"

from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger


class DeviceValueError(PKNyXValueError):
    """
    """


class Device(object):
    """ Device class

    @ivar :
    @type :
    """
    def __init__(self):
        """

        @param :
        @type :

        raise DeviceValueError:
        """
        super(Device, self).__init__()


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class DeviceTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
