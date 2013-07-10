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
"""

__revision__ = "$Id$"

import threading
import socket

from pknyx.common.exception import PKNyXValueError
from pknyx.services.loggingServices import Logger
from pknyx.stack.groupAddress import GroupAddress
from pknyx.stack.individualAddress import IndividualAddress
from pknyx.stack.multicastSocket import MulticastSocket
from pknyx.stack.transceiver.transceiver import Transceiver
from pknyx.stack.transceiver.tFrame import TFrame
from pknyx.stack.knxnetip.knxNetIPHeader import KnxnetIPHeader, KnxnetIPHeaderValueError


class GadSet(set):
    """
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


class UDPTransmitter(threading.Thread):
    """ Transmitter thread of the UDP transceiver

    @ivar _sock: multicast socket
    @type _sock: L{MulticastSocket}

    @ivar _running: True if thread is running
    @type _running: bool

    @ivar _localPort: local port used by the socket
    @type _localPort: int
    """
    def __init__(self, parent):
        """

        @param parent:
        @type parent:

        @param tLSAP:
        @type tLSAP: L{TransceiverLSAP}
        """
        super(UDPTransmitter, self).__init__(name="KNX Stack UDP Transmitter")

        self._parent = parent

        self._sock = MulticastSocket(self._parent.mcastPort, self._parent.mcastAddr)

        self._running = False

        self.setDaemon(True)
        #self.start()

    @property
    def localPort(self):
        return self._sock.localPort

    def run(self):
        """
        """
        Logger().info("Start")

        self._running = True
        while self._running:
            try:
                transmission = self._parent.tLSAP.getOutFrame()
                if transmission is not None:
                    lPDU = transmission.lPDU
                    lPDU[TFrame.CF_BYTE] |= TFrame.CF_L_DATA
                    lPDU[TFrame.SAH_BYTE] = self._parent.indivAddr.high
                    lPDU[TFrame.SAL_BYTE] = self._parent.indivAddr.low

                    checksum = 0x00
                    for i in range(self.OVERHEAD, len(lPDU)):
                        #checkSum = (byte)(checkSum ^ lPDU[i]);
                        checksum = (checksum ^ lPDU[i]) & 0xff

                    #System.arraycopy(lPDU, self.OVERHEAD, lPDU, self.OVERHEAD-1, len(lPDU)-self.OVERHEAD)
                    lPDU[self.OVERHEAD:] = lPDU[self.OVERHEAD-1:-1]
                    #lPDU[lPDU.length-1] = (byte)~checkSum;
                    lPDU[len(lPDU)-1] = checksum ^ 0xff

                    outFrame = lPDU[self.OVERHEAD-1:]
                    Logger().debug("UDPTransmitter.run(): outFrame= %s" % repr(outFrame))
                    try:
                        self._sock.send(outFrame)
                        transmission.result = Result.OK
                    except IOException:
                        transmission.result = Result.ERROR

                    if transmission.waitConfirm:
                        transmission.acquire()
                        try:
                            transmission.waitConfirm = False
                            transmission.notify()
                        finally:
                            transmission.release()

            except:
                Logger().exception("UDPTransmitter.run()", debug=True)

        self._sock.close()

        Logger().info("Stop")

    def stop(self):
        """ stop thread
        """
        Logger().info("Stop UDP Transmitter")

        self._running = False


class UDPReceiver(threading.Thread):
    """ Receiver thread for the UDP transceiver

    @ivar _localPort: local port used by the socket
    @type _localPort: int
    """
    def __init__(self, parent):
        """

        @param parent:
        @type parent:
        """
        super(UDPReceiver, self).__init__(name="KNX Stack UDP Receiver")

        self._parent = parent

        self._sock = MulticastSocket(self._parent.mcastPort)
        try:
            self._sock.joinGroup(self._parent.mcastAddr)
        except:
            self._sock.close();
            raise

        self._running = False

        self.setDaemon(True)
        #self.start()

    def run(self):
        """
        """
        Logger().info("Start")

        self._running = True
        while self._running:
            try:
                inFrame, (fromAddr, fromPort) = self._sock.receive()
                Logger().debug("UDPReceiver.run(): inFrame=%s" % repr(inFrame))
                inFrame = bytearray(inFrame)
                try:
                    header = KnxnetIPHeader(inFrame)
                except KnxnetIPHeaderValueError:
                    Logger().exception("UDPReceiver.run()", debug=True)


        #length = len(data)
        #checksum = 0x00
        #for i in range(length):
            ##checkSum = (byte)(checkSum ^ data[i]);
            #checksum = (checksum ^ data[i]) & 0xff

        #length -= 1
        ##if checksum == 0xff and \
        #if TFrame.MIN_LENGTH - self._parent.OVERHEAD <= length <= TFrame.MAX_LENGTH - self._parent.OVERHEAD and \
           #(fromPort != self._parent.localPort or fromAddr != self._parent.localAddr):
            ##byte[] lPDU = new byte[length + OVERHEAD];
            ##System.arraycopy(data, 0, lPDU, OVERHEAD, length);
            #lPDU = bytearray(self._parent.OVERHEAD + length)
            #lPDU[self._parent.OVERHEAD:] = data

            #domainAddr = lPDU[TFrame.DAL_BYTE] | lPDU[TFrame.DAH_BYTE] << 8
            #Logger().debug("UDPReceiver.run(): domainAddr=%s - %s" % (GroupAddress(domainAddr), IndividualAddress(domainAddr)))
            #if lPDU[TFrame.DAF_BYTE] & TFrame.DAF_MASK == TFrame.DAF_IA:  # domainAddr is an Individual Address
                #if domainAddr == self._parent.indivAddr:  # destination matches
                    #self._parent.tLSAP.putInFrame(lPDU)
            #else:  # domainAddr is an Group Address
                #self._parent.gadSet.acquire()
                #try:
                    #if domainAddr in self._parent.gadSet or GroupAddress("0/0/0") in self._parent.gadSet:
                        #self._parent.tLSAP.putInFrame(lPDU)
                #finally:
                    #self._parent.gadSet.release()

        #else:
            #Logger().error("UDPReceiver.run(): invalid checksum (%s)" % hex(checksum))


            except:
                Logger().exception("UDPReceiver.run()", debug=True)

        Logger().info("Stop")

    def stop(self):
        """ stop thread
        """
        Logger().info("Stop UDP Receiver")

        self._running = False



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
    @type _transmitter: L{Transmitter]

    @ivar _receiver: multicast receiver
    @type _receiver: L{Receiver}

    @ivar _gadSet: set of GAD
    @type _gadSet: L{GadSet}
    """
    def __init__(self, tLSAP, domainAddr=0, indivAddr="0.0.0", mcastAddr="224.0.23.12", mcastPort=3671):
        """

        @param tLSAP:
        @type tLSAP: L{TransceiverLSAP}

        @param domainAddr:
        @type domainAddr:

        @param indivAddr: own Individual Address (used when no source address is given in lSDU)
        @type indivAddr: L{IndividualAddress<pknyx.core.individualAddress>}

        @param mcastAddr: multicast address to bind to
        @type mcastAddr: str

        @param mcastPort: multicast address to bind to
        @type mcastPort: str

        raise UDPTransceiverValueError:
        """
        super(UDPTransceiver, self).__init__(tLSAP, domainAddr, indivAddr)

        self._domainAddr = domainAddr
        self._indivAddr = indivAddr
        self._mcastAddr = mcastAddr
        self._mcastPort = mcastPort

        # create transmitter and receiver
        self._transmitter = UDPTransmitter(self)
        try:
            self._receiver = UDPReceiver(self)
        except:
            Logger().exception("UDPTransceiver.__init__()")
            self._transmitter.cleanup()
            raise

        self._gadSet = GadSet()
        self.addGroupAddress(GroupAddress("0/0/0"))

    @property
    def tLSAP(self):
        return self._tLSAP

    @property
    def domainAddr(self):
        return self._domainAddr

    @property
    def indivAddr(self):
        return self._indivAddr

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
        return self._transmitter.localPort

    @property
    def gadSet(self):
        return self._gadSet

    def addGroupAddress(self, gad):
        """
        """
        if not isinstance(gad, GroupAddress):
            gad = GroupAddress(gad)

        self._gadSet.acquire()
        try:
            self._gadSet.add(gad)
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

    #def onReceive(self, frame, fromAddr, fromPort):
        #""" Frame receive handler

        #@param frame: received frame
        #@type frame: sequence
        #"""
        #frame = bytearray(frame)
        #try:
            #header = KnxnetIPHeader(frame)

        #conn.handleServiceType(h, data, offset + h.getStructLength(), fromAddr, fromPort)

        #except KnxnetIPHeaderValueError:
            #Logger().exception("UDPTransceiver.onReceive()", debug=True)

    def start(self):
        """
        """
        Logger().info("Start UDP Transceiver")

        self._transmitter.start()
        self._receiver.start()

    def stop(self):
        """
        """
        Logger().info("Stop UDP Transceiver")

        self._transmitter.stop()
        self._receiver.stop()


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
