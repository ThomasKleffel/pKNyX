# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{pKNyX} (U{http://www.pknyx.org}) is Copyright:
  - (C) 2013 Frédéric Mantegazza

Licensed under the EUPL, Version 1.1 or - as soon they will be approved by
the European Commission - subsequent versions of the EUPL (the "Licence");
You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:

 - U{http://ec.europa.eu/idabc/eupl}

Unless required by applicable law or agreed to in writing, software distributed
under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.

See the Licence for the specific language governing permissions and limitations
under the Licence.

Module purpose
==============

Datapoint Types management

Implements
==========

 - B{DPTConverter2ByteUnsigned}

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


class DPTConverter2ByteUnsigned(DPTConverterBase):
    """ DPT converter class for 2-Byte-Unsigned (U16) KNX Datapoint Type

    G{classtree}

     - 2 Byte Unsigned: UUUUUUUU UUUUUUUU
     - U: Bytes [0:65535]
    """
    DPT_Generic = DPT("7.xxx", "Generic", (0, 65535))

    DPT_Value_2_Ucount = DPT("7.001", "Unsigned count", (0, 65535), "pulses")
    DPT_TimePeriodMsec = DPT("7.002", "Time period (resol. 1ms)", (0, 65535), "ms")
    DPT_TimePeriod10Msec = DPT("7.003", "Time period (resol. 10ms)", (0, 655350), "ms")
    DPT_TimePeriod100Msec = DPT("7.004", "Time period (resol. 100ms)", (0, 6553500), "ms")
    DPT_TimePeriodSec = DPT("7.005", "Time period (resol. 1s)", (0, 65535), "s")
    DPT_TimePeriodMin = DPT("7.006", "Time period (resol. 1min)", (0, 65535), "min")
    DPT_TimePeriodHrs = DPT("7.007", "Time period (resol. 1h)", (0, 65535), "h")
    DPT_PropDataType = DPT("7.010", "Interface object property ID", (0, 65535))
    DPT_Length_mm = DPT("7.011", "Length", (0, 65535), "mm")
    #DPT_UEICurrentmA = DPT("7.012", "Electrical current", (0, 65535), "mA")  # Add special meaning for 0 (create Limit object)
    DPT_Brightness = DPT("7.013", "Brightness", (0, 65535), "lx")

    def _checkData(self, data):
        if not 0x0000 <= data <= 0xffff:
            raise DPTConverterValueError("data %s not in (0x0000, 0xffff)" % hex(data))

    def _checkValue(self, value):
        if not self._dpt.limits[0] <= value <= self._dpt.limits[1]:
            raise DPTConverterValueError("Value not in range %r" % repr(self._dpt.limits))

    def _toValue(self):
        if self._dpt is self.DPT_TimePeriod10Msec:
            value = self._data * 10.
        elif self._dpt is self.DPT_TimePeriod100Msec:
            value = self._data * 100.
        else:
            value = self._data
        #Logger().debug("DPTConverter2ByteUnsigned._toValue(): value=%d" % value)
        return value

    def _fromValue(self, value):
        if self._dpt is self.DPT_TimePeriod10Msec:
            data = int(round(value / 10.))
        elif self._dpt is self.DPT_TimePeriod100Msec:
            data = int(round(value / 100.))
        else:
            data = value
        #Logger().debug("DPTConverter2ByteUnsigned._fromValue(): data=%s" % hex(data))
        self._data = data

    def _toStrValue(self):
        s = "%d" % self.value

        # Add unit
        if self._displayUnit and self._dpt.unit is not None:
            try:
                s = "%s %s" % (s, self._dpt.unit)
            except TypeError:
                Logger().exception("DPTConverter2ByteUnsigned._toStrValue()", debug=True)
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

    class DPTConverter2ByteUnsignedTestCase(unittest.TestCase):

        def setUp(self):
            self.testTable = (
                (    0, 0x0000, "\x00\x00"),
                (    1, 0x0001, "\x00\x01"),
                (65535, 0xffff, "\xff\xff"),
            )
            self.conv = DPTConverter2ByteUnsigned("7.xxx")

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
