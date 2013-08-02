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

Example 3 - light timer

Implements
==========

 - B{DummyBlock}
 - B{WeatherTemperatureBlock}
 - B{WeatherWindBlock}
 - B{main}

Documentation
=============

A simple showing example how to use the framework.

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id: 1_main.py 213 2013-08-01 13:24:41Z fma $"

from pknyx.api import Logger
from pknyx.api import FunctionalBlock, Stack, ETS
from pknyx.api import Scheduler, Notifier

# ETS group address map
GAD_MAP = {"1": dict(name="", desc=""),
           "1/1": dict(name="", desc=""),
           "1/1/1": dict(name="", desc=""),
           "1/1/2": dict(name="", desc=""),
           "1/1/3": dict(name="", desc=""),
          }

stack = Stack(individualAddress="1.2.3")
ets = ETS(stack, gadMap=GAD_MAP)

schedule = Scheduler()
notify = Notifier()

logger = Logger()


class LightTimerFB(FunctionalBlock):
    """ Timer for light functional block

    This functional block automatically switches off a light after a delay.
    """

    # Datapoints definition
    DP_01 = dict(name="cmd", access="output", dptId="1.001", default="Off")
    DP_02 = dict(name="state", access="input", dptId="1.001", default="Off")
    DP_03 = dict(name="delay", access="input", dptId="7.005", default=10)

    GO_01 = dict(dp="cmd", flags="CWT", priority="low")
    GO_02 = dict(dp="state", flags="CWUI", priority="low")
    GO_03 = dict(dp="delay", flags="CWU", priority="low")

    DESC = "Timer for light block"

    def _init(self):
        """ Additionnal init of our functional block
        """
        self._timer = 0

    @schedule.every(seconds=1)
    def updateTimer(self):
        """
        """
        logger.trace("LightTimerFB.updateTimer()")

        if self._timer:
            self._timer -= 1
            if not self._timer:
                logger.info("%s: switch off light" % self._name)
                self.dp["cmd"].value = "Off"

    @notify.datapoint(dp="state", condition="change")
    def stateChanged(self, event):
        """
        """
        logger.debug("LightTimerFB.stateChanged(): event=%s" % repr(event))

        if event['newValue'] == "On":
            delay = self.dp["delay"].value
            Logger().info("%s: start timer for %ds" % (self._name, delay))
            self._timer = delay

    @notify.datapoint(dp="delay", condition="change")
    def delayChanged(self, event):
        """
        """
        logger.debug("LightTimerFB.delayChanged(): event=%s" % repr(event))

        # If the timer is running, we reset it to the new delay
        if self._timer:
            delay = self.dp["delay"].value
            Logger().info("%s: restart timer for %ds" % (self._name, delay))
            self._timer = delay


def main():

    # Register functional blocks
    ets.register(LightTimerFB, name="light_timer", desc="")

    # Weave datapoints
    ets.weave(fb="light_timer", dp="cmd", gad="1/1/1")
    ets.weave(fb="light_timer", dp="state", gad="1/1/2")
    ets.weave(fb="light_timer", dp="delay", gad="1/1/3")

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
    try:
        main()
    except:
        logger.exception("3_main")
