# -*- coding: utf-8 -*-

from pknyx.api import Device

from modbusFB import ModbusFB


class Modbus(Device):
    FB_01 = dict(cls=ReplayFB, name="modbus_fb", desc="modbus fb")

    LNK_01 = dict(fb="modbus_fb", dp="reg_1", gad="1/1/1")
    LNK_02 = dict(fb="modbus_fb", dp="reg_2", gad="1/1/2")
    LNK_03 = dict(fb="modbus_fb", dp="reg_3", gad="1/1/3")

    DESC = "Modbus"


DEVICE = Modbus
