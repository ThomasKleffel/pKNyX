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

 - B{DPTConverter2ByteSigned}

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


class DPTConverter2ByteSigned(DPTConverterBase):
    """ DPT converter class for 2-Byte-Unsigned (V16) KNX Datapoint Type

    G{classtree}

     - 2 Byte Signed: VVVVVVVV VVVVVVVV
     - V: Bytes [-32768:32767]
    """
    DPT_Generic = DPT("8.xxx", "Generic", (-32768, 32767))

    DPT_Value_2_Count = DPT("8.001", "Signed count", (-32768, 32767), "pulses")
    DPT_DeltaTimeMsec = DPT("8.002", "Delta time (ms)", (-32768, 32767), "ms")
    DPT_DeltaTime10Msec = DPT("8.003", "Delta time (10ms)", (-327680, 327670), "ms")
    DPT_DeltaTime100Msec = DPT("8.004", "Delta time (100ms)", (-3276800, 3276700), "ms")
    DPT_DeltaTimeSec = DPT("8.005", "Delta time (s)", (-32768, 32767), "s")
    DPT_DeltaTimeMin = DPT("8.006", "Delta time (min)", (-32768, 32767), "min")
    DPT_DeltaTimeHrs = DPT("8.007", "Delta time (h)", (-32768, 32767), "h")
    DPT_Percent_V16 = DPT("8.010", "Percent (16 bit)", (-327.68, 327.67), "%")
    DPT_Rotation_Angle = DPT("8.011", "Rotation angle", (-32768, 32767), "°")

    def _checkData(self, data):
        if not 0x0000 <= data <= 0xffff:
            raise DPTConverterValueError("data %s not in (0x0000, 0xffff)" % hex(data))

    def _checkValue(self, value):
        if not self._dpt.limits[0] <= value <= self._dpt.limits[1]:
            raise DPTConverterValueError("Value not in range %r" % repr(self._dpt.limits))

    def _toValue(self):
        if self._data >= 0x8000:
            data = -((self._data - 1) ^ 0xffff)  # invert twos complement
        else:
            data = self._data
        if self._dpt is self.DPT_DeltaTime10Msec:
            value = data * 10.
        elif self._dpt is self.DPT_DeltaTime100Msec:
            value =data * 100.
        elif self._dpt is self.DPT_Percent_V16:
            value = data / 100.
        else:
            value = data
        #Logger().debug("DPTConverter2ByteSigned._toValue(): value=%d" % value)
        return value

    def _fromValue(self, value):
        if value < 0:
            value = (abs(value) ^ 0xffff) + 1  # twos complement
        if self._dpt is self.DPT_DeltaTime10Msec:
            data = int(round(value / 10.))
        elif self._dpt is self.DPT_DeltaTime100Msec:
            data = int(round(value / 100.))
        elif self._dpt is self.DPT_Percent_V16:
            data = int(round(value * 100.))
        else:
            data = value
        #Logger().debug("DPTConverter2ByteSigned._fromValue(): data=%s" % hex(data))
        self._data = data

    def _toStrValue(self):
        if self._dpt is self.DPT_Percent_V16:
            s = "%.2f" % self.value
        else:
            s = "%d" % self.value

        # Add unit
        if self._displayUnit and self._dpt.unit is not None:
            try:
                s = "%s %s" % (s, self._dpt.unit)
            except TypeError:
                Logger().exception("DPTConverter2ByteSigned._toStrValue()", debug=True)
        return s

    def _toFrame(self):
        return struct.pack(">H", self._data)

    def _fromFrame(self, frame):
        self._data = struct.unpack(">H", frame)[0]

    #def _fromStrValue(self, strValue):


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')

    class DPTConverter2ByteSignedTestCase(unittest.TestCase):

        def setUp(self):
            self.testTable = (
                (-32768, 0x8000, "\x80\x00"),
                (    -4, 0xfffc, "\xff\xfc"),
                (    -1, 0xffff, "\xff\xff"),
                (     0, 0x0000, "\x00\x00"),
                (     1, 0x0001, "\x00\x01"),
                ( 32767, 0x7fff, "\x7f\xff"),
            )
            self.conv = DPTConverter2ByteSigned("8.xxx")

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
