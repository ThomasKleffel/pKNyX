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
        super(L_DataService, self).__init__(name="KNX Stack LinkLayer")

        self._ldl = None

        self._inQueue  = PriorityQueue(4, priorityDistribution)
        self._outQueue = PriorityQueue(4, priorityDistribution)

        self._running = False

        self.setDaemon(True)
        #self.start()

    def setListener(self, lgdl):
        """

        @param ngdl: listener to use to transmit data
        @type ngdl: L{L_GroupDataListener<pknyx.core.layer2.l_groupDataListener>}
        """
        self._ldl = lgdl

    def putInFrame(self, lPDU):
        """ Set input frame

        @param lPDU: Link Pxxx Data Unit
        @type: bytearray
        """
        Logger().debug("L_DataService.putInFrame(): lPDU=%s" % repr(lPDU))

        # test Control Field (CF) - not necessary cause should be done by the transceiver or BCU
        # if (lPDU[TFrame.CF_BYTE] & TFrame.CF_MASK) != TFrame.CF_L_DATA:
        #     return

        # Length of lPDU and length transmitted with lPDU must be equal
        length = (lPDU[TFrame.LEN_BYTE] & TFrame.LEN_MASK) >> TFrame.LEN_BITPOS
        if (lPDU[TFrame.LTP_BYTE] & TFrame.LTP_MASK) == TFrame.LTP_TABLE:
            length = TFrame.lenCode2Len(length)

        length += TFrame.MIN_LENGTH
        if length != len(lPDU):
            return

        # Get priority from lPDU (move test in Priority object)
        if (lPDU[TFrame.PR_BYTE] & TFrame.PR_MASK) == TFrame.PR_SYSTEM:
            priority = Priority('system')
        elif (lPDU[TFrame.PR_BYTE] & TFrame.PR_MASK) == TFrame.PR_NORMAL:
            priority = Priority('normal')
        elif (lPDU[TFrame.PR_BYTE] & TFrame.PR_MASK) == TFrame.PR_URGENT:
            priority = Priority('urgent')
        elif (lPDU[TFrame.PR_BYTE] & TFrame.PR_MASK) == TFrame.PR_LOW:
            priority = Priority('low')
        else:
            priority = Priority('low')

        # Add to inQueue and notify inQueue handler
        #lPDU[TFrame.PR_BYTE] = priority  # memorize priority
        self._inQueue.acquire()
        try:
            self._inQueue.add(lPDU, priority)
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

        if dest.isNull():
            raise N_GDSValueError("destination address is null")

        length = len(lSDU) - TFrame.MIN_LENGTH

        lSDU[TFrame.LTP_BYTE] = TFrame.LTP_TABLE if length > 15 else TFrame.LTP_BYTES
        lSDU[TFrame.PR_BYTE] |= TFrame.PR_CODE[priority.level]

        lSDU[TFrame.SAH_BYTE] = (src.raw >> 8) & 0xff
        lSDU[TFrame.SAL_BYTE] = src.raw & 0xff
        lSDU[TFrame.DAH_BYTE] = (dest.raw >> 8) & 0xff
        lSDU[TFrame.DAL_BYTE] = dest.raw & 0xff

        lSDU[TFrame.DAF_BYTE] |= TFrame.DAF_GAD if isinstance(dest, GroupAddress) else TFrame.DAF_IA
        lSDU[TFrame.LEN_BYTE] |= (TFrame.len2LenCode(length) if length > 15 else length) << TFrame.LEN_BITPOS

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

        lPDU = None
        self._running = True
        while self._running:
            try:

                # Test inQueue for frames to handle, else go sleeping
                self._inQueue.acquire()
                try:
                    while lPDU is None and self._running:
                        self._inQueue.wait()
                        lPDU = self._inQueue.remove()
                        Logger().debug("L_DataService.run(): lPDU=%s" % repr(lPDU))
                finally:
                    self._inQueue.release()

                # Handle frame
                if lPDU is not None:
                    src = ((lPDU[TFrame.SAH_BYTE] & 0xff) << 8) | (lPDU[TFrame.SAL_BYTE] & 0xff)
                    dest = ((lPDU[TFrame.DAH_BYTE] & 0xff) << 8) | (lPDU[TFrame.DAL_BYTE] & 0xff)
                    if (lPDU[TFrame.DAF_BYTE] & TFrame.DAF_MASK) == TFrame.DAF_GAD:
                        dest = GroupAddress(dest)
                    else:
                        dest = IndividualAddress(dest)
                    priority = lPDU[TFrame.PR_BYTE]
                    if self._ldl is not None:
                        self.lgdl.dataInd(src, dest, priority, lPDU)

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
