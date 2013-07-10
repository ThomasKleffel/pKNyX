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

Application layer group data management

Implements
==========

 - B{A_GroupDataService}

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
from pknyx.services.loggingServices import Logger
from pknyx.stack.layer7.apci import APCI
from pknyx.stack.layer7.apdu import APDU
from pknyx.stack.layer4.t_groupDataListener import T_GroupDataListener
from pknyx.stack.transceiver.tFrame import TFrame


class A_GDSValueError(PKNyXValueError):
    """
    """


class A_GroupDataService(T_GroupDataListener):
    """ A_GroupDataService class

    @ivar _tgds: transport group data service object
    @type _tgds: L{T_GroupDataService<pknyx.core.layer4.t_groupDataService>}

    @ivar _agdl: application group data listener
    @type _agdl: L{A_GroupDataListener<pknyx.core.layer7.a_groupDataListener>}
    """
    def __init__(self, tgds):
        """

        @param tgds: Transport group data service object
        @type tgds: L{T_GroupDataService<pknyx.core.layer4.t_groupDataService>}

        raise A_GDSValueError:
        """
        super(A_GroupDataService, self).__init__()

        self._tgds = tgds

        self._agdl = None

        tgds.setListener(self)

    def groupDataInd(src, gad, priority, tSDU):
        Logger().debug("A_GroupDataService.groupDataInd(): src=%s, gad=%s, priority=%s, tSDU=%s" % \
                       (src, gad, priority, repr(tSDU)))

        if self._agdl is None:
            Logger().warning("A_GroupDataService.groupDataInd(): not listener defined")
            return

        length = len(tSDU) - TFrame.MIN_LENGTH
        if length >= 1:
            apci = ((tSDU[TFrame.APDU_START+0] & 0x03) << 24) + ((tSDU[TFrame.APDU_START+1] & 0xff) << 16)

            if (apci & APCI._4) == APCI.GROUPVALUE_WRITE:
                if length >= 1:
                    data = APDU.getGroupValueData(tSDU, length)
                    self._agdl.groupValueWriteInd(src, gad, priority, data)

            elif (apci & APCI._4) == APCI.GROUPVALUE_READ:
                if length == 1:
                    self._agdl.groupValue_ReadInd(src, gad, priority)

            elif (apci & APCI._4) == APCI.GROUPVALUE_RES:
                if length >= 1:
                    data = APDU.getGroupValueData(tSDU, length)
                    self._agdl.groupValue_ReadCon(src, gad, priority, data)

    def setListener(self, agdl):
        """

        @param agdl: listener to use to transmit data
        @type agdl: L{A_GroupDataListener<pknyx.core.layer7.a_groupDataListener>}
        """
        self._agdl = agdl

    def groupValueWriteReq(self, src, gad, priority, data):
        """
        """
        Logger().debug("A_GroupDataService.groupValueWriteReq(): src=%s, gad=%s, priority=%s, data=%s" % \
                       (src, gad, priority, repr(data)))

        aPDU = APDU.makeGroupValue(APCI.GROUPVALUE_WRITE, data)
        return self._tgds.groupDataReq(src, gad, priority, aPDU)

    def groupValueReadReq(self, src, gad, priority):
        """
        """
        Logger().debug("A_GroupDataService.groupValueReadReq(): src=%s, gad=%s, priority=%s" % \
                       (src, gad, priority))

        aPDU = APDU.makeNoParamsReq(PCI.GROUPVALUE_READ)
        return self._tgds.groupDataReq(src, gad, priority, aPDU)

    def groupValueReadRes(self, src, gad, priority, data):
        """
        """
        Logger().debug("A_GroupDataService.groupValueReadRes(): src=%s, gad=%s, priority=%s, data=%s" % \
                       (src, gad, priority, repr(data)))

        aPDU = APDU.makeGroupValue(APCI.GROUPVALUE_RES, data)
        return self._tgds.groupDataReq(src, gad, priority, aPDU)


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class A_GDSTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
