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

 - B{DPTBoolean}

Usage
=====

>>> from dptConverterBoolean import DPTBoolean
>>> dptConv = DPTBoolean("1.001")
>>> dptConv.value
ValueError: data not initialized
>>> dptConv.data = 0x01
>>> dptConv.data
1
>>> dptConv.value
1
>>> dptConv.value = 0
>>> dptConv.data
0
>>> dptConv.frame
'\x00'
>>> dptConv.strValue
'Off'
>>> dptConv.strValue = 'On'
>>> dptConv.value
1
>>> dptConv.data = 2
ValueError: data 0x2 not in (0x00, 0x01)
>>> dptConv.value = 3
ValueError: value 3 not in (0, 1)
>>> dptConv.strValue = 'Dummy'
ValueError: DPT string Dummy not in ('Off', 'On')
>>> dptConv.handledDPTIDs
[<DPTID("1.xxx")>, <DPTID("1.001")>, <DPTID("1.002")>, <DPTID("1.003")>, <DPTID("1.004")>, <DPTID("1.005")>,
<DPTID("1.006")>, <DPTID("1.007")>, <DPTID("1.008")>, <DPTID("1.009")>, <DPTID("1.010")>, <DPTID("1.011")>,
<DPTID("1.012")>, <DPTID("1.013")>, <DPTID("1.014")>, <DPTID("1.015")>, <DPTID("1.016")>, <DPTID("1.017")>,
<DPTID("1.018")>, <DPTID("1.019")>, <DPTID("1.021")>, <DPTID("1.022")>, <DPTID("1.023")>]

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import struct

from pknyx.common.loggingServices import Logger
from pknyx.core.dpt.dpt import DPT_, DPT, DPTValueError


class DPTBoolean(DPT):
    """ DPT class for 1-Bit (B1) KNX Datapoint Type

     - 1 Byte: 00000000B
     - B: Binary [0, 1]

    .
    """
    DPT_Generic = DPT_("1.xxx", "Generic", (0, 1))

    DPT_Switch = DPT_("1.001", "Switch", ("Off", "On"))
    DPT_Bool = DPT_("1.002", "Boolean", (False, True))
    DPT_Enable = DPT_("1.003", "Enable", ("Disable", "Enable"))
    DPT_Ramp = DPT_("1.004", "Ramp", ("No ramp", "Ramp"))
    DPT_Alarm = DPT_("1.005", "Alarm", ("No alarm", "Alarm"))
    DPT_BinaryValue = DPT_("1.006", "Binary value", ("Low", "High"))
    DPT_Step = DPT_("1.007", "Step", ("Decrease", "Increase"))
    DPT_UpDown = DPT_("1.008", "Up/Down", ("Up", "Down"))
    DPT_OpenClose = DPT_("1.009", "Open/Close", ("Open", "Close"))
    DPT_Start = DPT_("1.010", "Start", ("Stop", "Start"))
    DPT_State = DPT_("1.011", "State", ("Inactive", "Active"))
    DPT_Invert = DPT_("1.012", "Invert", ("Not inverted", "Inverted"))
    DPT_DimSendStyle = DPT_("1.013", "Dimmer send-style", ("Start/stop", "Cyclically"))
    DPT_InputSource = DPT_("1.014", "Input source", ("Fixed", "Calculated"))
    DPT_Reset = DPT_("1.015", "Reset", ("No action", "Reset"))
    DPT_Ack = DPT_("1.016", "Acknowledge", ("No action", "Acknowledge"))
    DPT_Trigger = DPT_("1.017", "Trigger", ("Trigger", "Trigger"))
    DPT_Occupancy = DPT_("1.018", "Occupancy", ("Not occupied", "Occupied"))
    DPT_Window_Door = DPT_("1.019", "Window/Door", ("Closed", "Open"))
    DPT_LogicalFunction = DPT_("1.021", "Logical function", ("OR", "AND"))
    DPT_Scene_AB = DPT_("1.022", "Scene A/B", ("Scene A", "Scene B"))
    DPT_ShutterBlinds_Mode = DPT_("1.023", "Shutter/Blinds mode", ("Only move Up/Down", "Move Up/Down + StepStop"))

    def _checkData(self, data):
        if data not in (0x00, 0x01):
            try:
                raise DPTValueError("data %s not in (0x00, 0x01)" % hex(data))
            except TypeError:
                raise DPTValueError("data not in (0x00, 0x01)")

    def _checkValue(self, value):

        # For this DPT, we use the DPT_Generic, as other DPTs interpret value as string
        if value not in self.DPT_Generic.limits:
            raise DPTValueError("value %d not in %s" % (value, str(self.DPT_Generic.limits)))

    def _checkStrValue(self, strValue):
        if strValue not in self._handler.limits:
            raise DPTValueError("DPT string '%s' not in %s" % (strValue, str(self._handler.limits)))

    def _toValue(self):
        value = self.DPT_Generic.limits[self._data]
        #Logger().debug("DPTBoolean._toValue(): value=%d" % value)
        return value

    def _fromValue(self, value):
        #Logger().debug("DPTBoolean._fromValue(): value=%d" % value)
        self._checkValue(value)
        data = self.DPT_Generic.limits.index(value)
        #Logger().debug("DPTBoolean._fromValue(): data=%s" % hex(data))
        self._data = data

    def _toStrValue(self):
        return "%s" % self._handler.limits[self.value]

    def _fromStrValue(self, strValue):
        self._data = self._handler.limits.index(strValue)

    def _toFrame(self):
        return struct.pack(">B", self._data)

    def _fromFrame(self, frame):
        self._data = struct.unpack(">B", frame)[0]


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')

    class DPTBooleanTestCase(unittest.TestCase):

        def setUp(self):
            self.testTable = (
                (0, 0x00, "\x00"),
                (1, 0x01, "\x01")
            )
            self.dpt = DPTBoolean("1.xxx")

        def tearDown(self):
            pass

        #def test_constructor(self):
            #print self.dpt.handledDPTIDs

        def test_dpt(self):
            self.assertEqual(self.dpt.dpt, DPTBoolean.DPT_Generic)
            self.dpt.dpt = "1.001"
            self.assertEqual(self.dpt.dpt, DPTBoolean.DPT_Switch)

        def test_checkValue(self):
            with self.assertRaises(DPTValueError):
                self.dpt.value = self.dpt._handler.limits[1] + 1

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
