import requests

class Weather:
    def __init__(self, token):
        self.token = token

    def get_weather(self, lat, lon, city):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&q={city}&appid={self.token}&units=metric&lang=pt_br"
        response = requests.get(url)
        data = response.json()
        weather = {
            "current": data["main"]["temp"],
            "min": data["main"]["temp_min"],
            "max": data["main"]["temp_max"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "city": data["name"],
            "country": data["sys"]["country"]
        }
        return weather

    def get_location(self, city):
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={self.token}"
        response = requests.get(url)
        data = response.json()
        lat = str(data[0]["lat"])
        lon = str(data[0]["lon"])
        return lat, lon
