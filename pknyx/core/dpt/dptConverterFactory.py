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

 - B{DPTConverterFactoryObject}
 - B{DPTConverterFactory}

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
from pknyx.core.dpt.dptMainTypeMapper import DPTMainTypeMapper
from pknyx.core.dpt.dptConverterBoolean import DPTConverterBoolean              #  1.xxx
from pknyx.core.dpt.dptConverter3BitControl import DPTConverter3BitControl      #  3.xxx
#from pknyx.core.dpt.dptConverterCharacter import DPTConverterCharacter          #  4.xxx
from pknyx.core.dpt.dptConverter8BitUnsigned import DPTConverter8BitUnsigned    #  5.xxx
from pknyx.core.dpt.dptConverter8BitSigned import DPTConverter8BitSigned        #  6.xxx
from pknyx.core.dpt.dptConverter2ByteUnsigned import DPTConverter2ByteUnsigned  #  7.xxx
from pknyx.core.dpt.dptConverter2ByteSigned import DPTConverter2ByteSigned      #  8.xxx
from pknyx.core.dpt.dptConverter2ByteFloat import DPTConverter2ByteFloat        #  9.xxx
from pknyx.core.dpt.dptConverterTime import DPTConverterTime                    # 10.xxx
from pknyx.core.dpt.dptConverterDate import DPTConverterDate                    # 11.xxx
from pknyx.core.dpt.dptConverter4ByteUnsigned import DPTConverter4ByteUnsigned  # 12.xxx
from pknyx.core.dpt.dptConverter4ByteSigned import DPTConverter4ByteSigned      # 13.xxx
from pknyx.core.dpt.dptConverter4ByteFloat import DPTConverter4ByteFloat        # 14.xxx
from pknyx.core.dpt.dptConverterString import DPTConverterString                # 16.xxx
#from pknyx.core.dpt.dptConverterDateTime import DPTConverterDateTime            # 19.xxx

dptConverterFactory = None


class DPTConverterFactoryObject(object):
    """Datapoint Type converter factory class

    G{classtree}

    Maintains available KNX Datapoint Type main numbers and creates associated DPT converters.

    It stores all available, registered DPT main numbers with the corresponding converter and an optional description of
    the type.
    For more common used data types, the main types are declared as constants, although this doesn't necessarily indicate a
    translator is actually available.
    All DPT converter implementations in this package are registered here and available by default. Converters might be
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
    TYPE_Boolean = DPTMainTypeMapper("1.xxx", DPTConverterBoolean, "Boolean (main type 1)")
    TYPE_3BitControlled = DPTMainTypeMapper("3.xxx", DPTConverter3BitControl, "3-Bit-Control (main type 3)")
    #TYPE_Character= DPTMainTypeMapper("4.xxx", DPTConverterCharacter, "Character (main type 4)")
    TYPE_8BitUnsigned = DPTMainTypeMapper("5.xxx", DPTConverter8BitUnsigned, "8-Bit-Unsigned (main type 5)")
    TYPE_8BitSigned = DPTMainTypeMapper("6.xxx", DPTConverter8BitSigned, "8-Bit-Signed (main type 6)")
    TYPE_2ByteUnsigned = DPTMainTypeMapper("7.xxx", DPTConverter2ByteUnsigned, "2 Byte-Unsigned (main type 7)")
    TYPE_2ByteSigned = DPTMainTypeMapper("8.xxx", DPTConverter2ByteSigned, "2 Byte-Signed (main type 8)")
    TYPE_2ByteFloat = DPTMainTypeMapper("9.xxx", DPTConverter2ByteFloat, "2 Byte-Float (main type 9)")
    TYPE_Time = DPTMainTypeMapper("10.xxx", DPTConverterTime, "Time (main type 10)")
    TYPE_Date = DPTMainTypeMapper("11.xxx", DPTConverterDate, "Date (main type 11)")
    TYPE_4ByteUnsigned = DPTMainTypeMapper("12.xxx", DPTConverter4ByteUnsigned, "4-Byte-Unsigned (main type 12)")
    TYPE_4ByteSigned = DPTMainTypeMapper("13.xxx", DPTConverter4ByteSigned, "4-Byte-Signed (main type 13)")
    TYPE_4ByteFloat = DPTMainTypeMapper("14.xxx", DPTConverter4ByteFloat, "4-Byte-Float (main type 14)")
    TYPE_String = DPTMainTypeMapper("16.xxx", DPTConverterString, "String (main type 16)")
    #TYPE_DateTime = DPTMainTypeMapper("19.xxx", DPTConverterDateTime, "DateTime (main type 19)")
    #TYPE_HeatingMode = DPTMainTypeMapper("20.xxx", DPTConverterHeatingMode, "Heating mode (main type 20)")

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
        super(DPTConverterFactoryObject, self).__init__()

    @property
    def handledMainDPTIDs(self):
        """ Return all handled main Datapoint Type IDs the factory can create
        """
        handleMainDPTIDs = self._handledMainDPTMappers.keys()
        handleMainDPTIDs.sort()
        return handleMainDPTIDs

    def create(self, dptId):
        """ Create the Datapoint Type converter for the given dptId

        The creation is delegated to the main type mapper.

        @param dptId: Datapoint Type ID
        @type dptId: str
        """
        dptIdGeneric = DPTID(dptId).generic
        return self._handledDPT[dptIdGeneric].createConverter(dptId)


def DPTConverterFactory():
    """ Create or return the global dptConverterFactory object

    Sort of Singleton/Borg pattern.
    """
    global dptConverterFactory
    if dptConverterFactory is None:
        dptConverterFactory = DPTConverterFactoryObject()

    return dptConverterFactory


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')

    class DPTConverterFactoryObjectTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        #def test_constructor(self):
            #print DPTConverterFactory().handledMainDPTIDs

    unittest.main()
