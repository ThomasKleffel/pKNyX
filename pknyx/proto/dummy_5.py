# -*- coding: utf-8 -*-

from pknyx.api import Device, Stack, ETS

stack = Stack()
ets = ETS(stack)


class WeatherBlock(FuntionalBlock):

    # Datapoints definition
    DP_01 = dict(name="PID_TEMPERATURE", type="out", dptId="9.001", defaultValue=0.)
    DP_02 = dict(name="PID_HUMIDITY", type="out", dptId="9.007", defaultValue=0.)
    DP_03 = dict(name="PID_WIND_SPEED", type="out", dptId="9.005", defaultValue=0.)
    DP_04 = dict(name="PID_WIND_ALARM", type="out", dptId="1.005", defaultValue="No alarm")
    DP_05 = dict(name="PID_WIND_SPEED_LIMIT", type="in", dptId="9.005", defaultValue=15.)
    DP_06 = dict(name="PID_WIND_ALARM_ENABLE", type="in", dptId="1.003", defaultValue="Disable")
    DP_07 = dict(name="PID_LATTITUDE", type="param")
    DP_08 = dict(name="PID_LONGITUDE", type="param")
    DP_09 = dict(name="PID_ALTITUDE", type="param")

    # Group Objects datapoints definition
    GO_01 = dict(name="temperature", dp="PID_TEMPERATURE", flags="CRT", priority="low")
    GO_02 = dict(name="humidity", dp="PID_HUMIDITY", flags="CRT", priority="low")
    GO_03 = dict(name="wind_speed", dp="PID_WIND_SPEED", flags="CRT", priority="low")
    GO_04 = dict(name="wind_alarm", dp="PID_WIND_ALARM", flags="CRT", priority="normal")
    GO_05 = dict(name="wind_speed_limit", dp="PID_WIND_SPEED", flags="CWTU", priority="low")
    GO_06 = dict(name="wind_alarm_enable", dp="PID_WIND_SPEED", flags="CWTU", priority="low")

    # Interface Object Properties datapoints definition
    PR_01 = dict(dp="PID_LATTITUDE")
    PR_02 = dict(dp="PID_LONGITUDE")
    PR_03 = dict(dp="PID_ALTITUDE")

    # Polling Values datapoints definition
    #PV_01 = dict(dp="temperature")

    # Memory Mapped datapoints definition
    #MM_01 = dict(dp="temperature")

    @Device.schedule.every(minute=5)
    def checkWindSpeed(self):

        # How we retreive the speed is out of the scope of this proposal
        # speed = xxx

        # Now, write the new speed value to the Datapoint
        self.dp["PID_WIND_SPEED"].value = speed

        # Check alarm speed
        if self.dp["PID_WIND_ALARM_ENABLE"].value == "Enable":
            if speed >= self.dp["PID_WIND_SPEED_LIMIT"].value:
                self.dp["PID_WIND_ALARM"].value = "Alarm"
            elif speed < self.dp["PID_WIND_SPEED_LIMIT"].value - 5.:
                self.dp["PID_WIND_ALARM"].value = "No alarm"

    #@Device.notify


# Weather station class definition
class WeatherStation(Device):

    FB_01 = WeatherBlock(name="weather_block")

# Instanciation of the weather station device object
station = WeatherStation(name="weather_station", desc="My simple weather station example", address="1.2.3")

# Linking weather station Datapoints to Group Address
ets.link(dev=station, dp="temperature", gad="1/1/1")
ets.link(dev=station, dp="humidity", gad="1/1/2")
ets.link(dev=station, dp="wind_speed", gad="1/1/3")
ets.link(dev=station, dp="wind_alarm", gad="1/1/4")
ets.link(dev=station, dp="wind_speed_limit", gad="1/1/5")
ets.link(dev=station, dp="wind_alarm_enable", gad="1/1/6")
