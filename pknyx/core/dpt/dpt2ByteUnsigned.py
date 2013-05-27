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

 - B{DPT2ByteUnsigned}

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


class DPT2ByteUnsigned(DPT):
    """ DPT class for 2-Byte-Unsigned (U16) KNX Datapoint Type

      - 2 Byte Unsigned: UUUUUUUU UUUUUUUU
      - U: Bytes [0:65535]

    .
    """
    DPT_Generic = DPT_("7.xxx", "Generic", (0, 65535))

    DPT_Value_2_Ucount = DPT_("7.001", "Unsigned count", (0, 65535), "pulses")
    DPT_TimePeriodMsec = DPT_("7.002", "Time period (resol. 1ms)", (0, 65535), "ms")
    DPT_TimePeriod10Msec = DPT_("7.003", "Time period (resol. 10ms)", (0, 655350), "ms")
    DPT_TimePeriod100Msec = DPT_("7.004", "Time period (resol. 100ms)", (0, 6553500), "ms")
    DPT_TimePeriodSec = DPT_("7.005", "Time period (resol. 1s)", (0, 65535), "s")
    DPT_TimePeriodMin = DPT_("7.006", "Time period (resol. 1min)", (0, 65535), "min")
    DPT_TimePeriodHrs = DPT_("7.007", "Time period (resol. 1h)", (0, 65535), "h")
    DPT_PropDataType = DPT_("7.010", "Interface object property ID", (0, 65535))
    DPT_Length_mm = DPT_("7.011", "Length", (0, 65535), "mm")
    #DPT_UEICurrentmA = DPT("7.012", "Electrical current", (0, 65535), "mA")  # Add special meaning for 0 (create Limit object)
    DPT_Brightness = DPT_("7.013", "Brightness", (0, 65535), "lx")

    def _checkData(self, data):
        if not 0x0000 <= data <= 0xffff:
            raise DPTValueError("data %s not in (0x0000, 0xffff)" % hex(data))

    def _checkValue(self, value):
        if not self._handler.limits[0] <= value <= self._handler.limits[1]:
            raise DPTValueError("Value not in range %r" % repr(self._handler.limits))

    def _toValue(self):
        if self._handler is self.DPT_TimePeriod10Msec:
            value = self._data * 10.
        elif self._handler is self.DPT_TimePeriod100Msec:
            value = self._data * 100.
        else:
            value = self._data
        #Logger().debug("DPT2ByteUnsigned._toValue(): value=%d" % value)
        return value

    def _fromValue(self, value):
        if self._handler is self.DPT_TimePeriod10Msec:
            data = int(round(value / 10.))
        elif self._handler is self.DPT_TimePeriod100Msec:
            data = int(round(value / 100.))
        else:
            data = value
        #Logger().debug("DPT2ByteUnsigned._fromValue(): data=%s" % hex(data))
        self._data = data

    def _toStrValue(self):
        s = "%d" % self.value

        # Add unit
        if self._displayUnit and self._handler.unit is not None:
            try:
                s = "%s %s" % (s, self._handler.unit)
            except TypeError:
                Logger().exception("DPT2ByteUnsigned._toStrValue()", debug=True)
        return s

    #def _fromStrValue(self, strValue):

    def _toFrame(self):
        return struct.pack(">H", self._data)

    def _fromFrame(self, frame):
        self._data = struct.unpack(">H", frame)[0]


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')

    class DPT2ByteUnsignedTestCase(unittest.TestCase):

        def setUp(self):
            self.testTable = (
                (    0, 0x0000, "\x00\x00"),
                (    1, 0x0001, "\x00\x01"),
                (65535, 0xffff, "\xff\xff"),
            )
            self.dpt = DPT2ByteUnsigned("7.xxx")

        def tearDown(self):
            pass

        #def test_constructor(self):
            #print self.dpt.handledDPTIDs

        def test_checkValue(self):
            with self.assertRaises(DPTValueError):
                self.dpt._checkValue(self.dpt._handler.limits[1] + 1)

        def test_toValue(self):
            for value, data, frame in self.testTable:
                self.dpt.data = data
                value_ = self.dpt.value
                self.assertEqual(value_, value, "Conversion failed (converted value for %s is %d, should be %d)" %
                                 (hex(data), value_, value))

        def test_fromValue(self):
            for value, data, frame in self.testTable:
                self.dpt.value = value
                data_ = self.dpt.data
                self.assertEqual(data_, data, "Conversion failed (converted data for %d is %s, should be %s)" %
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
