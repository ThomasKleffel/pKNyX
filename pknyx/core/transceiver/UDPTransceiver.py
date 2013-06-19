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

__revision__ = "$Id: template.py 83 2013-06-05 14:30:02Z fma $"

import threading
import socket

from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger
from pknyx.core.groupAddress import GroupAddress
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
    """

    @ivar _sock:
    @type _sock: L{socket<socket>}

    @ivar _running: True if thread is running
    @type _running: bool

    @ivar _localPort: local port used by the socket
    @type _localPort: int
    """
    def __init__(self, tLSAP, mcastAddr, mcastPort):
        """

        @param tLSAP:
        @type tLSAP:
        """
        super(Transmitter, self).__init__(name="EIBStack UDP Transmitter")

        self._tLSAP = tLSAP

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #, socket.IPPROTO_UDP)
        #self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        self._sock.connect((mcastAddr, mcastPort))
        self._localPort = self._sock.getsockname()[1]  # getsockname() returns (host, port)

        self._running = False

        self.setDaemon(True)
        #self.start()

    @property
    def localPort(self):
        return setl._localPort

    def run(self):
        """
        """
        outFrame = DatagramPacket(bytearray(0), 0, mcastAddr, mcastPort)

        self._running = True
        while self._running:
            trm = self._tLSAP.getOutFrame()
            if trm is not None:
                lPDU = trm.frame

                lPDU[TFrame.CF_BYTE] |= TFrame.CF_L_DATA
                lPDU[TFrame.SAL_BYTE] = self._parent.individualAddress & 0xFF
                lPDU[TFrame.SAH_BYTE] = self._parent.individual >> 8
                checkSum = 0x00
                for i in range(self.OVERHEAD, len(lPDU)):
                    checkSum ^= lPDU[i]
                    checkSum &= 0xff

                #System.arraycopy(lPDU, self.OVERHEAD, lPDU, self.OVERHEAD-1, len(lPDU)-self.OVERHEAD )
                lPDU[self.OVERHEAD:] = lPDU[self.OVERHEAD-1:-1]
                lPDU[lPDU.length-1] = checkSum ^ 0xff  # What is ~ in java? Python inverts sign...

                outFrame.setData(lPDU, self.OVERHEAD-1, len(lPDU)-self.OVERHEAD+1)
                try:
                    self._sock.send(outFrame)
                    trm.result = Result.OK
                except IOException:
                    trm.result = Result.ERROR

                if trm.waitConfirm:
                    trm.acquire()
                    try:
                        trm.waitConfirm = False
                        trm.notify()
                    finally:
                        trm.release()

        self._sock.close()

    def cleanup(self):
        self.stop()
        self.join()

    def finalize(self):
        if self._running:
            self.cleanup()

    def stop(self):
        """ stop thread
        """
        self._running = False

    def isRunning(self):
        """ test if thread is running

        @return: True if running, False otherwise
        @rtype: bool
        """
        return self._running


class Receiver(threading.Thread):
    """

    @ivar _localPort: local port used by the socket
    @type _localPort: int
    """
    def __init__(self, tLSAP, mcastAddr, mcastPort, localPort):
        """

        @param tLSAP:
        @type tLSAP:

        @param localPort: local port used by the socket
        @type localPort: int
        """
        super(Receiver, self).__init__(name="EIBStack UDP Receiver")

        self._tLSAP = tLSAP
        self._localPort = localPort

        mSocket = new MulticastSocket(mcastPort)
        try:
            mSocket.joinGroup(mcastAddr)
        except:
            mSocket.close();
            raise

        self._running = False

        self.setDaemon(True)
        #self.start()

    def run(self):
        """
        """
        inFrame = DatagramPacket( new byte[TFrame.MAX_LENGTH], TFrame.MAX_LENGTH )

        self._running = True
        while self._running:
            try {
                inFrame.setLength( TFrame.MAX_LENGTH )
                mSocket.receive( inFrame )

                byte[] data = inFrame.getData()
                int length  = inFrame.getLength()
                byte checkSum = 0;
                for (byte i = 0; i < length; i++) {
                    checkSum = (byte)(checkSum ^ data[i]);
                }
                length--;
                if (   (checkSum == (byte)0xFF)
                    && (length >= TFrame.MIN_LENGTH - self.OVERHEAD)
                    && (length <= TFrame.MAX_LENGTH - self.OVERHEAD)
                    && (   (inFrame.getPort() != self._localPort)
                        || !inFrame.getAddress().equals( localAddr ))) {

                    byte[] lPDU = new byte[length + self.OVERHEAD];
                    System.arraycopy( data, 0, lPDU, self.OVERHEAD, length );

                    int da = (   ((lPDU[TFrame.DAL_BYTE] + 0x100) % 0x100)
                              + (((lPDU[TFrame.DAH_BYTE] + 0x100) % 0x100) << 8))
                    if ((lPDU[TFrame.DAF_BYTE] & TFrame.DAF_MASK) == TFrame.DAF_PA) {
                        if (da == ownPhysicalAddress) tLSAP.putInFrame( lPDU )
                    } else {
                        synchronized (gaSet) {
                            if (gaSet.contains( new Integer( da ) )) self._tLSAP.putInFrame( lPDU );
                        }
                    }
                }
            } catch (IOException e) {}
        }
    }

    private void cleanup() {
        running = false;
        try {
            mSocket.leaveGroup( mcastAddr );
        } catch (IOException e) {}
        mSocket.close();
    }

    protected void finalize() {
        if (running) cleanup();
    }
}



class UDPTransceiverValueError(PKNyXValueError):
    """
    """


class UDPTransceiver(Transceiver):
    """ UDPTransceiver class

    @ivar _localAddr:
    @type _localAddr:

    @ivar _localPort:
    @type _localPort:

    @ivar _mcastAddr:
    @type _mcastAddr:

    @ivar _mcastPort:
    @type _mcastPort:

    @ivar _transmitter:
    @type _transmitter:

    @ivar _receiver:
    @type _receiver:

    @ivar _gadSet: Set of GAD
    @type _gadSet: L{GadSet}
    """
    #MAX_LEN = TFrame.MAX_LENGTH

    def __init__(self, tLSAP, domainAddress, individualAddress, mcastURL="230.0.0.1"):
        """

        @param tLSAP:
        @type tLSAP:

        @param domainAddress:
        @type domainAddress:

        @param individualAddress: own Individual Address (use when not source address is given in lSDU)
        @type individualAddress: L{IndividualAddress<pknyx.core.individualAddress>}

        @param mcastURL:
        @type mcastURL:

        raise UDPTransceiverValueError:
        """
        super(UDPTransceiver, self).__init__(tLSAP, domainAddress, individualAddress)

        self._tLSAP = tLSAP

        colonIdx = mcastURL.indexOf(':')
        if colonIdx < 0:
            mcastAddr = InetAddress.getByName(mcastURL)
            mcastPort = 0xF625;
        else:
            mcastAddr = InetAddress.getByName(mcastURL.substring( 0, colonIdx ))
            try:
                mcastPort = Integer.parseInt( mcastURL.substring( colonIdx+1 ) );
            except NumberFormatException:
                raise IllegalArgumentException( "Malformed port number specified!" );

        if not mcastAddr.isMulticastAddress():
            raise IllegalArgumentException("Specified ip-address is not a multicast address!")

        if (mcastPort & 0xFFFF0000) != 0:
            raise IllegalArgumentException("Specified port out of range!")

        self._localAddr = InetAddress.getLocalHost()
        self._localPort = None

        # create transmitter and receiver
        transmitter = Transmitter(self, tLSAP, mcastAddr, mcastPort)
        try:
            receiver = Receiver(self, tLSAP, mcastAddr, mcastPort, transmitter.localPort)
        except:
            transmitter.cleanup()
            raise

        self._gadSet = GadSet()
        self._addGroupAddress(0, false)

    @property
    def tLSAP(self):
        return self._tLSAP

    @property
    def localPort(self):
        return self._localPort

    @localPort.setter
    def localPort(self, port):
        self._localPort = port

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
