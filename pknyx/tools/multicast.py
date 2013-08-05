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

Multicast tool to send read/write request on group address.

Implements
==========

 - B{Multicast}
 - B{MulticastValueError}

Documentation
=============

This script is used to send/receive multicast requests. It mimics what the stack does.

@todo: make the same using the stack.

Usage
=====

Usage: multicast.py -w [options] -> send a write request to group address
       multicast.py -r [options] -> send a read request to group address

Options:
  -h, --help            show this help message and exit
  -l LEVEL, --debug-level=LEVEL
                        debug level
  -g GAD, --group-address=GAD
                        group address
  -d DPTID, --dptId=DPTID
                        DPTID to use to encode data
  -s SRCADDR, --srcAddr=SRCADDR
                        source address to use

  Write:
    -v VALUE, --value=VALUE
                        value to send

  Read:

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import sys
import time
import optparse
import threading

from pknyx.common.exception import PKNyXValueError
from pknyx.services.logger import Logger
from pknyx.core.dptXlator.dptId import DPTID
from pknyx.core.dptXlator.dptXlatorFactory import DPTXlatorFactory
from pknyx.stack.priority import Priority
from pknyx.stack.groupAddress import GroupAddress
from pknyx.stack.individualAddress import IndividualAddress
from pknyx.stack.knxnetip.knxNetIPHeader import KNXnetIPHeader
from pknyx.stack.cemi.cemiLData import CEMILData
from pknyx.stack.multicastSocket import MulticastSocket
from pknyx.stack.layer7.apdu import APDU
from pknyx.stack.layer7.apci import APCI
from pknyx.stack.layer4.tpci import TPCI

from pknyx.core.ets import ETS
from pknyx.core.group import Group
from pknyx.stack.stack import Stack




class MulticastValueError(PKNyXValueError):
    """
    """


class Multicast(object):
    """ Multicast class

    @ivar _xxx:
    @type _xxx:
    """
    def __init__(self, src="0.0.0", mcastAddr="224.0.23.12", mcastPort=3671):
        """

        @param xxx:
        @type xxx:

        raise MulticastValueError:
        """
        super(Multicast, self).__init__()

        if not isinstance(src, IndividualAddress):
            src = IndividualAddress(src)
        self._src = src
        self._mcastAddr = mcastAddr
        self._mcastPort = mcastPort

        self._receiverSock = MulticastSocket(mcastPort)
        self._receiverSock.joinGroup(mcastAddr)

    def write(self, gad, value, dptId="1.001", priority=Priority("low"), hopCount=6):
        """ Send a write request
        """
        if not isinstance(gad, GroupAddress):
            gad = GroupAddress(gad)

        sock = MulticastSocket(self._mcastPort, self._mcastAddr)

        dptXlator = DPTXlatorFactory().create(dptId)
        type_ = type(dptXlator.dpt.limits[0])  # @todo: implement this in dptXlators
        value = type_(value)
        frame = dptXlator.dataToFrame(dptXlator.valueToData(value))

        # Application layer (layer 7)
        aPDU = APDU.makeGroupValue(APCI.GROUPVALUE_WRITE, frame, dptXlator.typeSize)

        # Transport layer (layer 4)
        tPDU = aPDU
        tPDU[0] |= TPCI.UNNUMBERED_DATA

        # Network layer (layer 3)
        nPDU = bytearray(len(tPDU) + 1)
        nPDU[0] = len(tPDU) - 1
        nPDU[1:] = tPDU

        # Link layer (layer 2)
        cEMI = CEMILData()
        cEMI.messageCode = CEMILData.MC_LDATA_IND
        cEMI.sourceAddress = self._src
        cEMI.destinationAddress = gad
        cEMI.priority = priority
        cEMI.hopCount = hopCount
        cEMI.npdu = nPDU

        cEMIFrame = cEMI.frame
        cEMIRawFrame = cEMIFrame.raw
        header = KNXnetIPHeader(service=KNXnetIPHeader.ROUTING_IND, serviceLength=len(cEMIRawFrame))
        frame = header.frame + cEMIRawFrame

        sock.transmit(frame)

    def read(self, gad, dptId="1.001", timeout=3, priority=Priority("low"), hopCount=6):
        """ Send a read request and wait for answer
        """
        if not isinstance(gad, GroupAddress):
            gad = GroupAddress(gad)

        self._receiverSock.timeout = timeout

        sock = MulticastSocket(self._mcastPort, self._mcastAddr)

        # Application layer (layer 7)
        aPDU = APDU.makeGroupValue(APCI.GROUPVALUE_READ)

        # Transport layer (layer 4)
        tPDU = aPDU
        tPDU[0] |= TPCI.UNNUMBERED_DATA

        # Network layer (layer 3)
        nPDU = bytearray(len(tPDU) + 1)
        nPDU[0] = len(tPDU) - 1
        nPDU[1:] = tPDU

        # Link layer (layer2)
        cEMI = CEMILData()
        cEMI.messageCode = CEMILData.MC_LDATA_IND
        cEMI.sourceAddress = self._src
        cEMI.destinationAddress = gad
        cEMI.priority = priority
        cEMI.hopCount = hopCount
        cEMI.npdu = nPDU

        cEMIFrame = cEMI.frame
        cEMIRawFrame = cEMIFrame.raw
        header = KNXnetIPHeader(service=KNXnetIPHeader.ROUTING_IND, serviceLength=len(cEMIRawFrame))
        frame = header.frame + cEMIRawFrame

        sock.transmit(frame)

        # Link layer (layer2)
        receivedData = None
        receivedStatus = None
        while True:
            try:
                inFrame, (fromAddr, fromPort) = self._receiverSock.receive()
                Logger().debug("Multicast.read(): inFrame=%s (%s, %d)" % (repr(inFrame), fromAddr, fromPort))
                inFrame = bytearray(inFrame)

                header = KNXnetIPHeader(inFrame)
                Logger().debug("Multicast.read(): KNXnetIP header=%s" % repr(header))

                frame = inFrame[KNXnetIPHeader.HEADER_SIZE:]
                Logger().debug("Multicast.read(): frame=%s" % repr(frame))
                cEMI = CEMILData(frame)
                Logger().debug("Multicast.read(): cEMI=%s" % cEMI)

                destAddr = cEMI.destinationAddress
                if isinstance(cEMI.destinationAddress, GroupAddress):
                    receivedData = cEMI
                    receivedStatus = 0
                elif isinstance(destAddr, IndividualAddress):
                    Logger().warning("Multicast.read(): unsupported destination address type (%s)" % repr(destAddr))
                else:
                    Logger().warning("Multicast.read(): unknown destination address type (%s)" % repr(destAddr))

            except:
                Logger().exception("Multicast.read()")
                raise

            # Network layer (layer 3)
            if cEMI is not None:
                if cEMI.messageCode == CEMILData.MC_LDATA_IND:
                    hopCount = cEMI.hopCount
                    mc = cEMI.messageCode
                    src = cEMI.sourceAddress
                    dest = cEMI.destinationAddress
                    priority = cEMI.priority
                    hopCount = cEMI.hopCount

                    if dest == gad and src != self._src:  # Avoid loop

                        # Transport layer (layer 4)
                        tPDU = cEMI.npdu[1:]
                        if isinstance(dest, GroupAddress) and not dest.isNull:
                            tPCI = tPDU[0] & 0xc0
                            if tPCI == TPCI.UNNUMBERED_DATA:

                                # Application layer (layer 7)
                                aPDU = tPDU
                                aPDU[0] &= 0x3f
                                length = len(aPDU) - 2
                                if length >= 0:
                                    aPCI = aPDU[0] << 8 | aPDU[1]
                                    if (aPCI & APCI._4) == APCI.GROUPVALUE_WRITE:
                                        Logger().debug("Multicast.read(): GROUPVALUE_WRITE ignored")
                                        continue

                                    elif (aPCI & APCI._4) == APCI.GROUPVALUE_READ:
                                        Logger().debug("Multicast.read(): GROUPVALUE_READ ignored")
                                        continue

                                    elif (aPCI & APCI._4) == APCI.GROUPVALUE_RES:
                                        data = APDU.getGroupValue(aPDU)

                                        dptXlator = DPTXlatorFactory().create(dptId)
                                        value = dptXlator.dataToValue(dptXlator.frameToData(data))
                                        return value


def write(gad, value, dptId="1.001", src="0.0.0",  priority=Priority("low"), hopCount=6):
    """
    """

def read(gad, dptId="1.001", src="0.0.0", timeout=3, priority=Priority("low"), hopCount=6):
    """
    """
    class DummyGroupObject(object):
        """
        """
        def __init__(self, dptId="1.001"):
            """
            """
            super(DummyGroupObject, self).__init__()

            self._dptXLator = DPTXlatorFactory().create(dptId)

        #def onWrite(self, src, gad, data):
            #Logger().debug("DummyGroupObject.onWrite(): src=%s, data=%s" % (src, repr(data)))

            ## Check if datapoint should be updated
            #if self._flags.write:  # and data != self.datapoint.data:
                #self.datapoint.frame = data

        #def onRead(self, src, gad):
            #Logger().debug("DummyGroupObject.onRead(): src=%s" % src)

            ## Check if data should be send over the bus
            #if self._flags.communicate:
                #if self._flags.read:
                    #frame, size = self._datapoint.frame
                    #self._group.groupValueResponse(self._priority, frame, size)

        def onResponse(self, src, gad, data):
            Logger().debug("DummyGroupObject.onResponse(): src=%s, data=%s" % (src, repr(data)))

            value = self._dptXLator.dataToValue(self._dptXLator.frameToData(data))
            Logger().info(value)


    stack = Stack(individualAddress=src)
    dummy = DummyGroupObject(dptId)
    group = stack.agds.subscribe(gad, dummy)

    stack.start()
    group.groupValueRead(priority)
    time.sleep(1)
    stack.stop()


def main():
    usage = "%prog -w [options] -> send a write request to group address\n"
    usage += "       %prog -r [options] -> send a read request to group address"

    # Common options
    parser = optparse.OptionParser(usage)
    parser.add_option("-l", "--debug-level", action="store", dest="debugLevel", default="info", metavar="LEVEL",
                      help="debug level")
    parser.add_option("-g", "--group-address", action="store", type="string", dest="gad", metavar="GAD",
                      help="group address")
    parser.add_option("-d", "--dptId", action="store", type="string", dest="dptId", default="1.xxx",
                      help="DPTID to use to encode data")
    parser.add_option("-s", "--srcAddr", action="store", type="string", dest="srcAddr", default="0.0.0",
                      help="source address to use")

    # Write GA options
    groupWrite = optparse.OptionGroup(parser, "Write")
    groupWrite.add_option("-w", "--write", action="store_true", dest="write", default=False,
                          help=optparse.SUPPRESS_HELP)
    groupWrite.add_option("-v", "--value", action="store", type="string", dest="value",
                          help="value to send")
    parser.add_option_group(groupWrite)

    # Read GA options
    groupRead = optparse.OptionGroup(parser, "Read")
    groupRead.add_option("-r", "--read", action="store_true", dest="read", default=False,
                         help=optparse.SUPPRESS_HELP)
    parser.add_option_group(groupRead)

    # Parse
    options, args = parser.parse_args()

    # Check commands validity
    if not (options.write or options.read):
        parser.error("no command specified")
    elif not options.write ^ options.read:
        parser.error("multiple commands specified")
    if options.gad is None:
        parser.error("no group address specified")
    if options.write and options.value is None:
        parser.error("must give a value when sending a write request")

    #print("DEBUG::main(): options=%s, args=%s" % (options, args))

    Logger().setLevel(options.debugLevel)
    if options.write:
        multicast = Multicast(options.srcAddr)
        multicast.write(options.gad, options.value, options.dptId)
    elif options.read:
        #multicast = Multicast(options.srcAddr)
        #value = multicast.read(options.gad, options.dptId)
        #print value
        read(options.gad, options.dptId)


if __name__ == '__main__':
    main()
