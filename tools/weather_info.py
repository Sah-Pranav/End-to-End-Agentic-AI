from langchain.tools import Tool
import requests
import os
from exception.customexception import handle_tool_exception

class WeatherInfoTool:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not self.api_key:
            raise ValueError("Missing OPENWEATHERMAP_API_KEY environment variable.")
        self.weather_tool_list = [
            Tool.from_function(
                name="get_weather_info",
                description="Get real-time weather information for a city in Germany.",
                func=self.get_weather_info,
            )
        ]

    def get_weather_info(self, city: str):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city},DE&appid={self.api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                desc = data["weather"][0]["description"].capitalize()
                temp = data["main"]["temp"]
                return f"Weather in {city}: {desc}, {temp}°C"
            else:
                return f"Could not fetch weather for {city}."
        except Exception as e:
            return handle_tool_exception("WeatherInfoTool", e)

if __name__ == "__main__":
    tool = WeatherInfoTool()
    print(tool.get_weather_info("Berlin"))
