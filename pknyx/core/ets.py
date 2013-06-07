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

ETS management

Implements
==========

 - B{ETS}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger
from pknyx.core.stack import Stack
from pknyx.core.device import Device


class ETSValueError(PKNyXValueError):
    """
    """


class ETS(object):
    """ ETS class

    @ivar _stack: KNX stack object
    @type _stack: L{Stack}

    @ivar _devices: registered devices
    @type _devices: set of L{Device}

    raise ETSValueError:
    """
    def __init__(self, stack):
        """

        @param stack: KNX stack object
        @type stack: L{Stack}

        raise ETSValueError:
        """
        super(ETS, self).__init__()

        if not isinstance(Stack, stack):
            raise ETSValueError("invalid stack object (%s)" % repr(stack))
        self._stack = stack

        self._devices = set()
        self._links = {}

    @property
    def stack(self):
        return self._stack

    @property
    def devices(self):
        return self._devices

    def link(self, device, dpName, gad):
        """ Link a datapoint to a GAD

        @param device: device owning the datapoint
        @type device: L{Device}

        @param dpName: name of the datapoint to link
        @type dpName: str

        @param gad : Groupaddress to link to
        @type gad : str or L{GroupAddress}

        raise ETSValueError:
        """
        #if not isinstance(Device, device):
            #raise ValueError("invalid device (%s)" % repr(device)

        # Get datapoint
        datapoint = device.dp[dpName]

        # Ask the group data service to subscribe this datapoint to the given gad
        # In return, get the created accesspoint
        accesspoint = self._stack.gds.subscribe(datapoint, gad)

        # If the datapoint does not already have an accesspoint, set it
        # This accesspoint will be used by the datapoint to send datas to the default GAD
        # This mimics the S flag of ETS real application
        # @todo: find a way to change it later? Or let the datapoint manage this?
        if datapoint.accesspoint is None:
            datapoint.accesspoint = accesspoint

        # Store the association
        #lnk = Link(device, dpName, gad)
        #self._links.add(lnk)
        try:
            self._links[dpName].add(gad)
        except KeyError:
            self._links[dpName] = set((gad,))

        # Add the device to the known devices
        # Really usefull?
        self._devices.add(device)

    def showLinks(self, by='datapoint'):
        """
        """
        if by not in ('datapoint', 'gad'):
            raise ETSValueError("invalid 'by' param (%s)" % repr(by))
        if by == 'datapoint':
            return self._links


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class ETSTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
