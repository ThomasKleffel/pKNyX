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

Sun position management

Implements
==========

 - B{SunPositionBlock}

Documentation
=============

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

import time

from pknyx.api import Logger
from pknyx.api import FunctionalBlock
from pknyx.api import Scheduler

from sun import Sun

schedule = Scheduler()

logger = Logger()


class SunPositionBlock(FunctionalBlock):

    # Datapoints definition
    DP_01 = dict(name="right_ascension", access="output", dptId="14.007", default=0.)
    DP_02 = dict(name="declination", access="output", dptId="14.007", default=0.)
    DP_03 = dict(name="elevation", access="output", dptId="14.007", default=0.)
    DP_04 = dict(name="azimuth", access="output", dptId="14.007", default=0.)
    DP_05 = dict(name="latitude", access="param", dptId="14.007", default=0.)
    DP_06 = dict(name="longitude", access="param", dptId="14.007", default=0.)
    DP_07 = dict(name="time_zone", access="param", dptId="1.xxx", default=1)
    DP_08 = dict(name="saving_time", access="param", dptId="1.xxx", default=1)

    GO_01 = dict(dp="right_ascension", flags="CRT", priority="low")
    GO_02 = dict(dp="declination", flags="CRT", priority="low")
    GO_03 = dict(dp="elevation", flags="CRT", priority="low")
    GO_04 = dict(dp="azimuth", flags="CRT", priority="low")
    GO_05 = dict(dp="latitude", flags="CRWT", priority="low")
    GO_06 = dict(dp="longitude", flags="CRWT", priority="low")
    GO_07 = dict(dp="time_zone", flags="CRWT", priority="low")
    GO_08 = dict(dp="saving_time", flags="CRWT", priority="low")

    DESC = "Sun position management block"

    def _init(self):
        """ Additionnal inits of our Functional Block
        """
        self._sun = Sun(latitude=self.dp["latitude"].value,
                        longitude = self.dp["longitude"].value,
                        timeZone = self.dp["time_zone"].value,
                        savingTime = self.dp["saving_time"].value)

    #@notify.datapoint("latitude")
    #@notify.datapoint("longitude")
    #@notify.datapoint("time_zone")
    #@notify.datapoint("saving_time")
    def updateParams(self):

        self._sun.latitude = self.dp["latitude"].value
        self._sun.longitude = self.dp["longitude"].value
        self._sun.timeZone = self.dp["time_zone"].value
        self._sun.savingTime = self.dp["saving_time"].value

    @schedule.every(seconds=5)
    def updateSunPosition(self):
        logger.trace("WeatherSunPositionBlock.updatePosition()")

        # Read inputs/params
        self._sun.latitude = self.dp["latitude"].value
        self._sun.longitude = self.dp["longitude"].value
        self._sun.timeZone = self.dp["time_zone"].value
        self._sun.savingTime = self.dp["saving_time"].value

        # Computations
        tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.localtime()

        rightAscension, declination = self._sun.equatorialCoordinates(tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec)
        elevation, azimuth = self._sun.azimuthalCoordinates(tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec)

        # Write outputs
        self.dp["right_ascension"].value = rightAscension
        self.dp["declination"].value = declination
        self.dp["elevation"].value = elevation
        self.dp["azimuth"].value = azimuth
