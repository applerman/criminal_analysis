# import googlemaps
from geopy.geocoders import GoogleV3
import json

# source: https://developers.google.com/maps/web-services/client-library
# def addressToGPS_googleAPI(address):
#     # Replace the API key below with a valid API key.
#     gmaps = googlemaps.Client(key='AIzaSyANmi4ehVT6n9f2cFuAHjM8e20YO2GJKx8')
#     
#     # Geocoding and address, which already checks the status for me
#     geocode_result = gmaps.geocode(address)
#     
#     if len(geocode_result):
#         return (geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng'])
#     
#     return None

def addressToGPS(address):
    geolocator = GoogleV3()
    location = geolocator.geocode(address)
    #return location
    return (location.latitude, location.longitude)

def test_addressToGPS():
    print addressToGPS('1600 Amphitheatre Parkway, Mountain View, CA')

if __name__ == "__main__":
    test_addressToGPS()

