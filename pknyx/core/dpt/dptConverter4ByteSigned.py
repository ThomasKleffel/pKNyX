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

Datapoint Types management

Implements
==========

 - B{DPT4ByteSigned}

Usage
=====

see L{DPTBoolean}

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import struct

from pknyx.common.loggingServices import Logger
from pknyx.core.dpt.dptId import DPTID
from pknyx.core.dpt.dpt import DPT_, DPT, DPTValueError


class DPT4ByteSigned(DPT):
    """ DPT class for 4-Byte-Signed (V32) KNX Datapoint Type

     - 4 Byte Signed: VVVVVVVV VVVVVVVV VVVVVVVV VVVVVVVV
     - V: Bytes [-2147483648:2147483647]

    .
    """
    DPT_Generic = DPT_("13.xxx", "Generic", (-2147483648, 2147483647))

    DPT_Value_4_Count = DPT_("13.001", "Signed count", (-2147483648, 2147483647), "pulses")
    DPT_Value_FlowRate_m3h = DPT_("13.001", "Flow rate", (-214748.3648, 214748.3647), "m³/h")
    DPT_ActiveEnergy = DPT_("13.010", "Active energy", (-214748.3648, 214748.3647), "W.h")
    DPT_ApparentEnergy = DPT_("13.011", "Apparent energy", (-214748.3648, 214748.3647), "VA.h")
    DPT_ReactiveEnergy = DPT_("13.012", "Reactive energy", (-214748.3648, 214748.3647), "VAR.h")
    DPT_ActiveEnergy_kWh = DPT_("13.013", "Active energy (kWh)", (-214748.3648, 214748.3647), "kW.h")
    DPT_ApparentEnergy_kVAh = DPT_("13.014", "Apparent energy (kVAh)", (-214748.3648, 214748.3647), "kVA.h")
    DPT_ReactiveEnergy_KVARh = DPT_("13.015", "Reactive energy (kVARh)", (-214748.3648, 214748.3647), "kVAR.h")
    DPT_LongDeltaTimeSec = DPT_("13.100", "Long delta time", (-214748.3648, 214748.3647), "s")

    def _checkData(self, data):
        if not 0x00000000 <= data <= 0xffffffff:
            raise DPTValueError("data %s not in (0x00000000, 0xffffffff)" % hex(data))

    def _checkValue(self, value):
        if not self._handler.limits[0] <= value <= self._handler.limits[1]:
            raise DPTValueError("Value not in range %r" % repr(self._handler.limits))

    def _toValue(self):
        if self._data >= 0x80000000:
            data = -((self._data - 1) ^ 0xffffffff)  # invert twos complement
        else:
            data = self._data
        if self._handler is self.DPT_Value_FlowRate_m3h:
            value = data / 10000.
        else:
            value = data
        #Logger().debug("DPT4ByteSigned._toValue(): value=%d" % value)
        return value

    def _fromValue(self, value):
        if value < 0:
            value = (abs(value) ^ 0xffffffff) + 1  # twos complement
        if self._handler is self.DPT_Value_FlowRate_m3h:
            data = int(round(value * 10000.))
        else:
            data = value
        #Logger().debug("DPT4ByteSigned._fromValue(): data=%s" % hex(data))
        self._data = data

    def _toFrame(self):
        return struct.pack(">L", self._data)

    def _fromFrame(self, frame):
        self._data = struct.unpack(">L", frame)[0]

    def _toStrDPT(self):
        if self._handler is self.DPT_Value_FlowRate_m3h:
            s = "%.4f" % self.value
        else:
            s = "%d" % self.value

        # Add unit
        if self._displayUnit and self._handler.unit is not None:
            try:
                s = "%s %s" % (s, self._handler.unit)
            except TypeError:
                Logger().exception("DPT4ByteSigned", debug=True)
        return s

    #def _fromStrDPT(self, strValue):


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')

    class DPT4ByteSignedTestCase(unittest.TestCase):

        def setUp(self):
            self.testTable = (
                (-2147483648, 0x80000000, "\x80\x00\x00\x00"),
                (         -4, 0xfffffffc, "\xff\xff\xff\xfc"),
                (         -1, 0xffffffff, "\xff\xff\xff\xff"),
                (          0, 0x00000000, "\x00\x00\x00\x00"),
                (          1, 0x00000001, "\x00\x00\x00\x01"),
                ( 2147483647, 0x7fffffff, "\x7f\xff\xff\xff"),
            )
            self.conv = DPT4ByteSigned("13.xxx")

        def tearDown(self):
            pass

        #def test_constructor(self):
            #print self.conv.handledDPTIDs

        def test_checkValue(self):
            with self.assertRaises(DPTValueError):
                self.conv._checkValue(self.conv._handler.limits[1] + 1)

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
