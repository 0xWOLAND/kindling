# !/usr/bin/python3

import math
import requests


class functions:
    @staticmethod
    def slope(vertical, horizontal):
        return (vertical / horizontal) * 100
    @staticmethod
    def dist(x, y, x0, y0):
        return math.sqrt(abs((math.pow(x - x0, 2) + (math.pow(y - y0, 2)))))
    @staticmethod
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
    @staticmethod
    def ip():
        ip_request = requests.get('https://get.geojs.io/v1/ip.json')
        my_ip = ip_request.json()['ip']
        geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
        geo_request = requests.get(geo_request_url)
        geo_data = geo_request.json()
    @staticmethod
    def coord():
        """  Function To Print GeoIP Latitude & Longitude """
        ip_request = requests.get('https://get.geojs.io/v1/ip.json')
        my_ip = ip_request.json()['ip']
        geo_request = requests.get('https://get.geojs.io/v1/ip/geo/' + my_ip + '.json')
        geo_data = geo_request.json()
        return {'latitude': geo_data['latitude'], 'longitude': geo_data['longitude']}
    @staticmethod
    def triangle_points(r, t, h, k):
        x = float(r * math.cos(t) + h)
        y = float(r * math.sin(t) + k)
        coord = [y, x]
        return coord
    @staticmethod
    def ellipse(r, t, h, k, wind_vector, wind_direction):
        x = float(r * math.cos(t) + h) / wind_vector
        y = float(r * math.sin(t) + k) * wind_vector
        wind_direction = functions.deg_to_rad(wind_direction)
        x1 = x * math.cos(wind_direction) + y * math.sin(wind_direction)
        y1 = y * math.cos
        coord = [x1,y1]
        return coord
    @staticmethod
    def deg_to_rad(deg):
        x = (deg * math.pi) / 180
        return x
