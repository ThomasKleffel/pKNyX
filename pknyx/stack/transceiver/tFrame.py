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

Frame management

Implements
==========

 - B{TFrame}

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
from pknyx.services.loggingServices import Logger
from pknyx.stack.transceiver.transceiver import Transceiver


class TFrameValueError(PKNyXValueError):
    """
    """


class TFrame(object):
    """ TFrame class
    """
    L2_START = Transceiver.OVERHEAD

    LTP_BYTE  = L2_START
    LTP_MASK  = 0x80
    LTP_BYTES = 0x80
    LTP_TABLE = 0x00
    CF_BYTE   = L2_START
    CF_MASK   = 0x73
    CF_L_DATA = 0x10
    CF_L_POLL = 0x50
    PR_BYTE   = L2_START
    PR_MASK   = 0x0c
    PR_SYSTEM = 0x00
    PR_NORMAL = 0x08
    PR_URGENT = 0x04
    PR_LOW    = 0x0c
    PR_CODE = (PR_SYSTEM, PR_NORMAL, PR_URGENT, PR_LOW)

    SAH_BYTE = L2_START + 1
    SAL_BYTE = L2_START + 2
    DAH_BYTE = L2_START + 3
    DAL_BYTE = L2_START + 4

    DAF_BYTE   = L2_START + 5
    DAF_MASK   = 0x80
    DAF_IA     = 0x00
    DAF_GAD    = 0x80
    HC_BYTE    = L2_START + 5
    HC_MASK    = 0x70
    HC_BITPOS  = 4
    LEN_BYTE   = L2_START + 5
    LEN_MASK   = 0x0f
    LEN_BITPOS = 0

    TPCI_BYTE  = L2_START + 6
    APDU_START = L2_START + 6

    MIN_LENGTH = L2_START + 7
    MAX_LENGTH = MIN_LENGTH + 244

    LEN_TAB = (16, 17, 18, 19, 20, 22, 25, 29, 34, 40, 80, 120, 160, 200, 244)

    def __init__(self):
        """

        @param :
        @type :

        raise TFrameValueError:
        """
        super(TFrame, self).__init__()

    @classmethod
    def lenCode2Len(cls, lenCode):
        """
        """
        return LEN_TAB[lenCode]

    @classmethod
    def len2LenCode(cls, length):
        """
        """
        code = 0
        while length > LEN_TAB[code]:
            code += 1

        return code

    @classmethod
    def create(cls, length):
        """
        """
        if length > 15:
            code = 0
            while length > LEN_TAB[code]:
                code += 1
            length = LEN_TAB[code]

        return bytearray(TFrame.MIN_LENGTH + length)


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class TFrameTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
