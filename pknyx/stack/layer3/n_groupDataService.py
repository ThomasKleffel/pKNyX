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

Network layer group data management

Implements
==========

 - B{N_GroupDataService}

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
from pknyx.logging.loggingServices import Logger
from pknyx.stack.layer2.l_dataListener import L_DataListener
from pknyx.stack.transceiver.tFrame import TFrame


class N_GDSValueError(PKNyXValueError):
    """
    """


class N_GroupDataService(L_DataListener):
    """ N_GroupDataService class

    @ivar _lds: link data service object
    @type _lds: L{L_DataService<pknyx.core.layer2.l_dataService>}

    @ivar _ngdl: network group data listener
    @type _ngdl: L{N_GroupDataListener<pknyx.core.layer3.n_groupDataListener>}
    """
    def __init__(self, lds):
        """

        @param lds: Link data service object
        @type lds: L{L_DataService<pknyx.core.layer2.l_dataService>}

        raise N_GDSValueError:
        """
        super(N_GroupDataService, self).__init__()

        self._lds = lds

        self._ngdl = None

        lds.setListener(self)

    def _setHopCount(self, nPDU, hc):
        """

        @todo: create a NPDU object, and move this method there
        """
        nPDU[TFrame.HC_BYTE] = (hc << TFrame.HC_BITPOS) & TFrame.HC_MASK

    def _getHopCount(self, nPDU):
        """

        @todo: create a NPDU object, and move this method there
        """
        return (nPDU[TFrame.HC_BYTE] & TFrame.HC_MASK) >> TFrame.HC_BITPOS

    def dataInd(self, src, dest, isGAD, priority, lSDU):
        Logger().debug("N_GroupDataService.groupDataInd(): src=%s, dest=%s, isGAD=%s, priority=%s, lSDU=%s" % \
                       (src, dest, isGAD, priority, repr(lSDU)))

        if self._ngdl is None:
            Logger().warning("N_GroupDataService.dataInd(): not listener defined")
            return

        hopCount = self._getHopCount(lSDU)

        if isGAD:  # Should be True for groupXXX
            if dest.isNull():
                self._ngdl.broadcastInd(src, priority, hopCount, lSDU)
            else:
                self._ngdl.groupDataInd(src, dest, priority, lSDU)
                #self._ngdl.groupDataInd(src, dest, priority, hopCount, lSDU)
        else:
            self._ngdl.dataInd(src, priority, hopCount, lSDU)


    def setListener(self, ngdl):
        """

        @param ngdl: listener to use to transmit data
        @type ngdl: L{N_GroupDataListener<pknyx.core.layer3.n_groupDataListener>}
        """
        self._ngdl = ngdl

    def groupDataReq(self, src, gad, priority, nSDU):
        """
        """
        Logger().debug("N_GroupDataService.groupDataReq(): src=%s, gad=%s, priority=%s,nSDU=%s" % \
                       (src, gad, priority, repr(nSDU)))

        if gad.isNull():
            raise N_GDSValueError("GAD is null")

        hopCount = 6  # force hopCount as we don't transmit it for now

        if (hopCount & 0xFFFFFFF8) != 0:
            raise N_GDSValueError("invalid hopCount (%d)" % hopCount)
        self._setHopCount(nSDU, hopCount)

        return self._lds.dataReq(src, gad, priority, nSDU)


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class N_GDSTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
