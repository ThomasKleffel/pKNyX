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

Example 2

Implements
==========

 - B{main}

Documentation
=============

A simple example showing how to use the framework. Here, the code is split up to different modules.

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.api import Logger
from pknyx.api import Stack, ETS
from pknyx.api import Scheduler

from sunPositionFB import SunPositionFB

# ETS group address map
GAD_MAP = {"1": dict(name="weather_station", desc="Weather station"),
           "1/3": dict(name="sun_position", desc="Sun position"),
           "1/3/1": dict(name="right_ascension", desc="Right ascension"),
           "1/3/2": dict(name="declination", desc="Declination"),
           "1/3/3": dict(name="elevation", desc="Elevation"),
           "1/3/4": dict(name="azimuth", desc="Azimuth"),
           "1/3/5": dict(name="latitude", desc="Latitude"),
           "1/3/6": dict(name="longitude", desc="Longitude"),
           "1/3/7": dict(name="time_zone", desc="Time zone"),
           "1/3/8": dict(name="saving_time", desc="Saving time flag")
          }

stack = Stack(individualAddress="1.2.3")
ets = ETS(stack, gadMap=GAD_MAP)

schedule = Scheduler()

logger = Logger()


def main():

    # Register functional blocks
    ets.register(SunPositionFB, name="sun_position", desc="sun 1")

    # Weave weather station datapoints to group addresses
    # @todo: allow use of gad name, from gad map
    ets.weave(fb="sun_position", dp="right_ascension", gad="1/3/1")
    ets.weave(fb="sun_position", dp="declination", gad="1/3/2")
    ets.weave(fb="sun_position", dp="elevation", gad="1/3/3")
    ets.weave(fb="sun_position", dp="azimuth", gad="1/3/4")
    ets.weave(fb="sun_position", dp="latitude", gad="1/3/5")
    ets.weave(fb="sun_position", dp="longitude", gad="1/3/6")
    ets.weave(fb="sun_position", dp="time_zone", gad="1/3/7")
    ets.weave(fb="sun_position", dp="saving_time", gad="1/3/8")

    print
    ets.printGroat("gad")
    print
    ets.printGroat("go")
    print
    schedule.printJobs()
    print

    # Run the stack main loop (blocking call)
    stack.mainLoop()


if __name__ == "__main__":
    main()
