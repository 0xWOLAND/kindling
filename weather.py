# !/usr/bin/python3
import urllib.request as request
from json import loads
from time import sleep

import requests
from pyowm import OWM
from pyowm.utils.geo import Polygon as GeoPolygon

import functions


class weather:
    global lat
    global lon
    global api_key
    global np

    def __init__(self, api_key, lat, lon):
        self.api_key = api_key
        self.lat = lat
        self.lon = lon

    def api_keys(self):
        i = {'owm_api_key': '258e1d9242c7f27fb8c93e5c3d82e3ca',
'google_api_key': 'AIzaSyBRsTtJ_jPBgFLGVY9G6gRi5hv7CtKRSSA',
'open_api_key': 'WfKLQgReR7LXxlVXchCn0RrPQJT651TI'}
        return i
    def setLat(self, l):
        self.lat = l

    def setLon(self, i):
        self.lon = i

    def setApikey(self, x):
        self.api_key = x

    def getLat(self):
        return self.lat

    def getLon(self):
        return self.lon

    def getApikey(self):
        return self.api_key

    def owm(self):
        owm = OWM(self.api_key)
        return owm

    def obs(self):
        owm = self.owm()
        obs = owm.weather_at_coords(self.lat, self.lon)
        return obs

    def getWeather(self):
        obs = self.obs()
        return obs.get_weather()

    def weather_id(self):
        w = self.getWeather()
        return w.get_weather_code()
    def wind(self):
        w = self.getWeather()
        return w.get_wind()

    def clouds(self):
        w = self.getWeather()
        return w.get_clouds()

    def rain(self):
        w = self.getWeather()
        return w.get_rain()

    def humidity(self):
        w = self.getWeather()
        return w.get_humidity()

    def pressure(self):
        w = self.getWeather()
        return w.get_pressure()

    def fahr(self):
        w = self.getWeather()
        return w.get_temperature('fahrenheit')

    def celc(self):
        w = self.getWeather()
        return w.get_temperature(unit='celsius')

    def icon(self):
        w = self.getWeather()
        return w.get_weather_icon_name()

    def square(self):
        i = [[float(self.lon), float(self.lat)],
             [float(self.lon - 0.005), float(self.lat)],
             [float(self.lon - 0.005), float(self.lat - 0.005)]]
        return i

    def polygon(self):
        i = 0
        num = 45
        loc = []
        while i < 3:
            temp = (functions.deg_to_rad(num))
            x = functions.triangle_points(h=self.lon, k=self.lat, r=0.005, t=temp)
            loc.append(x)
            num += 120
            i += 1
        # Creates triangle centered at (self.lon, self.lat)
        gp = GeoPolygon([[
            [loc[0][0], loc[0][1]],
            [loc[1][0], loc[1][1]],
            [loc[2][0], loc[2][1]],
            [loc[0][0], loc[0][1]]]])
        return gp

    def mgr(self):
        owm = self.owm()
        mgr = owm.agro_manager()
        return mgr

    def new_polygon(self):
        global np
        possible_id = self.isClose()
        check = isinstance(possible_id, str)
        mgr = self.mgr()
        if check:
            np = mgr.get_polygon(possible_id)
        else:
            np = mgr.create_polygon(self.polygon(), 'poly')
            self.write_id()

    def isClose(self):
        f = open('templates/polygons.txt')
        r = f.readlines()
        isTrue = False
        for i in r:
            arr = i.split(sep=',')
            private_lat = float(arr[2])
            private_lon = float(arr[3])
            dist = functions.dist(x=self.lon, y=self.lat, x0=private_lon, y0=private_lat)
            if dist <= 100:
                isTrue = True
                id = str(arr[1])
            else:
                pass
        if isTrue:
            return id
        else:
            return False

    def write_id(self):
        f = open('templates/polygons.txt', 'a+')
        id = self.new_polygon_id()
        user_id = self.new_polygon_user_id()
        f.write('{0},{1},{2},{3}\n'.format(user_id, id, self.lat, self.lon))

    def new_polygon_id(self):
        try:
            return np.id
        except:
            return None

    def new_polygon_user_id(self):
        try:
            return np.user_id
        except:
            return None

    def setPolygonName(self, name):
        try:
            np.name = name
        except:
            None

    def getPolygonName(self):
        try:
            return np.name
        except:
            return None

    def deletePolygon(self):
        try:
            mgr = self.mgr()
            return mgr.delete_polygon(np)
        except:
            return None

    # ---------------------------------------------------------------------------------------------------------
    # Soil Data is updated twice a day
    def soil(self):
        mgr = self.mgr()
        self.new_polygon()
        poly = np
        soil = mgr.soil_data(poly)
        return soil

    def soil_surface_temp(self, unit):
        if unit.lower == 'celcius' or unit.lower == 'fahrenheit' or unit.lower == 'kelvin':
            soil = self.soil()
            return soil.surface_temp(unit='kelvin')
        else:
            return None

    def soil_ten_cm_temp(self, unit):
        if unit == 'celcius' or unit == 'fahrenheit' or unit == 'kelvin':
            soil = self.soil()
            return soil.ten_cm_temp(unit=unit)
        else:
            return None

    def loc(self):
        loc = self.wind()
        try:
            deg = functions.deg_to_rad(float(loc['deg']) - 90)
            num = functions.triangle_points(h=self.lon, k=self.lat, r=0.005, t=deg)
            return num
        except:
            return None

    def moisture(self):
        soil = self.soil()
        return soil.moisture

    def moisture_percent(self):
        return self.moisture() * 100

    def is_fuel_dead(self):
        moisture = self.moisture_percent()
        dead = False
        if moisture >= 30:
            return False
        else:
            return True

    
