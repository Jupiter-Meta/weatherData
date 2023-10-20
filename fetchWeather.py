
import requests
import pymongo

# OpenWeatherAPI configuration
api_key = 'a1ce3564a0ea8c3c2bb353c83bc683a0'
lat = 17.4345706  # Replace with the city you want to fetch weather data for
lon = 78.3738571
api_weather = "http://api.openweathermap.org/data/2.5/weather?lat="+str(lat)+"&lon="+str(lon)+"&appid=eb370f9ef90cb3375bb7c497f844f0c5"
api_aqi = "http://api.openweathermap.org/data/2.5/air_pollution?lat="+str(lat)+"&lon="+str(lon)+"&appid=eb370f9ef90cb3375bb7c497f844f0c5"

# MongoDB configuration
mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
db = mongo_client['jm']
collection = db['weather']

def fetch_weather_data():
    try:
        response = requests.get(api_weather)
        weatherData = response.json()
        print(weatherData)

        response2 = requests.get(api_aqi)
        aqiData = response.json()
        print(aqiData)
        
        
        if response.status_code == 200:
            return weatherData
        else:
            print(f"Error: {data['message']}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def save_to_mongodb(weather_data):
    if weather_data:
        collection.insert_one(weather_data)
        print("Weather data saved to MongoDB.")

if __name__ == "__main__":
    weather_data = fetch_weather_data()
    # if weather_data:
    #     save_to_mongodb(weather_data)
