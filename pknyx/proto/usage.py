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
#@trigger.group(id="1/1/1").changed()   <<<<<<<<< Does not work
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
                      ETS


class VMC(Device):
    """ VMC virtual device

    @todo: add parameters, for more generic devices (as real devices)
    @todo: make as thread
    @todo: should also react with time-based events, system events... -> decorator @trigger.xxx
    """

    # Datapoints are created as class entities and automatically instancianted as real DP in constructor
    # Their name must start with 'DP_' ; they will be stored in self.dp dict-like object.
    # Ex: DP_1 = ("truc", "1.001", "cwtu", "low", 0) ... > self.dp["truc"]  <<<< special dict, with additionnal features

    DP_01 = ("temp_entree", "9.001", "cwtu", "low", 0)
    DP_02 = {'name': "temp_sortie", dptId: "9.001", 'flags': "cwtu", 'priority': "low", 'initValue': 0}
    DP_03 = dict(name="temp_repris", dptId="9.001", flags="cwtu", priority="low", initValue=0)

    def init(self):
        """
        """

    def initDP(self):
        """
        """
        self.dp["temp_entree"].value = 0  # Add persistence feature!!!

    #def bus(self, event):
        #"""
        #This method must be overloaded. It is called when an event occurs on the bus which changes GA
        #linked with at least one DP of this device.
        #"""
        #print event.src
        #print event.dest
        #print event.value
        #print event.priority
        #print event.cEMI

    @trigger.schedule.at()
    @trigger.dp.change()
    def notify(self, event):
        """
        """
        print event.src
        print event.dest
        print event.value
        print event.priority
        print event.cEMI

    def execute(self):
        """
        This method is called regularly by the thread. Do here whatever you need to do.
        Stop thread if return True?
        If not overloaded in the Device sub-class, the thread sleeps forever. Only callbacks, if any, will run.
        """


vmc = VMC("1.2.3")
#vmc.link("temp_entree", "1/1/1")  # allow wildcard and regexp?
#vmc.dpTempSalon.link("1/1/1")
#ETS.addLink(vmc.dpTempSalon, "1/1/1")
ETS.link(vmc, "temp_entree", "1/1/1")
ETS.link(vmc, "temp_entree", ("1/1/1", "1/1/2"))


################################################################################

