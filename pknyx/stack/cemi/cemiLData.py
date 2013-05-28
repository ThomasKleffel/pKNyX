# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{pKNyX} (U{http:#www.pknyx.org}) is Copyright:
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

 - U{http:#www.gnu.org/licenses/gpl.html}

Module purpose
==============

cEMI frame management

Implements
==========

 - B{CEMILData}

Documentation
=============


Usage
=====

>>> from cemiLData import CEMILData
>>> f = CEMILData()

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger
from pknyx.core.cemi.cemi import CEMI, CEMIValueError


class CEMILData(CEMI):
    """ cEMI L-Data handling

    @ivar data:
    @type data:
    """
    MC_LDATA_REQUEST = 0x11  # message code for L-Data request
    MC_LDATA_CONFIRM = 0x2E  # message code for L-Data confirmation
    MC_LDATA_INDICAT = 0x29  # message code for L-Data indication
    BASIC_LENGTH = 9

    def __init__(self, data=None):
        """ Create a new cEMI L-Data object

        @param data:
        @type data:
        """
        super(CEMILData, self).__init__()

        self._data = data  # TODO: check validity

        self._messageCode = None
        self._ctrlField1 = None  # Control field 1, the lower 8 bits contain control information
        self._ctrlField2 = None  # Control field 2, the lower 8 bits contain control information
        self._priority = None
        self._sourceAddress = None
        self._destAddres = None

    def _checkData(self, data):
        """

        @param data:
        @type data:
        """
        if len(data) < CEMI.BASIC_LENGTH + 1:
            raise CEMIValueError("too short data")

    def _toData(self):
        """
        """

    def _fromData(self, data):
        """
        """
        #self._data = data

        #final ByteArrayInputStream is = new ByteArrayInputStream(data, offset, data.length - offset)
        #readMC(is)
        #readAddInfo(is)
        #readCtrlAndAddr(is)
        #if (ctrl1 & 0x80) == 0 :
                #throw new KNXFormatException("only cEMI standard frame supported")
        #readPayload(is);

    def getPayload(self):
        pass

    def getMessageCode(self):
        pass

    def getStructLength(self):
        pass

    def toByteArray(self):
        pass

