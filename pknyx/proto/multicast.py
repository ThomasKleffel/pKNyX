# http://wiki.python.org/moin/UdpCommunication
# http://www.tldp.org/HOWTO/Multicast-HOWTO-6.html
# http://engineering.bittorrent.com/2013/02/04/udp-multicast-in-python-and-bittorrent-live/
# http://pymotw.com/2/socket/multicast.html
# http://twistedmatrix.com/documents/current/core/howto/udp.html#auto3
# http://stackoverflow.com/questions/603852/multicast-in-python

# ->>>>>>> https://pypi.python.org/pypi/py-multicast


# UDP multicast examples, Hugo Vincent, 2005-05-14.

import socket


def send(data, port=50000, addr='239.192.1.100'):
    """send(data[, port[, addr]]) - multicasts a UDP datagram.
    """

    # Create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Make the socket multicast-aware, and set TTL.
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20) # Change TTL (=20) to suit

    # Send the data
    s.sendto(data, (addr, port))


def recv(port=50000, addr="239.192.1.100", buf_size=1024):
    """recv([port[, addr[,buf_size]]]) - waits for a datagram and returns the data.
    """

    # Create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set some options to make it multicast-friendly
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except AttributeError:
        pass # Some systems don't support SO_REUSEPORT
    s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 20)
    s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)

    # Bind to the port
    s.bind(('', port))

    # Set some more multicast options
    intf = socket.gethostbyname(socket.gethostname())
    s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(intf))
    s.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton(intf))

    # Receive the data, then unregister multicast receive membership, then close the port
    data, sender_addr = s.recvfrom(buf_size)
    s.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton('0.0.0.0'))
    s.close()
    return data

# ----------------------------------------------------------------------------------------------------------

class McastSocket(socket.socket):
    """
    """
    def __init__(self, local_port, reuse=False):
        """
        """
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        if reuse:
            self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if hasattr(socket, "SO_REUSEPORT"):
                self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                self.bind(('', local_port))

    def mcast_add(self, addr, iface):
        sock.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        socket.inet_aton(mcast_addr) + socket.inet_aton(mcast_iface))


# Then to listen to multicast events locally
sock = McastSocket(local_port=12345, reuse=1)
sock.mcast_add('239.192.9.9', '127.0.0.1')

# ----------------------------------------------------------------------------------------------------------

import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 4242))
# wrong: mreq = struct.pack("sl", socket.inet_aton("224.51.105.104"), socket.INADDR_ANY)
mreq = struct.pack("=4sl", socket.inet_aton("224.51.105.104"), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    print sock.recv(10240)

# ----------------------------------------------------------------------------------------------------------

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
sock.sendto("robot", ("239.192.0.100", 1000))

# ----------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------

