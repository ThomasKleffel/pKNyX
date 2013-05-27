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

 - B{DPTValueError}
 - B{DPT_}
 - B{DPT}

Documentation
=============

From KNX documentation::

                    Datapoint Type
                          |
            ----------------------------
            |                           |
        Data Type                   Dimension
            |                           |
       -----------                 ----------
      |           |               |          |
   Format      Encoding         Range       Unit

The Datapoint Types are defined as a combination of a data type and a dimension. It has been preferred not to define the
data types separately from any dimension. This only leads to more abstract naming and identifications.

Any Datapoint Type thus standardizes one combination of format, encoding, range and unit. The Datapoint Types will be
used to describe further KNX Interworking Standards.

The Datapoint Types are identified by a 16 bit main number separated by a dot from a 16-bit subnumber, e.g. "7.002".
The coding is as follows::

    ---------------------------------------
     Field              | Stands for
    --------------------+------------------
     main number (left) | Format, Encoding
     subnumber (right)  | Range, Unit
    ---------------------------------------

Datapoint Types with the same main number thus have the same format and encoding.

Datapoint Types with the same main number have the same data type. A different subnumber indicates a different dimension
(different range and/or different unit).

Usage
=====

>>> from dpt import DPT_
>>> dpt_ = DPT_("1.001", "Switch", ("Off", "On"))
>>> dpt_
<DPT_(id="<DPTID("1.001")>", desc="Switch", limits=('Off', 'On'))>
>>> dpt_.id
<DPTID("1.001")>
>>> dpt_.id.main
'1'
>>> dpt_.id.generic
<DPTID("1.xxx")>
>>> dpt_.desc
'Switch'
>>> dpt_.limits
('Off', 'On')

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger
from pknyx.core.dpt.dptId import DPTID


class DPTValueError(PKNyXValueError):
    """
    """


class DPT_(object):
    """ Datapoint Type hanlding class

    Manage Datapoint Type informations and behavior.

    @ivar _id: Datapoint Type ID
    @type _id: L{DPTID}

    @ivar _desc: description of the DPT
    @type _desc: str

    @ivar _limits: value limits the DPT can handle
    @type _limits: tuple of int/float/str

    @ivar _unit: optional unit of the DPT
    @type _unit: str
    """
    def __init__(self, dptId, desc, limits, unit=None):
        """ Init the DPT_ object

        @param dptId: available implemented Datapoint Type ID
        @type dptId: L{DPTID} or str

        @param desc: description of the DPT
        @type desc: str

        @param limits: value limits the DPT can handle
        @type limits: tuple of int/float/str

        @param unit: optional unit of the DPT
        @type unit: str

        @raise DPTValueError:
        """
        super(DPT_, self).__init__()

        #Logger().debug("DPT.__init__(): id=%s, desc=%s, limits=%r, unit=%s" % (dptId, desc, limits, unit))

        if not isinstance(dptId, DPTID):
            dptId = DPTID(dptId)
        self._id = dptId
        self._desc = desc
        try:
            self._limits = tuple(limits)
        except TypeError:
            Logger().exception("DPT.__init__()", debug=True)
            raise DPTValueError("invalid limits")
        self._unit = unit

    def __repr__(self):
        if self._unit is not None:
            s = "<DPT_(id=\"%r\", desc=\"%s\", limits=%s, unit=\"%s\")>" % (self._id, self._desc, repr(self._limits), self._unit)
        else:
            s = "<DPT_(id=\"%r\", desc=\"%s\", limits=%s)>" % (self._id, self._desc, repr(self._limits))
        return s

    @property
    def id(self):
        """ return the DPT ID
        """
        return self._id

    @property
    def desc(self):
        """ return the DPT description
        """
        return self._desc

    @property
    def limits(self):
        """ return the DPT limits
        """
        return self._limits

    @property
    def unit(self):
        """ return the DPT unit
        """
        return self._unit


class DPT(object):
    """ Base DPT class

    Manage conversion between KNX encoded data and python types.

    Each DPT class can handles all DPT_s of a same main type.

    The handled DPTs must be defined in sub-classes, as class objects, and named B{DPT_xxx}.

    The term B{data} refers to the KNX representation of the python type B{value}. It is stored in the object.
    The B{frame} is the 'data' as bytes (python str), which can be sent/received over the bus.

    @ivar _knownHandlers: table containing all DPT_ the DPT can handle (defined in sub-classes)
    @type _knownHandlers: dict

    @ivar _handler: current DPT_ object of the DPT
    @type _handler: L{DPT<pknyx.core.dpt>}

    @ivar _data: KNX encoded data
    @type _data: depends on sub-class
    """
    def __new__(cls, *args, **kwargs):
        """ Init the class with all available types for this DPT

        All class objects defined in sub-classes name B{DPT_xxx}, will be treated as DPT objects and added to the
        B{_knownHandlers} dict.
        """
        self = object.__new__(cls, *args, **kwargs)
        cls._knownHandlers = {}
        for key, value in cls.__dict__.iteritems():
            if key.startswith("DPT_"):
                cls._knownHandlers[value.id] = value

        return self

    def __init__(self, dptId):
        """ Creates a DPT for the given Datapoint Type ID

        @param dptId: available implemented Datapoint Type ID
        @type dptId: L{DPTID} or str

        @raise DPTValueError:
        """
        super(DPT, self).__init__()

        if not isinstance(dptId, DPTID):
            dptId = DPTID(dptId)
        try:
            self._handler = self._knownHandlers[dptId]
        except KeyError:
            Logger().exception("DPT.__init__()", debug=True)
            raise DPTValueError("unhandled DPT ID (%s)" % dptId)

        self._data = None
        self._displayUnit = True

    def __repr__(self):
        try:
            data_ = hex(self._data)
        except TypeError:
            data_ = None
        return "<%s(dpt='%s', data=%r)>" % (reprStr(self.__class__), self._handler.id, data_)

    def _checkData(self, data):
        """ Check if the data can be handled by the Datapoint Type

        @param data: KNX Datapoint Type to check
        @type data: int

        @raise ValueError: data can't be handled
        """
        Logger().warning("DPT._checkData() not implemented is sub-class")

    def _checkValue(self, value):
        """ Check if the value can be handled by the Datapoint Type

        @param value: value to check
        @type value: depends on the DPT

        @raise ValueError: value can't be handled
        """
        Logger().warning("DPT._checkValue() not implemented is sub-class")

    def _checkStrValue(self, strValue):
        """ Check if the DPT string representation can be handled by the Datapoint Type

        @todo: manage upper/lower, unit/no unit...

        @param strValue: string representation of the data
        @type strValue: str

        @raise ValueError: string can't be handled
        """
        Logger().warning("DPT._checkStrDPT() not implemented is sub-class")

    #def _checkFrame(self, frame):
        #""" Check if KNX frame can be handled by the Datapoint Type

        #@param frame: KNX Datapoint Type to check
        #@type frame: str

        #@raise ValueError: frame can't be handled
        #"""
        #Logger().warning("DPT._checkFrame() not implemented is sub-class")

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
        For some DPTs, like Boolean, it can also interprets the data as a string (0 -> "Up")

        @return: DPT string representation
        @rtype: str
        """
        raise NotImplementedError

    def _fromStrValue(self, strValue):
        """ Conversion from DPT string representation to KNX encoded data

        @todo: manage upper/lower, unit/no unit...

        @param strValue: string representation of the data
        @type strValue: str
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
        return self._handler

    @dpt.setter
    def dpt(self, dptId):
        if not isinstance(dptId, DPTID):
            dptId = DPTID(dptId)
        try:
            self._handler = self._knownHandlers[dptId]
        except KeyError:
            Logger().exception("DPT.dpt", debug=True)
            raise DPTValueError("unhandled DPT ID (%s)" % dptId)

    @property
    def knownHandlers(self):
        knownHandlers = self._knownHandlers.keys()
        knownHandlers.sort()
        return knownHandlers

    @property
    def data(self):
        #if self._data is None:
            #raise DPTValueError("data not initialized")
        return self._toData()

    @data.setter
    def data(self, data):
        self._checkData(data)
        self._fromData(data)

    @property
    def value(self):
        if self._data is None:
            raise DPTValueError("data not initialized")
        return self._toValue()

    @value.setter
    def value(self, value):
        self._checkValue(value)
        self._fromValue(value)

    @property
    def strValue(self):
        if self._data is None:
            raise DPTValueError("data not initialized")
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
            raise DPTValueError("data not initialized")
        return self._toFrame()

    @frame.setter
    def frame(self, frame):
        #self._checkFrame(frame)
        self._fromFrame(frame)


if __name__ == '__main__':
    import unittest


    class DPT_TestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            with self.assertRaises(DPTValueError):
                DPT_("9.001", "Temperature", -273)

    class DPTTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            with self.assertRaises(DPTValueError):
                DPT("1.001")


    unittest.main()
