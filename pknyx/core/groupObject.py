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

Group data service management

Implements
==========

 - B{GroupObject}

Documentation
=============

B{GroupObject} are used by L{Datapoint<pknyx.core.datapoint>} to communicate over the bus using group data service.

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common.exception import PKNyXValueError
from pknyx.logging.loggingServices import Logger


class GroupObjectValueError(PKNyXValueError):
    """
    """


class GroupObject(object):
    """ GroupObject class

    @ivar _group: group where this group object belongs
    @type _group: L{Group<pknyx.core.group>}
    """
    def __init__(self, group):
        """

        @param group: group to add this group object to
        @type group: L{Group<pknyx.core.group>}

        raise GroupObjectValueError:
        """
        super(GroupObject, self).__init__()

        self._group = group

    def groupValueWrite(self, src, data, priority):
        """ Write data request on the GAD associated with this group
        """
        self._group.groupValueWrite(src, data, priority)

    def groupValueRead(self, src, priority):
        """ Read data request on the GAD associated with this group
        """
        self._group.groupValueRead(src, priority)

    def groupValueResponse(self, src, data, priority):
        """ Response data request on the GAD associated with this group
        """
        self._group.groupValueResponse(src, data, priority)


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class GroupObjectTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()














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
>>> dp.id
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
from pknyx.logging.loggingServices import Logger
from pknyx.core.dptXlator.dptXlatorFactory import DPTXlatorFactory
from pknyx.core.dptXlator.dpt import DPTID
from pknyx.core.groupObject import GroupObject
from pknyx.core.groupDataListener import GroupDataListener
from pknyx.stack.flags import Flags
from pknyx.stack.priority import Priority


class DPValueError(PKNyXValueError):
    """
    """


class Datapoint(GroupDataListener):
    """ Datapoint handling class

    The term B{data} refers to the KNX representation of the python type B{value}. It is stored in this object.
    The B{frame} is the 'data' as bytes (python str), which can be sent/received over the bus.

    @ivar _owner: owner of the Datapoint
    @type _owner: L{Device<pknyx.core.device>} -> could be a more generic object

    @ivar _id: id of the Datapoint
    @type _id: str

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

    @ivar _accesspoint : Accesspoint to use to communicate with the bus
                         A Datapoint can be linked to several GAD (by the way of L{Group}), but can only send requests
                        (write/read/response) to the first GAD. This Accespoint belongs to the Group handling that GAD.
    @type _accesspoint : L{Accesspoint}

    @todo: add desc. param
    @todo: also create the generic handler (if not the default one), and a .generic property
    """
    def __init__(self, owner, id, name, dptId=DPTID(), flags=Flags(), priority=Priority(), defaultValue=None):
        """

        @param owner: owner of the Datapoint
        @type owner: L{Device<pknyx.core.device>} -> could be a more generic object

        @param id: id of the Datapoint
        @type id: str

        @param dptId: Datapoint Type ID
        @type dptId: str or L{DPTID}

        @param flags: bus message flags
        @type flags: str or L{Flags}

        @param priority: bus message priority
        @type priority: str or L{Priority}

        @param defaultValue: value to use as default
        @type defaultValue: depend on the DPT

        @todo: if flag 'U' is set, do an automatic read request on the bus?
        """
        super(Datapoint, self).__init__()

        #Logger().debug("Datapoint.__init__(): id=%s, dptId=%s, flags=%s, priority=%s, defaultValue=%s" % \
                       #(repr(id), repr(dptId), repr(flags), repr(priority), repr(defaultValue)))

        self._owner = owner
        self._id = id
        if not isinstance(dptId, DPTID):
            dptId = DPTID(dptId)
        self._dptId = dptId
        if not isinstance(flags, Flags):
            flags = Flags(flags)
        self._flags = flags
        if not isinstance(priority, Priority):
            priority = Priority(priority)
        self._priority = priority

        self._dptXlator = DPTXlatorFactory().create(dptId)
        self._dptXlatorGeneric = None

        self._data = defaultValue

        self._accesspoint = None

    def __repr__(self):
        return "<Datapoint(id='%s', dptId='%s', flags='%s', priority='%s')>" % \
               (self._id, self._dptId, self._flags, self._priority)

    def __str__(self):
        return "<Datapoint('%s')>" % self._id

    def onGroupValueWrite(self, cEMI):
        Logger().debug("Datapoint.onGroupWrite(): cEMI=%s" % repr(cEMI))

        data = cEMI.data
        self._dptXlator.checkData(data)
        oldData = self._data

        # Notify owner if data changed
        # Use the subscribing mecanism to call the registered owner methods (via @trigger...)
        # The dispatching should be done in the Device.notify() method
        if data != oldData and self._flags.write:
            self._data = data
            self._owner.notify(self)

    def onGroupValueRead(self, cEMI):
        Logger().debug("Datapoint.onGroupRead(): cEMI=%s" % repr(cEMI))

        # Check if data should be send over the bus
        if self._flags.read and self._flags.communicate:
            self._accesspoint.groupValueResponse(self._address, self._data, self._priority)

    def onGroupValueResponse(self, cEMI):
        Logger().debug("Datapoint.onGroupResponse(): cEMI=%s" % repr(cEMI))

        data = cEMI.data
        self._dptXlator.checkData(data)
        oldData = self._data

        # Notify owner if data changed
        # Use the subscribing mecanism to call the registered owner methods (via @trigger...)
        # The dispatching should be done in the Device.notify() method
        if data != oldDate and self._flags.update:
            self._data = data
            self._owner.notify(self)

    @property
    def owner(self):
        return self._owner

    @property
    def id(self):
        return self._id

    #@id.setter
    #def id(self, id):
        #self._id = id

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

        self._dptXlator.checkData(data)
        oldData = self._data
        self._data = data

        # Check if data should be send over the bus
        if (data != oldDate or self._flags.stateless) and self._flags.transmit and self._flags.communicate:
            self._accesspoint.groupValueWrite(self._address, data, self._priority)

    @property
    def value(self):
        if self._data is None:
            raise DPValueError("data not initialized")
        return self._dptXlator.dataToValue(self._data)

    @value.setter
    def value(self, value):
        self._dptXlator.checkValue(value)
        self.data = self._dptXlator.valueToData(value)  # Note usage of .data and not ._data!!!

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
        self.data = self._dptXlator.frameToData(frame)  # Note usage of .data and not ._data!!!

    @property
    def accesspoint(self):
        return self._accesspoint

    @accesspoint.setter
    def accesspoint(self, accesspoint):
        self._accesspoint = accesspoint

        # If the flag init is set, send a read request on that accesspoint, which is bound to the default GAD
        # this datapoint should use for read/write on bus
        if self._flags.init:
            accesspoint.groupValueRead(self._address, self._priority)


if __id__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class DPTestCase(unittest.TestCase):

        def setUp(self):
            self.dp = Datapoint(self, id="dp1", dptId="1.001", flags="CRT", priority="low", defaultValue=0.)

        def tearDown(self):
            pass

        def test_display(self):
            print repr(self.dp)
            print self.dp

        def test_constructor(self):
            DP_01 = dict(id="temperature", dptId="9.001", flags="CRT", priority="low", defaultValue=0.)
            DP_02 = dict(id="humidity", dptId="9.007", flags="CRT", priority="low", defaultValue=0.)
            DP_03 = dict(id="wind_speed", dptId="9.005", flags="CRT", priority="low", defaultValue=0.)
            DP_04 = dict(id="wind_alarm", dptId="1.005", flags="CRT", priority="urgent", defaultValue="No alarm")
            DP_05 = dict(id="wind_speed_limit", dptId="9.005", flags="CWTU", priority="low", defaultValue=15.)
            DP_06 = dict(id="wind_alarm_enable", dptId="1.003", flags="CWTU", priority="low", defaultValue="Disable")
            Datapoint(self, **DP_01)
            Datapoint(self, **DP_02)
            Datapoint(self, **DP_03)
            Datapoint(self, **DP_04)
            Datapoint(self, **DP_05)
            Datapoint(self, **DP_06)


    unittest.main()
