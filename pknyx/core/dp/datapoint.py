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

Datapoint (DP) store knowledge about a datapoint in the KNX network, used for communication within the
pKNyX framework, to the KNX network, and with the user.
Datapoint is identified through a  L{GroupAddress}. A name is supplied to allow a
more friendly interaction with the user, the selected name does not have to be unique. <<<<<<<< ????
Information exchanged between datapoints consists of a certain encoding, defined by a
L{DPT}. This information exchange is done through messages, which are
sent with a L{Priority} associated with the respective datapoint. Every datapoint
object has its own DPT and priority.

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

Usage
=====

>>> from dp import Datapoint as DP
>>> dp = DP("test", "1/2/3", "1.xxx")
>>> dp
<DP("test", <GroupAddress("1/2/3")>, <DPTID("1.xxx")>, <Priority(low)>, stateBased="True")>
>>> dp.main
'test'
>>> dp.mainGroupAddress
<GroupAddress("1/2/3")>
>>> dp.dptId
<DPTID("1.xxx")>
>>> dp.priority
<Priority(low)>
>>> dp.stateBased
True

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger
from pknyx.core.groupAddress import GroupAddress
from pknyx.core.dpt.dpt import DPTID
from pknyx.core.priority import Priority


class DPValueError(PKNyXValueError):
    """
    """


class Datapoint(object):
    """ Datapoint handling class

    @ivar _name: name of the Datapoint
    @type _name: str

    @ivar _mainGroupAddress: main group address identifiying this Datapoint
    @type _mainGroupAddress: L{GroupAddress}

    @ivar _dptId: Datapoint Type ID
    @type _dptId: L{DPTID}

    @ivar _priority: bus message priority
    @type _priority: L{Priority}

    @ivar _stateBased: True if Datapoint is state-based
    @type _stateBased: bool
    """
    def __init__(self, name, mainGroupAddress, dptId, priority=Priority(), stateBased=True):
        """

        @param name: name of the Datapoint
        @type name: str

        @param mainGroupAddress: main group address identifiying this Datapoint
        @type mainGroupAddress: L{GroupAddress} or str

        @param dptId: Datapoint Type ID
        @type dptId: L{DPTID} or str

        @param priority: bus message priority
        @type priority: L{Priority} or str

        @param stateBased: True if Datapoint is state-based
        @type stateBased: bool
        """
        super(Datapoint, self).__init__()

        #Logger().debug("Datapoint.__init__(): name=%s, mainGroupAddress=%s, dptId=%r, priority=%s, stateBased=%s" % \
                       #(name, mainGroupAddress, dptId, priority, stateBased))

        self._name = name
        if not isinstance(mainGroupAddress, GroupAddress):
            mainGroupAddress = GroupAddress(mainGroupAddress)
        self._mainGroupAddress = mainGroupAddress
        if not isinstance(dptId, DPTID):
            dptId = DPTID(dptId)
        self._dptId = dptId
        if not isinstance(priority, Priority):
            priority = Priority(priority)
        self._priority = priority
        self._stateBased = stateBased

    def __repr__(self):
        s = "<Datapoint(\"%s\", %s, %s, %s, stateBased=\"%s\")>" % \
             (self._name, repr(self._mainGroupAddress), repr(self._dptId), repr(self._priority), self._stateBased)
        return s

    @property
    def name(self):
        """ return the Datapoint name
        """
        return self._name

    @property
    def mainGroupAddress(self):
        """ return the main group address
        """
        return self._mainGroupAddress

    @property
    def dptId(self):
        """ return the DPT ID
        """
        return self._dptId

    #@dptId.setter
    #def dptId(self, dptId):
        #""" Change the Datapoint DPT ID
        #"""
        #if not isinstance(dptId, DPTID):
            #dptId = DPTID(dptId)
        #self._dptId = dptId

    @property
    def priority(self):
        """ return the Datapoint priority
        """
        return self._priority

    #@priority.setter
    #def priority(str, level):
        #""" Change the Datapoint priority
        #"""
        #if not isinstance(priority, Priority):
            #priority = Priority(priority)
        #self._priority = priority

    @property
    def stateBased(self):
        """ return the Datapoint behaviour
        """
        return self._stateBased


if __name__ == '__main__':
    import unittest


    class DPTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass
