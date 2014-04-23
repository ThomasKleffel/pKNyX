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

Manage GroupAddress table mapping.

Implements
==========

 - B{GroupAddressTableMapper}

Documentation
=============

Allow the mapping between real L{GroupAddress<pknyx.stack.groupAddress>} and nick names, for easier use.

By default, the mapper will look in the given path for a module named B{gadMapTable.py}, and will load the map table
from B{GAD_MAP_TABLE} dict.

The GAD map table must be in the form:

GAD_MAP_TABLE = {"1/-/-": dict(name="light", desc="Lights (1/-/-)"),
                 "1/1/-": dict(name="light_cmd", desc="Commands (1/1/-)"),
                 "1/1/1": dict(name="light_cmd_test", desc="Test (1/1/1)"),
                 "1/2/-": dict(name="light_state", desc="States (1/2/-)"),
                 "1/2/1": dict(name="light_state_test", desc="Test (1/2/1)"),
                 "1/3/-": dict(name="light_delay", desc="Delays (1/3/-)"),
                 "1/3/1": dict(name="light_delay_test", desc="Test (1/3/1)"),
                }

GroupAddressTableMapper object is a singleton.

Usage
=====

>>> mapper = GroupAddressTableMapper()
>>> mapper.loadFrom("/tmp")
>>> print mapper.table
{'1/2/1': {'name': 'light_state_test', 'desc': 'Test'}, '1/3/-': {'name': 'light_delay', 'desc': 'Delays'},
'1/2/-': {'name': 'light_state', 'desc': 'States'}, '1/1/-': {'name': 'light_cmd', 'desc': 'Commands'},
'1/-/-': {'name': 'light', 'desc': 'Lights'}, '1/1/1': {'name': 'light_cmd_test', 'desc': 'Test'},
'1/3/1': {'name': 'light_delay_test', 'desc': 'Test'}}
>>> print mapper.deepTable

>>> print mapper.getNickname("1/1/1")
'light_cmd_test'
>>> print mapper.getGad("light_state_test")
'1/2/1'
>>> print mapper.getDesc("1/3/1")
'Test (1/3/1)'
>>> print mapper.getDesc("light_state_test")
'Test (1/3/1)'

@author: Frédéric Mantegazza
@copyright: (C) 2014 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import os.path
import imp

from pknyx.common.exception import PKNyXValueError
from pknyx.common.singleton import Singleton
from pknyx.services.logger import Logger
from pknyx.stack.groupAddress import GroupAddress, GroupAddressValueError


class GroupAddressTableMapperValueError(PKNyXValueError):
    """
    """


class GroupAddressTableMapper(object):
    """ GroupAddressTableMapper class

    @ivar _gadMapModule: customized map module name
    @type _gadMapModule: str

    @ivar _gadMapTable: GroupAddress mapping table
    @type _gadMapTable: dict
    """
    __metaclass__ = Singleton

    def __init__(self, module='gadMapTable'):
        """ Init the GroupAddressTableMapper.

        @param module: module name to load
        @type module: str

        raise GroupAddressTableMapperValueError:
        """
        super(GroupAddressTableMapper, self).__init__()

        self._gadMapModule = module

        self._gadMapTable = {}

    @property
    def table(self):
        return self._gadMapTable

    def isTableValid(self, table):
        """ Check GAD map table validity.

        GAD and nickname should be unique (GAD are, as they are dict keys!)
        """
        nicknames = {}
        for key, value in table.iteritems():
            if nicknames.has_key(value['name']):
                Logger().warning("Duplicated nickname '%s' in GAD map table" % value['name'])
                return False
            else:
                nicknames[value['name']] = dict(gad=key, desc=value['desc'])

        return True

    def _loadTable(self, path):
        """ Do load the GAD map table from module.

        @param path: path from where import module
        @type paht: str
        """
        gadMapTable = {}
        if os.path.exists(path):
            Logger().debug("GroupAddressTableMapper.loadTable(): GAD map path is '%s'" % path)

            try:
                fp, pathname, description = imp.find_module(self._gadMapModule, [os.path.curdir, path])
            except ImportError:
                Logger().warning("Can't find '%s' module in '%s'" % (self._gadMapModule, path))
            else:
                try:
                    gadMapModule = imp.load_module(self._gadMapModule, fp, pathname, description)
                finally:
                    if fp:
                        fp.close()
                gadMapTable.update(gadMapModule.GAD_MAP_TABLE)

        elif path != "$PKNYX_GAD_MAP_PATH":
            Logger().warning("GAD map path '%s' does not exists" % path)

        return gadMapTable

    def loadFrom(self, path):
        """ Load GAD map table from module in GAD map path.
        """
        table = self._loadTable(path)
        if self.isTableValid(table):
            self._gadMapTable = {}
            self._gadMapTable.update(table)

    def updateFrom(self, path):
        """ Updated GAD map table from module in GAD map path.
        """
        table = self._loadTable(path)
        if self.isTableValid(table):
            self._gadMapTable.update(table)

    def loadWith(self, table):
        """ Load GAD map table from given table.
        """
        if self.isTableValid(table):
            self._gadMapTable = {}
            self._gadMapTable.update(table)

    def updateWith(self, table):
        """ Updated GAD map table from given table.
        """
        if self.isTableValid(table):
            self._gadMapTable.update(table)

    def getGad(self, nickname):
        """ Convert GAD nickname to GAD.

        @param nickname: GAD nickname
        @type nickname: str

        @return: real GAD
        @rtype: str

        @raise GroupAddressTableMapperValueError:
        """
        for key, value in self._gadMapTable.iteritems():
            if nickname == value['name']:
                return key
        else:
            raise GroupAddressTableMapperValueError("Can't find '%s' GAD nickname in GAD map table" % nickname)

    def getNickname(self, gad):
        """ Convert GAD to GAD nickname.

        @param: real GAD
        @type: str

        @return: GAD nickname
        @rtype: str

        @raise GroupAddressTableMapperValueError:
        """
        try:
            return self._gadMapTable[gad]['name']
        except KeyError:
            raise GroupAddressTableMapperValueError("Can't find GAD '%s' in GAD map table" % gad)

    def getDesc(self, gad):
        """ Return the description of the given GAD/nickname.

        @param: GAD/nickname
        @type: str

        @return: GAD/nickname description
        @rtype: str

        @raise GroupAddressTableMapperValueError:
        """
        try:
            value = self._gadMapTable[gad]
        except KeyError:
            try:
                value = self._gadMapTable[self.getGad(gad)]
            except KeyError:
                raise GroupAddressTableMapperValueError("Can't find GAD nor nickname '%s' in GAD map table" % gad)

        try:
            return value['desc']
        except KeyError:
            raise GroupAddressTableMapperValueError("Can't find a description for given GAD/nickname (%s)" % gad)


if __name__ == '__main__':
    import unittest

    # Mute logger
    Logger().setLevel('error')

    GAD_MAP_TABLE = {"1/-/-": dict(name="light", desc="Lights (1/-/-)"),
                     "1/1/-": dict(name="light_cmd", desc="Commands (1/1/-)"),
                     "1/1/1": dict(name="light_cmd_test", desc="Test (1/1/1)"),
                     "1/2/-": dict(name="light_state", desc="States (1/2/-)"),
                     "1/2/1": dict(name="light_state_test", desc="Test (1/2/1)"),
                     "1/3/-": dict(name="light_delay", desc="Delays (1/3/-)"),
                     "1/3/1": dict(name="light_delay_test", desc="Test (1/3/1)"),
                    }


    class GroupAddressTableMapperTestCase(unittest.TestCase):

        def setUp(self):
            self._gadTableMapper = GroupAddressTableMapper()
            self._gadTableMapper.loadWith(GAD_MAP_TABLE)

        def tearDown(self):
            pass

        def test_table(self):
            self.assertEqual(self._gadTableMapper.table, GAD_MAP_TABLE)

        def test_isTableValid(self):
            TABLE_OK = {"1/1/1": dict(name="test 1", desc="Test (1/1/1)"),
                        "1/1/2": dict(name="test 2", desc="Test (1/1/2)")
                       }
            TABLE_WRONG = {"1/1/1": dict(name="test", desc="Test (1/1/1)"),
                           "1/1/2": dict(name="test", desc="Test (1/1/2)")
                          }
            self.assertEqual(self._gadTableMapper.isTableValid(TABLE_OK), True)
            self.assertEqual(self._gadTableMapper.isTableValid(TABLE_WRONG), False)

        def test_getGad(self):
            self.assertEqual(self._gadTableMapper.getGad("light"), "1/-/-")
            self.assertEqual(self._gadTableMapper.getGad("light_cmd"), "1/1/-")
            self.assertEqual(self._gadTableMapper.getGad("light_cmd_test"), "1/1/1")

        def test_getNickname(self):
            self.assertEqual(self._gadTableMapper.getNickname("1/-/-"), "light")
            self.assertEqual(self._gadTableMapper.getNickname("1/1/-"), "light_cmd")
            self.assertEqual(self._gadTableMapper.getNickname("1/1/1"), "light_cmd_test")

        def test_getDesc(self):
            self.assertEqual(self._gadTableMapper.getDesc("1/-/-"), "Lights (1/-/-)")
            self.assertEqual(self._gadTableMapper.getDesc("1/1/-"), "Commands (1/1/-)")
            self.assertEqual(self._gadTableMapper.getDesc("1/1/1"), "Test (1/1/1)")
            self.assertEqual(self._gadTableMapper.getDesc("light"), "Lights (1/-/-)")
            self.assertEqual(self._gadTableMapper.getDesc("light_cmd"), "Commands (1/1/-)")
            self.assertEqual(self._gadTableMapper.getDesc("light_cmd_test"), "Test (1/1/1)")


    unittest.main()
