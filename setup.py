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

Packaging

Implements
==========

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013-2015 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pknyx.common import config


setup(name=config.APP_NAME,
      version="%s.pkg%d" % (config.VERSION, config.VERSION_PACKAGE),

      description="Python KNX framework",
      long_description=open('README').read(),
      url="http://www.pknyx.org",

      author="Frédéric Mantegazza",
      author_email="fma@pknyx.org",

      license="GPL",

      maintainer="Frederic Mantegazza",
      maintainer_email="fma@pknyx.org",

      download_url="http://www.pknyx.org/wiki/Download",

      packages=["pknyx",
                "pknyx.common",
                "pknyx.core",
                "pknyx.core.dptXlator",
                "pknyx.plugins",
                "pknyx.services",
                "pknyx.stack",
                "pknyx.stack.cemi",
                "pknyx.stack.knxnetip",
                "pknyx.stack.layer2",
                "pknyx.stack.layer3",
                "pknyx.stack.layer4",
                "pknyx.stack.layer7",
                "pknyx.stack.transceiver",
                "pknyx.tools",
                "pknyx.tools.templates",
                ],

      scripts=["pknyx/scripts/pknyx-group.py",
               "pknyx/scripts/pknyx-admin.py"],

      install_requires=["APScheduler == 2.1.2",
                        "argparse"],
)
