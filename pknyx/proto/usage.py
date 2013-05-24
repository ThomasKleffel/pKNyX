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

Framework usage ideas

Documentation
=============

 - General configuration (GA mapping)
  - manual mapping of group addresses
  - ETS import
  - auto-detecting group addresses by listening to the bus

 -

@author: Frédéric Mantegazza
@copyright: (C) 2013 Frédéric Mantegazza
@license: GPL
"""

__revision__ = "$Id$"


################################################################################

from pknyx import GroupAddressManager, Rule, RuleManager, Scheduler

scheduler = Scheduler()


class SimpleRule(Rule):

    @scheduler.every(hours=2)
    def simpleEvent(self):
        ga = GroupAddressManager().find("1/1/1")
        ga.write(1)


myRule = SimpleRule()
RuleManager().register(myRule)

################################################################################

from pknyx.services import group, schedule, log, manager
from pknyx.elements import Rule


class HeatingRules(Rule):

    @schedule.every(hours=2)
    def bathroom(self):
        group.write("1/1/1", 0)


manager.registerRule(HeatingRules)  # Auto-instanciation

################################################################################

from pknyx.rule import Rule


class Heating(Rule):

    def bathroom(self, every="2h"):
        ga = self.get("1/1/1")
        ga.write(0)


Heating()  # Auto-registering

################################################################################

from pknyx.services import schedule, manager
from pknyx.elements import Rule


class HeatingRules(Rule):

    @schedule.every(hours=2)
    def bathroom(self):
        ga = self.groupAddressManager.find("1/1/1")
        ga.write(0)


heatRules = HeatingRules()
manager.registerRule(heatRules)

""" Notes

- Register some services in Rule class
- registerRule() can take a Rule instance, a Rule subclass, or a function. In this last case, the function
will be binded to a Rule instance, and registered.
- Instead of the decorator, the behavior of the rule can be given as parameter to registerRule() (simple string, or
object describing the behavior).

Or rules only as functions?
-> Use Participant for complete state-based stuff...
"""

################################################################################

from pknyx.services import Trigger, Logger  #, Scheduler
from pknyx.managers import RulesManager, GroupAddressManager

#schedule = Scheduler()
trigger = Trigger()
logger = Logger()
grp = GroupAddressManager()
rules = RulesManager()

#@schedule.every(minutes=1)
@trigger.schedule.every(hour=1)
@trigger.group(id="1/1/1").changed()
@trigger.system.start
def heatingBathroomManagement(event):
    """ Simple heating management

    @param event: contain some informations about the triggering event
    @type event: dict or Event-type?
    """
    temp = grp.findById("bathroom_temp").read()
    #tempObj = grp.find("bathroom_temp")
    #tempObj = grp.find("1/1/1")
    #temp = tempObj.read()  # read from bus
    #temp = tempObj.value   # get last known value
    tempSetup = grp.findById("bathroom_temp_setup").read()
    heaterObj = grp.findById("bathroom_heater")

    if temp < tempSetup - 0.25:
        logger.info("bathroom heater on")
        heaterObj.write(1)
    elif temp > tempSetup + 0.25:
        logger.info("bathroom heater off")
        heaterObj.write(0)

rules.register(heatingBathroomManagement)

################################################################################

from pknyx.api import Device, \
                      Datapoint as DP


class VMC(Device):
    """ VMC virtual device
    """

    def _createDP(self):
        self.dpTempSalon = DP("temp_salon", "9.001", flags="cwtu")

    def update(self, event):
        pass


vmc = VMC("1.1.1")
vmc.link("temp_1", "1/1/1")  # alt: vmc.dpTempSalon.link("1/1/1")
