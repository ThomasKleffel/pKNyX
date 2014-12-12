# -*- coding: utf-8 -*-

from pknyx.api import FunctionalBlock
from pknyx.api import logger, schedule, notify


class AverageFB(FunctionalBlock):
    DP_01 = dict(name="temp_average", access="output", dptId="9.001", default=19.)
    DP_02 = dict(name="temp_1", access="input", dptId="9.001", default=19.)
    DP_03 = dict(name="temp_2", access="input", dptId="9.001", default=19.)
    DP_04 = dict(name="temp_3", access="input", dptId="9.001", default=19.)

    GO_01 = dict(dp="temp_average", flags="CRT", priority="low")
    GO_02 = dict(dp="temp_1", flags="CWUI", priority="low")
    GO_03 = dict(dp="temp_2", flags="CWUI", priority="low")
    GO_04 = dict(dp="temp_3", flags="CWUI", priority="low")

    DESC = "Average FB"

    @notify.datapoint(dp="temp_1", condition="change")
    @notify.datapoint(dp="temp_2", condition="change")
    @notify.datapoint(dp="temp_3", condition="change")
    def tempChanged(self, event):
        """ Method called when any of the 'temp_x' Datapoint change
        """
        logger.debug("%s: event=%s" % (self.name, repr(event)))

        dpName = event['dp']
        newValue = event['newValue']
        oldValue = event['oldValue']
        logger.info("%s: '%s' value changed from %s to %s" % (self.name, dpName, oldValue, newValue))

        # Compute new average
        average = 0.
        for dpName in ("temp_1", "temp_2", "temp_3"):
            average += self.dp[dpName].value
        average /= 3.

        # Store new average in Datapoint
        self.dp["temp_average"].value = average
        logger.info("%s: new average is %.1f" % (self.name, average))
