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

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger
from pknyx.core.groupDataService import GroupDataService
from pknyx.core.layer7.a_groupDataService import A_GroupDataService
from pknyx.core.layer4.t_groupDataService import T_GroupDataService
from pknyx.core.layer3.n_groupDataService import N_GroupDataService
from pknyx.core.layer2.l_dataService import L_DataService
from pknyx.core.transceiver. import A_GroupDataService


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

    def __init__(self):
        """

        raise StackValueError:
        """
        super(Stack, self).__init__()

        self._lds = L_DataService(PRIORITY_DISTRIBUTION)
        self._ngds = N_GroupDataService(self._lds)
        self._tgds = T_GroupDataService(self._ngds)
        self._agds = A_GroupDataService(self._tgds)
        self._tc = UDPTransceiver(self._lds, domainAddr, physAddr)

    @property
    def agds(self):
        return self._agds

    @property
    def gds(self):
        return self._gds

    def start(self):
        """ Start the stack threads

        @todo: name it 'server_forever()'?
        """


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
