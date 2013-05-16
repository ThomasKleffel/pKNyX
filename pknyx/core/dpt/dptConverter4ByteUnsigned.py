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

 - B{DPTConverter4ByteUnsigned}

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


class DPTConverter4ByteUnsigned(DPTConverterBase):
    """ DPT converter class for 4-Byte-Unsigned (U32) KNX Datapoint Type

    G{classtree}

     - 4 Byte Unsigned: UUUUUUUU UUUUUUUU UUUUUUUU UUUUUUUU
     - U: Bytes [0:4294967295]
    """
    DPT_Generic = DPT("12.xxx", "Generic", (0, 4294967295))

    DPT_Value_4_Ucount = DPT("12.001", "Unsigned count", (0, 4294967295), "pulses")

    def _checkData(self, data):
        if not 0x00000000 <= data <= 0xffffffff:
            raise DPTConverterValueError("data %s not in (0x00000000, 0xffffffff)" % hex(data))

    def _checkValue(self, value):
        if not self._dpt.limits[0] <= value <= self._dpt.limits[1]:
            raise DPTConverterValueError("Value not in range %r" % repr(self._dpt.limits))

    def _toValue(self):
        value = self._data
        #Logger().debug("DPTConverter4ByteUnsigned._toValue(): value=%d" % value)
        return value

    def _fromValue(self, value):
        data = value
        #Logger().debug("DPTConverter4ByteUnsigned._fromValue(): data=%s" % hex(data))
        self._data = data

    def _toStrValue(self):
        s = "%d" % self.value

        # Add unit
        if self._displayUnit and self._dpt.unit is not None:
            try:
                s = "%s %s" % (s, self._dpt.unit)
            except TypeError:
                Logger().exception("DPTConverter4ByteUnsigned._toStrValue()", debug=True)
        return s

    #def _fromStrValue(self, strValue):

    def _toFrame(self):
        return struct.pack(">L", self._data)

    def _fromFrame(self, frame):
        self._data = struct.unpack(">L", frame)[0]


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')

    class DPTConverter4ByteUnsignedTestCase(unittest.TestCase):

        def setUp(self):
            self.testTable = (
                (         0, 0x00000000, "\x00\x00\x00\x00"),
                (         1, 0x00000001, "\x00\x00\x00\x01"),
                (4294967295, 0xffffffff, "\xff\xff\xff\xff"),
            )
            self.conv = DPTConverter4ByteUnsigned("12.xxx")

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
