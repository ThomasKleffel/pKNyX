# -*- coding: utf-8 -*-

from pknyx.api import Device, Stack, ETS

stack = Stack()
ets = ETS(stack)


class WeatherBlock(FuntionalBlock):

    # Datapoints definition
    DP_01 = dict(name="temperature", type="output", com="groupObject", defaultValue=19.)
    DP_02 = dict(name="humidity", ype="output", dptId="9.007", defaultValue=50.)
    DP_03 = dict(name="wind_speed", type="output", dptId="9.005", defaultValue=0.)
    DP_04 = dict(name="wind_alarm", type="output", dptId="1.005", defaultValue="No alarm")
    DP_05 = dict(name="wind_speed_limit", type="input", dptId="9.005", defaultValue=15.)
    DP_06 = dict(name="wind_alarm_enable", type="input", dptId="1.003", defaultValue="Disable")
    DP_07 = dict(name="lattitude", type="param")
    DP_08 = dict(name="longitude", type="param")
    DP_09 = dict(name="altitude", type="param")

    # Group Objects datapoints definition (can (should?) be defined in subclass)
    GO_01 = dict(dp="temperature", flags="CRT", priority="low")
    GO_02 = dict(dp="humidity", flags="CRT", priority="low")
    GO_03 = dict(dp="wind_speed", flags="CRT", priority="low")
    GO_04 = dict(dp="wind_alarm", flags="CRT", priority="normal")
    GO_05 = dict(dp="wind_speed_limit", flags="CWTU", priority="low")
    GO_06 = dict(dp="wind_alarm_enable", flags="CWTU", priority="low")

    # Interface Object Properties datapoints definition (name will be "PID_<upper(dp.name)>")
    PR_01 = dict(dp="lattitude")
    PR_02 = dict(dp="longitude")
    PR_03 = dict(dp="altitude")

    # Polling Values datapoints definition
    #PV_01 = dict(dp="temperature")

    # Memory Mapped datapoints definition
    #MM_01 = dict(dp="temperature")

    DESC = "Weather station block"

    @Device.schedule.every(minute=5)
    def checkWindSpeed(self, event):

        # How we retreive the speed is out of the scope of this proposal
        # speed = xxx

        # Now, write the new speed value to the Datapoint
        self.dp["wind_speed"].value = speed

        # Check alarm speed
        if self.dp["wind_alarm_enable"].value == "Enable":
            if speed >= self.dp["wind_speed_limit"].value:
                self.dp["wind_alarm"].value = "Alarm"
            elif speed < self.dp["wind_speed_limit"].value - 5.:
                self.dp["wind_alarm"].value = "No alarm"

    @Device.notify.datapoint(id="wind_speed")  # Single DP
    #@Device.notify.datapoint(id="temperature")  # Single DP
    #@Device.notify.datapoint(ids=("wind_speed", "temperature"))  # Multiple DP
    #@Device.notify.datapoint()  # All DP
    #@Device.notify.datapoint(id="wind_speed", change=True)  # Only if value changed
    #@Device.notify.datapoint(id="wind_speed", condition="change")  # Only if value changed (could be "always")
    #@Device.notify.group(gad="1/1/1")  # Single group object
    def doSomething(self, event):
        """
        event.type
        event.dp
        event.old
        event.new
        """
        pass


# Weather station class definition
class WeatherStation(Device):

    FB_01 = WeatherBlock(name="weather_block")

# Instanciation of the weather station device object
station = WeatherStation(name="weather_station", desc="My simple weather station", address="1.2.3")

# Linking weather station Datapoints to Group Address
ets.link(dev=station, dp="temperature", gad="1/1/1")
ets.link(dev=station, dp="humidity", gad="1/1/2")
ets.link(dev=station, dp="wind_speed", gad="1/1/3")
ets.link(dev=station, dp="wind_alarm", gad="1/1/4")
ets.link(dev=station, dp="wind_speed_limit", gad="1/1/5")
ets.link(dev=station, dp="wind_alarm_enable", gad="1/1/6")
