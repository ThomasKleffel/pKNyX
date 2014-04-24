# -*- coding: utf-8 -*-

from pknyx.api import Device

from replayFB import ReplayFB


class Replay(Device):
    FB_01 = dict(cls=ReplayFB, name="replay_fb", desc="replay fb")

    LNK_01 = dict(fb="replay_fb", dp="replay", gad="1/1/1")
    LNK_02 = dict(fb="replay_fb", dp="replay_period", gad="1/1/2")
    LNK_03 = dict(fb="replay_fb", dp="light_1", gad="1/1/3")
    LNK_04 = dict(fb="replay_fb", dp="light_2", gad="1/1/4")
    LNK_05 = dict(fb="replay_fb", dp="light_3", gad="1/1/5")
    LNK_06 = dict(fb="replay_fb", dp="light_4", gad="1/1/6")
    LNK_07 = dict(fb="replay_fb", dp="light_5", gad="1/1/7")

    DESC = "Replay"


DEVICE = Replay
