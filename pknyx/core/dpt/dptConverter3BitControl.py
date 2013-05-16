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

Datapoint Types management.

Implements
==========

 - B{DPTConverter3BitControl}

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
from pknyx.core.dpt.dpt import DPT
from pknyx.core.dpt.dptConverterBase import DPTConverterBase, DPTConverterValueError
from pknyx.core.dpt.dptConverterBoolean import DPTConverterBoolean


class DPTConverter3BitControl(DPTConverterBase):
    """ DPT converter class for 3-Bit-Control (B1U3) KNX Datapoint Type

    G{classtree}

    This is a composite converter.

     - 1 Byte: 0000CSSSS
     - C: Control bit [0, 1]
     - S: StepCode [0:7]

    The _data param of this converter only handles the stepCode; the control bit is handled by the sub-converter.

    @todo: create and use a DPTCompositeConverterBase?

    @ivar _dptConverter: sub-converter
    @type _dptConverter: L{DPTConverterBase<pknyx.core.dpt.dptConverterBase>}
    """
    DPT_Generic = DPT("3.xxx", "Generic", (-7, 7))

    DPT_Control_Dimming = DPT("3.007", "Dimming", (-7, 7))
    DPT_Control_Blinds = DPT("3.008", "Blinds", (-7, 7))

    def __init__(self, dptId):
        super(DPTConverter3BitControl, self).__init__(dptId)

        mainId, subId = dptId.split('.')
        dptId_ = "1.%s" % subId
        self._dptConverter = DPTConverterBoolean(dptId_)

    def _checkData(self, data):
        if not 0x00 <= data <= 0x0f:
            raise DPTConverterValueError("data %s not in (0x00, 0x0f)" % hex(data))

    def _checkValue(self, value):
        if not self._dpt.limits[0] <= value <= self._dpt.limits[1]:
            raise DPTConverterValueError("value %d not in range %r" % (value, repr(self._dpt.limits)))

    def _toData(self):

        # Combinate the control, which is stored in the sub-converter, and the stepCode, which is stored here.
        ctrl = self._dptConverter.data
        stepCode = self._data
        data = ctrl << 3 | stepCode
        return data

    def _fromData(self, data):

        # Split control and stepCode; store control in sub-converter, and stepCode here.
        ctrl = (data & 0x08) >> 3
        self._dptConverter.data = ctrl
        stepCode = data & 0x07
        self._data = stepCode

    def _toValue(self):
        ctrl = self._dptConverter.data
        stepCode = self._data
        value = stepCode if ctrl else -stepCode
        return value

    def _fromValue(self, value):
        ctrl = 1 if value > 0 else 0
        self._dptConverter.data = ctrl
        stepCode = abs(value) & 0x07
        self._data = stepCode

    def _toStrValue(self):
        """
        @todo: use ctrl/stepCode properties once implemented
        @todo: manage _displayUnit (convert stepCode to steps?)
        """
        stepCode = self._data
        if stepCode == 0:
            s = "Break"
        else:
            s = "%s:%d" % (self._dptConverter.strValue, stepCode)
        return s

    #def _fromStrValue(self, strValue):

    # Add properties control and stepCode + helper methods (+ intervals?)

    def _toFrame(self):

        # Note the usage of self.data, and not self._data!
        return struct.pack(">B", self.data)

    def _fromFrame(self, frame):

        # Note the usage of self.data, and not self._data!
        self.data = struct.unpack(">B", frame)[0]

    #def nbIntervalsToStepCode(self, nbIntervals):
        #""" Compute the stepCode for a given number of intervals

        #The number of intervals is rounded to the nearest intervals representable with a stepcode
        #(e.g 48 rounded of to 32, 3 rounded of to 2).

        #@todo: use property, and work on _data

        #@param nbIntervals: number of intervals to devide the 0-100% range
        #@type nbIntervals: int

        #@return: stepCode
        #@rtype: int
        #"""
        #if nbIntervals - 1 not in range(64):
            #raise ValueError("nbIntervals not in range (1, 64)");
        #stepCode = 7
        #thres = 0x30
        #while thres >= nbIntervals:
            #stepCode -= 1
            #thres >>= 1
        #return stepCode

    #def stepCodeToNbIntervals(self, stepCode):
        #""" Compute the number of intervals for a given stepCode

        #@todo: use property, and work on _data

        #@param stepCode: stepCode to use
        #@type stepCode: int

        #@return: number of intervals
        #@rtype: int
        #"""
        #return 1 << stepCode - 1


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')

    class DPTConverter3BitControlTestCase(unittest.TestCase):

        def setUp(self):
            self.testTable = (
                ( 0, 0x00, '\x00'),
                ( 1, 0x09, '\x09'),
                (-1, 0x01, '\x01'),
                ( 7, 0x0f, '\x0f'),
                (-7, 0x07, '\x07'),
            )
            self.stepCodeIntervalTable = (
                (1,  1),
                (2,  2),
                (3,  4),
                (4,  8),
                (5, 16),
                (6, 32),
                (7, 64),
            )
            self.conv = DPTConverter3BitControl("3.xxx")

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

        #def test_nbIntervalsToStepCode(self):
            #for stepCode, nbIntervals in self.stepCodeIntervalTable:
                #nbIntervals_ = self.conv.stepCodeToNbIntervals(stepCode)
                #self.assertEqual(nbIntervals_, nbIntervals, "Conversion failed (computed nbIntervals for stepCode %d is %d, should be %d)" %
                                 #(stepCode, nbIntervals_, nbIntervals))

        #def test_stepCodeToNbIntervals(self):
            #for stepCode, nbIntervals in self.stepCodeIntervalTable:
                #stepCode_ = self.conv.nbIntervalsToStepCode(nbIntervals)
                #self.assertEqual(stepCode_, stepCode, "Conversion failed (computed stepCode for %d intervals is %d, should be %d)" %
                                 #(nbIntervals, stepCode_, stepCode))


    unittest.main()
