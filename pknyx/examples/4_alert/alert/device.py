# -*- coding: utf-8 -*-

from pknyx.api import Device

from alertFB import AlertFB


class Alert(Device):
    FB_01 = dict(cls=AlertFB, name="alert_fb", desc="alert fb")

    LNK_01 = dict(fb="alert_fb", dp="temp_1", gad="1/1/1")
    LNK_02 = dict(fb="alert_fb", dp="temp_2", gad="1/1/2")
    LNK_03 = dict(fb="alert_fb", dp="door_1", gad="1/1/3")

    DESC = "Alert"


DEVICE = Alert
