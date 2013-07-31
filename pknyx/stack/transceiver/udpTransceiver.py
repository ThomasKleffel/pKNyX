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

Transceiver management

Implements
==========

 - B{UDPTransceiver}
 - B{UDPTransceiverValueError}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL

@todo: run transmitter and receiver in a simple threaded method, instead of a complete class thread.
"""

__revision__ = "$Id$"

import threading
import socket

from pknyx.common.exception import PKNyXValueError
from pknyx.services.logger import Logger
from pknyx.stack.result import Result
from pknyx.stack.knxAddress import KnxAddress
from pknyx.stack.groupAddress import GroupAddress
from pknyx.stack.individualAddress import IndividualAddress
from pknyx.stack.multicastSocket import MulticastSocket
from pknyx.stack.transceiver.transceiver import Transceiver
from pknyx.stack.transceiver.tFrame import TFrame
from pknyx.stack.knxnetip.knxNetIPHeader import KNXnetIPHeader, KNXnetIPHeaderValueError
from pknyx.stack.cemi.cemiLData import CEMILData, CEMIValueError


class GadSet(set):
    """ A locking set of GroupAddress
    """
    def __init__(self):
        """
        """
        super(GadSet, self).__init__()

        self._condition = threading.Condition()

    def acquire(self):
        self._condition.acquire()

    def release(self):
        self._condition.release()

    def wait(self):
        self._condition.wait()

    def notify(self):
        self._condition.notify()

    def notifyAll(self):
        self._condition.notifyAll()


class UDPTransceiverValueError(PKNyXValueError):
    """
    """


class UDPTransceiver(Transceiver):
    """ UDPTransceiver class

    @ivar _mcastAddr:
    @type _mcastAddr:

    @ivar _mcastPort:
    @type _mcastPort:

    @ivar _transmitter: multicast transmitter
    @type _transmitter: L{Transmitter}

    @ivar _receiver: multicast receiver
    @type _receiver: L{Receiver}

    @ivar _gadSet: set of GAD
    @type _gadSet: L{GadSet}
    """
    def __init__(self, tLSAP, domainAddr=KnxAddress(0), individualAddress=IndividualAddress("0.0.0"),
                 mcastAddr="224.0.23.12", mcastPort=3671):
        """

        @param tLSAP:
        @type tLSAP: L{TransceiverLSAP}

        @param domainAddr:
        @type domainAddr:

        @param individualAddress: own Individual Address (used when no source address is given in lSDU)
        @type individualAddress: str or L{IndividualAddress<pknyx.core.individualAddress>}

        @param mcastAddr: multicast address to bind to
        @type mcastAddr: str

        @param mcastPort: multicast address to bind to
        @type mcastPort: str

        raise UDPTransceiverValueError:
        """
        super(UDPTransceiver, self).__init__(tLSAP, domainAddr, individualAddress)

        if not isinstance(domainAddr, KnxAddress):
            domainAddr = KnxAddress(domainAddr)
        self._domainAddr = domainAddr
        if not isinstance(individualAddress, IndividualAddress):
            individualAddress = IndividualAddress(individualAddress)
        self._individualAddress = individualAddress
        self._mcastAddr = mcastAddr
        self._mcastPort = mcastPort

        self._transmitterSock = MulticastSocket(mcastPort, mcastAddr)
        self._receiverSock = MulticastSocket(mcastPort)
        self._gadSet = GadSet()

        self.addGroupAddress(GroupAddress("0/0/0"))

        # Create transmitter and receiver threads
        self._transmitter = threading.Thread(target=self._transmitterLoop, name="UDP transmitter")
        #self._transmitter.setDaemon(True)
        self._receiver = threading.Thread(target=self._receiverLoop, name="UDP receiver")
        #self._receiver.setDaemon(True)

    @property
    def tLSAP(self):
        return self._tLSAP

    @property
    def domainAddr(self):
        return self._domainAddr

    @property
    def individualAddress(self):
        return self._individualAddress

    @property
    def mcastAddr(self):
        return self._mcastAddr

    @property
    def mcastPort(self):
        return self._mcastPort

    @property
    def localAddr(self):
        return self._localAddr

    @property
    def localPort(self):
        return self._transmitterSock.localPort

    @property
    def gadSet(self):
        return self._gadSet

    def _transmitterLoop(self):
        """
        """
        Logger().info("Start")

        while self._running:
            try:
                transmission = self.tLSAP.getOutFrame()
                Logger().debug("UDPTransceiver._transmitterLoop(): transmission=%s" % repr(transmission))

                if transmission is not None:

                    #lPDU = transmission.lPDU
                    #Logger().debug("UDPTransceiver._transmitterLoop(): lPDU=%s" % repr(lPDU))
                    #lPDU[TFrame.CF_BYTE] |= TFrame.CF_L_DATA
                    #lPDU[TFrame.SAH_BYTE] = self.individualAddress.high
                    #lPDU[TFrame.SAL_BYTE] = self.individualAddress.low

                    #checksum = 0x00
                    #for c in lPDU[self.OVERHEAD:]:
                        #checksum = (checksum ^ c) & 0xff

                    #lPDU[self.OVERHEAD:] = lPDU[self.OVERHEAD-1:]
                    #lPDU[-1] = checksum ^ 0xff

                    #outFrame = lPDU[self.OVERHEAD-1:]  # use eCMI
                    #header = KNXnetIPHeader(service=KNXnetIPHeader.ROUTING_IND, serviceLength=len(outFrame))
                    #outFrame = header.frame + outFrame
                    #Logger().debug("UDPTransceiver._transmitterLoop(): outFrame= %s" % repr(outFrame))

                    try:
                        #self._transmitterSock.transmit(outFrame)
                        transmission.result = Result.OK
                    except IOError:
                        Logger().exception("UDPTransceiver._transmitterLoop()")
                        transmission.result = Result.ERROR

                    if transmission.waitConfirm:
                        transmission.acquire()
                        try:
                            transmission.waitConfirm = False
                            transmission.notify()
                        finally:
                            transmission.release()
                        Logger().debug("UDPTransceiver._transmitterLoop(): transmission=%s" % repr(transmission))

            except:
                Logger().exception("UDPTransceiver._transmitterLoop()")  #, debug=True)

        self._transmitterSock.close()

        Logger().info("Stopped")

    def _receiverLoop(self):
        """
        """
        Logger().info("Start")

        try:
            self._receiverSock.joinGroup(self._mcastAddr)
        except:
            self._receiverSock.close()
            raise

        while self._running:
            try:
                inFrame, (fromAddr, fromPort) = self._receiverSock.receive()
                Logger().debug("UDPTransceiver._receiverLoop(): inFrame=%s" % repr(inFrame))
                inFrame = bytearray(inFrame)
                try:
                    header = KNXnetIPHeader(inFrame)
                except KNXnetIPHeaderValueError:
                    Logger().exception("UDPTransceiver._receiverLoop()", debug=True)
                Logger().debug("UDPTransceiver._receiverLoop(): KNXnetIP header=%s" % repr(header))

                frame = inFrame[KNXnetIPHeader.HEADER_SIZE:]
                try:
                    cEMI = CEMILData(frame)
                except CEMIValueError:
                    Logger().exception("UDPTransceiver._receiverLoop()", debug=True)
                Logger().debug("UDPTransceiver._receiverLoop(): cEMI=%s" % cEMI)

                destAddr = cEMI.destinationAddress
                if isinstance(destAddr, IndividualAddress) and destAddr == self._individualAddress:  # destination matches
                    #self._tLSAP.putInFrame(cEMI)
                    Logger().warning("UDPTransceiver._receiverLoop(): IndividualAddress destination not supported")
                elif isinstance(cEMI.destinationAddress, GroupAddress):
                    self._gadSet.acquire()
                    try:

                        # @todo: add cmp support in KnxAddress to avoid .raw usage
                        if destAddr in self._gadSet or GroupAddress("0/0/0").raw in self._gadSet:
                            self._tLSAP.putInFrame(cEMI)

                    finally:
                        self._gadSet.release()
                else:
                    Logger().warning("UDPTransceiver._receiverLoop(): unknown destination address type (%s)" % repr(destAddr))

            except socket.timeout:
                pass
                #Logger().exception("UDPTransceiver._receiverLoop()", debug=True)

            except:
                Logger().exception("UDPTransceiver._receiverLoop()")  #, debug=True)

        self._receiverSock.close()

        Logger().info("Stopped")

    def addGroupAddress(self, gad):
        """
        """
        if not isinstance(gad, GroupAddress):
            gad = GroupAddress(gad)

        self._gadSet.acquire()
        try:
            self._gadSet.add(gad.raw)  # Make a GADSet object with a .contain() method
        finally:
            self._gadSet.release()

    def removeGroupAddress(self, gad):
        """
        """
        self._gadSet.acquire()
        try:
            self._gadSet.remove(gad)
        finally:
            self._gadSet.release()

    def start(self):
        """
        """
        Logger().trace("UDPTransceiver.start()")

        self._running = True
        self._transmitter.start()
        self._receiver.start()
        Logger().info("UDP Transceiver started")

    def stop(self):
        """
        """
        Logger().trace("UDPTransceiver.stop()")

        self._running = False
        self._receiver.join()
        self._transmitter.join()
        Logger().info("UDP Transceiver stopped")


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class UDPTransceiverTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
