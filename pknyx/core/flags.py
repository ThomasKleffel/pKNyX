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

Documentation
=============

linknx :

The "flags" parameter is similar to the ETS flags. The value of each flag is represented by a letter:
 - c: Communication (allow the object to interact with the KNX bus)
 - r: Read (allow the object to answer to a read request from another participant)
 - w: Write (update the object's internal value with the one received in write telegram if they are different)
 - t : Transmit (allow the object to transmit it's value on the bus if it's modified internally by a rule or via XML protocol)
 - u : Update (update the object's internal value with the one received in "read response" telegram if they are different)
 - f : Force (force the object value to be transmitted on the bus, even if it didn't change).
       In the recent versions you can use s : Stateless flag alternatively which means exactly the same
       (object does not update it's state so linknx should always send it's value to the bus
 - i : Init (useless for the moment. Will perhaps replace the parameter init="request" in the future)

Each letter appearing inside the value of this parameter means the corresponding flag is set.
If "flags" is not specified, the default value is "cwtu" (Communication, Write, Transmit and Update).

The default set of flags is good for most normal objects like switches where the value kept internally by linknx is
corresponding to real object state. Another set of flags can be for example "crwtf" (or "crwts") for objects that
should send it's value to the KNX bus even if linknx maintains the same value. This is usefull for scenes.
Setting scene value to 'on' should send this value to KNX every time action is triggered to make the scene happen.

ETS:
S         C   R   W   T   U
S         K   L   E   T   Act

 - S -> le DP envoie sa valeur sur la GA ayant ce flag (première GA associée à ce DP)
 - K -> communication : si pas présent, le DP n'envoie rien sur le bus (à utiliser pour com.interne au framework)
 - L -> lecture : le DP renverra sa valeur si une demande de lecture est faite sur une GA associée à ce DP (1 seul DP par
        GA devrait avoir ce flag)
 - E -> écriture : la valeur du DP sera modifiée si un télégramme de type 'write' est envoyé sur un des GA associée à ce DP
 - T -> transmission : si la valeur du DP est modifiée en interne (ou via plugin pour framewok), il enverra sa nouvelle
        valeur sur le bus, sur la GA ayant le flag S associé
 - Act -> update : le DP met à jour sa valeur s'il voit passer un télégramme en réponse à une demande de lecture sur
          l'une des GA associée à ce DP

 - C -> communication: the DP will interact with the bus
 - R -> read: the DP will send back its internal value on the bus if he receives a read request on one of its bound GAD.
        Only 1 DP per GAD should have this flag set
 - W -> write: the DP will update its internal value if he receives a write request on one of its bound GAD
 - T -> tansmit: when its internal value changes, the DP will send its new value on the first bounded GAD
 - U -> update: the DP will send back its internal value on the bus if he receives a response request on one of its
        bound GAD.
 - S -> stateless: like T, but transmits its value even if it didn't changed
 - I -> init: send a read request

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

    def __repr__(self):
        return "<Flags(\"%s\")>" % self._raw

    def __str__(self):
        return self._raw

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

        def test_display(self):
            print repr(self.flags)
            print self.flags

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
