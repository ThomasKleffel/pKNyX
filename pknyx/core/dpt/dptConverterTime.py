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

 - B{DPTConverterTime}

Usage
=====

see L{DPTConverterBoolean}

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import struct

from pknyx.common.loggingServices import Logger
from pknyx.core.dpt.dptId import DPTID
from pknyx.core.dpt.dpt import DPT
from pknyx.core.dpt.dptConverterBase import DPTConverterBase, DPTConverterValueError


class DPTConverterTime(DPTConverterBase):
    """ DPT converter class for Time (N3U5r2U6r2U6) KNX Datapoint Type

     - 3 Byte: NNNHHHHH rrMMMMMM rrSSSSSS
     - N: Week day [0:7]
     - H: Hour [0:23]
     - M: Minute [0:59]
     - S: Second [0:59]
     - r: reserved (0)

    .
    """
    DPT_Generic = DPT("10.xxx", "Generic", (0, 16777215))

    DPT_TimeOfDay = DPT("10.001", "Time of day", ((0, 0, 0, 0), (7, 23, 59, 59)))

    def _checkData(self, data):
        if not 0x000000 <= data <= 0xffffff:
            raise DPTConverterValueError("data %s not in (0x000000, 0xffffff)" % hex(data))

    def _checkValue(self, value):
        for index in range(4):
            if not self._dpt.limits[0][index] <= value[index] <= self._dpt.limits[1][index]:
                raise DPTConverterValueError("value not in range %r" % repr(self._dpt.limits))

    def _toValue(self):
        wDay = (self._data >> 21) & 0x07
        hour = (self._data >> 16) & 0x1f
        min_ = (self._data >> 8) & 0x3f
        sec = self._data & 0x3f
        value = (wDay, hour, min_, sec)
        #Logger().debug("DPTConverterTime._toValue(): value=%d" % value)
        return value

    def _fromValue(self, value):
        # add from string and from int (sec)?
        wDay = value[0]
        hour = value[1]
        min_ = value[2]
        sec = value[3]
        data = wDay << 21 | hour << 16 | min_ << 8 | sec
        #Logger().debug("DPTConverterTime._fromValue(): data=%s" % hex(data))
        self._data = data

    def _toFrame(self):
        data = [(self._data >> shift) & 0xff for shift in range(16, -1, -8)]
        return struct.pack(">3B", *data)

    def _fromFrame(self, frame):
        data = struct.unpack(">3B", frame)
        self._data = data[0] << 16 | data[1] << 8 | data[2]

    def _toStrValue(self):
        wDay = self.value[0]
        hour = self.value[1]
        min_ = self.value[2]
        sec = self.value[3]
        if wDay == 0:
            format_ = "%H:%M:%S"  # "No day, %H:%M:%S"
        else:
            format_ = "%a, %H:%M:%S"
        s = time.strftime(format_, (0, 0, 0, hour, min_, sec, wDay - 1, 0, 0))
        return s

    #def _fromStrValue(self, strValue):

    @property
    def weekDay(self):
        wDay = self.value[0]
        hour = self.value[1]
        min_ = self.value[2]
        sec = self.value[3]
        if wDay == 0:
            format_ = "No day"  # "No day, %H:%M:%S"
        else:
            format_ = "%a"
        s = time.strftime(format_, (0, 0, 0, hour, min_, sec, wDay - 1, 0, 0))
        return s

    @property
    def hour(self):
        return self.value[1]

    @property
    def minute(self):
        return self.value[2]

    @property
    def second(self):
        return self.value[3]


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')

    class DPTConverterTimeTestCase(unittest.TestCase):

        def setUp(self):
            self.testTable = (
                ((0,  0,  0,  0), 0x000000, "\x00\x00\x00"),
                ((1,  2,  3,  4), 0x220304, "\x22\x03\x04"),
                ((7, 23, 59, 59), 0xf73b3b, "\xf7\x3b\x3b"),
            )
            self.conv = DPTConverterTime("10.001")

        def tearDown(self):
            pass

        #def test_constructor(self):
            #print self.conv.handledDPTIDs

        def test_checkValue(self):
            with self.assertRaises(DPTConverterValueError):
                self.conv._checkValue((-1, 0, 0, 0))
            with self.assertRaises(DPTConverterValueError):
                self.conv._checkValue((0, -1, 0, 0))
            with self.assertRaises(DPTConverterValueError):
                self.conv._checkValue((0, 0, -1, 0))
            with self.assertRaises(DPTConverterValueError):
                self.conv._checkValue((0, 0, 0, -1))

            with self.assertRaises(DPTConverterValueError):
                self.conv._checkValue((8, 23, 59, 59))
            with self.assertRaises(DPTConverterValueError):
                self.conv._checkValue((7, 24, 59, 59))
            with self.assertRaises(DPTConverterValueError):
                self.conv._checkValue((7, 23, 60, 59))
            with self.assertRaises(DPTConverterValueError):
                self.conv._checkValue((7, 23, 59, 60))

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
