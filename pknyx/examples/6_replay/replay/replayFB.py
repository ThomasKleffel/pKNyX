# -*- coding: utf-8 -*-

import time
import Queue

from pknyx.api import FunctionalBlock
from pknyx.api import logger, schedule, notify


class ReplayFB(FunctionalBlock):
    DP_01 = dict(name="replay", access="input", dptId="1.011", default="Inactive")
    DP_02 = dict(name="replay_period", access="input", dptId="7.006", default=1440)  # min (= 24h)
    DP_03 = dict(name="light_1", access="output", dptId="1.001", default="Off")
    DP_04 = dict(name="light_2", access="output", dptId="1.001", default="Off")
    DP_05 = dict(name="light_3", access="output", dptId="1.001", default="Off")
    DP_06 = dict(name="light_4", access="output", dptId="1.001", default="Off")
    DP_07 = dict(name="light_5", access="output", dptId="1.001", default="Off")

    GO_01 = dict(dp="replay", flags="CRWU", priority="low")
    GO_02 = dict(dp="replay_period", flags="CRWU", priority="low")
    GO_03 = dict(dp="light_1", flags="CWTU", priority="low")
    GO_04 = dict(dp="light_2", flags="CWTU", priority="low")
    GO_05 = dict(dp="light_3", flags="CWTU", priority="low")
    GO_06 = dict(dp="light_4", flags="CWTU", priority="low")
    GO_07 = dict(dp="light_5", flags="CWTU", priority="low")

    DESC = "Replay FB"

    def init(self):
        self._sequence = Queue.Queue(100)

    @notify.datapoint(dp="light_1", condition="change")
    @notify.datapoint(dp="light_2", condition="change")
    @notify.datapoint(dp="light_3", condition="change")
    @notify.datapoint(dp="light_4", condition="change")
    @notify.datapoint(dp="light_5", condition="change")
    def lightStateChanged(self, event):
        """ Method called when any of the 'light_x' Datapoint change
        """
        logger.debug("%s: event=%s" % (self.name, repr(event)))

        dpName = event['dp']
        newValue = event['newValue']
        oldValue = event['oldValue']
        time_ = time.time()
        logger.info("%s: '%s' value changed from %s to %s at %s" % (self.name, dpName, oldValue, newValue, time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(time_))))

        # Store Datapoint new value and current date/time
        try:
            self._sequence.put_nowait({'dp': dpName, 'value': newValue, 'time': time_})
        except Queue.Full:
            logger.exception("%s: storage sequence is full; skipping..." % self.name, debug=True)

        #logger.debug("%s: self._sequence=%s" % (self.name, self._sequence))

    @schedule.every(seconds=1)
    def processQueue(self):
        """ Process queue

        Get the older entry in the sequence (queue).
        If replay is active and time elapsed, the matching Datapoint is set with the stored value.
        Otherwise, the entry is discarded.
        """
        try:
            item = self._sequence.get_nowait()
            #logger.debug("%s: item=%s" % (self.name, item))
        except Queue.Empty:
            logger.exception("%s: storage sequence is empty; skipping..." % self.name, debug=True)

        # Check if item needs to be replayed
        delta = (time.time() - item['time']) / 60.
        if self.dp['replay'].value == "Active"  and delta > self.dp['replay_period'].value:
            self.dp[item['dp']].value = item['value']
            logger.info("%s: '%s' replayed at %s (%s)" % (self.name, dpName, time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(item['time'])), item['value']))
