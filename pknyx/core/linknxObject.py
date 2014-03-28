# -*- coding: utf-8 -*-

""" Python KNX framework

License
=======

 - B{pKNyX} (U{http://www.pknyx.org}) is Copyright:
  - (C) 2013-2014 Frédéric Mantegazza

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

linknx object emulation.

Implements
==========

 - B{LinknxObject}

Documentation
=============

B{LinknxObject} are used by L{Datapoint<pknyx.core.datapoint>} to act as web server, compatible with linknx.

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2014 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.common.exception import PKNyXValueError
from pknyx.services.logger import Logger


class LinknxObjectValueError(PKNyXValueError):
    """
    """


class LinknxObject(object):
    """ LinknxObject class

    @ivar _datapoint: associated datapoint
    @type _datapoint: L{Datapoint<pknyx.core.datapoint>}

    @ivar _description: description used in knxweb2
    @type _description: str
    """
    def __init__(self, datapoint, description):  #, category, location):
        """ Init the LinknxObject

        @param datapoint: associated datapoint
        @type datapoint: L{Datapoint<pknyx.core.datapoint>}

        @param description: description used in knxweb2
        @type description: str

        raise LinknxObjectValueError:
        """
        super(LinknxObject, self).__init__()

        self._datapoint = datapoint
        self._description = description
        self._category = category
        self._location = location

    def __repr__(self):
        return "<LinknxObject(dp='%s', desc='%s')>" % (self.name, self._description)

    def __str__(self):
        return "<LinknxObject('%s')>" % self.name

    @property
    def datapoint(self):
        return self._datapoint

    @property
    def name(self):
        return self._datapoint.name

    @property
    def description(self):
        return self._description

    @property
    def category(self):
        return self._category

    @property
    def location(self):
        return self._location

    def getConfig(self):
        """ Return object config as xml

        @return: object configuration as xml
        @rtype: str

        @todo: use xml tree
        """
        return "<object id=\"%s\" type=\"%s\">%s</object>" % (self.name, self.datapoint.dptId, self.description)

    def read(self):
        """
        """

    def write(self, value):
        """
        """


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')


    class LinknxObjectTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_constructor(self):
            pass


    unittest.main()


