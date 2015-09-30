# -*- coding: utf-8 -*-

from pknyx.api import Device

from toggle import Toggle


class ServerDev(Device, xxx):
    FB_01 = dict(cls=Toggle, name="toggle_wg", desc="Toggle widget")

    LNK_01 = dict(fb="toggle_wg", dp="cmd", gad="1/1/1")
    LNK_02 = dict(fb="toggle_wg", dp="state", gad="1/2/1")

    DESC = "Server object"


DEVICE = ServerDev
