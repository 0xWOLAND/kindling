
import pandas as pd
from BackEnd.functions import functions
import gmaps
import folium
class FireModel:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def init_map(self):
        m = folium.Map(location=[self.lat, self.lon], zoom_start=10)
        coords = self.get_lat_lon()
        closest_fire = self.closest_fire_coord()
        folium.Marker(location=[closest_fire[0],closest_fire[1]], popup='The closest fire to your location', tooltip='Click for more information',
                      icon=folium.Icon(icon='fire', color='red')).add_to(m)
        for i in range(len(coords)):
            x = coords[i][0]
            y = coords[i][1]
            if x != closest_fire[0] and y != closest_fire[1]:
                folium.Marker(location=[x,y], popup='Fire at ({}, {})'.format(x,y),
                          tooltip='Click for more information',
                          icon=folium.Icon(icon='fire', color='lightred')).add_to(m)
        folium.Marker(location=[self.lat, self.lon], popup='Your Location',
                      tooltip='Click for more information', icon=folium.Icon(icon='human', )).add_to(m)
        return m

    def make_map(self):
        m = folium.Map(location=[self.lat, self.lon], zoom_start=10)
        self.save_map(m)
        return m

    def save_map(self, m):
        m.save('templates/map.html')

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
            dist = functions.dist(x=self.lat, y=self.lon, x0=ls[i][0], y0=ls[i][1])
            if dist < closest:
                closest = dist
                closest_x = ls[i][0]
                closest_y = ls[i][1]
        nums = [closest_x, closest_y]
        return nums

    def closest_fire(self, m):
        closest_fire = self.closest_fire_coord()
        folium.Marker(location=[closest_fire[0],closest_fire[1]], popup='The closest fire to your location', tooltip='Click for more information',
                      icon=folium.Icon(icon='fire', color='red')).add_to(m)
        self.save_map(m)

    def all_fires(self, m):
        coords = self.get_lat_lon()
        closest_fire_coord = self.closest_fire_coord()
        for i in range(len(coords)):
            x = coords[i][0]
            y = coords[i][1]
            if x != closest_fire_coord[0] and y != closest_fire_coord[1]:
                folium.Marker(location=[x,y], popup='Fire at ({}, {})'.format(x,y),
                          tooltip='Click for more information',
                          icon=folium.Icon(icon='fire', color='lightred')).add_to(m)
        self.save_map(m)

    def add_user(self,m):
        folium.Marker(location=[self.lat,self.lon], popup='Your Location',
                      tooltip='Click for more information', icon=folium.Icon(icon='human',)).add_to(m)
        self.save_map(m)
    def main(self):
        m = self.make_map()
        self.closest_fire(m)
        self.all_fires(m)
        self.add_user(m)

class MapWrapper:
    def __init__(self, m):
        self.html = m.get_root().render()
