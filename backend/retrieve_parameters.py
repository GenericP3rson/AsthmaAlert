import requests
import json


# Pollen Levels
def pollen_level(lat, lon):
    api_key = "5d1aa97559fb4d84a578476bf89a6a20"
    # Number from 1 to 3 that indicates how many days forecast to request
    days = 1
    link = "https://api.breezometer.com/pollen/v2/forecast/daily?lat={}&lon={}&key={}&days={}&features=plants_information".format(lat, lon, api_key, days)
    data = requests.get(link)
    data = data.json()
    
    pollen_data = {}

    if data['data'] != None:
        for plant in data['data'][0]["plants"]:
            if data['data'][0]["plants"][plant]["data_available"]:
                pollen_data[data['data'][0]["plants"][plant]["display_name"]] = data['data'][0]["plants"][plant]["index"]["value"]
    else:
        return None
    return pollen_data

# print(pollen_level(42.342068, -71.202459))


def humidity_level(lat, lon):
    api_key = "3bb8aadaa3f8d3fd4a54f576f1945112"
    link = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(lat, lon, api_key)
    data = requests.get(link)
    data = data.json()
    humidity = data['main']['humidity']
    return humidity

# print(humidity_level(42.342068, -71.202459))

def elevation_level(lat, lon):
    api_key = "AIzaSyAAq8Uo2UFgfz4E5zBhg96MR9r3U7bB4HQ"
    link = "https://maps.googleapis.com/maps/api/elevation/json?locations={},{}&key={}".format(lat, lon, api_key)
    data = requests.get(link)
    data = data.json()
    elevation = data["results"][0]["elevation"]
    return elevation

# print(altitude(42.342068, -71.202459))

def airquality(lat, lon):
    API = "dffe7bb6-e8c3-44ea-a973-c1d2abd163f5"
    test = "http://api.airvisual.com/v2/nearest_city?lat={}&lon={}&key={}".format(
        lat, lon, API)
    # print(lat, lon, f.read())
    x = requests.get(test)
    return json.loads(x.text)["data"]["current"]["pollution"]["aqius"]

def temperature(lat, lon):
    api_key = "3bb8aadaa3f8d3fd4a54f576f1945112"
    test = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(lat, lon, api_key)
    data = requests.get(test)
    data = data.json()
    return data["main"]["temp"]

