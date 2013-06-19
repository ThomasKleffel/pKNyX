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

 - B{Transceiver}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id: apdu.py 95 2013-06-14 14:18:16Z fma $"

from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger


class Transceiver(object):
    """
    """
    OVERHEAD = 2

    def __init__(self, tLSAP, da, ia):
        """
        """
        super(Transceiver, self).__init__()

        self._tLSAP = tLSAP
        self._domainAddress = da
        self._individualAddress = ia

    def cleanup(self):
        raise NotImplementedError

    @property
    def domainAddress(self):
        return self._domainAddress

    @property
    def individualAddress(self):
        return self._individualAddress

    def addGroupAddress(self, gad, sendL2Ack):
        raise NotImplementedError

    def removeGroupAddress(self, gad):
        raise NotImplementedError


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class TransceiverTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
