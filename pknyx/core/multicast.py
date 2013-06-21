#!/bin/env python

import socket
import struct
import platform
import array
try:
    import fcntl
    NO_FCNTL = False
except ImportError:
    NO_FCNTL = True

SIOCGIFCONF = 0x8912
SIOCGIFFLAGS = 0x8913

IFF_MULTICAST = 0x1000


class IfConfigNotSupported(Exception):
    """
    """


def ifconfig():
    """ Fetch network stack configuration
    """
    if NO_FCNTL:
        raise IfConfigNotSupported ("No fcntl")

    class _interface:
        """
        """
        def __init__(self, name):
            """
            """
            self.name = name
            self.addresses = []
            self.up = False
            self.multicast = False

        @property
        def ip(self):
            try:
                return self.addresses[0]
            except IndexError:
                return None

    # An ugly hack to account for different ifreq sizes on different architectures
    arch = platform.architecture()[0]
    if arch == "32bit":
        offsets = (32, 32)
    elif arch == "64bit":
        offsets = (16, 40)
    else:
        raise OSError("unsupported architecture: %s" % (arch))

    # Get the list of all network interfaces
    _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    buffer = array.array ('B', '\0' * 128 * offsets[1])
    reply_length = struct.unpack ('iL', fcntl.ioctl(_socket.fileno(), SIOCGIFCONF, struct.pack('iL', 4096, buffer.buffer_info()[0])))[0]
    if_list = buffer.tostring()
    if_list = filter(lambda x: len(x[0]) > 0, [(if_list[i:i+offsets[0]].split('\0', 1)[0], socket.inet_ntoa(if_list[i+20:i+24])) for i in range(0, 4096, offsets[1])])

    iff = {}

    # Get ip addresses for each interface
    for (ifname, addr) in if_list:
        iff[ifname] = iff.get(ifname, _interface(ifname))
        flags, = struct.unpack('H', fcntl.ioctl(_socket.fileno(), SIOCGIFFLAGS, ifname + '\0'*256)[16:18])
        iff[ifname].addresses.append(addr)
        iff[ifname].up = bool(flags & 1)
        iff[ifname].multicast = bool(flags & IFF_MULTICAST)

    _socket.close()

    return iff


class InterfaceNotFound(Exception):
    """
    """


class DatagramReceiver(object):
    """A datagram socket wrapper.
    """
    iflist = None

    def __init__(self, address, port):
        """ Init DatagramReceiver object

        @param address:
        @type address:

        @param port:
        @type port:

        raise InterfaceNotFound:
        """
        super(DatagramReceiver, self).__init__()

        if address is not None and len(address) > 0:
            try:
                socket.inet_aton (address)
            except socket.error:
                try:
                    ifcfg = ifconfig()
                except IfConfigNotSupported:
                    raise InterfaceNotFound(address)

                if address in ifcfg:
                    iff = ifcfg[address]
                else:
                    raise InterfaceNotFound(address)
                self.localAddress = iff.ip
            else:
                self.localAddress = address
        else:
            self.localAddress = None

        if self.localAddress is None:
            self.localAddress = ""

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.address = address
        self.port = port
        self.multicast = False

        self.bind()

    def __unicast__(self):
        """
        """
        return "DatagramReceiver [{0}] {1}:{2}".format(self._socket, self.localAddress, self.port)

    def bind(self):
        """
        """
        self._socket.bind ((self.localAddress, self.port))

    def pipe(self, ostream):
        """

        @param ostream:
        @type ostream:
        """
        while True:
            self.pipeone (ostream)

    def pipeone(self, ostream, size=1500):
        """

        @param ostream:
        @type ostream:

        @param size:
        @type size: int
        """
        data, addr = self._socket.recvfrom(size)

        if ostream is not None:
            if callable(ostream): target = ostream
            else: target = ostream.write
            return target (data)
        else:
            return data

    def read(self, size=1500):
        """

        @param size:
        @type size: int
        """
        return self.pipeone (None, size)
    recv = read

    def cleanup(self):
        """
        """
        pass

    def close(self):
        """
        """
        self.cleanup()
        self._socket.close()


class Multicast(ReceiverDatagram):
    """
    """
    def __init__(self, bindAddrOrIface, mcastAddr, mcastPort, ttl=32, loop=1):
        """
        """
        super(Multicast, self).__init__ (bindAddrOrIface, mcastPort)

        self.ttl = ttl
        self.loop = loop
        self.mcastAddr = mcastAddr
        self.multicast = True

        self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.ttl)
        self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, self.loop)

        self._socket.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(self.localAddress))
        self._socket.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton (self.mcastAddr) + socket.inet_aton(self.localAddress))

    def __unicast__(self):
        """
        """
        return "MulticastReceiver [{0}] {1}:{2} @ {3}".format (self._socket, self.mcastAddr, self.port, self.localAddress)

    def bind(self):
        """
        """
        self._socket.bind(('', self.port))

    def cleanup(self):
        """
        """
        self._socket.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton (self.mcastAddr) + socket.inet_aton(self.localAddress))


def datagramReceiver(destination_address, destination_port, source_interface=None, ttl=32):
    multicast = ord(socket.inet_aton(destination_address)[0]) in range(224, 240)

    if multicast:
        receiver = Multicast(source_interface, destination_address, destination_port, ttl=ttl)
    else:
        receiver = DatagramReceiver(destination_address, destination_port)

    return receiver


class DatagramSender(DatagramReceiver):
    """
    """
    def __init__(self, srcAddr, srcPort, destAddr, destPort, ttl=32, loop=1):
        """
        """
        super(DatagramSender, self).__init__(srcAddr, srcPort)

        isMulticast = ord(socket.inet_aton(destAddr)[0]) in range(224, 240)
        if not isMulticast:
            raise Exception("invalid multicast address (%s)" % repr(destAddr))

        self._ttl = ttl
        self._loop = loop
        self._destAddr = destAddr
        self._destPort = destPort

        self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self._ttl)
        self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, self._loop)

    def write(self, data, *args):
        """

        @param data:
        @type data:
        """
        self._socket.sendto(data, (self._destAddr, self._destPort))
