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

Flags management

Implements
==========

 - B{FlagsValueError}
 - B{Flags}

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import re

from pknyx.common.exception import PKNyXValueError
from pknyx.common.loggingServices import Logger


class FlagsValueError(PKNyXValueError):
    """
    """


class Flags(object):
    """ Flag class

    @ivar _raw: raw set of flags
    @type _raw: str
    """
    def __init__(self, raw="CWTU"):
        """ Create a new set of flags

        @param raw: raw set of flags
        @type raw: str

        raise FlagsValueError: invalid flags

        @todo: allow +xx and -xx usage
        """
        super(Flags, self).__init__()

        try:
            if not re.match("^C?R?W?T?U?I?S?$", raw):
                raise FlagsValueError("invalid flags set (%r)" % repr(raw))
        except:
            Logger().exception("Flags.__init__()", debug=True)
            raise FlagsValueError("invalid flags set (%r)" % repr(raw))
        self._raw = raw

    @property
    def raw(self):
        return self._raw

    @property
    def communicate(self):
        return 'C' in self._raw

    @property
    def read(self):
        return 'R' in self._raw

    @property
    def write(self):
        return 'W' in self._raw

    @property
    def transmit(self):
        return 'T' in self._raw

    @property
    def update(self):
        return 'U' in self._raw

    @property
    def init(self):
        return 'I' in self._raw

    @property
    def stateless(self):
        return 'S' in self._raw


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class DFlagsTestCase(unittest.TestCase):

        def setUp(self):
            self.flags = Flags("CRWTUIS")

        def tearDown(self):
            pass

        def test_constructor(self):
            with self.assertRaises(FlagsValueError):
                Flags("A")
            with self.assertRaises(FlagsValueError):
                Flags("CWUT")
            with self.assertRaises(FlagsValueError):
                Flags("CCWUT")
            with self.assertRaises(FlagsValueError):
                Flags("CRWTUISA")

        def test_properties(self):
            self.assertEqual(self.flags.raw, "CRWTUIS")
            self.assertEqual(self.flags.communicate, True)
            self.assertEqual(self.flags.read, True)
            self.assertEqual(self.flags.write, True)
            self.assertEqual(self.flags.transmit, True)
            self.assertEqual(self.flags.update, True)
            self.assertEqual(self.flags.init, True)
            self.assertEqual(self.flags.stateless, True)


    unittest.main()
