from flask import Flask, render_template, url_for
from pyowm import OWM
from BackEnd.FireModel import FireModel
from BackEnd.functions import functions

app = Flask(__name__)

api_keys = {'owm_api_key': '258e1d9242c7f27fb8c93e5c3d82e3ca',
            'google_api_key': 'AIzaSyBRsTtJ_jPBgFLGVY9G6gRi5hv7CtKRSSA',
            'open_api_key': 'WfKLQgReR7LXxlVXchCn0RrPQJT651TI'}
coordinates = functions.coord()
lat = float(coordinates['latitude'])
lon = float(coordinates['longitude'])


# ----------------------------------------------------------------
@app.route('/')
@app.route('/mobile')
def hello():
    return render_template('home.html')


@app.route('/nearyou')
def top():
    return render_template('nearyou.html')

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


if __name__ == "__main__":
    app.run(debug=True)
