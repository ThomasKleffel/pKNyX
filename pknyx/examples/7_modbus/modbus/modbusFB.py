# -*- coding: utf-8 -*-

import time
import Queue

from pymodbus.client.sync import ModbusTcpClient

from pknyx.api import FunctionalBlock
from pknyx.api import logger, schedule, notify

import settings


class ModbusFB(FunctionalBlock):
    DP_01 = dict(name="reg_1", access="input", dptId="7.xxx", default=0)
    DP_02 = dict(name="reg_2", access="input", dptId="7.xxx", default=0)
    DP_03 = dict(name="reg_3", access="output", dptId="7.xxx", default=0)

    GO_01 = dict(dp="reg_1", flags="CRWU", priority="low")
    GO_02 = dict(dp="reg_2", flags="CRWU", priority="low")
    GO_03 = dict(dp="reg_3", flags="CWTU", priority="low")

    DESC = "Modbus FB"

    def init(self):
        self._client = ModbusTcpClient(host=settings.MODBUS_HOST, port=settings.MODBUS_PORT)

    def _read(self, register):
        """

        @param register: name of the variable to read
        @type register: int

        @return: register value
        @rtype: int
        """
        self._client.connect()
        try:
            result = self._client.read_holding_registers(register, 1, unit=settings.MODBUS_UNIT)
            value = result.registers[0]
            return value
        finally:
            self._client.close()

    def _write(self, register, value):
        """

        @param var: name of the variable to read
        @type var: str
        """
        self._client.connect()
        try:
            self._client.write_register(register, value, unit=settings.MODBUS_UNIT)
        finally:
            self._client.close()

    @notify.datapoint(dp="reg_1", condition="change")
    @notify.datapoint(dp="reg_2", condition="change")
    @notify.datapoint(dp="reg_3", condition="change")
    def RegisterStateChanged(self, event):
        """ Method called when any of the 'reg_x' Datapoint change
        """
        logger.debug("%s: event=%s" % (self.name, repr(event)))

        dpName = event['dp']
        newValue = event['newValue']
        oldValue = event['oldValue']
        logger.info("%s: '%s' value changed from %s to %s" % (self.name, dpName, oldValue, newValue))

        # Send new register value to modbus client
        self._write(config.KNX_TO_MODBUS[dpName], newValue)

    @schedule.every(seconds=settings.MODBUS_REFRESH_RATE)
    def modbusRefresh(self):
        """ Read modbus output registers
        """
        for register, dp in config.MODBUS_TO_KNX.items():
            value = self._read(register)
            self.dp[dp].value = value
