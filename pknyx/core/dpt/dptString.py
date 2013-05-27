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

Datapoint Types management.

Implements
==========

 - B{DPTString}

Usage
=====

see L{DPTBoolean}

Note
====

KNX century encoding is as following:

 - if byte year >= 90, then real year is 20th century year
 - if byte year is < 90, then real year is 21th century year

Python time module does not encode century the same way:

 - if byte year >= 69, then real year is 20th century year
 - if byte year is < 69, then real year is 21th century year

The DPTString class follows the python encoding.

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import struct

from pknyx.common.loggingServices import Logger
from pknyx.core.dpt.dptId import DPTID
from pknyx.core.dpt.dpt import DPT_, DPT, DPTValueError


class DPTString(DPT):
    """ DPT class for String (A112) KNX Datapoint Type

     - 14 Byte: AAAAAAAA ... AAAAAAAA
     - A: Char [0:255]

    .
    """
    DPT_Generic = DPT_("16.xxx", "Generic", (0, 5192296858534827628530496329220095))

    DPT_String_ASCII = DPT_("16.000", "String", (14 * (0,), 14 * (127,)))
    DPT_String_8859_1 = DPT_("16.001", "String", (14 * (0,), 14 * (255,)))

    def _checkData(self, data):
        if not 0x0000000000000000000000000000 <= data <= 0xffffffffffffffffffffffffffff:
            raise DPTValueError("data %s not in (0x0000000000000000000000000000, 0xffffffffffffffffffffffffffff)" % hex(data))

    def _checkValue(self, value):
        for index in range(14):
            if not self._handler.limits[0][index] <= value[index] <= self._handler.limits[1][index]:
                raise DPTValueError("value not in range %r" % repr(self._handler.limits))

    def _toValue(self):
        value = tuple([int((self._data >> shift) & 0xff) for shift in range(104, -1, -8)])
        #Logger().debug("DPTString._toValue(): value=%d" % value)
        return value

    def _fromValue(self, value):
        data = 0x00
        for shift in range(104, -1, -8):
            data |= value[13 - shift / 8] << shift
        #Logger().debug("DPTString._fromValue(): data=%s" % hex(data))
        self._data = data

    def _toStrValue(self):
        s = "".join([chr(c) for c in self.value])
        s = s.rstrip('\x00')  # Remove trailing null chars
        return s

    def _fromStrValue(self, strValue):
        strValue = strValue.ljust(14, '\x00')  # Complete with null chars
        value = [ord(c) for c in strValue]
        self.value = value

    def _toFrame(self):
        return struct.pack(">14B", *self.value)

    def _fromFrame(self, frame):
        value = struct.unpack(">14B", frame)
        self.value = value

    @property
    def day(self):
        return self.value[0]

    @property
    def month(self):
        return self.value[1]

    @property
    def year(self):
        return self.value[2]


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')

    class DPTStringTestCase(unittest.TestCase):

        def setUp(self):
            self.testTable = (
                (14 * (0,),                                            0x0000000000000000000000000000, 14 * "\x00"),
                ((48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 0, 0, 0, 0), 0x3031323334353637383900000000, "0123456789\x00\x00\x00\x00"),
                (14 * (255,),                                          0xffffffffffffffffffffffffffff, 14 * "\xff"),
            )
            self.dpt = DPTString("16.001")

        def tearDown(self):
            pass

        #def test_constructor(self):
            #print self.dpt.handledDPTIDs

        #def test_checkValue(self):
            #with self.assertRaises(DPTValueError):
                #self.dpt._checkValue((0, 1, 1969))

        def test_toValue(self):
            for value, data, frame in self.testTable:
                self.dpt.data = data
                value_ = self.dpt.value
                self.assertEqual(value_, value, "Conversion failed (converted value for %s is %s, should be %s)" %
                                 (hex(data), value_, value))

        def test_fromValue(self):
            for value, data, frame in self.testTable:
                self.dpt.value = value
                data_ = self.dpt.data
                self.assertEqual(data_, data, "Conversion failed (converted data for %s is %s, should be %s)" %
                                 (value, hex(data_), hex(data)))

        def test_toFrame(self):
            for value, data, frame in self.testTable:
                self.dpt.data = data
                frame_ = self.dpt.frame
                self.assertEqual(frame_, frame, "Conversion failed (converted frame for %s is %r, should be %r)" %
                                 (hex(data), frame_, frame))

        def test_fromFrame(self):
            for value, data, frame in self.testTable:
                self.dpt.frame = frame
                data_ = self.dpt.data
                self.assertEqual(data_, data, "Conversion failed (converted data for %r is %s, should be %s)" %
                                 (frame, hex(data_), hex(data)))

    unittest.main()
