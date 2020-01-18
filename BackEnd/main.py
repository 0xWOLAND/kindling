# !/usr/bin/python3
'''
import pandas as pd
from pyowm import OWM
from FireModel import FireModel
import folium
import functions
from weather import weather

api_keys = {'owm_api_key': '258e1d9242c7f27fb8c93e5c3d82e3ca',
'google_api_key': 'AIzaSyBRsTtJ_jPBgFLGVY9G6gRi5hv7CtKRSSA',
'open_api_key': 'WfKLQgReR7LXxlVXchCn0RrPQJT651TI'}
# Read in the data as data






coordinates = functions.coord()
lat = float(coordinates['latitude'])
lon = float(coordinates['longitude'])
# ------------------------------------------------------------------------------------------------------------------
owm = OWM(api_keys['owm_api_key'])
w = weather(api_keys['owm_api_key'], lat, lon)
d = pd.read_csv(
    'https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_7d.csv')
print("d: {}".format(len(d)))
ls = []
inter = []
for i in range(len(d)):
    inter.append(d['latitude'][i])
    inter.append(d['longitude'][i])
    ls.append(inter)
    inter = []
print(ls)
closest = 1234567876543456787643
closest_x = 0
closest_y = 0
for i in range(len(ls)):
    dist = functions.dist(x=lat,y=lon,x0=ls[i][0],y0=ls[i][1])
    if dist < closest:
        closest = dist
        closest_x = ls[i][0]
        closest_y = ls[i][1]

print("The closest fire is at ({},{}) with a distance of {} miles from the user".format(closest_x,closest_y,closest))
m = folium.Map(location=[lat,lon],zoom_start=15)
folium.Marker(location=[lat,lon],popup='Your Location', tooltip='Click for more information', icon=folium.Icon(icon='fire',color='red')).add_to(m)
m.save('map.html')
f = FireModel(lat,lon)
'''
t = text('"Dont forget to do your college applications" -- a wise plum')
for i in range(10):
    t.main()
