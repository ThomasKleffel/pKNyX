# -*- coding: utf-8 -*-

from pknyx.api import Device

from averageFB import AverageFB


class Average(Device):
    FB_01 = dict(cls=AverageFB, name="average_fb", desc="average fb")

    LNK_01 = dict(fb="average_fb", dp="temp_average", gad="1/1/1")
    LNK_02 = dict(fb="average_fb", dp="temp_1", gad="1/1/2")
    LNK_03 = dict(fb="average_fb", dp="temp_2", gad="1/1/3")
    LNK_04 = dict(fb="average_fb", dp="temp_3", gad="1/1/4")

    DESC = "Average"


DEVICE = Average
