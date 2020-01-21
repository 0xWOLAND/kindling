# coding: utf-8

from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
import functions 
from FireModel import FireModel
from weather import weather
app = Flask(__name__, template_folder="templates")

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyBZa-XgzpZuRt0jqaTBlqShQwusUNrA9WA"

# you can also pass key here
GoogleMaps(
    app,
    key="AIzaSyBZa-XgzpZuRt0jqaTBlqShQwusUNrA9WA"
)

# NOTE: this example is using a form to get the apikey

coordinates = functions.coord()
lat = float(coordinates['latitude'])
lon = float(coordinates['longitude'])


# ----------------------------------------------------------------
@app.route('/')
@app.route('/mobile')
def hello():
    return render_template('home.html')

@app.route('/a')
def address():
    return "Address" 

@app.route('/report')
def mid():
    return render_template('report.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/traveling')
def bot():
    return "Alert user of fires at a specific location"


@app.route('/desktop')
def desktop():
    return render_template("desktop.html")

@app.route("/nearyou")
def mapview():
 # ------------------------------------------------------------------------------------------------------------
    # Prepare Coords for Fire Spread
    coordinates = functions.coord()
    lat = float(coordinates['latitude'])
    lon = float(coordinates['longitude'])
    f = FireModel(lat, lon)
    loc = f.get_lat_lon()
    m = []
    for i in range(len(loc)):
        m.append({'lat': loc[i][0], 'lng': loc[i][1]})
    closest = []
    second = []
    third = []
    n1 =2783465827645
    n2=230945723095
    n3 = 235723659723
    for i in range(len(loc)):
        if functions.dist(lat, lon, loc[i][0], loc[i][1]) < n1 and functions.dist(lat, lon, loc[i][0], loc[i][1]) < n2 and functions.dist(lat, lon, loc[i][0], loc[i][1]) < n3:
            n1 = functions.dist(lat, lon, loc[i][0], loc[i][1])
            closest = [loc[i][0], loc[i][1]]
        elif functions.dist(lat, lon, loc[i][0], loc[i][1]) >= n1 and functions.dist(lat, lon, loc[i][0], loc[i][1]) < n2 and functions.dist(lat, lon, loc[i][0], loc[i][1]) < n3:
            n2 = functions.dist(lat, lon, loc[i][0], loc[i][1])
            second = [loc[i][0], loc[i][1]]
        elif functions.dist(lat, lon, loc[i][0], loc[i][1]) >= n1 and functions.dist(lat, lon, loc[i][0], loc[i][1]) >= n2 and functions.dist(lat, lon, loc[i][0], loc[i][1]) < n3:
            n3 = functions.dist(lat, lon, loc[i][0], loc[i][1])
            third = [loc[i][0], loc[i][1]]
    c_raw = functions.fire_ring(closest[0], closest[1])
    s_raw = functions.fire_ring(second[0], second[1])
    t_raw = functions.fire_ring(third[0], third[1])

# ------------------------------------------------------------------------------------------------------------------------------------------------
    w = weather('258e1d9242c7f27fb8c93e5c3d82e3ca', lat, lon)
    l = w.weather_id()
    s = w.moisture()
    verdict = ""
    if l < 250 and l >= 200 and s < 0.25:
        verdict = "Chance of Natural Wildfire Breakout"
    else:
        verdict = "Low Chance of Natural Wildfire Breakout" 

    infoboxmap = Map(
        identifier="infoboxmap",
        zoom=10,
        lat=lat,
        lng=lon,
        markers=m,
        polygons=[{
            'stroke_color': '#9E0031',
            'stroke_opacity': 1.0,
            'stroke_weight': 3,
            'path': c_raw,
            'infobox': 'This is a polygon'
        },{
        
            'stroke_color': '#8E0045',
            'stroke_opacity': 1.0,
            'stroke_weight': 3,
            'path': s_raw,
            'infobox': 'This is a polygon'
        },{
        
            'stroke_color': '#770058',
            'stroke_opacity': 1.0,
            'stroke_weight': 3,
            'path': t_raw,
            'infobox': 'This is a polygon'
        }],
        circles=[{
            'stroke_color': '#9E0031',
            'stroke_opacity': 1.0,
            'stroke_weight': 7,
            'fill_color': '#9E0031',
            'fill_opacity': 0.2,
            'center': {
                'lat': lat,
                'lng': lon
            },
            'radius': 200,
            'infobox': "This is a circle"
        }]
    )

    



    return render_template(
        'example.html',
        infoboxmap=infoboxmap,
        GOOGLEMAPS_KEY=request.args.get('apikey'), res=verdict
    )



@app.route('/clickpost/', methods=['POST'])
def clickpost():
    # Now lat and lon can be accessed as:
    lat = request.form['lat']
    lng = request.form['lng']
    return "ok"

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
