# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{pKNyX} (U{http://www.pknyx.org}) is Copyright:
  - (C) 2013-2015 Frédéric Mantegazza

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

Device (process) management.

Implements
==========

 - B{Device}

Documentation
=============

The Device is the top-level object. It runs as a process. It mainly encapsulates some initialisations.

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common import config
from pknyx.common.exception import PKNyXValueError
from pknyx.common.frozenDict import FrozenDict
from pknyx.services.logger import Logger
from pknyx.stack.stack import Stack

import time


class DeviceValueError(PKNyXValueError):
    """
    """


class Device(object):
    """ Device class definition.
    """
    def __new__(cls, *args, **kwargs):
        """ Init the class with all available types for this DPT
        """
        self = super(Device, cls).__new__(cls)

        # Retreive all parents classes, to get all objects defined there
        classes = cls.__bases__ + (cls,)  # do we really want that?

        # class objects named B{FB_xxx} are treated as FunctionalBlock and added to the B{_functionalBlocks} dict
        functionalBlocks = {}
        for cls_ in classes:
            for key, value in cls_.__dict__.iteritems():
                if key.startswith("FB_"):
                    Logger().debug("Device.__new__(): %s=(%s)" % (key, repr(value)))
                    name = value['name']

                    # Check if already registered
                    if functionalBlocks.has_key(name):
                        raise DeviceValueError("duplicated FB (%s)" % name)

                    cls = value["cls"]
                    value_ = dict(value)  # use a copy to let original untouched
                    value_.pop('cls')     # remove 'cls' key from FB_xxx dict
                    functionalBlocks[name] = cls(**value_)

        self._functionalBlocks = FrozenDict(functionalBlocks)

        # class objects named B{LNK_xxx} are treated as links and added to the B{_links} set
        links = set()
        for cls_ in classes:
            for key, value in cls_.__dict__.iteritems():
                if key.startswith("LNK_"):
                    Logger().debug("Device.__new__(): %s=(%s)" % (key, repr(value)))
                    link = (value['fb'], value['dp'], value['gad'])  # TODO: add flags
                    if link in links:
                        raise FunctionalBlockValueError("duplicated link (%s)" % link)

                    links.add(link)

        self._links = frozenset(links)

        #try:
            #self._desc = cls.__dict__["DESC"]
        #except KeyError:
            #Logger().exception("Device.__new__()", debug=True)
            #self._desc = "Device"

        return self

    def __init__(self, individualAddress):
        """ Init Device object.
        """
        super(Device, self).__init__()

        self._individualAddress = individualAddress

        self._stack = Stack(self._individualAddress)

        self.init()

    @property
    def indAddr(self):
        return self._individualAddress

    @property
    def stack(self):
        return self._stack

    @property
    def fb(self):
        return self._functionalBlocks

    @property
    def lnk(self):
        return self._links

    def init(self):
        """ Additionnal user init
        """
        pass

    def start(self):
        """ Start device execution
        """
        self._stack.start()

    def mainLoop(self):
        """ Main loop of the device

        Can be overriden to launch servers or so.
        """
        while True:
            time.sleep(0.001)

    def stop(self):
        """ Stop device execution
        """
        self._stack.stop()

    def shutdown(self):
        """ Additionnal user shutdown
        """
        pass

    #def register(self):
        #"""
        #"""
        #Logger().trace("Device._register()")

        #for key, value in self.__class__.__dict__.iteritems():
            #if key.startswith("FB_"):
                #Logger().debug("Device._register(): %s=(%s)" % (key, repr(value)))
                #cls = value["cls"]

                ## Remove 'cls' key from FB_xxx dict
                ## Use a copy to let original untouched
                #value_ = dict(value)
                #value_.pop('cls')
                #ETS().register(cls, **value_)

    #def weave(self):
        #"""
        #"""
        #Logger().trace("Device._weave()")

        #for key, value in self.__class__.__dict__.iteritems():
            #if key.startswith("LNK_"):
                #Logger().debug("Device._weave(): %s=(%s)" % (key, repr(value)))
                #ETS().weave(**value)


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class DeviceTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
