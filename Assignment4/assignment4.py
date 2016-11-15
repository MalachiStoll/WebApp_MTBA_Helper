import urllib.request   # urlencode function
import json
from pprint import pprint


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


# A little bit of scaffolding if you want to use it

def get_json(google_url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib.request.urlopen(google_url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    """
    This part of the function is accounting for the spaces for the user input. 
    The URL format for the API uses a '%20' for a space. 
    """
    if ' ' in place_name:
        while ' ' in place_name:
            x = []
            for i in place_name:
                x.append(i)
            while ' ' in x:
                x[x.index(' ')] = '%20'
            place_name = ''.join(x) 
    """
    This loads the Google API and uses the user input to search for the longitude and latitude. 
    This also inputs Massachusetts at the end of the search as we are looking for an MBTA stop, which only applies to MA. 
    """
    google_url = "https://maps.googleapis.com/maps/api/geocode/json?address="+place_name+"&key=AIzaSyC7za9dnqPz90wB-v5O-5UTE-ApNhUrryc"
    response_data = get_json(google_url)    
    latitude = str(response_data["results"][0]["geometry"]['location']['lat'])
    longitude = str(response_data["results"][0]["geometry"]['location']['lng'])    
    return latitude, longitude

def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.
    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """
    mbta_url = "http://realtime.mbta.com/developer/api/v2/stopsbylocation?api_key=wX9NwuHnZU2ToO7GmGR9uw&lat="+latitude+"&lon="+longitude+"&format=json"
    g = urllib.request.urlopen(mbta_url)
    response_text_mbta = g.read().decode('utf-8')
    response_data_mbta = json.loads(response_text_mbta)
    """
    This statement checks to see if there is a result from the MBTA API. 
    If there is not, it will ask the user if they want to run the function again. 
    If they do, the function will run again. 
    If there is, this will continually run to find a complete result with a complete parent station name and distance.  
    """
    if response_data_mbta['stop'] != []:
        z = 0
        mbta_station_name = response_data_mbta['stop'][z]['parent_station_name']
        distance = response_data_mbta['stop'][z]['distance']
        stop_lat = response_data_mbta['stop'][z]['stop_lat']
        stop_lon = response_data_mbta['stop'][z]['stop_lon']
        while mbta_station_name == '':
            z += 1
            mbta_station_name = response_data_mbta['stop'][z]['parent_station_name']
            distance = response_data_mbta['stop'][z]['distance']
        return mbta_station_name, distance, stop_lat, stop_lon        

def find_stop_near(place_name):
    """
    Given a place name or address, return the nearest MBTA stop and the 
    distance from the given place to that stop.
    """
    latitude, longitude = get_lat_long(place_name) 
    mbta_station_name, distance, stop_lat, stop_lon = get_nearest_station(latitude, longitude)
    return mbta_station_name, distance, stop_lat, stop_lon,
def main():
    place_name = input('Please enter a location:')   


if __name__ == '__main__':
    main()
