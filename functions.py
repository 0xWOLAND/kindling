# !/usr/bin/python3

import math
import requests
from FireModel import FireModel
from weather import weather


def slope(vertical, horizontal):
    return (vertical / horizontal) * 100

def dist(x, y, x0, y0):
    return math.sqrt(abs((math.pow(x - x0, 2) + (math.pow(y - y0, 2)))))

def circledist(coord1: object, coord2: object):
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

def ip():
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']
    geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
    geo_request = requests.get(geo_request_url)
    geo_data = geo_request.json()

def coord():
    """  Function To Print GeoIP Latitude & Longitude """
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']
    geo_request = requests.get('https://get.geojs.io/v1/ip/geo/' + my_ip + '.json')
    geo_data = geo_request.json()
    return {'latitude': geo_data['latitude'], 'longitude': geo_data['longitude']}

def triangle_points(r, t, h, k):
    x = float(r * math.cos(t) + h)
    y = float(r * math.sin(t) + k)
    coord = [y, x]
    return coord

def ellipse(r, h, t,  k, wind_vector, wind_dir):

    x = float(r * math.cos(t)) * wind_vector
    y = float(r * math.sin(t)) * (wind_vector * 0.5)
    deg = deg_to_rad(wind_dir)
    x1 = (x * math.cos(deg) - y * math.sin(deg)) + h
    y1 = (y * math.cos(deg) + x * math.sin(deg)) + k
    coord = [x1,y1]
    return coord


def deg_to_rad(deg):
    x = (deg * math.pi) / 180
    return x


def fire_ring(x, y):
    coordinates = coord()
    lat = float(coordinates['latitude'])
    lon = float(coordinates['longitude'])
    w = weather('258e1d9242c7f27fb8c93e5c3d82e3ca', lat, lon)
    f = FireModel(lat, lon)
    loc = f.get_lat_lon()
    d = w.wind()['deg']
    s = w.wind()['speed']
    poly = []
    for j in range(360):
        poly.append(ellipse(0.01,x, j, y,s, d))
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
    for i in range(len(poly)):
        if right:
            poly[i][0] -= dx
        else:
            poly[i][0] += dx
        if top:
            poly[i][1] += dy
        else:
            poly[i][1] -= dy
    return poly


'''
    
    def ellipse(r, h, t_val,  k, wind_vector, wind_dir):
        t = functions.deg_to_rad(t_val)
        x = float(math.cos(t) + h) * wind_vector
        y = float(math.sin(t) + k) * (0.5 * wind_vector)
        deg = functions.deg_to_rad(wind_dir)
        x1 = x * math.cos(deg) - y * math.sin(deg)
        y1 = y * math.cos(deg) + x * math.sin(deg)
        coord = [x1,y1]
        return coord

'''