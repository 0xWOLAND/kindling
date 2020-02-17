# coding: utf-8
import geocoder
from flask import Flask, render_template, request, url_for, redirect
from flask_googlemaps import GoogleMaps, Map, icons
import math
import pandas as pd
import gmaps
import urllib.request
import numpy
import json
import datetime
from geopy.geocoders import Nominatim
app = Flask(__name__, template_folder="templates")

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyBZa-XgzpZuRt0jqaTBlqShQwusUNrA9WA"

# you can also pass key here
GoogleMaps(
    app,
    key="AIzaSyBZa-XgzpZuRt0jqaTBlqShQwusUNrA9WA"
)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Rotate:
    def __init__(self, x, y, deg):
        self.x = x
        self.y = y
        self.deg = deg

    def rotate(self):
        deg = self.deg_to_rad()
        X = float(self.x * math.cos(deg) + self.y * math.sin(deg))
        Y = float(self.y * math.cos(deg) - self.x * math.sin(deg))
        return [X, Y]

    def deg_to_rad(self):
        return self.deg * math.pi / 180


class FireModel:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def get_lat_lon(self):
        d = pd.read_csv('https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_7d.csv')
        ls = []
        inter = []
        for i in range(len(d)):
            inter.append(d['latitude'][i])
            inter.append(d['longitude'][i])
            ls.append(inter)
            inter = []
        return ls

    def closest_fire_coord(self):
        ls = self.get_lat_lon()
        closest = 1234567876543456787643
        closest_x = 0
        closest_y = 0
        for i in range(len(ls)):
            dist = dist(x=self.lat, y=self.lon, x0=ls[i][0], y0=ls[i][1])
            if dist < closest:
                closest = dist
                closest_x = ls[i][0]
                closest_y = ls[i][1]
        nums = [closest_x, closest_y]
        return nums


def slope(vertical, horizontal):
    return (vertical / horizontal) * 100

def dist(x, y, x0, y0):
    return math.sqrt(abs((math.pow(x - x0, 2) + (math.pow(y - y0, 2)))))

def circledist(coord1, coord2):
    # Coordinates in decimal degrees (e.g. 2.2948, 12.89234)
    lon1, lat1 = coord1
    lon2, lat2 = coord2

    R = 6371000
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c  # output distance in meters

    km = meters / 1000.0  # output in kilometers

    meters = round(meters, 3)
    km = round(km, 3)

    return km

def hour():
    now = datetime.datetime.now()
    return now.hour
def coord():
    g = geocoder.ip('me')
    print(g.latlng)
    return g.latlng

def triangle_points(r, t, h, k):
    x = float(r * math.cos(t) + h)
    y = float(r * math.sin(t) + k)
    coord = [y, x]
    return coord

def ellipse(r, h, t,  k, wind_vector, windy_dir):
    x = float(r * math.cos(t)) * wind_vector
    y = float(r * math.sin(t)) * (wind_vector*0.5)
    x1 = (x * math.cos(wind_dir) - y * math.sin(wind_dir)) + h
    y1 = (y * math.cos(wind_dir) + x * math.sin(wind_dir)) + k
    coord = [x1,y1]
    return coord


def deg_to_rad(deg):
    x = (deg * math.pi) / 180
    return x
 

def fire_ring(x, y):
    coordinates = coord()
    lat = float(coordinates[0])
    lon = float(coordinates[1])
    w = weather('258e1d9242c7f27fb8c93e5c3d82e3ca', lat, lon)
    f = FireModel(lat, lon)
    loc = f.get_lat_lon()
    d = w.wind()['deg']
    s = w.wind()['speed']
    poly = []
    for j in range(360):
        poly.append(ellipse(0.01,x, j, y,s*0.5, d))
    poly.append(ellipse(0.01,x, 0, y,s*0.5, d))
    max_dist = 0
    max_dist = 0
    edge = []
    for i in range(len(poly)):
        if dist(x,y,poly[i][0],poly[i][1]) > max_dist:
            max_dist = dist(x,y,poly[i][0],poly[i][1])
            edge = [poly[i][0], poly[i][1]]
    dx = x - edge[0]
    dy = y - edge[1]
    if dx >= 0:
        right = True
    else:
        right = False
    if dy >= 0:
        top = True
    else:
        top = False
    x_true = False
    y_true = False
    n = poly
    for i in range(len(poly)):
        poly[i][0] += dx
        poly[i][1] += dy
    return poly

def get_location(address_or_zipcode):
    lat, lng = None, None
    api_key = 'AIzaSyBZa-XgzpZuRt0jqaTBlqShQwusUNrA9WA'
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = "{}?address={}&key={}".format(base_url, address_or_zipcode,api_key)
    # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key
    r = rq.get(endpoint)
    if r.status_code not in range(200, 299):
        return None, None
    try:
        '''
        This try block incase any of our inputs are invalid. This is done instead
        of actually writing out handlers for all kinds of responses.
        '''
        results = r.json()['results'][0]
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
    except:
        pass
    return lat, lng

# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

class text:
    def __init__(self, message, number):
        self.message = message
        self.number = number

    def main(self):
        # Your Account Sid and Auth Token from twilio.com/console
        # DANGER! This is insecure. See http://twil.io/secure
        coordinates = coord()
        lat = float(coordinates[0])
        lon = float(coordinates[1])
        w = weather('258e1d9242c7f27fb8c93e5c3d82e3ca', lat, lon)
        geolocator = Nominatim()
        location = geolocator.reverse("{}, {}".format(lat,lon))
        s = w.moisture()
        website = "http://kindlingmaps-1579146339794.appspot.com/nearyou/{}&{}".format(lat,lon)
        msg = "Fire reported at {}, Soil Moisture Content: {}, Reporter's message: {}, View Map of Location at {}".format(location.address, s, self.message,website) 
        print(msg)
        account_sid = 'ACea8786990058ddc73047b144e7e3b5df'
        auth_token = '60730010a28a1cabaf43081b83c7b67c'
        client = Client(account_sid, auth_token)
        m = client.messages.create(
        body='{}'.format(msg),
        from_='[+][1][4792501916]',
        to='[+][1][{}]'.format(self.number)
        )
        return(m.sid)

# !/usr/bin/python3
from json import loads
from time import sleep

import requests as rq
from pyowm import OWM
from pyowm.utils.geo import Polygon as GeoPolygon



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
            temp = (deg_to_rad(num))
            x = triangle_points(h=self.lon, k=self.lat, r=0.005, t=temp)
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
            d = dist(x=self.lon, y=self.lat, x0=private_lon, y0=private_lat)
            if d <= 100:
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
            deg = deg_to_rad(float(loc['deg']) - 90)
            num = triangle_points(h=self.lon, k=self.lat, r=0.005, t=deg)
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

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
coordinates = coord()
lat = float(coordinates[0])
lon = float(coordinates[1])


# ----------------------------------------------------------------
@app.route('/mobile')
@app.route('/')
def hello():
    return render_template('home.html')


@app.route('/report', methods=["POST", "GET"])
def mid():
    if request.method == "POST":
        extra_notes = request.form["name"]
        t = text(extra_notes, '5127847689')
        t.main()
        return render_template('after_text.html')
    else:
        return render_template('report.html')

@app.route('/traveling', methods=["POST", "GET"])
def bot():
    if request.method == "POST":
        time = hour()
        x = get_location(request.form["address_line"])
        lat = x[0]
        lon = x[1]
        f = FireModel(lat, lon)
        loc = f.get_lat_lon()
        fires_lat = []
        fires_lon = []
        for i in range(len(loc)):
            fires_lat.append(loc[i][0])
            fires_lon.append(loc[i][1])
        m = []
        w = weather('258e1d9242c7f27fb8c93e5c3d82e3ca', loc[0][0], loc[0][1])
        s = w.moisture()
        for i in range(len(loc)):
            if(s > 0.4):
                severity = "Low"
            elif(s <= 0.4 and s > 0.3):
                severity = "Medium"
            else:
                severity = "High"
            res = "Severity: {}".format(severity)
            m.append({'icon': 'static/css/fire copy.png','lat': loc[i][0], 'lng': loc[i][1], 'infobox':res})
        closest = []
        second = []
        third = []
        n1 =2783465827645
        n2=230945723095
        n3 = 235723659723
        for i in range(len(loc)):
            if dist(lat, lon, loc[i][0], loc[i][1]) < n1 and dist(lat, lon, loc[i][0], loc[i][1]) < n2 and dist(lat, lon, loc[i][0], loc[i][1]) < n3:
                n1 = dist(lat, lon, loc[i][0], loc[i][1])
                closest = [loc[i][0], loc[i][1]]
            elif dist(lat, lon, loc[i][0], loc[i][1]) >= n1 and dist(lat, lon, loc[i][0], loc[i][1]) < n2 and dist(lat, lon, loc[i][0], loc[i][1]) < n3:
                n2 = dist(lat, lon, loc[i][0], loc[i][1])
                second = [loc[i][0], loc[i][1]]
            elif dist(lat, lon, loc[i][0], loc[i][1]) >= n1 and dist(lat, lon, loc[i][0], loc[i][1]) >= n2 and dist(lat, lon, loc[i][0], loc[i][1]) < n3:
                n3 = dist(lat, lon, loc[i][0], loc[i][1])
                third = [loc[i][0], loc[i][1]]
        c_raw = fire_ring(closest[0], closest[1])
        s_raw = fire_ring(second[0], second[1])
        t_raw = fire_ring(third[0], third[1])
    # -------------------------------------------------------------------------------------
        c_raw_x = []
        c_raw_y = []
        c_raw_length = len(c_raw)
        for c in range(len(c_raw)):
            c_raw_x.append(c_raw[c][0])
            c_raw_y.append(c_raw[c][1])
        s_raw_x = []
        s_raw_y = []
        s_raw_length = len(s_raw)
        for s in range(len(s_raw)):
            s_raw_x.append(s_raw[s][0])
            s_raw_y.append(s_raw[s][1])
        t_raw_x = []
        t_raw_y = []
        t_raw_length = len(t_raw)
        for t in range(len(t_raw)):
            t_raw_x.append(t_raw[t][0])
            t_raw_y.append(t_raw[t][1])
    # ------------------------------------------------------------------------------------------------------------------------------------------------
        w = weather('258e1d9242c7f27fb8c93e5c3d82e3ca', lat, lon)
        l = w.weather_id()
        s = w.moisture()
        verdict = ""
        if l < 250 and l >= 200 and s < 0.25:
            verdict = "Chance of Natural Wildfire Breakout"
        else:
            verdict = "Low Chance of Natural Wildfire Breakout" 





        return render_template(
            'example.html',
            lat=float(lat),
            lon=float(lon),
            v=verdict,
            fires_lat=fires_lat,
            fires_lon=fires_lon,
            length=len(loc),
            c_raw_x=c_raw_x,
            c_raw_y=c_raw_y,
            s_raw_x=s_raw_x,
            s_raw_y=s_raw_y,
            t_raw_x=t_raw_x,
            t_raw_y=t_raw_y,
            c_raw_length=c_raw_length,
            s_raw_length=s_raw_length,
            t_raw_length=t_raw_length,
            time=time

        )
        
    else:
        return render_template("specific_loc.html")


@app.route('/desktop')
def desktop():
    return render_template("desktop.html")

@app.route("/nearyou")
def mapview():
 # ------------------------------------------------------------------------------------------------------------
    # Prepare Coords for Fire Spread
    coordinates = coord()
    time = hour()
    lat = float(coordinates[0])
    lon = float(coordinates[1])
    f = FireModel(lat, lon)
    loc = f.get_lat_lon()
    fires_lat = []
    fires_lon = []
    for i in range(len(loc)):
        fires_lat.append(loc[i][0])
        fires_lon.append(loc[i][1])
    m = []
    w = weather('258e1d9242c7f27fb8c93e5c3d82e3ca', loc[0][0], loc[0][1])
    s = w.moisture()
    for i in range(len(loc)):
        if(s > 0.4):
            severity = "Low"
        elif(s <= 0.4 and s > 0.3):
            severity = "Medium"
        else:
            severity = "High"
        res = "Severity: {}".format(severity)
        m.append({'icon': 'static/css/fire copy.png','lat': loc[i][0], 'lng': loc[i][1], 'infobox':res})
    closest = []
    second = []
    third = []
    n1 =2783465827645
    n2=230945723095
    n3 = 235723659723
    for i in range(len(loc)):
        if dist(lat, lon, loc[i][0], loc[i][1]) < n1 and dist(lat, lon, loc[i][0], loc[i][1]) < n2 and dist(lat, lon, loc[i][0], loc[i][1]) < n3:
            n1 = dist(lat, lon, loc[i][0], loc[i][1])
            closest = [loc[i][0], loc[i][1]]
        elif dist(lat, lon, loc[i][0], loc[i][1]) >= n1 and dist(lat, lon, loc[i][0], loc[i][1]) < n2 and dist(lat, lon, loc[i][0], loc[i][1]) < n3:
            n2 = dist(lat, lon, loc[i][0], loc[i][1])
            second = [loc[i][0], loc[i][1]]
        elif dist(lat, lon, loc[i][0], loc[i][1]) >= n1 and dist(lat, lon, loc[i][0], loc[i][1]) >= n2 and dist(lat, lon, loc[i][0], loc[i][1]) < n3:
            n3 = dist(lat, lon, loc[i][0], loc[i][1])
            third = [loc[i][0], loc[i][1]]
    c_raw = fire_ring(closest[0], closest[1])
    s_raw = fire_ring(second[0], second[1])
    t_raw = fire_ring(third[0], third[1])
# -------------------------------------------------------------------------------------
    c_raw_x = []
    c_raw_y = []
    c_raw_length = len(c_raw)
    for c in range(len(c_raw)):
        c_raw_x.append(c_raw[c][0])
        c_raw_y.append(c_raw[c][1])
    s_raw_x = []
    s_raw_y = []
    s_raw_length = len(s_raw)
    for s in range(len(s_raw)):
        s_raw_x.append(s_raw[s][0])
        s_raw_y.append(s_raw[s][1])
    t_raw_x = []
    t_raw_y = []
    t_raw_length = len(t_raw)
    for t in range(len(t_raw)):
        t_raw_x.append(t_raw[t][0])
        t_raw_y.append(t_raw[t][1])
# ------------------------------------------------------------------------------------------------------------------------------------------------
    w = weather('258e1d9242c7f27fb8c93e5c3d82e3ca', lat, lon)
    l = w.weather_id()
    s = w.moisture()
    verdict = ""
    if l < 250 and l >= 200 and s < 0.25:
        verdict = "Chance of Natural Wildfire Breakout"
    else:
        verdict = "Low Chance of Natural Wildfire Breakout" 





    return render_template(
        'example.html',
        lat=float(lat),
        lon=float(lon),
        v=verdict,
        fires_lat=fires_lat,
        fires_lon=fires_lon,
        length=len(loc),
        c_raw_x=c_raw_x,
        c_raw_y=c_raw_y,
        s_raw_x=s_raw_x,
        s_raw_y=s_raw_y,
        t_raw_x=t_raw_x,
        t_raw_y=t_raw_y,
        c_raw_length=c_raw_length,
        s_raw_length=s_raw_length,
        t_raw_length=t_raw_length,
        time=time

    )


@app.route("/nearyou/<latitude>&<longitude>")
def newview(latitude,longitude):
 # ------------------------------------------------------------------------------------------------------------
    # Prepare Coords for Fire Spread
    lat = float(latitude)
    time = hour()
    lon = float(longitude)
    f = FireModel(lat, lon)
    f = FireModel(lat, lon)
    loc = f.get_lat_lon()
    fires_lat = []
    fires_lon = []
    for i in range(len(loc)):
        fires_lat.append(loc[i][0])
        fires_lon.append(loc[i][1])
    m = []
    w = weather('258e1d9242c7f27fb8c93e5c3d82e3ca', loc[0][0], loc[0][1])
    s = w.moisture()
    for i in range(len(loc)):
        if(s > 0.4):
            severity = "Low"
        elif(s <= 0.4 and s > 0.3):
            severity = "Medium"
        else:
            severity = "High"
        res = "Severity: {}".format(severity)
        m.append({'icon': 'static/css/fire copy.png','lat': loc[i][0], 'lng': loc[i][1], 'infobox':res})
    closest = []
    second = []
    third = []
    n1 =2783465827645
    n2=230945723095
    n3 = 235723659723
    for i in range(len(loc)):
        if dist(lat, lon, loc[i][0], loc[i][1]) < n1 and dist(lat, lon, loc[i][0], loc[i][1]) < n2 and dist(lat, lon, loc[i][0], loc[i][1]) < n3:
            n1 = dist(lat, lon, loc[i][0], loc[i][1])
            closest = [loc[i][0], loc[i][1]]
        elif dist(lat, lon, loc[i][0], loc[i][1]) >= n1 and dist(lat, lon, loc[i][0], loc[i][1]) < n2 and dist(lat, lon, loc[i][0], loc[i][1]) < n3:
            n2 = dist(lat, lon, loc[i][0], loc[i][1])
            second = [loc[i][0], loc[i][1]]
        elif dist(lat, lon, loc[i][0], loc[i][1]) >= n1 and dist(lat, lon, loc[i][0], loc[i][1]) >= n2 and dist(lat, lon, loc[i][0], loc[i][1]) < n3:
            n3 = dist(lat, lon, loc[i][0], loc[i][1])
            third = [loc[i][0], loc[i][1]]
    c_raw = fire_ring(closest[0], closest[1])
    s_raw = fire_ring(second[0], second[1])
    t_raw = fire_ring(third[0], third[1])
# -------------------------------------------------------------------------------------
    c_raw_x = []
    c_raw_y = []
    c_raw_length = len(c_raw)
    for c in range(len(c_raw)):
        c_raw_x.append(c_raw[c][0])
        c_raw_y.append(c_raw[c][1])
    s_raw_x = []
    s_raw_y = []
    s_raw_length = len(s_raw)
    for s in range(len(s_raw)):
        s_raw_x.append(s_raw[s][0])
        s_raw_y.append(s_raw[s][1])
    t_raw_x = []
    t_raw_y = []
    t_raw_length = len(t_raw)
    for t in range(len(t_raw)):
        t_raw_x.append(t_raw[t][0])
        t_raw_y.append(t_raw[t][1])
# ------------------------------------------------------------------------------------------------------------------------------------------------
    w = weather('258e1d9242c7f27fb8c93e5c3d82e3ca', lat, lon)
    l = w.weather_id()
    s = w.moisture()
    verdict = ""
    if l < 250 and l >= 200 and s < 0.25:
        verdict = "Chance of Natural Wildfire Breakout"
    else:
        verdict = "Low Chance of Natural Wildfire Breakout" 





    return render_template(
        'example.html',
        lat=float(lat),
        lon=float(lon),
        v=verdict,
        fires_lat=fires_lat,
        fires_lon=fires_lon,
        length=len(loc),
        c_raw_x=c_raw_x,
        c_raw_y=c_raw_y,
        s_raw_x=s_raw_x,
        s_raw_y=s_raw_y,
        t_raw_x=t_raw_x,
        t_raw_y=t_raw_y,
        c_raw_length=c_raw_length,
        s_raw_length=s_raw_length,
        t_raw_length=t_raw_length,
        time=time

    )

@app.route('/clickpost/', methods=['POST'])
def clickpost():
    # Now lat and lon can be accessed as:
    lat = request.form['lat']
    lng = request.form['lng']
    return "ok"



if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
