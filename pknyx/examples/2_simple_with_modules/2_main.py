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

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id: ets.py 161 2013-07-10 13:21:51Z fma $"

from pknyx.api import Logger
from pknyx.api import Stack, ETS
from pknyx.api import Scheduler

from sunPositionBlock import SunPositionBlock

# ETS Group Object Association Table (GrOAT)
GROAT = {"1": dict(name="weather_station", desc="Weather station"),
         "1/3": dict(name="sun_position", desc="Sun position"),
         "1/3/1": dict(name="heat_setpoint_living", desc="Salle à Manger"),
         "1/3/2": dict(name="heat_setpoint_bedroom_1", desc="Chambre 1"),
         "1/3/3": dict(name="heat_setpoint_bedroom_2", desc="Chambre 2"),
         "1/3/4": dict(name="heat_setpoint_bedroom_3", desc="Chambre 3"),
         "1/3/5": dict(name="heat_temperature_living", desc="Salle à Manger"),
         "1/3/6": dict(name="heat_temperature_bedroom_1", desc="Chambre 1"),
         "1/3/7": dict(name="heat_temperature_bedroom_2", desc="Chambre 2"),
         "1/3/8": dict(name="heat_temperature_bedroom_3", desc="Chambre 3"),
         "1/3/9": dict(name="light_state_bedroom_1", desc="Chambre 1"),
        }

stack = Stack(individualAddress="1.2.3")
ets = ETS(stack, groat=GROAT)

schedule = Scheduler()

logger = Logger()


def main():

    # Register Functional Blocks
    ets.register(SunPositionBlock, name="sun_position", desc="sun 1")

    # Weave weather station Datapoints to Group Addresses
    # @todo: allow use of gad name, from GrOAT
    ets.weave(fb="sun_position", dp="right_ascension", gad="1/3/1")
    ets.weave(fb="sun_position", dp="declination", gad="1/3/2")
    ets.weave(fb="sun_position", dp="elevation", gad="1/3/3")
    ets.weave(fb="sun_position", dp="azimuth", gad="1/3/4")
    ets.weave(fb="sun_position", dp="latitude", gad="1/3/5")
    ets.weave(fb="sun_position", dp="longitude", gad="1/3/6")
    ets.weave(fb="sun_position", dp="time_zone", gad="1/3/7")
    ets.weave(fb="sun_position", dp="saving_time", gad="1/3/8")
    ets.weave(fb="sun_position", dp="saving_time", gad="1/3/9")

    print
    print
    ets.printGroat("gad")
    print
    print
    ets.printGroat("go")

    # Start the scheduler
    # @todo: move to a better place
    print
    schedule.start()
    schedule.printJobs()
    print

    # Run the stack main loop (blocking call)
    stack.mainLoop()

    schedule.stop()


if __name__ == "__main__":
    main()
