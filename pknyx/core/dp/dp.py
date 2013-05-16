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

 - B{DP}

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

Usage
=====

>>> from dp import DP
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


class DP(object):
    """ Datapoint handling class

    G{classtree}

    @ivar _name: name of the Datapoint
    @type _name: str

    @ivar _mainGroupAddress: main group address identifiying this Datapoint
    @type _mainGroupAddress: L{GroupAddress}

    @ivar _dptId: Datapoint Type ID
    @type _dptId: L{DPTID}

    @ivar _priority: bus message priority
    @type _priority: L{Priority}

    @ivar _stateBased: True if DP is state-based
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

        @param stateBased: True if DP is state-based
        @type stateBased: bool
        """
        super(DP, self).__init__()

        #Logger().debug("DP.__init__(): name=%s, mainGroupAddress=%s, dptId=%r, priority=%s, stateBased=%s" % \
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
        s = "<DP(\"%s\", %s, %s, %s, stateBased=\"%s\")>" % \
             (self._name, repr(self._mainGroupAddress), repr(self._dptId), repr(self._priority), self._stateBased)
        return s

    @property
    def name(self):
        """ return the DP name
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
        #""" Change the DP DPT ID
        #"""
        #if not isinstance(dptId, DPTID):
            #dptId = DPTID(dptId)
        #self._dptId = dptId

    @property
    def priority(self):
        """ return the DP priority
        """
        return self._priority

    #@priority.setter
    #def priority(str, level):
        #""" Change the DP priority
        #"""
        #if not isinstance(priority, Priority):
            #priority = Priority(priority)
        #self._priority = priority

    @property
    def stateBased(self):
        """ return the DP behaviour
        """
        return self._stateBased


if __name__ == '__main__':
    import unittest


    class DPTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass
