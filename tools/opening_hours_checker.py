from langchain.tools import Tool
import requests
import os

class OpeningHoursCheckerTool:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")  # make sure env var name matches your .env
        self.opening_hours_tool_list = [
            Tool.from_function(
                name="check_opening_hours",
                description="Check the opening hours of a bakery given its place_id.",
                func=self.check_opening_hours,
            )
        ]

    def check_opening_hours(self, place_id):
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,opening_hours&key={self.api_key}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and "result" in data:
            if "opening_hours" in data["result"]:
                hours = data["result"]["opening_hours"].get("weekday_text", [])
                return f"Opening hours for {data['result']['name']}:\n" + "\n".join(hours)
            else:
                return "Opening hours not available for this bakery."
        else:
            error_message = data.get("error_message", "Unknown error")
            return f"Failed to retrieve opening hours. Error: {error_message}"
