from langchain.tools import Tool
import requests
import os
from exception.customexception import handle_tool_exception

class PlaceSearchTool:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Missing GOOGLE_API_KEY environment variable.")
        self.place_search_tool_list = [
            Tool.from_function(
                name="search_bakeries",
                description="Search for bakeries in any city in Germany, returning name, address and place_id.",
                func=self.search_bakeries,
            )
        ]

    def search_bakeries(self, city: str):
        try:
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=bakeries+in+{city}&key={self.api_key}"
            response = requests.get(url)
            if response.status_code != 200:
                return f"API request failed with status code {response.status_code}"

            data = response.json()
            if not data.get("results"):
                return f"No bakery information found for {city}."

            places = [
                f"{place['name']} ({place['formatted_address']}) | place_id: {place['place_id']}"
                for place in data["results"][:5]
            ]
            return "\n".join(places)
        except Exception as e:
            return handle_tool_exception("PlaceSearchTool", e)

if __name__ == "__main__":
    tool = PlaceSearchTool()
    print(tool.search_bakeries("Berlin"))
