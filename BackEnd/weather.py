# !/usr/bin/python3
import urllib.request as request
from json import loads
from time import sleep

import requests
from pyowm import OWM
from pyowm.utils.geo import Polygon as GeoPolygon

from BackEnd.functions import functions


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
            print('np')
            np = mgr.get_polygon(possible_id)
        else:
            np = mgr.create_polygon(self.polygon(), 'poly')
            self.write_id()

    def isClose(self):
        f = open('../templates/polygons.txt', 'r')
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

    def google_elevation(self, elevation_api_key):
        locations = [(self.lat, self.lon), (self.lat + 1, self.lon + 1)]
        for loc in locations:
            web = 'https://maps.googleapis.com/maps/api/elevation/json?locations={},{}&key={}'.format(loc[0], loc[1],
                                                                                                      elevation_api_key)
            print(web)
            try:
                Request = request(web)
                response = request.urlopen(Request).read()
                places = loads(response)
                print('At {} elevation is: {}'.format(loc, places['results'][0]['elevation']))
                sleep(1)
            except:
                print('Error for location: {0}'.format(loc))

    # Returns Elevations of Current Fire Location and 724.572318682 meters in the direction of the wind
    def open_elevation(self, elevation_api_key):
        # Uses the pair: (Latitude, Longitude) **Normal
        dest = self.loc()
        web = 'http://open.mapquestapi.com/elevation/v1/profile?key={0}&shapeFormat=raw&latLngCollection={1},{2},{3},' \
              '{4}'.format(
            elevation_api_key, self.lat, self.lon, dest[0], dest[1])
        res = requests.get(web)
        resp = str(res.text)
        print("IsInstance Check: {}".format(isinstance(resp, str)))
        final = ""
        counter = 0
        for i in resp:
            if i == 's':
                counter += 1
            final += i
            if not counter <= 2:
                break
        final = final[:-4]
        final = final[21:]
        counter = 0
        temp = ""
        for j in final:
            if j.isnumeric() or j == '.':
                temp += j
                if not final[counter + 1].isnumeric() and final[counter + 1] is not '.':
                    temp += ','
            counter += 1
        temp = temp[:-1]
        val = list(temp.split(sep=","))
        return val

    def slope(self):
        api_key = self.api_keys()
        ls = self.open_elevation(elevation_api_key=api_key['open_api_key'])
        y = float(ls[3]) - float(ls[1])
        x = float(ls[2]) - float(ls[0])
        return float(y/x)
