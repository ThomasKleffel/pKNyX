# -*- coding: utf-8 -*-

from pknyx.api import Device

from fb.weatherTempFB import WeatherTempFB
from fb.weatherWindFB import WeatherWindFB


class Weather(Device):
    FB_01 = dict(cls=WeatherTempFB, name="weather_temp_fb", desc="weather temp fb")
    FB_02 = dict(cls=WeatherWindFB, name="weather_wind_fb", desc="weather wind fb")

    LNK_01 = dict(fb="weather_temp_fb", dp="temperature", gad="1/1/1")
    LNK_02 = dict(fb="weather_temp_fb", dp="humidity", gad="1/1/2")
    LNK_03 = dict(fb="weather_wind_fb", dp="wind_speed", gad="1/1/3")
    LNK_04 = dict(fb="weather_wind_fb", dp="wind_alarm", gad="1/1/4")
    LNK_05 = dict(fb="weather_wind_fb", dp="wind_speed_limit", gad="1/1/5")
    LNK_06 = dict(fb="weather_wind_fb", dp="wind_alarm_enable", gad="1/1/6")

    DESC = "Weather"


DEVICE = Weather
