#!/bin/python3
import requests
import pymongo,time

# OpenWeatherAPI configuration
api_key = 'a1ce3564a0ea8c3c2bb353c83bc683a0'
lat = 17.4345706  # Replace with the city you want to fetch weather data for
lon = 78.3738571
api_weather = "http://api.openweathermap.org/data/2.5/weather?lat="+str(lat)+"&lon="+str(lon)+"&appid=eb370f9ef90cb3375bb7c497f844f0c5&units=metric"
api_aqi = "http://api.openweathermap.org/data/2.5/air_pollution?lat="+str(lat)+"&lon="+str(lon)+"&appid=eb370f9ef90cb3375bb7c497f844f0c5&units=metric "

# MongoDB configuration
mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
db = mongo_client['jm']
collection = db['weather']

def fetch_weather_data():
    try:
        # print("Weather")
        response = requests.get(api_weather)
        weatherData = response.json()
        print(weatherData)
        print( )
        # print("AQI")
        response2 = requests.get(api_aqi)
        aqiData = response2.json()
        print(aqiData)

        data = {'fetchTime':round(time.time()), 'lastUpdate':weatherData['dt'], 'lat':weatherData['coord']['lat'], 'lon':weatherData['coord']['lon'],'location':weatherData['name'], 'temp':weatherData['main']['temp'],'humidity':weatherData['main']['humidity'], 'aqi':aqiData['list'][0]['main']['aqi'], 'co':aqiData['list'][0]['components']['co'], 'no':aqiData['list'][0]['components']['no'], 'no2':aqiData['list'][0]['components']['no2'], 'o3':aqiData['list'][0]['components']['o3'], 'so2':aqiData['list'][0]['components']['so2'], 'pm2_5':aqiData['list'][0]['components']['pm2_5'], 'pm10':aqiData['list'][0]['components']['pm10'], 'nh3':aqiData['list'][0]['components']['nh3'] }
        print(data)
        
        if response.status_code == 200:
            return data
        else:
            print(f"Error: {data['message']}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def save_to_mongodb(data):
    if data:
        collection.insert_one(data)
        print("Weather data saved to MongoDB.")

if __name__ == "__main__":
    data = fetch_weather_data()
    if data:
        save_to_mongodb(data)
