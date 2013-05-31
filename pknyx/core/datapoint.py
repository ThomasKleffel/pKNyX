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

(move to ETS class doc.)

linknx :

The "flags" parameter is similar to the ETS flags. The value of each flag is represented by a letter:
 - c: Communication (allow the object to interact with the KNX bus)
 - r: Read (allow the object to answer to a read request from another participant)
 - w: Write (update the object's internal value with the one received in write telegram if they are different)
 - t : Transmit (allow the object to transmit it's value on the bus if it's modified internally by a rule or via XML protocol)
 - u : Update (update the object's internal value with the one received in "read response" telegram if they are different)
 - f : Force (force the object value to be transmitted on the bus, even if it didn't change).
       In the recent versions you can use s : Stateless flag alternatively which means exactly the same
       (object does not update it's state so linknx should always send it's value to the bus
 - i : Init (useless for the moment. Will perhaps replace the parameter init="request" in the future)

Each letter appearing inside the value of this parameter means the corresponding flag is set.
If "flags" is not specified, the default value is "cwtu" (Communication, Write, Transmit and Update).

The default set of flags is good for most normal objects like switches where the value kept internally by linknx is
corresponding to real object state. Another set of flags can be for example "crwtf" (or "crwts") for objects that
should send it's value to the KNX bus even if linknx maintains the same value. This is usefull for scenes.
Setting scene value to 'on' should send this value to KNX every time action is triggered to make the scene happen.

ETS: S         K   L   E   T   Act
     S         C   R   W   T   U

 - S -> le DP envoie sa valeur sur la GA ayant ce flag (première GA associée à ce DP)
 - K -> communication : si pas présent, le DP n'envoie rien sur le bus (à utiliser pour com.interne au framework)
 - L -> lecture : le DP renverra sa valeur si une demande de lecture est faite sur une GA associée à ce DP (1 seul DP par
        GA devrait avoir ce flag)
 - E -> écriture : la valeur du DP sera modifiée si un télégramme de type 'write' est envoyé sur un des GA associée à ce DP
 - T -> transmission : si la valeur du DP est modifiée en interne (ou via plugin pour framewok), il enverra sa nouvelle
        valeur sur le bus, sur la GA ayant le flag S associé
 - Act -> update : le DP met à jour sa valeur s'il voit passer un télégramme en réponse à une demande de lecture sur
          l'une des GA associée à ce DP

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
from pknyx.stack.dataPointListener import DatapointListener


class DPValueError(PKNyXValueError):
    """
    """


class Datapoint(object):
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

        self._listener = DatapointListener(self)

    def __repr__(self):
        s = "<Datapoint(\"%s\", %s, flags=\"%s\", %s)>" % \
             (self._name, repr(self._dptId), self._flags, repr(self._priority))
        return s

    def onRead(self, cEMI):
        """
        """

    def onWrite(self, cEMI):
        """
        """

    def onResponse(self, cEMI):
        """
        """

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def dptId(self):
        return self._dptId

    @dptId.setter
    def dptId(self, dptId):
        if not isinstance(dptId, DPTID):
            dptId = DPTID(dptId)
        self._dptId = dptId

    #@property
    #def dptXlator(self):
        #""" return the DPT
        #"""
        #return self._dptXlator

    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, flags):
        if not isinstance(flags, Flags):
            flags = Flags(flags)
        self._flags = flags

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(str, level):
        if not isinstance(priority, Priority):
            priority = Priority(priority)
        self._priority = priority

    @property
    def data(self):
        return self.data

    @data.setter
    def data(self, data):
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
        self._data = self._dptXlator.valueToData(value)

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
        self._data = self._dptXlator.frameToData(frame)


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
