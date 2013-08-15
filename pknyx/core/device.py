#!/usr/bin/python
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

Implements
==========

 - B{}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id: multicast.py 319 2013-08-15 11:11:25Z fma $"

import sys
import argparse


def run():
    """
    """


def check():
    """
    """


def simul():
    """
    """


def monitor():
    """
    """


def main():

    # Common options
    parser = argparse.ArgumentParser(prog="process.py",
                                     description="This tool is used to launch pKNyX processes.",
                                     epilog="Under developement...")
    parser.add_argument("-l", "--logger",
                        choices=["trace", "debug", "info", "warning", "error", "exception", "critical"],
                        action="store", dest="debugLevel", default="warning", metavar="LEVEL",
                        help="logger level")

    parser2 = argparse.ArgumentParser(add_help=False)
    parser2.add_argument("-s", "--srcAddr", action="store", type=str, dest="src", default="0.0.0",
                         help="source address to use")

    # Create sub-parsers
    subparsers = parser.add_subparsers(title="subcommands", description="valid subcommands",
                                       help="sub-command help")

    # Run parser
    parserRun = subparsers.add_parser("run",
                                      parents=[parser2],
                                      help="Run process")
    parserRun.set_defaults(func=run)
    parserRun.add_argument("gad", type=str,
                           help="group address")
    parserRun.add_argument("value", type=str,
                           help="value to send")

    # Check parser
    parserCheck = subparsers.add_parser("check",
                                        parents=[parser2],
                                        help="Check process")
    parserCheck.set_defaults(func=check)
    parserCheck.add_argument("-t", "--timeout", type=int, default=1, metavar="TIMEOUT",
                             help="read timeout")
    parserCheck.add_argument("-n", "--no-wait", action="store_false", dest="wait", default=True,
                             help="wait for response")
    parserCheck.add_argument("gad", type=str,
                             help="group address")

    # Simul parser
    parserSimul = subparsers.add_parser("simul",
                                        parents=[parser2],
                                        help="Simulate process")
    parserSimul.set_defaults(func=simul)
    parserSimul.add_argument("gad", type=str,
                             help="group address")
    parserSimul.add_argument("value", type=str,
                             help="value to send")

    # Monitor parser
    parserMonitor = subparsers.add_parser("monitor",
                                          help="monitor bus")
    parserMonitor.set_defaults(func=monitor)

    # Parse
    args = parser.parse_args()

    Logger().setLevel(args.debugLevel)

    options = dict(vars(args))
    options.pop("debugLevel")
    options.pop("func")
    args.func(**options)


if __name__ == '__main__':
    main()
