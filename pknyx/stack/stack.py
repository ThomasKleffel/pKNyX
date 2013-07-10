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

KNX Stack management

Implements
==========

 - B{Stack}
 - B{StackValueError}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import time

from pknyx.common.exception import PKNyXValueError
from pknyx.services.logger import Logger
from pknyx.core.groupDataService import GroupDataService
from pknyx.stack.knxAddress import KnxAddress
from pknyx.stack.individualAddress import IndividualAddress
from pknyx.stack.layer7.a_groupDataService import A_GroupDataService
from pknyx.stack.layer4.t_groupDataService import T_GroupDataService
from pknyx.stack.layer3.n_groupDataService import N_GroupDataService
from pknyx.stack.layer2.l_dataService import L_DataService
from pknyx.stack.transceiver.udpTransceiver import UDPTransceiver


class StackValueError(PKNyXValueError):
    """
    """


class Stack(object):
    """ Stack class

    @ivar _agds: Application group data service object
    @type _agds: L{A_GroupDataService}

    @ivar _gds: Group data service object
    @type _gds: L{GroupDataService}
    """
    PRIORITY_DISTRIBUTION = (-1, 3, 2)

    def __init__(self, domainAddr=KnxAddress(0), individualAddress=IndividualAddress("0.0.0"), serNo=-1,
                 transCls=UDPTransceiver, transParams=dict(mcastAddr="224.0.23.12", mcastPort=3671)):
        """

        raise StackValueError:
        """
        super(Stack, self).__init__()

        if not isinstance(domainAddr, KnxAddress):
            domainAddr = KnxAddress(domainAddr)
        if not isinstance(individualAddress, IndividualAddress):
            individualAddress=IndividualAddress(individualAddress)

        self._lds = L_DataService(Stack.PRIORITY_DISTRIBUTION)
        self._ngds = N_GroupDataService(self._lds)
        self._tgds = T_GroupDataService(self._ngds)
        self._agds = A_GroupDataService(self._tgds)
        self._gds = GroupDataService(self._agds)
        self._tc = transCls(self._lds, domainAddr, individualAddress, **transParams)

    @property
    def agds(self):
        return self._agds

    @property
    def gds(self):
        return self._gds

    @property
    def individualAddress(self):
        return self._tc.individualAddress

    def start(self):
        """ Start the stack threads

        @todo: name it 'server_forever()'?
        """
        Logger().trace("Stack.start()")

        self._lds.start()
        self._tc.start()
        Logger().info("Stack started")

    def stop(self):
        """
        """
        Logger().trace("Stack.stop()")

        self._lds.stop()
        self._tc.stop()
        Logger().info("Stack stopped")

    def mainLoop(self):
        """ Start the main loop.
        """
        self.start()
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class StackTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
