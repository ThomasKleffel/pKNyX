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

 - B{Transmission}
 - B{TransmissionValueError}

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
from pknyx.core.result import Result


class TransmissionValueError(PKNyXValueError):
    """
    """


class Transmission(object):
    """ Transmission class

    @ivar _frame:
    @type _frame: bytearray

    @ivar _waitConfirm:
    @type _waitConfirm: bool

    @ivar _result:
    @type _result: int
    """
    def __init__(self, lPDU, waitConfirm):
        """

        @param lPDU:
        @type lPDU: bytearray

        @param waitConfirm:
        @type waitConfirm: bool

        raise TransmissionValueError:
        """
        super(Transmission, self).__init__()

        self._lPDU = lPDU
        self._waitConfirm = waitConfirm
        self._result = Result.OK

    @property
    def lPDU(self):
        return self._lPDU

    @property
    def waitConfirm(self):
        return self._waitConfirm

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, code):
        if code not in Result.availableCodes:
            raise TransmissionValueError("invalid result code (%s)" % repr(code))

        self._result = code


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class TransmissionTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()
