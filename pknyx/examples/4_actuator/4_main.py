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

Example 4 - actuator

Implements
==========

 - B{ActuatorFB}
 - B{main}

Documentation
=============

This example implements an actuator which simply update its state.

2 datapoints are create:
 - 'cmd' is the command (input)
 - 'state' is the sate (output)

This functional block monitors the 'cmd' datapoint; when this datapoint changes, it updated the 'state' datapoint
accordingly.

Can be used with the timer functional block.

Usage
=====

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"

from pknyx.api import Logger
from pknyx.api import FunctionalBlock, Stack, ETS
from pknyx.api import Scheduler, Notifier

stack = Stack(individualAddress="1.2.4")
ets = ETS(stack)

schedule = Scheduler()
notify = Notifier()

logger = Logger()


class ActuatorFB(FunctionalBlock):
    """ Actuator functional block
    """

    # Datapoints definition
    DP_01 = dict(name="cmd", access="input", dptId="1.001", default="Off")
    DP_02 = dict(name="state", access="output", dptId="1.001", default="Off")

    GO_01 = dict(dp="cmd", flags="CWU", priority="low")
    GO_02 = dict(dp="state", flags="CRT", priority="low")

    DESC = "Actuator"

    @notify.datapoint(dp="cmd", condition="change")
    def stateChanged(self, event):
        """ Method called when the 'cmd' datapoint changes

        We just copy the 'cmd' datapoint value to the 'state' datapoint.
        """
        logger.debug("ActuatorFB.cmdChanged(): event=%s" % repr(event))

        value = event['newValue']
        Logger().info("%s: switch output %s" % (self.name, value))
        self.dp["state"].value = value


def main():

    # Register functional blocks
    ets.register(ActuatorFB, name="actuator", desc="")

    # Weave datapoints
    ets.weave(fb="actuator", dp="cmd", gad="6/0/1")
    ets.weave(fb="actuator", dp="state", gad="6/1/1")

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
        logger.exception("4_main")
