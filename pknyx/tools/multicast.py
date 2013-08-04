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

Multicast tool.

Implements
==========

 - B{}

Documentation
=============

This script is used to send/receive multicast requests.

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id: template.py 155 2013-07-10 12:34:24Z fma $"

import sys
import optparse

#from pknyx.common.exception import PKNyXValueError
from pknyx.services.logger import Logger


class XxxValueError(PKNyXValueError):
    """
    """


class Xxx(object):
    """ Xxx class

    @ivar _xxx:
    @type _xxx:
    """
    def __init__(self):
        """

        @param xxx:
        @type xxx:

        raise XxxValueError:
        """
        super(Xxx, self).__init__()


def main():
    usage  = "%prog -r [options] -> read object value\n"
    usage += "       %prog -w [options] -> write objet value"

    # Common options
    parser = optparse.OptionParser(usage)
    parser.add_option("-t", "--host", action="store", type="string", dest="host", default="localhost",
                      help="hostname of the machine running the linknx daemon ('localhost')")
    parser.add_option("-p", "--port", action="store", type="int", dest="port", default=1028,
                      help="port linknx listens on (1028)")
    #parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                      #help="let the script output useful information, for debugging purpose")
    parser.add_option("-o", "--object-id", action="store", type="string", dest="objectId", metavar="ID",
                      help="object id to control")

    # Read GA options
    groupRead = optparse.OptionGroup(parser, "Read")
    groupRead.add_option("-r", "--read", action="store_true", dest="read", default=False,
                         help=optparse.SUPPRESS_HELP)
    parser.add_option_group(groupRead)

    # Write GA options
    groupWrite = optparse.OptionGroup(parser, "Write")
    groupWrite.add_option("-w", "--write", action="store_true", dest="write", default=False,
                          help=optparse.SUPPRESS_HELP)
    groupWrite.add_option("-v", "--value", action="store", type="string", dest="value",
                          help="value to send on object id")
    parser.add_option_group(groupWrite)

    # Parse
    options, args = parser.parse_args()

    # Check commands validity
    if not (options.read or options.write):
        parser.error("no command specified")
    elif not options.read ^ options.write:
        parser.error("multiple commands specified")
    if options.objectId is None:
        parser.error("no object id specified")
    if options.write and options.value is None:
        parser.error("must give a value when writing on object id")

    #print("DEBUG::main(): options=%s, args=%s" % (options, args))

    #try:
    if options.read:
        print(read(options.host, options.port, options.objectId))
    elif options.write:
        write(options.host, options.port, options.objectId, options.value)
    #except socket.error as e:
        #print("ERROR::main(): connection error (%s)" % e.message)
    #except Exception as e:
        #print("ERROR::main(): linknx error (%s)" % e.message)



if __name__ == '__main__':
    main()
