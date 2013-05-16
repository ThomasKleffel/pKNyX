# -*- coding: utf-8 -*-

""" Python KNX framework.

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

This module implements a head position publisher mecanism. It listens on a socket, waiting for incoming clients
connection. Each time the head position changes, it publishes the new position to all connected clients.

Implements
==========

 - PublisherHandler
 - PublisherServer
 - Publisher

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import time
import threading
import socket
import SocketServer

from pknyx.common import config
from pknyx.common.loggingServices import Logger
#from pknyx.controller.spy import Spy


class PublisherHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        Logger().debug("PublisherHandler.handle(): new connection from %s:%d" % self.client_address)
        Spy().newPosSignal.connect(self.__newPosition)
        Spy().execute(force=True)

        # Wait forever
        while Spy().isRunning():
            time.sleep(.1)

    def __newPosition(self, yaw, pitch):
        """ Signal callback.
        """
        #Logger().debug("PublisherHandler.__newPosition(): yaw=%.1f, pitch=%.1f" % (yaw, pitch))
        try:
            #Logger().debug("PublisherHandler.__newPosition(): sending to %s:%d" % self.client_address)
            self.request.sendall("%f, %f" % (yaw, pitch))
        except socket.error, msg:
            Logger().exception("PublisherHandler.__newPosition()")
            self.request.close()
            Spy().newPosSignal.disconnect(self.__newPosition)
            Logger().debug("PublisherHandler.handle(): connection from %s:%d closed" % self.client_address)


class PublisherServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        Logger().exception("PublisherServer.handle_error()")
        Logger().error("Error while handling request from ('%s', %d)" % client_address)


class Publisher(threading.Thread):
    """ Publisher object.
    """
    def __init__(self):
        """ Init the publisher.
        """
        threading.Thread.__init__(self)
        self.setDaemon(1)
        self.setName("Publisher")
        try:
            self.__server = PublisherServer((config.PUBLISHER_HOST, config.PUBLISHER_PORT), PublisherHandler)
        except socket.error, error:
            Logger().exception("Publisher.__init__()")
            err, msg = tuple(error)
            raise socket.error(msg)

    def run(self):
        """ Main entry of the thread.
        """
        Logger().info("Starting Publisher...")
        self.__server.serve_forever()
        Logger().info("Publisher stopped")
