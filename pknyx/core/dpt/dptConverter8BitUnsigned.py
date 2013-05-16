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

 - B{DPTConverter8BitUnsigned}

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


class DPTConverter8BitUnsigned(DPTConverterBase):
    """ DPT converter class for 8-Bit-Unsigned (U8) KNX Datapoint Type

     - 1 Byte: UUUUUUUU
     - U: Byte [0:255]

    .
    """
    DPT_Generic = DPT("5.xxx", "Generic", (0, 255))

    DPT_Scaling = DPT("5.001", "Scaling", (0, 100), "%")
    DPT_Angle = DPT("5.003", "Angle", (0, 360), "°")
    DPT_Percent_U8 = DPT("5.004", "Percent (8 bit)", (0, 255), "%")
    DPT_DecimalFactor = DPT("5.005", "Decimal factor", (0, 1), "ratio")
    #DPT_Tariff = DPT("5.006", "Tariff", (0, 254), "ratio")
    DPT_Value_1_Ucount = DPT("5.010", "Unsigned count", (0, 255), "pulses")

    def _checkData(self, data):
        if not 0x00 <= data <= 0xff:
            raise DPTConverterValueError("data %s not in (0x00, 0xff)" % hex(data))

    def _checkValue(self, value):
        if not self._dpt.limits[0] <= value <= self._dpt.limits[1]:
            raise DPTConverterValueError("value not in range %r" % repr(self._dpt.limits))

    def _toValue(self):
        value = self._data
        if self._dpt is self.DPT_Scaling:
            value = value * 100. / 255.
        elif self._dpt is self.DPT_Angle:
            value = value * 360. / 255.
        elif self._dpt is self.DPT_DecimalFactor:
            value = value / 255.
        #Logger().debug("DPTConverter8BitUnsigned._toValue(): value=%d" % value)
        return value

    def _fromValue(self, value):
        if self._dpt is self.DPT_Scaling:
            data = int(round(value * 255 / 100.))
        elif self._dpt is self.DPT_Angle:
            data = int(round(value * 255 / 360.))
        elif self._dpt is self.DPT_DecimalFactor:
            data = int(round(value * 255))
        else:
            data = value
        #Logger().debug("DPTConverter8BitUnsigned._valueToData(): data=%s" % hex(data))
        self._data = data

    def _toStrValue(self):
        if self._dpt in (self.DPT_Scaling, self.DPT_Angle):  #,self.DPT_DecimalFactor):
            s = "%.1f" % self.value
        elif self._dpt is self.DPT_DecimalFactor:
            s = "%.2f" % self.value
        else:
            s = "%d" % self.value

        # Add unit
        if self._displayUnit and self._dpt.unit is not None:
            try:
                s = "%s %s" % (s, self._dpt.unit)
            except TypeError:
                Logger().exception("DPTConverter8BitUnsigned._toStrValue()", debug=True)
        return s

    #def _fromStrValue(self, strValue):

    def _toFrame(self):
        return struct.pack(">B", self._data)

    def _fromFrame(self, frame):
        self._data = struct.unpack(">B", frame)[0]


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')

    class DPTConverter8BitUnsignedTestCase(unittest.TestCase):

        def setUp(self):
            self.testTable = (
                (  0, 0x00, "\x00"),
                (  1, 0x01, "\x01"),
                (255, 0xff, "\xff"),
            )
            self.conv = DPTConverter8BitUnsigned("5.xxx")

        def tearDown(self):
            pass

        #def test_constructor(self):
            #print self.conv.handledDPTIDs

        def test_checkValue(self):
            with self.assertRaises(DPTConverterValueError):
                self.conv._checkValue(self.conv._dpt.limits[1] + 1)

        def test_toValue(self):
            for value, data, frame in self.testTable:
                self.conv.data = data
                value_ = self.conv.value
                self.assertEqual(value_, value, "Conversion failed (converted value for %s is %d, should be %d)" %
                                 (hex(data), value_, value))

        def test_fromValue(self):
            for value, data, frame in self.testTable:
                self.conv.value = value
                data_ = self.conv.data
                self.assertEqual(data_, data, "Conversion failed (converted data for %d is %s, should be %s)" %
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
