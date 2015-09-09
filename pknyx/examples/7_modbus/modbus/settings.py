# -*- coding: utf-8 -*-

from pknyx.common import config

DEVICE_NAME = "modbus"
DEVICE_IND_ADDR = "1.1.1"
DEVICE_VERSION = "0.1"

# Override default logger level
config.LOGGER_LEVEL = "info"

# Modbus stuff
MODBUS_HOST = "plc"
MODBUS_PORT = 502
MODBUS_TIMEOUT = 2.  # s
MODBUS_UNIT = 180
MODBUS_REFRESH_RATE = 10  # s

KNX_TO_MODBUS = {
    "reg_1": 1,
    "reg_2": 2,
    "reg_3": 3,
}

MODBUS_TO_KNX = {
    1: "reg_1",
    2: "reg_2",
    3: "reg_3",
}
