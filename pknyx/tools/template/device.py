# -*- coding: utf-8 -*-

from pknyx.api import Device, FunctionalBlock
from pknyx.api import logger, schedule, notify


class MyFB(FunctionalBlock):
    DP_01 = dict(name="mydp", access="output", dptId="1.001", default="Off")

    GO_01 = dict(dp="mydp", flags="CWT", priority="low")

    DESC = "My FB"


class MyDevice(Device):
    FB_01 = dict(cls=MyFB, name="myfb", desc="my fb")

    LNK_01 = dict(fb="myfb", dp="mydp", gad="1/1/1")

    DESC = "My device"


DEVICE = MyDevice
