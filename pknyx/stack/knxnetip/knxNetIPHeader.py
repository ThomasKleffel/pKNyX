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

Implements
==========

 - B{}

Documentation
=============

KNXnet/IP header is used to encapsulate cEMI frames.

It contains:

 - header length (8bits) - 0x06
 - protocol version (8 bits) - 0x10
 - service type identifier (16 bits)
 - total frame length (16 bits)

Usage
=====

>>> header = KnxnetIPHeader(frame="\x06\x10\x05\x30\x00\x11\x29\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80")
>>> header.serviceType
1328
>>> header.serviceName
'routing.ind'
>>> header.totalLength
17
>> header.byteArray
bytearray(b'\x06\x10\x05\x30\x00\x11')

>>> data = "\x29\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80\x00"
>>> header = KnxnetIPHeader(serviceType=KnxnetIPHeader.ROUTING_IND, totalLength=KnxnetIPHeader.HEADER_SIZE+len(data))
>>> header.totalLength
18
>> header.byteArray
bytearray(b'\x06\x10\x05\x30\x00\x12')

@author: Frédéric Mantegazza
@author: B. Malinowsky
@copyright: (C) 2013 Frédéric Mantegazza
@copyright: (C) 2006, 2011 B. Malinowsky
@license: GPL
"""

__revision__ = "$Id$"

import struct

from pknyx.common.exception import PKNyXValueError
from pknyx.logging.loggingServices import Logger


class KnxnetIPHeaderValueError(PKNyXValueError):
    """
    """


class KnxnetIPHeader(object):
    """ KNXNet/IP head object

    @ivar _serviceType: Service type identifier
    @type _serviceType: int

    @ivar _totalLength: total length of the KNXNet/IP telegram
    @type _totalLength: int

    raise KnxnetIPHeaderValueError:
    """

    # Services type identifier values
    CONNECT_REQ = 0x0205
    CONNECT_RES = 0x0206
    CONNECTIONSTATE_REQ = 0x0207
    CONNECTIONSTATE_RES = 0x0208
    DISCONNECT_REQ = 0x0209
    DISCONNECT_RES = 0x020A
    DESCRIPTION_REQ = 0x0203
    DESCRIPTION_RES = 0x204
    SEARCH_REQ = 0x201
    SEARCH_RES = 0x202
    DEVICE_CONFIGURATION_REQ = 0x0310
    DEVICE_CONFIGURATION_ACK = 0x0311
    TUNNELING_REQ = 0x0420
    TUNNELING_ACK = 0x0421
    ROUTING_IND = 0x0530
    ROUTING_LOST_MSG = 0x0531

    SERVICE_TYPES = (CONNECT_REQ, CONNECT_RES,
                     CONNECTIONSTATE_REQ, CONNECTIONSTATE_RES,
                     DISCONNECT_REQ, DISCONNECT_RES,
                     DESCRIPTION_REQ, DESCRIPTION_RES,
                     SEARCH_REQ, SEARCH_RES,
                     DEVICE_CONFIGURATION_REQ, DEVICE_CONFIGURATION_ACK,
                     TUNNELING_REQ, TUNNELING_ACK,
                     ROUTING_IND, ROUTING_LOST_MSG
                     )

    HEADER_SIZE = 0x06
    KNXNETIP_VERSION = 0x10

    def __init__(self, frame=None, serviceType=None, totalLength=0):
        """ Creates a new KNXnet/IP header

        Header can be loaded either from frame or from sratch

        @param frame: byte array with contained KNXnet/IP frame
        @type frame: sequence

        @param serviceType: service type identifier
        @type serviceType: int

        @param totalLength: total length of the frame this header encapsulates
        @type totalLength: int

        @raise KnxNetIPHeaderValueError:
        """

        # Check params
        if frame is not None and serviceType is not None:
            raise KnxnetIPHeaderValueError("can't give both frame and service type")

        if frame is not None:
            frame = bytearray(frame)
            if len(frame) < KnxnetIPHeader.HEADER_SIZE:
                    raise KnxnetIPHeaderValueError("frame too short for KNXnet/IP header (%d)" % len(frame))

            headersize = frame[0] & 0xff
            if headersize != KnxnetIPHeader.HEADER_SIZE:
                raise KnxnetIPHeaderValueError("wrong header size (%d)" % headersize)

            protocolVersion = frame[1] & 0xff
            if protocolVersion != KnxnetIPHeader.KNXNETIP_VERSION:
                raise KnxnetIPHeaderValueError("unsupported KNXnet/IP protocol (%d)" % protocolVersion)

            self._serviceType = (frame[2] & 0xff) << 8 | (frame[3] & 0xff)
            if self._serviceType not in KnxnetIPHeader.SERVICE_TYPES:
                raise KnxnetIPHeaderValueError("unsupported service type (%d)" % self._serviceType)

            self._totalLength = (frame[4] & 0xff) << 8 | (frame[5] & 0xff)
            if len(frame) != self._totalLength:
                raise KnxnetIPHeaderValueError("wrong frame length (%d; should be %d)" % (len(frame), self._totalLength))

        elif serviceType is not None:
            if serviceType not in KnxnetIPHeader.SERVICE_TYPES:
                raise KnxnetIPHeaderValueError("unsupported service type (%d)" % self._serviceType)
            if not totalLength:
                raise KnxnetIPHeaderValueError("total length missing")
            self._serviceType = serviceType
            self._totalLength = totalLength

        else:
            raise KnxnetIPHeaderValueError("must give either frame or service type")

    @property
    def serviceType(self):
        return self._serviceType

    @property
    def totalLength(self):
        return self._totalLength

    @property
    def byteArray(self):
        s = struct.pack(">2B2H", KnxnetIPHeader.HEADER_SIZE, KnxnetIPHeader.KNXNETIP_VERSION, self._serviceType, self._totalLength)
        return bytearray(s)

    @property
    def serviceName(self):
        if self._serviceType == KnxnetIPHeader.CONNECT_REQ:
            return "connect.req"
        elif self._serviceType == KnxnetIPHeader.CONNECT_RES:
            return "connect.res"
        elif self._serviceType == KnxnetIPHeader.CONNECTIONSTATE_REQ:
            return "connectionstate.req"
        elif self._serviceType == KnxnetIPHeader.CONNECTIONSTATE_RES:
            return "connectionstate.res"
        elif self._serviceType == KnxnetIPHeader.DISCONNECT_REQ:
            return "disconnect.req"
        elif self._serviceType == KnxnetIPHeader.DISCONNECT_RES:
            return "disconnect.res"
        elif self._serviceType == KnxnetIPHeader.DESCRIPTION_REQ:
            return "description.req"
        elif self._serviceType == KnxnetIPHeader.DESCRIPTION_RES:
            return "description.res"
        elif self._serviceType == KnxnetIPHeader.SEARCH_REQ:
            return "search.req"
        elif self._serviceType == KnxnetIPHeader.SEARCH_RES:
            return "search.res"
        elif self._serviceType == KnxnetIPHeader.DEVICE_CONFIGURATION_REQ:
            return "device-configuration.req"
        elif self._serviceType == KnxnetIPHeader.DEVICE_CONFIGURATION_ACK:
            return "device-configuration.ack"
        elif self._serviceType == KnxnetIPHeader.TUNNELING_REQ:
            return "tunneling.req"
        elif self._serviceType == KnxnetIPHeader.TUNNELING_ACK:
            return "tunneling.ack"
        elif self._serviceType == KnxnetIPHeader.ROUTING_IND:
            return "routing.ind"
        elif self._serviceType == KnxnetIPHeader.ROUTING_LOST_MSG:
            return "routing-lost.msg"
        else:
            return "unknown/unsupported service"


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class KnxnetIPHeaderTestCase(unittest.TestCase):

        def setUp(self):
            self._header1 = KnxnetIPHeader(frame="\x06\x10\x05\x30\x00\x11\x29\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80")
            data = "\x29\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80\x00"
            self._header2 = KnxnetIPHeader(serviceType=KnxnetIPHeader.ROUTING_IND,
                                           totalLength=KnxnetIPHeader.HEADER_SIZE+len(data))

        def tearDown(self):
            pass

        def test_constructor(self):
            with self.assertRaises(KnxnetIPHeaderValueError):
                KnxnetIPHeader(frame="\x06\x10\x05\x30\x00")  # frame length
            with self.assertRaises(KnxnetIPHeaderValueError):
                KnxnetIPHeader(frame="\x05\x10\x05\x30\x00\x11\x29\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80")  # header size
            with self.assertRaises(KnxnetIPHeaderValueError):
                KnxnetIPHeader(frame="\x06\x11\x05\x30\x00\x11\x29\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80")  # protocol version
            with self.assertRaises(KnxnetIPHeaderValueError):
                KnxnetIPHeader(frame="\x06\x10\x05\x31\x00\x11\x29\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80")  # service type
            with self.assertRaises(KnxnetIPHeaderValueError):
                KnxnetIPHeader(frame="\x06\x10\x05\x30\x00\x10\x29\x00\xbc\xd0\x11\x0e\x19\x02\x01\x00\x80")  # total length

        def test_serviceType(self):
            self.assertEqual(self._header1.serviceType, KnxnetIPHeader.ROUTING_IND)
            self.assertEqual(self._header2.serviceType, KnxnetIPHeader.ROUTING_IND)

        def test_totalLength(self):
            self.assertEqual(self._header1.totalLength, 17)
            self.assertEqual(self._header2.totalLength, 18)

        def test_byteArray(self):
            self.assertEqual(self._header1.byteArray, "\x06\x10\x05\x30\x00\x11")
            self.assertEqual(self._header2.byteArray, "\x06\x10\x05\x30\x00\x12")

        def test_serviceName(self):
            self.assertEqual(self._header1.serviceName, "routing.ind")
            self.assertEqual(self._header2.serviceName, "routing.ind")

    unittest.main()
