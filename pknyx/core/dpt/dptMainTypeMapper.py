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


if __name__ == '__main__':
    import unittest

    from pknyx.core.dpt.dptConverterBoolean import DPTBoolean

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
            #with self.assertRaises(DPTValueError):
                #DPTMainTypeMapper("1.001", DPT, "Dummy")
            with self.assertRaises(DPTValueError):
                DPTMainTypeMapper("1.xxx", DummyClass, "Dummy")
            DPTMainTypeMapper("1.xxx", DPTBoolean, "Dummy")


    unittest.main()
