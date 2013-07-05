# -*- coding: utf-8 -*-

import math
import time

from pknyx.common.helpers import dd2dms, dms2dd

from pknyx.api import FunctionalBlock, Device, Stack, ETS
#from pknyx.api import Scheduler, Notifier

# ETS GAD map
# @todo: make a tool to import from ETS
GAD_MAP = {"1": "heating",
           "1/1": "setpoint",
           "1/1/1": "living",
           "1/1/2": "bedroom 1",
           "1/1/3": "bedroom 2",
           "1/1/4": "bedroom 3",
           "1/2": "temperature",
           "1/2/1": "living",
           "1/2/2": "bedroom 1",
           "1/2/3": "bedroom 2",
           "1/2/4": "bedroom 3",
           "2": "lights",
           "2/1": "living",
           "2/2": "etage",
           "2/2/2": "bedroom 1"
          }


stack = Stack()
ets = ETS(stack)
ets.gadMap = GAD_MAP

#schedule = Scheduler()
#notify = Notifier()


class WeatherWindBlock(FunctionalBlock):

    # Datapoints definition
    DP_01 = dict(name="wind_speed", access="output", dptId="9.005", default=0.)
    DP_02 = dict(name="wind_alarm", access="output", dptId="1.005", default="No alarm")
    DP_03 = dict(name="wind_speed_limit", access="input", dptId="9.005", default=15.)
    DP_04 = dict(name="wind_alarm_enable", access="input", dptId="1.003", default="Disable")

    GO_01 = dict(dp="wind_speed", flags="CRT", priority="low")
    GO_02 = dict(dp="wind_alarm", flags="CRT", priority="normal")
    GO_03 = dict(dp="wind_speed_limit", flags="CWT", priority="low")
    GO_04 = dict(dp="wind_alarm_enable", flags="CWT", priority="low")

    DESC = "Wind management block"

    #schedule.every(minute=5)
    def updatehWindSpeed(self, event):

        # How we retreive the speed is out of the scope of this proposal
        # speed = xxx

        # Now, write the new speed value to the Datapoint
        # This will trigger the bus notification, if a group object is associated
        self.dp["wind_speed"].value = speed

    #notify.datapoint(name="wind_speed_limit")  # Single DP
    #notify.datapoint()  # All DP
    #notify.group(gad="1/1/1")  # Single group address
    def checkWindSpeed(self, event):

        # Read inputs/params
        wind_speed = self.dp["wind_speed"]
        wind_alarm_enable = self.dp["wind_alarm_enable"].value
        wind_speed_limit = self.dp["wind_speed_limit"].value

        # Check if alarm
        if wind_speed > wind_speed_limit:
            wind_alarm = "Alarm"
        elif wind_speed < wind_speed_limit - 5.:  # Little histeresis
            wind_alarm = "No alarm"

        # Write outputs
        if wind_alarm_enable:
            self.dp["wind_alarm"].value = wind_alarm


class WeatherTemperatureBlock(FunctionalBlock):

    # Datapoints definition
    DP_01 = dict(name="temperature", access="output", com="GO", dptId="9.001", default=19.)
    DP_02 = dict(name="humidity", access="output", com="GO", dptId="9.007", default=50.)

    GO_01 = dict(dp="temperature", flags="CRT", priority="low")
    GO_02 = dict(dp="humidity", flags="CRT", priority="low")

    DESC = "Temperature management block"

    #schedule.every(minute=5)
    def updateTemperature(self, event):

        # How we retreive the temperature is out of the scope of this proposal
        # temperature = xxx
        self.dp["temperature"] = temperature

    #schedule.every(minute=5)
    def updateHumidity(self, event):

        # How we retreive the humidity is out of the scope of this proposal
        # humidity = xxx
        self.dp["humidity"] = humidity


class WeatherSunPositionBlock(FunctionalBlock):

    # Datapoints definition
    DP_01 = dict(name="right_ascension", access="output", com="GO", dptId="14.007", default=0.)
    DP_02 = dict(name="declination", access="output", com="GO", dptId="14.007", default=0.)
    DP_03 = dict(name="elevation", access="output", com="GO", dptId="14.007", default=0.)
    DP_04 = dict(name="azimuth", access="output", com="GO", dptId="14.007", default=0.)
    DP_05 = dict(name="latitude", access="param", com="PR", dptId="14.007", default=0.)
    DP_06 = dict(name="longitude", access="param", com="PR", dptId="14.007", default=0.)
    DP_07 = dict(name="timezone", access="param", com="PR", dptId="1.xxx", default=1)
    DP_08 = dict(name="saving_time", access="param", com="PR", dptId="1.xxx", default=1)

    GO_01 = dict(dp="right_ascension", flags="CRT", priority="low")
    GO_02 = dict(dp="declination", flags="CRT", priority="low")
    GO_03 = dict(dp="elevation", flags="CRT", priority="low")
    GO_04 = dict(dp="azimuth", flags="CRT", priority="low")
    GO_05 = dict(dp="latitude", flags="CRT", priority="low")
    GO_06 = dict(dp="longitude", flags="CRT", priority="low")
    GO_07 = dict(dp="timezone", flags="CRT", priority="low")
    GO_08 = dict(dp="saving_time", flags="CRT", priority="low")

    DESC = "Sun position management block"

    def _computeJulianDay(self, year, month, day, hour, minute, second):
        """ Compute the julian day.
        """
        day += hour / 24. + minute / 1440. + second / 86400.

        if month in (1, 2):
            year -= 1
            month += 12

        a = int(year / 100.)
        b = 2 - a + int(a / 4.)

        julianDay = int(365.25 * (year + 4716.)) + int(30.6001 * (month + 1)) + day + b - 1524.5
        julianDay -= (self._timeZone + self._savingTime) / 24.
        julianDay -= 2451545.  # ???!!!???

        return julianDay

    def _siderealTime(self, julianDay):
        """ Compute the sidereal time.
        """
        centuries = julianDay / 36525.
        siderealTime = (24110.54841 + (8640184.812866 * centuries) + (0.093104 * (centuries ** 2)) - (0.0000062 * (centuries ** 3))) / 3600.
        siderealTime = ((siderealTime / 24.) - int(siderealTime / 24.)) * 24.

        return siderealTime

    def _equatorialCoordinates(self, year, month, day, hour, minute, second):
        """ Compute rightAscension and declination.
        """
        julianDay =  self.computeJulianDay(year, month, day, hour, minute, second)

        g = 357.529 + 0.98560028 * julianDay
        q = 280.459 + 0.98564736 * julianDay
        l = q + 1.915 * math.sin(math.radians(g)) + 0.020 * math.sin(math.radians(2 * g))
        e = 23.439 - 0.00000036 * julianDay
        rightAscension = math.degrees(math.atan(math.cos(math.radians(e)) * math.sin(math.radians(l)) / math.cos(math.radians(l)))) / 15.
        if math.cos(math.radians(l)) < 0.:
            rightAscension += 12.
        if math.cos(math.radians(l)) > 0. and math.sin(math.radians(l)) < 0.:
            rightAscension += 24.

        declination = math.degrees(math.asin(math.sin(math.radians(e)) * math.sin(math.radians(l))))

        return rightAscension, declination

    def _azimuthalCoordinates(self, year, month, day, hour, minute, second):
        """ Compute elevation and azimuth.
        """
        julianDay =  self.computeJulianDay(year, month, day, hour, minute, second)
        siderealTime = self.siderealTime(julianDay)
        angleH = 360. * siderealTime / 23.9344
        angleT = (hour - (self._timeZone + self._savingTime) - 12. + minute / 60. + second / 3600.) * 360. / 23.9344
        angle = angleH + angleT
        rightAscension, declination = self.equatorialCoordinates(year, month, day, hour, minute, second)
        angle_horaire = angle - rightAscension * 15. + self._longitude

        elevation = math.degrees(math.asin(math.sin(math.radians(declination)) * math.sin(math.radians(self._latitude)) - math.cos(math.radians(declination)) * math.cos(math.radians(self._latitude)) * math.cos(math.radians(angle_horaire))))

        azimuth = math.degrees(math.acos((math.sin(math.radians(declination)) - math.sin(math.radians(self._latitude)) * math.sin(math.radians(elevation))) / (math.cos(math.radians(self._latitude)) * math.cos(math.radians(elevation)))))
        sinazimuth = (math.cos(math.radians(declination)) * math.sin(math.radians(angle_horaire))) / math.cos(math.radians(elevation))
        if (sinazimuth < 0.):
            azimuth = 360. - azimuth

        return elevation, azimuth

    #schedule.every(minute=5)
    def updatePosition(self, event):

        # Read inputs/params
        self._latitude = self.dp["latitude"].value
        self._longitude = self.dp["longitude"].value
        self._timeZone = self.dp["timezone"].value
        self._savingTime = self.dp["saving_time"].value

        # Computations
        tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.localtime()
        julianDay =  sun.computeJulianDay(tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec)
        siderealTime = sun.siderealTime(julianDay)

        rightAscension, declination = sun.equatorialCoordinates(tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec)
        elevation, azimuth = sun.azimuthalCoordinates(tm_year, tm_mon, tm_day, tm_hour, tm_min, tm_sec)

        # Write outputs
        self.dp["right_ascension"].value = rightAscension
        self.dp["declination"].value = declination
        self.dp["elevation"].value = elevation
        self.dp["azimuth"].value = azimuth


# Weather station class definition
class WeatherStationDevice(Device):

    #FB_01 = WeatherWindBlock(name="weather_wind_block", desc="Wind")
    #FB_02 = WeatherTemperatureBlock(name="weather_temperature_block", desc="Temp")
    #FB_03 = WeatherSunPositionBlock(name="weather_sun_position_block", desc="Sun")
    FB_01 = dict(name="weather_wind_block", cls=WeatherWindBlock, desc="wind 1")
    FB_02 = dict(name="weather_temperature_block", cls=WeatherTemperatureBlock, desc="temp 1")
    FB_03 = dict(name="weather_sun_position_block", cls=WeatherSunPositionBlock, desc="sun 1")

    DESC = "Virtual weather station"

    #@notify.datapoint(name="elevation")
    #@notify.datapoint(name="azimuth")
    def bla(self, event):
        pass

# @todo: remove the Device -> done at process level?

# Instanciation of the weather station device object
station = WeatherStationDevice(name="weather_station", desc="Weather", address="1.2.3")

ets.register(station)

# Weave weather station Datapoints to GroupAddresses
ets.weave(dev=station, dp="temperature", gad="1/1/1")
ets.weave(dev=station, dp="humidity", gad="1/1/2")

ets.weave(dev=station, dp="wind_speed", gad="1/1/3")
ets.weave(dev=station, dp="wind_alarm", gad="1/1/4")
ets.weave(dev=station, dp="wind_speed_limit", gad="1/1/5")
ets.weave(dev=station, dp="wind_alarm_enable", gad="1/1/6")

ets.weave(dev=station, dp="right_ascension", gad="1/1/3")
ets.weave(dev=station, dp="declination", gad="1/1/4")
ets.weave(dev=station, dp="elevation", gad="1/1/5")
ets.weave(dev=station, dp="azimuth", gad="1/1/6")
ets.weave(dev=station, dp="latitude", gad="1/1/7")
ets.weave(dev=station, dp="longitude", gad="1/1/8")
ets.weave(dev=station, dp="timezone", gad="1/1/9")
ets.weave(dev=station, dp="saving_time", gad="1/1/10")

print
print
ets.printMapTable("gad")
print
print
ets.printMapTable("go")
