from langchain.tools import Tool
import requests
import os

class WeatherInfoTool:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        self.weather_tool_list = [
            Tool.from_function(
                name="get_weather_info",
                description="Get real-time weather information for a given city in Germany.",
                func=self.get_weather_info,
            )
        ]

    def get_weather_info(self, city):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},DE&appid={self.api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return f"Current weather in {city}: {data['weather'][0]['description']}, {data['main']['temp']}°C"
        else:
            return "Weather information not available for that location."
