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

 - B{DPTDate}

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

The DPTDate class follows the python encoding.

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import struct

from pknyx.common.loggingServices import Logger
from pknyx.core.dpt.dptId import DPTID
from pknyx.core.dpt.dpt import DPT_, DPT, DPTValueError


class DPTDate(DPT):
    """ DPT class for Date (r3U5r4U4r1U7) KNX Datapoint Type

     - 3 Byte: rrrDDDDD rrrrMMMM rYYYYYYY
     - D: Day [1:31]
     - M: Month [1:12]
     - Y: Year [0:99]
     - r: reserved (0)

    .
    """
    DPT_Generic = DPT_("11.xxx", "Generic", (0, 16777215))

    DPT_Date = DPT_("11.001", "Date", ((1, 1, 1969), (31, 12, 2068)))

    def _checkData(self, data):
        if not 0x000000 <= data <= 0xffffff:
            raise DPTValueError("data %s not in (0x000000, 0xffffff)" % hex(data))

    def _checkValue(self, value):
        for index in range(3):
            if not self._handler.limits[0][index] <= value[index] <= self._handler.limits[1][index]:
                raise DPTValueError("value not in range %r" % repr(self._handler.limits))

    def _toValue(self):
        day = (self._data >> 16) & 0x1f
        month = (self._data >> 8) & 0x0f
        year = self._data & 0x7f
        if year >= 69:
            year += 1900
        else:
            year += 2000
        value = (day, month, year)
        #Logger().debug("DPTDate._toValue(): value=%d" % value)
        return value

    def _fromValue(self, value):
        day = value[0]
        month = value[1]
        year = value[2]
        if year >= 2000:
            year -= 2000
        else:
            year -= 1900
        data = day << 16 | month << 8 | year
        #Logger().debug("DPTDate._fromValue(): data=%s" % hex(data))
        self._data = data

    def _toStrValue(self):
        day = value[0]
        month = value[1]
        year = value[2]
        s = time.strftime("%Y-%m-%d", (year, month, day, 0, 0, 0, 0, 0, 0))
        return s

    #def _fromStrValue(self, strValue):

    def _toFrame(self):
        data = [(self._data >> shift) & 0xff for shift in range(16, -1, -8)]
        return struct.pack(">3B", *data)

    def _fromFrame(self, frame):
        data = struct.unpack(">3B", frame)
        self._data = data[0] << 16 | data[1] << 8 | data[2]

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

    class DPTDateTestCase(unittest.TestCase):

        def setUp(self):
            self.testTable = (
                (( 1,  1, 2000), 0x010100, "\x01\x01\x00"),
                (( 1,  1, 2068), 0x010144, "\x01\x01\x44"),
                (( 1,  1, 1969), 0x010145, "\x01\x01\x45"),
                ((31, 12, 1999), 0x1f0c63, "\x1f\x0c\x63"),
            )
            self.conv = DPTDate("11.001")

        def tearDown(self):
            pass

        #def test_constructor(self):
            #print self.conv.handledDPTIDs

        def test_checkValue(self):
            with self.assertRaises(DPTValueError):
                self.conv._checkValue((0, 1, 1969))
            with self.assertRaises(DPTValueError):
                self.conv._checkValue((1, 0, 1969))
            with self.assertRaises(DPTValueError):
                self.conv._checkValue((1, 1, 1968))

            with self.assertRaises(DPTValueError):
                self.conv._checkValue((32, 12, 2068))
            with self.assertRaises(DPTValueError):
                self.conv._checkValue((31, 13, 2068))
            with self.assertRaises(DPTValueError):
                self.conv._checkValue((31, 12, 2069))

        def test_toValue(self):
            for value, data, frame in self.testTable:
                self.conv.data = data
                value_ = self.conv.value
                self.assertEqual(value_, value, "Conversion failed (converted value for %s is %s, should be %s)" %
                                 (hex(data), value_, value))

        def test_fromValue(self):
            for value, data, frame in self.testTable:
                self.conv.value = value
                data_ = self.conv.data
                self.assertEqual(data_, data, "Conversion failed (converted data for %s is %s, should be %s)" %
                                 (value, hex(data_), hex(data)))

        def test_toFrame(self):
            for value, data, frame in self.testTable:
                self.conv.data = data
                frame_ = self.conv.frame
                self.assertEqual(frame_, frame, "Conversion failed (converted frame for %s is %r, should be %r)" %
                                 (hex(data), frame_, frame))

        def test_fromFrame(self):
            for value, data, frame in self.testTable:
                self.conv.frame = frame
                data_ = self.conv.data
                self.assertEqual(data_, data, "Conversion failed (converted data for %r is %s, should be %s)" %
                                 (frame, hex(data_), hex(data)))

    unittest.main()
