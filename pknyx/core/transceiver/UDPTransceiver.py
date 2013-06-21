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
from pknyx.common.loggingServices import Logger
from pknyx.core.groupAddress import GroupAddress
from pknyx.core.multicast import MulticastSocket
from pknyx.core.transceiver.transceiver import Transceiver
from pknyx.core.transceiver.tFrame import TFrame


class GadSet(threading.Condition, set):
    """
    """
    def __init__(self):
        """
        """
        super(GadSet, self).__init__()


class Transmitter(threading.Thread):
    """ Transmitter thread of the transceiver

    @ivar _sock: multicast socket
    @type _sock: L{MulticastSocket}

    @ivar _running: True if thread is running
    @type _running: bool

    @ivar _localPort: local port used by the socket
    @type _localPort: int
    """
    def __init__(self, parent, tLSAP, mcastAddr, mcastPort):
        """

        @param parent:
        @type parent:

        @param tLSAP:
        @type tLSAP: L{TransceiverLSAP}
        """
        super(Transmitter, self).__init__(name="EIBStack UDP Transmitter")

        self._parent = parent
        self._tLSAP = tLSAP
        self._mcastAddr = mcastAddr
        self._mcastPort = mcastPort

        self._sock = MulticastSocket(mcastPort, mcastAddr)

        self._running = False

        self.setDaemon(True)
        #self.start()

    @property
    def localPort(self):
        return setl._sock.localPort

    def run(self):
        """
        """
        self._running = True
        while self._running:
            transmission = self._tLSAP.getOutFrame()
            if transmission is not None:
                lPDU = transmission.frame
                lPDU[TFrame.CF_BYTE] |= TFrame.CF_L_DATA
                lPDU[TFrame.SAH_BYTE] = self._parent.indivAddr.high
                lPDU[TFrame.SAL_BYTE] = self._parent.indivAddr.low

                checksum = 0x00
                for i in range(self.OVERHEAD, len(lPDU)):
                    checksum ^= lPDU[i]
                    checksum &= 0xff

                #System.arraycopy(lPDU, self.OVERHEAD, lPDU, self.OVERHEAD-1, len(lPDU)-self.OVERHEAD )
                lPDU[self.OVERHEAD:] = lPDU[self.OVERHEAD-1:-1]
                lPDU[lPDU.length-1] = checksum ^ 0xff  # What is ~ in java? Python inverts sign...

                outFrame = lPDU[self.OVERHEAD-1:]
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

        self._sock.close()

    def cleanup(self):
        """
        """
        self.stop()
        self.join()

    def finalize(self):
        """
        """
        if self.isAlive():
            self.cleanup()

    def stop(self):
        """ stop thread
        """
        self._running = False


class Receiver(threading.Thread):
    """

    @ivar _localPort: local port used by the socket
    @type _localPort: int
    """
    def __init__(self, parent):
        """

        @param parent:
        @type parent:
        """
        super(Receiver, self).__init__(name="EIBStack UDP Receiver")

        self._parent = parent

        self._mSock = MulticastSocket(self._parent.mcastPort)
        try:
            self._mSock.joinGroup(self._parent.mcastAddr)
        except:
            self._mSock.close();
            raise

        self._running = False

        self.setDaemon(True)
        #self.start()

    def run(self):
        """
        """
        self._running = True
        while self._running:
            try:
                inFrame = self._mSock.receive()
                data, (fromAddr, fromPort) = inFrame

                checksum = 0x00
                for i in range(len(data)):
                    checksum ^= data[i]
                    checksum &= 0xff

                length = len(data) - 1
                if checksum == 0xff and \
                   TFrame.MIN_LENGTH - self.OVERHEAD <= length <= TFrame.MAX_LENGTH - self.OVERHEAD and \
                   (fromPort != self._parent.localPort or fromAddr != self._parent.localAddr):
                    lPDU = bytearray(length + self.OVERHEAD)
                    lPDU[self.OVERHEAD:] = data
                    domainAddr = lPDU[TFrame.DAL_BYTE] | lPDU[TFrame.DAH_BYTE] << 8
                    if lPDU[TFrame.DAF_BYTE] & TFrame.DAF_MASK == TFrame.DAF_IA:
                        if domainAddr == self._parent.indivAddr:
                            self._parent.tLSAP.putInFrame(lPDU)
                    else:
                        self._parent.gadSet.acquire()
                        try:
                            if domainAddr in self._parent.gadSet:
                                self._parent.tLSAP.putInFrame(lPDU)
                        finally:
                            self._parent.gadSet.release()

            except Exception:
                Logger().exception("Receiver.run()", debug=True)

    def cleanup(self):
        """
        """
        self.stop()
        #self.join()
        try:
            self._mSock.leaveGroup(self._mcastAddr)
        except Exception:
            Logger().exception("Receiver.cleanup()", debug=True)
        self._mSock.close()

    def finalize(self):
        """
        """
        if self.isAlive():
            cleanup();

    def stop(self):
        """ stop thread
        """
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
    def __init__(self, tLSAP, domainAddr="0.0.0", indivAddr="0.0.0", mcastAddr="230.0.0.1", mcastPort=0xf625):
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

        self._mcastAddr = mcastAddr
        self._mcastPort = mcastPort

        # create transmitter and receiver
        transmitter = Transmitter(self)
        self._localPort = transmitter.localPort
        try:
            receiver = Receiver(self)
        except:
            transmitter.cleanup()
            raise

        self._gadSet = GadSet()
        self._addGroupAddress(GroupAddress("0/0/0"), false)  # ????

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
        return self._localPort

    @property
    def gadSet(self):
        return self._gadSet

    def cleanup(self, ):
        """ Cleanup transmission
        """
        self._transmitter.cleanup()
        self._receiver.cleanup()

    def addGroupAddress(self, gad, sendL2Ack=True):  ## WTF?
        """
        """
        if not isinstance(GroupAddress, gad):
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
