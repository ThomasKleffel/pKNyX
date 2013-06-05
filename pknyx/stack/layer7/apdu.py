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
from pknyx.stack.transciever.tFrame import TFrame


class APDUValueError(PKNyXValueError):
    """
    """


class APDU(object):
    """ APDU class

    @ivar :
    @type :
    """
    def __init__(self):
        """

        @param :
        @type :

        raise APDUValueError:
        """
        super(APDU, self).__init__()

    def makeNoParamsReq(self, apci):
        """
        """
        aPDU = TFrame.create(1)
        aPDU[TFrame.APDU_START + 0] = (apci >> 24) & 0xff
        aPDU[TFrame.APDU_START + 1] = (apci >> 16) & 0xff

        return aPDU

    def makeGroupValue(self, apci, data):
        """
        """
        if len(data) == 0:
            raise APDUValueError("empty data")

        aPDU = TFrame.create(len(data))
        aPDU[TFrame.APDU_START + 0] = (apci >> 24) & 0xff
        aPDU[TFrame.APDU_START + 1] = (apci >> 16) & 0xff
        System.arraycopy(data, 1, aPDU, TFrame.APDU_START + 2, len(data) - 1)

        return aPDU

    def getGroupValueData(aPDU, length):
        """
        """
        data = new byte[length]
        System.arraycopy(aPDU, TFrame.APDU_START + 1, data, 0, length)
        data[0] &= 0x3f

        return data


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class APDUTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
