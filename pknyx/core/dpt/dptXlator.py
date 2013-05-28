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

Datapoint Types translation management

Implements
==========

 - B{DPTXlatorValueError}
 - B{DPTXlator}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id: dpt.py 34 2013-05-27 12:33:55Z fma $"

from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger
from pknyx.core.dpt.dptId import DPTID


class DPTXlatorValueError(PKNyXValueError):
    """
    """


class DPTXlator(object):
    """ Base DPT translator class

    Manage conversion between KNX encoded data and python types.

    Each DPTXlator class can handles all DPTs of a same main type.

    The handled DPTs must be defined in sub-classes, as class objects, and named B{DPT_xxx}.

    @ivar _handledDPT: table containing all DPT the DPTXlator can handle (defined in sub-classes)
    @type _handledDPT: dict

    @ivar _dpt: current DPT object of the DPTXlator
    @type _dpt: L{DPT}

    @ivar _data: KNX encoded data
    @type _data: depends on sub-class

    @todo: remove the strValue stuff
    """
    def __new__(cls, *args, **kwargs):
        """ Init the class with all available types for this DPT

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
        """ Creates a DPT for the given Datapoint Type ID

        @param dptId: available implemented Datapoint Type ID
        @type dptId: str or L{DPTID}

        @raise DPTXlatorValueError:
        """
        super(DPT, self).__init__()

        if not isinstance(dptId, DPTID):
            dptId = DPTID(dptId)
        try:
            self._dpt = self._handledDPT[dptId]
        except KeyError:
            Logger().exception("DPTXlator.__init__()", debug=True)
            raise DPTXlatorValueError("unhandled DPT ID (%s)" % dptId)

        self._data = None

    def __repr__(self):
        try:
            data_ = hex(self._data)
        except TypeError:
            data_ = None
        return "<%s(dpt='%s', data=%r)>" % (reprStr(self.__class__), self._dpt.id, data_)

    @property
    def handledDPT(self):
        handledDPT = self._handledDPT.keys()
        handledDPT.sort()
        return handledDPT

    @property
    def dpt(self):
        return self._dpt

    @dpt.setter
    def dpt(self, dptId):
        if not isinstance(dptId, DPTID):
            dptId = DPTID(dptId)
        try:
            self._dpt = self._handledDPT[dptId]
        except KeyError:
            Logger().exception("DPTXlator.dpt", debug=True)
            raise DPTXlatorValueError("unhandled DPT ID (%s)" % dptId)

    @property
    def unit(self):
        return self._dpt.unit

    def checkData(self, data):
        """ Check if the data can be handled by the Datapoint Type

        @param data: KNX Datapoint Type to check
        @type data: int

        @raise DPTXlatorValueError: data can't be handled
        """
        Logger().warning("DPTXlator._checkData() not implemented is sub-class")

    def checkValue(self, value):
        """ Check if the value can be handled by the Datapoint Type

        @param value: value to check
        @type value: depends on the DPT

        @raise DPTXlatorValueError: value can't be handled
        """
        Logger().warning("DPTXlator._checkValue() not implemented is sub-class")

    def checkFrame(self, frame):
        """ Check if KNX frame can be handled by the Datapoint Type

        @param frame: KNX Datapoint Type to check
        @type frame: str

        @raise DPTXlatorValueError: frame can't be handled
        """
        Logger().warning("DPTXlator._checkFrame() not implemented is sub-class")

    def dataToValue(self, data):
        """ Conversion from KNX encoded data to python value

        @param data: KNX encoded data
        @type data: int

        @return: python value
        @rtype: depends on the DPT
        """
        raise NotImplementedError

    def valueToData(self, value):
        """ Conversion from python value to KNX encoded data

        @param value: python value
        @type value: depends on the DPT
        """
        raise NotImplementedError

    def dataToFrame(self, data):
        """ Conversion from KNX encoded data to bus frame

        @param data: KNX encoded data
        @type data: int

        @return: KNX encoded data as bus frame
        @rtype: str
        """
        raise NotImplementedError

    def frameToData(self, frame):
        """ Conversion from bus frame to KNX encoded data

        @param frame: KNX encoded data as bus frame
        @type frame: str

        @return: KNX encoded data
        @rtype: depends on the DPT
        """
        raise NotImplementedError


if __name__ == '__main__':
    import unittest


    class DPTXlatorTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            with self.assertRaises(DPTXlatorValueError):
                DPTXlator("1.001")


    unittest.main()
