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

Datapoint Type converter management

Implements
==========

 - B{DPTConverterValueError}
 - B{DPTConverterBase}

Documentation
=============

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"


from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger
from pknyx.common.helpers import reprStr
from pknyx.core.dpt.dptId import DPTID


class DPTConverterValueError(PKNyXValueError):
    """
    """


class DPTConverterBase(object):
    """ Base DPT converter class

    Manage conversion between KNX encoded data and python types.

    Each converter class can handles all DPTs of a same main type.

    The handled DPTs must be defined in sub-classes, as class objects, and named B{DPT_xxx}.

    The term B{data} refers to the KNX representation of the python type B{value}. It is stored in the object.
    The B{frame} is the 'data' as bytes (python str), which can be sent/received over the bus.

    @ivar _handledDPT: table containing all DPT the converter can handle (defined in sub-classes)
    @type _handledDPT: dict

    @ivar _dpt: current DPT object of the converter
    @type _dpt: L{DPT<pknyx.core.dpt>}

    @ivar _data: KNX encoded data
    @type _data: depends on sub-class
    """
    def __new__(cls, *args, **kwargs):
        """ Init the class with all available Datapoint Types for this converter

        All class objects defined in sub-classes name B{DPT_xxx}, will be treated as DPT objects and added to the
        B{_handledDPT} dict.
        """
        self = object.__new__(cls, *args, **kwargs)
        cls._handledDPT = {}
        for key, value in cls.__dict__.iteritems():
            if key.startswith("DPT_"):
                cls._handledDPT[value.id] = value

        return self

    def __init__(self, dptId):
        """ Creates a converter for the given Datapoint Type ID

        @param dptId: available implemented Datapoint Type ID
        @type dptId: L{DPTID} or str

        @raise DPTConverterValueError:
        """
        super(DPTConverterBase, self).__init__()

        if not isinstance(dptId, DPTID):
            dptId = DPTID(dptId)
        try:
            self._dpt = self._handledDPT[dptId]
        except KeyError:
            Logger().exception("DPTConverterBase.__init__()", debug=True)
            raise DPTConverterValueError("unhandled DPT ID (%s)" % dptId)

        self._data = None
        self._displayUnit = True

    def __repr__(self):
        try:
            data_ = hex(self._data)
        except TypeError:
            data_ = None
        return "<%s(dpt='%s', data=%r)>" % (reprStr(self.__class__), self._dpt.id, data_)

    def _checkData(self, data):
        """ Check if the data can be handled by the Datapoint Type

        @param data: KNX Datapoint Type to check
        @type data: int

        @raise ValueError: data can't be handled
        """
        Logger().warning("DPTConverterBase._checkData() not implemented is sub-class")

    def _checkValue(self, value):
        """ Check if the value can be handled by the Datapoint Type

        @param value: value to check
        @type value: depends on the DPT

        @raise ValueError: value can't be handled
        """
        Logger().warning("DPTConverterBase._checkValue() not implemented is sub-class")

    #def _checkFrame(self, frame):
        #""" Check if KNX frame can be handled by the Datapoint Type

        #@param frame: KNX Datapoint Type to check
        #@type frame: str

        #@raise ValueError: frame can't be handled
        #"""
        #Logger().warning("DPTConverterBase._checkFrame() not implemented is sub-class")

    def _checkStrValue(self, strDPT):
        """ Check if the DPT string representation can be handled by the Datapoint Type

        @todo: manage upper/lower, unit/no unit...

        @param strDPT: string representation of the data
        @type strDPT: str

        @raise ValueError: string can't be handled
        """
        Logger().warning("DPTConverterBase._checkStrDPT() not implemented is sub-class")

    def _toData(self):
        """ Return KNX encoded data

        @return: KNX encoded data
        @rtype: int
        """
        return self._data

    def _fromData(self, data):
        """ Store KNX encoded data

        @param data: KNX encoded data
        @type data: int
        """
        self._data = data

    def _toValue(self, data):
        """ Conversion from KNX encoded data to python value

        @param data: KNX encoded data
        @type data: int

        @return: python value
        @rtype: depends on the DPT
        """
        raise NotImplementedError

    def _fromValue(self, value):
        """ Conversion from python value to KNX encoded data

        @param value: python value
        @type value: depends on the DPT
        """
        raise NotImplementedError

    def _toStrValue(self):
        """ Conversion from KNX encoded data to DPT string representation

        It mainly converts the data to a string, adding the unit if any.
        For some converters, like Boolean, it can also interprets the data as a string (0 -> "Up")

        @return: DPT string representation
        @rtype: str
        """
        raise NotImplementedError

    def _fromStrValue(self, strDPT):
        """ Conversion from DPT string representation to KNX encoded data

        @todo: manage upper/lower, unit/no unit...

        @param strDPT: string representation of the data
        @type strDPT: str
        """
        raise NotImplementedError

    def _toFrame(self, data):
        """ Conversion from KNX encoded data to bus frame

        @param data: KNX encoded data
        @type data: int

        @return: KNX encoded data as bus frame
        @rtype: str
        """
        raise NotImplementedError

    def _fromFrame(self, frame):
        """ Conversion from bus frame to KNX encoded data

        @param frame: KNX encoded data as bus frame
        @type frame: str

        @return: KNX encoded data
        @rtype: depends on the DPT
        """
        raise NotImplementedError

    @property
    def dpt(self):
        return self._dpt

    @property
    def handledDPTIDs(self):
        handledDPTIDs = self._handledDPT.keys()
        handledDPTIDs.sort()
        return handledDPTIDs

    @property
    def data(self):
        #if self._data is None:
            #raise DPTConverterValueError("data not initialized")
        return self._toData()

    @data.setter
    def data(self, data):
        self._checkData(data)
        self._fromData(data)

    @property
    def value(self):
        if self._data is None:
            raise DPTConverterValueError("data not initialized")
        return self._toValue()

    @value.setter
    def value(self, value):
        self._checkValue(value)
        self._fromValue(value)

    @property
    def strValue(self):
        if self._data is None:
            raise DPTConverterValueError("data not initialized")
        return self._toStrValue()

    @strValue.setter
    def strValue(self, strValue):
        self._checkStrValue(strValue)
        self._fromStrValue(strValue)

    @property
    def frame(self):
        """
        @todo: use PDT_UNSIGNED_CHAR........
        """
        if self._data is None:
            raise DPTConverterValueError("data not initialized")
        return self._toFrame()

    @frame.setter
    def frame(self, frame):
        #self._checkFrame(frame)
        self._fromFrame(frame)


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')

    class AbstractDPTConverterTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            with self.assertRaises(DPTConverterValueError):
                DPTConverterBase(DPTID("1.001"))

    unittest.main()
