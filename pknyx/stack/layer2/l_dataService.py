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

 - B{L_DataService}
 - B{L_DSValueError}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import threading

from pknyx.common.exception import PKNyXValueError
from pknyx.services.logger import Logger
from pknyx.stack.groupAddress import GroupAddress
from pknyx.stack.individualAddress import IndividualAddress
from pknyx.stack.priorityQueue import PriorityQueue
from pknyx.stack.layer3.n_groupDataListener import N_GroupDataListener
from pknyx.stack.transceiver.transceiverLSAP import TransceiverLSAP
from pknyx.stack.transceiver.transmission import Transmission
from pknyx.stack.transceiver.tFrame import TFrame
from pknyx.stack.cemi.cemiLData import CEMILData


class L_DSValueError(PKNyXValueError):
    """
    """


class L_DataService(threading.Thread, TransceiverLSAP):
    """ L_DataService class

    @ivar _ldl: link data listener
    @type _ldl: L{L_DataListener<pknyx.core.layer2.l_dataListener>}

    @ivar _inQueue: input queue
    @type _inQueue: L{PriorityQueue}

    @ivar _outQueue: output queue
    @type _outQueue: L{PriorityQueue}

    @ivar _running: True if thread is running
    @type _running: bool
    """
    def __init__(self, priorityDistribution):
        """

        @param priorityDistribution:
        @type priorityDistribution:

        raise L_DSValueError:
        """
        super(L_DataService, self).__init__(name="LinkLayer")

        self._ldl = None

        self._inQueue  = PriorityQueue(4, priorityDistribution)
        self._outQueue = PriorityQueue(4, priorityDistribution)

        self._running = False

        self.setDaemon(True)
        #self.start()

    def setListener(self, ldl):
        """

        @param ldl: listener to use to transmit data
        @type ldl: L{L_GroupDataListener<pknyx.core.layer2.l_groupDataListener>}
        """
        self._ldl = ldl

    def putInFrame(self, cEMI):
        """ Set input frame

        @param cEMI:
        @type:
        """
        Logger().debug("L_DataService.putInFrame(): cEMI=%s" % cEMI)

        # Get priority from cEMI
        priority = cEMI.priority

        # Add to inQueue and notify inQueue handler
        self._inQueue.acquire()
        try:
            self._inQueue.add(cEMI, priority)
            self._inQueue.notify()
        finally:
            self._inQueue.release()

    def getOutFrame(self):
        """ Get output frame

        Blocks until there is a transmission pending in outQueue, then returns this transmission

        @return: pending transmission in outQueue
        @rtype: L{Transmission}
        """
        transmission = None

        # Test outQueue for frames to transmit, else go sleeping
        self._outQueue.acquire()
        try:
            transmission = self._outQueue.remove()
            while transmission is None and self._running:
                self._outQueue.wait()
                transmission = self._outQueue.remove()
        finally:
            self._outQueue.release()

        return transmission

    def dataReq(self, src, dest, priority, lSDU):
        """
        """
        Logger().debug("L_DataService.dataReq(): src=%s, dest=%s, priority=%s, lSDU=%s" % \
                       (src, dest, priority, repr(lSDU)))

        if dest.isNull:
            raise N_GDSValueError("destination address is null")

        cEMI = CEMILData()
        cEMI.messageCode = CEMILData.MC_LDATA_REQ
        cEMI.sourceAddress = src
        cEMI.destinationAddress = dest
        cEMI.priority = priority

        #length = len(lSDU) - TFrame.MIN_LENGTH

        #lSDU[TFrame.LTP_BYTE] = TFrame.LTP_TABLE if length > 15 else TFrame.LTP_BYTES
        #lSDU[TFrame.PR_BYTE] |= TFrame.PR_CODE[priority.level]

        #lSDU[TFrame.SAH_BYTE] = (src.raw >> 8) & 0xff
        #lSDU[TFrame.SAL_BYTE] = src.raw & 0xff
        #lSDU[TFrame.DAH_BYTE] = (dest.raw >> 8) & 0xff
        #lSDU[TFrame.DAL_BYTE] = dest.raw & 0xff

        #lSDU[TFrame.DAF_BYTE] |= TFrame.DAF_GAD if isinstance(dest, GroupAddress) else TFrame.DAF_IA
        #lSDU[TFrame.LEN_BYTE] |= (TFrame.len2LenCode(length) if length > 15 else length) << TFrame.LEN_BITPOS

        waitL2Con = True  # ???!!!???
        transmission = Transmission(lSDU, waitL2Con)
        transmission.acquire()
        try:
            self._outQueue.acquire()
            try:
                self._outQueue.add(transmission, priority)
                self._outQueue.notifyAll()
            finally:
                self._outQueue.release()

            while transmission.waitConfirm:
                transmission.wait()
        finally:
            transmission.release()

        return transmission.result

    def run(self):
        """ inQueue handler main loop
        """
        Logger().info("Start")

        self._running = True
        while self._running:
            try:
                cEMI = None

                # Test inQueue for frames to handle, else go sleeping
                self._inQueue.acquire()
                try:
                    while cEMI is None and self._running:
                        self._inQueue.wait()
                        cEMI = self._inQueue.remove()
                        Logger().debug("L_DataService.run(): cEMI=%s" % cEMI)
                finally:
                    self._inQueue.release()

                # Handle frame
                if cEMI is not None:
                    src = cEMI.sourceAddress
                    dest = cEMI.destinationAddress
                    priority = cEMI.priority
                    if self._ldl is not None:
                        self._ldl.dataInd(cEMI)
                        #self._ldl.dataInd(src, dest, priority, cEMI.npdu)

            except:
                Logger().exception("L_DataService.run()")  #, debug=True)

        Logger().info("Stop")

    def stop(self):
        """ stop thread
        """
        Logger().info("Stop L_DataService")

        self._running = False

        # Release output queue listeners blocked on wait()
        self._outQueue.acquire()
        try:
            self._outQueue.notifyAll()
        finally:
            self._outQueue.release()

        #self._inQueue.acquire()
        #try:
            #self._inQueue.notifyAll()
        #finally:
            #self._inQueue.release()


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class L_GDSTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
