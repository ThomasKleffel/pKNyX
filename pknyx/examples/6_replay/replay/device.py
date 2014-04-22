# -*- coding: utf-8 -*-

from pknyx.api import Device

from replayFB import ReplayFB


class Replay(Device):
    FB_01 = dict(cls=ReplayFB, name="replay_fb", desc="replay fb")

    LNK_01 = dict(fb="replay_fb", dp="dp_01", gad="1/1/1")

    DESC = "Replay"


DEVICE = Replay
