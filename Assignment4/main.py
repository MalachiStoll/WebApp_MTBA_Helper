from flask import Flask, render_template, request, redirect, url_for
from assignment4 import find_stop_near, get_nearest_station
import math

app = Flask(__name__)

app.config['DEBUG'] = True

#post getting user input
#get it will render the html 

@app.route('/', methods=['GET', 'POST'])
def mbta_station():
    
    if request.method == 'POST':
        place_name = request.form['place_name']
        mbta_station_name, distance, stop_lat, stop_lon = find_stop_near(place_name)
        return render_template('MBTA_output.html', place_name=place_name, 
            mbta_station_name=mbta_station_name, distance=distance,
            stop_lat = stop_lat, stop_lon = stop_lon)
    return render_template('MBTA_input.html')



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
