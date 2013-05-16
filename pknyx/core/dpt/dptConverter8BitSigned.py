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

 - B{DPTConverter8BitSigned}

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


def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


class DPTConverter8BitSigned(DPTConverterBase):
    """ DPT converter class for 8-Bit-Signed (V8) KNX Datapoint Type

     - 1 Byte: VVVVVVVV
     - V: Byte [-128:127]

    .
    """
    DPT_Generic = DPT("6.xxx", "Generic", (-128, 127))

    DPT_Percent_V8 = DPT("6.001", "Percent (8 bit)", (-128, 127), "%")
    DPT_Value_1_Count = DPT("6.010", "Signed count", (-128, 127), "pulses")
    #DPT_Status_Mode3 = DPT("6.020", "Status mode 3", (, ))

    def _checkData(self, data):
        if not 0x00 <= data <= 0xff:
            raise DPTConverterValueError("data %s not in (0x00, 0xff)" % hex(data))

    def _checkValue(self, value):
        if not self._dpt.limits[0] <= value <= self._dpt.limits[1]:
            raise DPTConverterValueError("value not in range %r" % repr(self._dpt.limits))

    def _toValue(self):
        if self._data >= 0x80:
            value = -((self._data - 1) ^ 0xff)  # invert twos complement
        else:
            value = self._data
        #Logger().debug("DPTConverter8BitSigned._toValue(): value=%d" % value)
        return value

    def _fromValue(self, value):
        if value < 0:
            value = (abs(value) ^ 0xff) + 1  # twos complement
        data = value
        #Logger().debug("DPTConverter8BitSigned._fromValue(): data=%s" % hex(data))
        self._data = data

    def _toStrValue(self):
        s = "%d" % self.value

        # Add unit
        if self._displayUnit and self._dpt.unit is not None:
            try:
                s = "%s %s" % (s, self._dpt.unit)
            except TypeError:
                Logger().exception("DPTConverter8BitSigned._toStrValue()", debug=True)
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

    class DPTConverter8BitSignedTestCase(unittest.TestCase):

        def setUp(self):
            self.testTable = (
                (-128, 0x80, "\x80"),
                (  -4, 0xfc, "\xfc"),
                (  -1, 0xff, "\xff"),
                (   0, 0x00, "\x00"),
                (   1, 0x01, "\x01"),
                ( 127, 0x7f, "\x7f"),
            )
            self.conv = DPTConverter8BitSigned("6.xxx")

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
