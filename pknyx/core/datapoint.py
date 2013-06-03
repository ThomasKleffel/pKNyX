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

Datapoint management

Implements
==========

 - B{Datapoint}

Documentation
=============

Usage
=====

>>> from datapoint import Datapoint
>>> dp = Datapoint("test")
>>> dp
<Datapoint("test", <DPTID("1.xxx")>, flags=<Flags("CWTU")>, Priority(low)>)>
>>> dp.name
'test'
>>> dp.dptId
<DPTID("1.xxx")>
>>> dp.flags
<Flags("CWTU")>
>>> dp.priority
<Priority(low)>

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger
from pknyx.core.dptXlator.dptXlatorFactory import DPTXlatorFactory
from pknyx.core.dptXlator.dpt import DPTID
from pknyx.core.flags import Flags
from pknyx.core.priority import Priority
from pknyx.core.accesspoint import Accesspoint
from pknyx.core.dataPointListener import DatapointListener


class DPValueError(PKNyXValueError):
    """
    """


class Datapoint(DatapointListener):
    """ Datapoint handling class

    The term B{data} refers to the KNX representation of the python type B{value}. It is stored in this object.
    The B{frame} is the 'data' as bytes (python str), which can be sent/received over the bus.

    @ivar _name: name of the Datapoint
    @type _name: str

    @ivar _dptId: Datapoint Type ID
    @type _dptId: str or L{DPTID}

    @ivar _flags: bus message flags
    @type _flags: str or L{Flags}

    @ivar _priority: bus message priority
    @type _priority: str or L{Priority}

    @ivar _data: KNX encoded data
    @type _data: depends on sub-class

    @ivar _dptXlator: DPT translator associated with this Datapoint
    @type _dptXlator: L{DPTXlator<pknyx.core.dptXlator>}

    @ivar _accesspoint : Accesspoint  to use to communicate with the bus
    @type _accesspoint : L{Accesspoint}

    @todo: add desc. param
    @todo: also create the generic handler (if not the default one), and a .generic property
    """
    def __init__(self, name, dptId=DPTID(), flags=Flags(), priority=Priority(), defaultValue=None):
        """

        @param name: name of the Datapoint
        @type name: str

        @param dptId: Datapoint Type ID
        @type dptId: str or L{DPTID}

        @param flags: bus message flags
        @type flags: str or L{Flags}

        @param priority: bus message priority
        @type priority: str or L{Priority}

        @param defaultValue: value to use as default
        @type defaultValue: depend on the DPT
        """
        super(Datapoint, self).__init__()

        #Logger().debug("Datapoint.__init__(): name=%s, dptId=%r, flags=%r, priority=%s" % \
                       #(name, dptId, flags, priority, stateBased))

        self._name = name
        if not isinstance(dptId, DPTID):
            dptId = DPTID(dptId)
        self._dptId = dptId
        if not isinstance(flags, Flags):
            flags = Flags(flags)
        self._flags = flags
        if not isinstance(priority, Priority):
            priority = Priority(priority)
        self._priority = priority

        self._data = None

        self._dptXlator = DPTXlatorFactory().create(dptId)
        self._dptXlatorGeneric = None

        self._accesspoint = None

    def __repr__(self):
        s = "<Datapoint(\"%s\", %s, flags=\"%s\", %s)>" % \
             (self._name, repr(self._dptId), self._flags, repr(self._priority))
        return s

    #def onGroupWrite(self, cEMI):
        #"""
        #"""

    #def onGroupRead(self, cEMI):
        #"""
        #"""

    #def onGroupResponse(self, cEMI):
        #"""
        #"""

    @property
    def name(self):
        return self._name

    #@name.setter
    #def name(self, name):
        #self._name = name

    @property
    def dptId(self):
        return self._dptId

    #@dptId.setter
    #def dptId(self, dptId):
        #if not isinstance(dptId, DPTID):
            #dptId = DPTID(dptId)
        #self._dptId = dptId

    @property
    def dptXlator(self):
        """ return the DPT
        """
        return self._dptXlator

    @property
    def flags(self):
        return self._flags

    #@flags.setter
    #def flags(self, flags):
        #if not isinstance(flags, Flags):
            #flags = Flags(flags)
        #self._flags = flags

    @property
    def priority(self):
        return self._priority

    #@priority.setter
    #def priority(str, level):
        #if not isinstance(priority, Priority):
            #priority = Priority(priority)
        #self._priority = priority

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):

        # Check flags and _accesspoint -> send value over bus if changed (or if forced)
        self._dptXlator.checkData(data)
        self._data = data

    @property
    def value(self):
        if self._data is None:
            raise DPValueError("data not initialized")
        return self._dptXlator.dataToValue(self._data)

    @value.setter
    def value(self, value):
        self._dptXlator.checkValue(value)
        self.data = self._dptXlator.valueToData(value)  # Note usage of .data and not ._data

    @property
    def unit(self):
        return self._dptXlator.unit

    @property
    def frame(self):
        """
        @todo: use PDT_UNSIGNED_CHAR........
        """
        if self._data is None:
            raise DPValueError("data not initialized")
        return self._dptXlator.dataToFrame(self._data)

    @frame.setter
    def frame(self, frame):
        self._dptXlator.checkFrame(frame)
        self.data = self._dptXlator.frameToData(frame)  # Note usage of .data and not ._data


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class DPTestCase(unittest.TestCase):

        def setUp(self):
            self.dp = Datapoint("test")

        def tearDown(self):
            pass

        #def test_constructor(self):
            #with self.assertRaises(DPValueError):
                #Datapoint("name")


    unittest.main()
