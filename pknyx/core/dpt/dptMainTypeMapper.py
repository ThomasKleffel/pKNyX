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

 - B{DPTMainTypeMapper}

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
from pknyx.core.dpt.dptConverterBase import DPTConverterBase, DPTConverterValueError


class DPTMainTypeMapper(object):
    """ Datapoint Type main type mapper class

    G{classtree}

    Maps a Datapoint Type main part to a corresponding converter class doing the DPT conversion.

    @ivar _dptId: Datapoint Type ID
    @type _dptId: DPTID

    @ivar _converterClass: Datapoint Type converter class
    @type _converterClass: L{DPTConverterBase}

    @ivar _desc: description of the DPT
    @type _desc: str
    """
    def __init__(self, dptId, converterClass, desc=""):
        """ Creates a new Datapoint Type main type to converter mapper

        @param dptId: Datapoint Type ID
                      This id must be in the generic form ("1.xxx")
        @type dptId: int

        @param converterClass: Datapoint Type converter class
        @type converterClass: L{DPTConverterBase}

        @param desc: description of the Datapoint Type main type mapper
        @type desc: str

        @raise DPTConverterValueError:
        """
        super(DPTMainTypeMapper, self).__init__()

        if not issubclass(converterClass, DPTConverterBase):
            raise DPTConverterValueError("converterClass %s not a sub-class of DPTConverterBase" % reprStr(converterClass))

        self._dptId = DPTID(dptId)
        self._converterClass = converterClass
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
    def converterClass(self):
        """ return the Datapoint Type converter class
        """
        return self._converterClass

    def createConverter(self, dptId):
        """ Create the Datapoint Type converter for the given dptId

        This method instanciates the converter using the stored converter class.

        @param dptId: Datapoint Type ID (full)
        @type dptId: str
        """
        return self._converterClass(dptId)


if __name__ == '__main__':
    import unittest

    from pknyx.core.dpt.dptConverterBoolean import DPTConverterBoolean

    # Mute logger
    Logger().setLevel('error')

    class DummyClass:
        pass

    class DPTMainTypeMapperTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            #with self.assertRaises(DPTConverterValueError):
                #DPTMainTypeMapper("1.001", DPTConverterBase, "Dummy")
            with self.assertRaises(DPTConverterValueError):
                DPTMainTypeMapper("1.xxx", DummyClass, "Dummy")
            DPTMainTypeMapper("1.xxx", DPTConverterBoolean, "Dummy")


    unittest.main()
