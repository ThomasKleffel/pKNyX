# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{pKNyX} (U{http://www.pknyx.org}) is Copyright:
  - (C) 2013 Frédéric Mantegazza

Licensed under the EUPL, Version 1.1 or - as soon they will be approved by
the European Commission - subsequent versions of the EUPL (the "Licence");
You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:

 - U{http://ec.europa.eu/idabc/eupl}

Unless required by applicable law or agreed to in writing, software distributed
under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.

See the Licence for the specific language governing permissions and limitations
under the Licence.

Module purpose
==============

KNX Bus management

Implements
==========

 - B{VBusMonitor2}

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""
__revision__ = "$Id$"

import os
import sys
import subprocess

from pknyx.common.loggingServices import Logger
from pknyx.backends.eibd.eibConnection import EIBConnection, EIBBuffer, EIBAddr


class EIBAddress(EIBAddr):
    def toGroup(self):
        return "%d/%d/%d" % ((self.data >> 11) & 0x1f, (self.data >> 8) & 0x07, (self.data) & 0xff)

    def toPhysical(self):
        return "%d.%d.%d" % ((self.data >> 12) & 0x0f, (self.data >> 8) & 0x0f, (self.data) & 0xff)


class VBusMonitor2(object):
    """
    """
    def __init__(self, url):
        """
        """
        super(VBusMonitor2, self).__init__()

        self._connection = EIBConnection()
        err = self._connection.EIBSocketURL(url)
        if err:
            Logger().critical("VBusMonitor2.__init__(): %s" % os.strerror(self._connection.errno))
            Logger().critical("VBusMonitor2.__init__(): call to EIBConnection.EIBSocketURL() failed (err=%d)" % err)
            sys.exit(-1)

    def run(self):
        """
        """
        err = self._connection.EIBOpenVBusmonitor()
        if err:
            Logger().critical("VBusMonitor2.run(): %s" % os.strerror(self._connection.errno))
            Logger().critical("VBusMonitor2.run(): call to EIBConnection.EIBOpenVBusmonitor() failed (err=%d)" % err)
            sys.exit(-1)
        while True:
            buffer_ = EIBBuffer()
            lenght = self._connection.EIBGetBusmonitorPacket(buffer_)
            if length == -1:
                Logger().critical("VBusMonitor2.run(): %s" % os.strerror(self._connection.errno))
                Logger().critical("VBusMonitor2.run(): call to EIBConnection.EIBGetBusmonitorPacket() failed")
                sys.exit(-1)
            print buffer_


class KNX(object):
    """ From Domogik project
    """
    def __init__(self):
        """
        """
        super(KNX, self).__init__()

    def listen(self):
        #command = "groupsocketlisten ip:linknxwebbox"
        command = "vbusmonitor2 ip:linknxwebbox"
        self.pipe = subprocess.Popen(command,
                     shell = True,
                     bufsize = 1024,
                     stdout = subprocess.PIPE
                     ).stdout
        self._read = True

        while self._read:
            data = self.pipe.readline()
            if not data:
                break
            print repr(data)

    def stop_listen(self):
        self._read = False


if __name__ == "__main__":
    vBusMonitor2 = VBusMonitor2("ip:linknxwebbox")
    vBusMonitor2.run()

    #device = "ipt:192.168.1.148"
    #obj = KNX()
    #obj.listen()
