# -*- coding: utf-8 -*-

from pknyx.api import FunctionalBlock
from pknyx.api import logger, schedule, notify


class Widget(FunctionalBlock):
    pass


class Toggle(Widget, xxx):
    DP_01 = dict(name="cmd", access="output", dptId="1.001", default="Off")
    DP_02 = dict(name="state", access="input", dptId="1.001", default="Off")

    GO_01 = dict(dp="cmd", flags="CWT", priority="low")
    GO_02 = dict(dp="state", flags="CWUI", priority="low")

    DESC = "Toggle button"

    def init(self):
        self._timer = 0

    @notify.datapoint(dp="state", condition="change")
    def stateChanged(self, event):
        """ Update the server internal state
        """
        pass

    @trucmuche.chose
    def change(self, dp, value):
        """ Called by the client listening thread
        """
        self.dp["cmd"].value = value
