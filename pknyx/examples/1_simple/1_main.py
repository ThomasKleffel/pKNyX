# -*- coding: utf-8 -*-

import math
import time

from pknyx.api import Logger
from pknyx.api import FunctionalBlock, Stack, ETS
from pknyx.api import Scheduler

# ETS Group Object Association Table (GrOAT)
GROAT = {"1": dict(name="weather_station", desc="Weather station"),
         "1/1": dict(name="temperatures", desc="Temperatures"),
         "1/1/1": dict(name="external_temperature", desc="External temperature"),
         "1/1/2": dict(name="external_humidity", desc="External humidity"),
         "1/2": dict(name="wind", desc="Wind"),
         "1/2/1": dict(name="wind_speed", desc="Wind speed"),
         "1/2/2": dict(name="wind_alarm", desc="Wind alarm"),
         "1/2/3": dict(name="wind_speed_limit", desc="Wind speed limit"),
         "1/2/4": dict(name="wind_alarm_enable", desc="Wind alarm enable"),
        }

stack = Stack(individualAddress="1.2.3")
ets = ETS(stack, groat=GROAT)

schedule = Scheduler()

logger = Logger()


class DummyBlock(FunctionalBlock):
    """ This block is just here to generate an error
    """

    @schedule.every(minutes=5)
    def generateException(self):
        logger.trace("DummyBlock.generateException()")
        raise Exception("Error test")


class WeatherTemperatureBlock(FunctionalBlock):

    # Datapoints definition
    DP_01 = dict(name="temperature", access="output", dptId="9.001", default=19.)
    DP_02 = dict(name="humidity", access="output", dptId="9.007", default=50.)

    GO_01 = dict(dp="temperature", flags="CRT", priority="low")
    GO_02 = dict(dp="humidity", flags="CRT", priority="low")

    DESC = "Temperature management block"

    @schedule.every(minutes=1)
    def updateTemperatureHumidity(self):
        logger.trace("WeatherTemperatureBlock.updateTemperatureHumidity()")

        # Retreive temperature/humidity
        temperature = 20.
        humidity = 55.
        self.dp["temperature"].value = temperature
        self.dp["humidity"].value = humidity


class WeatherWindBlock(FunctionalBlock):

    # Datapoints definition
    DP_01 = dict(name="wind_speed", access="output", dptId="9.005", default=0.)
    DP_02 = dict(name="wind_alarm", access="output", dptId="1.005", default="No alarm")
    DP_03 = dict(name="wind_speed_limit", access="input", dptId="9.005", default=15.)
    DP_04 = dict(name="wind_alarm_enable", access="input", dptId="1.003", default="Disable")

    GO_01 = dict(dp="wind_speed", flags="CRT", priority="low")
    GO_02 = dict(dp="wind_alarm", flags="CRTS", priority="normal")
    GO_03 = dict(dp="wind_speed_limit", flags="CW", priority="low")
    GO_04 = dict(dp="wind_alarm_enable", flags="CW", priority="low")

    DESC = "Wind management block"

    @schedule.every(minutes=1)
    def updateWindSpeed(self):
        logger.trace("WeatherWindBlock.updateWindSpeed()")

        # Retreive speed
        speed = 12.

        # Write the new speed value to matching Datapoint
        # This will trigger the bus notification (if a group object is associated)
        self.dp["wind_speed"].value = speed

    #notify.datapoint(name="wind_speed_limit")  # single DP
    #notify.datapoint()  # all DP
    #notify.group(gad="1/1/1")  # single group address
    def checkWindSpeed(self, event):
        logger.trace("WeatherWindBlock.checkWindSpeed()")

        # Read inputs/params
        wind_speed = self.dp["wind_speed"].value
        wind_alarm_enable = self.dp["wind_alarm_enable"].value
        wind_speed_limit = self.dp["wind_speed_limit"].value

        # Check if alarm
        if wind_speed > wind_speed_limit:
            wind_alarm = "Alarm"
        elif wind_speed < wind_speed_limit - 5.:
            wind_alarm = "No alarm"

        # Write outputs
        if wind_alarm_enable:
            self.dp["wind_alarm"].value = wind_alarm


def main():

    # Register Functional Blocks
    ets.register(DummyBlock, name="dummy", desc="dummy")
    ets.register(WeatherTemperatureBlock, name="weather_temperature", desc="temp 1")
    ets.register(WeatherWindBlock, name="weather_wind", desc="wind 1")

    # Weave blocks Datapoints to Group Addresses
    # @todo: allow use of gad name, from GROAT
    ets.weave(fb="weather_temperature", dp="temperature", gad="1/1/1")
    ets.weave(fb="weather_temperature", dp="humidity", gad="1/1/2")
    ets.weave(fb="weather_wind", dp="wind_speed", gad="1/2/1")
    ets.weave(fb="weather_wind", dp="wind_alarm", gad="1/2/2")
    ets.weave(fb="weather_wind", dp="wind_speed_limit", gad="1/2/3")
    ets.weave(fb="weather_wind", dp="wind_alarm_enable", gad="1/2/4")

    print
    print
    ets.printGroat("gad")
    print
    print
    ets.printGroat("go")

    # Start the scheduler
    print
    schedule.start()
    schedule.printJobs()
    print

    # Run the stack main loop (blocking call)
    stack.mainLoop()

    schedule.stop()


if __name__ == "__main__":
    try:
        main()
    except:
        logger.exception("1_main")
