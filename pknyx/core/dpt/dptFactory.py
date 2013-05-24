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

 - B{DPTMainTypeMapper}
 - B{DPTFactoryObject}
 - B{DPTFactory}

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import re

from pknyx.common.loggingServices import Logger
from pknyx.common.helpers import reprStr
from pknyx.core.dpt.dptId import DPTID
from pknyx.core.dpt.dpt import DPT, DPTValueError
#from pknyx.core.dpt.dptMainTypeMapper import DPTMainTypeMapper
from pknyx.core.dpt.dptBoolean import DPTBoolean              #  1.xxx
from pknyx.core.dpt.dpt3BitControl import DPT3BitControl      #  3.xxx
#from pknyx.core.dpt.dptCharacter import DPTCharacter          #  4.xxx
from pknyx.core.dpt.dpt8BitUnsigned import DPT8BitUnsigned    #  5.xxx
from pknyx.core.dpt.dpt8BitSigned import DPT8BitSigned        #  6.xxx
from pknyx.core.dpt.dpt2ByteUnsigned import DPT2ByteUnsigned  #  7.xxx
from pknyx.core.dpt.dpt2ByteSigned import DPT2ByteSigned      #  8.xxx
from pknyx.core.dpt.dpt2ByteFloat import DPT2ByteFloat        #  9.xxx
from pknyx.core.dpt.dptTime import DPTTime                    # 10.xxx
from pknyx.core.dpt.dptDate import DPTDate                    # 11.xxx
from pknyx.core.dpt.dpt4ByteUnsigned import DPT4ByteUnsigned  # 12.xxx
from pknyx.core.dpt.dpt4ByteSigned import DPT4ByteSigned      # 13.xxx
from pknyx.core.dpt.dpt4ByteFloat import DPT4ByteFloat        # 14.xxx
from pknyx.core.dpt.dptString import DPTString                # 16.xxx
#from pknyx.core.dpt.dptDateTime import DPTDateTime            # 19.xxx

dptFactory = None


class DPTMainTypeMapper(object):
    """ Datapoint Type main type mapper class

    Maps a Datapoint Type main part to a corresponding DPT class doing the DPT conversion.

    @ivar _dptId: Datapoint Type ID
    @type _dptId: DPTID

    @ivar _dptClass: Datapoint Type class
    @type _dptClass: class

    @ivar _desc: description of the DPT
    @type _desc: str
    """
    def __init__(self, dptId, dptClass, desc=""):
        """ Creates a new Datapoint Type main type to DPT mapper

        @param dptId: Datapoint Type ID
                      This id must be the generic form ("1.xxx")
        @type dptId: str or L{DPTID}

        @param dptClass: Datapoint Type class
        @type dptClass: class

        @param desc: description of the Datapoint Type main type mapper
        @type desc: str

        @raise DPTValueError:
        """
        super(DPTMainTypeMapper, self).__init__()

        if not issubclass(dptClass, DPT):
            raise DPTValueError("dptClass %s not a sub-class of DPT" % reprStr(dptClass))
        if not isinstance(dptId, DPTID):
            dptId = DPTID(dptId)
        self._dptId = dptId
        self._dptClass = dptClass
        self._desc = desc

    @property
    def id(self):
        """ return the DPT ID
        """
        return self._dptId

    @property
    def desc(self):
        """ return the mapper description
        """
        return self._desc

    @property
    def dptClass(self):
        """ return the Datapoint Type class
        """
        return self._dptClass

    def createConverter(self, dptId):
        """ Create the Datapoint Type for the given dptId

        This method instanciates the DPT using the stored DPT class.

        @param dptId: Datapoint Type ID (full)
        @type dptId: str or L{DPTID}
        """
        return self._dptClass(dptId)


class DPTFactoryObject(object):
    """Datapoint Type factory class

    Maintains available KNX Datapoint Type main numbers and creates associated DPTs.

    It stores all available, registered DPT main numbers with the corresponding DPT and an optional description of
    the type.
    For more common used data types, the main types are declared as constants, although this doesn't necessarily indicate a
    translator is actually available.
    All DPT implementations in this package are registered here and available by default. Converters might be
    added or removed by the user.

    A Datapoint Type consists of a data type and a dimension. The data type is referred to through a main number, the
    existing dimensions of a data type are listed through sub numbers. The data type specifies format and encoding, while
    dimension specifies the range and unit.
    A datapoint type identifier (dptID for short), stands for one particular Datapoint Type. The preferred - but not
    enforced - way of naming a dptID is using the expression I{main number}.I{sub number}.
    In short, a datapoint type has a dptID and standardizes one combination of format, encoding, range and unit.

    @ivar _handledMainDPTMappers: table containing all main Datapoint Type mappers
    @type _handledMainDPTMappers: dict
    """
    TYPE_Boolean = DPTMainTypeMapper("1.xxx", DPTBoolean, "Boolean (main type 1)")
    TYPE_3BitControlled = DPTMainTypeMapper("3.xxx", DPT3BitControl, "3-Bit-Control (main type 3)")
    #TYPE_Character= DPTMainTypeMapper("4.xxx", DPTCharacter, "Character (main type 4)")
    TYPE_8BitUnsigned = DPTMainTypeMapper("5.xxx", DPT8BitUnsigned, "8-Bit-Unsigned (main type 5)")
    TYPE_8BitSigned = DPTMainTypeMapper("6.xxx", DPT8BitSigned, "8-Bit-Signed (main type 6)")
    TYPE_2ByteUnsigned = DPTMainTypeMapper("7.xxx", DPT2ByteUnsigned, "2 Byte-Unsigned (main type 7)")
    TYPE_2ByteSigned = DPTMainTypeMapper("8.xxx", DPT2ByteSigned, "2 Byte-Signed (main type 8)")
    TYPE_2ByteFloat = DPTMainTypeMapper("9.xxx", DPT2ByteFloat, "2 Byte-Float (main type 9)")
    TYPE_Time = DPTMainTypeMapper("10.xxx", DPTTime, "Time (main type 10)")
    TYPE_Date = DPTMainTypeMapper("11.xxx", DPTDate, "Date (main type 11)")
    TYPE_4ByteUnsigned = DPTMainTypeMapper("12.xxx", DPT4ByteUnsigned, "4-Byte-Unsigned (main type 12)")
    TYPE_4ByteSigned = DPTMainTypeMapper("13.xxx", DPT4ByteSigned, "4-Byte-Signed (main type 13)")
    TYPE_4ByteFloat = DPTMainTypeMapper("14.xxx", DPT4ByteFloat, "4-Byte-Float (main type 14)")
    TYPE_String = DPTMainTypeMapper("16.xxx", DPTString, "String (main type 16)")
    #TYPE_DateTime = DPTMainTypeMapper("19.xxx", DPTDateTime, "DateTime (main type 19)")
    #TYPE_HeatingMode = DPTMainTypeMapper("20.xxx", DPTHeatingMode, "Heating mode (main type 20)")

    #linknx implements (@03/2013):
    #1.001: switching (on/off) (EIS1) - done
    #3.007: dimming (control of dimmer using up/down/stop) (EIS2) - done
    #3.008: blinds (control of blinds using close/open/stop) - done
    #5.xxx: 8bit unsigned integer (from 0 to 255) (EIS6) - done
    #5.001: scaling (from 0 to 100%) - done
    #5.003: angle (from 0 to 360°) - done
    #6.xxx: 8bit signed integer (EIS14) - done
    #7.xxx: 16bit unsigned integer (EIS10) - done
    #8.xxx: 16bit signed integer - done
    #9.xxx: 16 bit floating point number (EIS5) - done
    #10.001: time (EIS3) - done
    #11.001: date (EIS4) - done
    #12.xxx: 32bit unsigned integer (EIS11) - done
    #13.xxx: 32bit signed integer - done
    #14.xxx: 32 bit IEEE 754 floating point number - done
    #16.000: string (max 14 ASCII char) (EIS15) - done
    #20.102: heating mode (comfort/standby/night/frost)

    def __new__(cls, *args, **kwargs):
        """ Init the class with all available main Types

        All class objects name B{TYPE_xxx}, will be treated as MainTypeMapper objects and added to the
        B{_handledDPT} dict.
        """
        self = object.__new__(cls, *args, **kwargs)
        cls._handledMainDPTMappers = {}
        for key, value in cls.__dict__.iteritems():
            if key.startswith("TYPE_"):
                cls._handledMainDPTMappers[value.id] = value

        return self

    def __init__(self):
        """ Init the Datapoint Type convertor factory
        """
        super(DPTFactoryObject, self).__init__()

    @property
    def handledMainDPTIDs(self):
        """ Return all handled main Datapoint Type IDs the factory can create
        """
        handleMainDPTIDs = self._handledMainDPTMappers.keys()
        handleMainDPTIDs.sort()
        return handleMainDPTIDs

    def create(self, dptId):
        """ Create the Datapoint Type for the given dptId

        The creation is delegated to the main type mapper.

        @param dptId: Datapoint Type ID
        @type dptId: str
        """
        if not isinstance(dptId, DPTID):
            dptId = DPTID(dptId)
        return self._handledDPT[dptId.generic].createConverter(dptId)


def DPTFactory():
    """ Create or return the global dptFactory object

    Sort of Singleton/Borg pattern.
    """
    global dptFactory
    if dptFactory is None:
        dptFactory = DPTFactoryObject()

    return dptFactory


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')

    class DPTMainTypeMapperTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            #with self.assertRaises(DPTValueError):
                #DPTMainTypeMapper("1.001", DPT, "Dummy")
            with self.assertRaises(DPTValueError):
                DPTMainTypeMapper("1.xxx", DummyClass, "Dummy")
            DPTMainTypeMapper("1.xxx", DPTBoolean, "Dummy")

    class DPTFactoryObjectTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        #def test_constructor(self):
            #print DPTFactory().handledMainDPTIDs

    unittest.main()
