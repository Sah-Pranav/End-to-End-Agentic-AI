from langchain.tools import Tool
import requests
import os

class PlaceSearchTool:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.place_search_tool_list = [
            Tool.from_function(
                name="search_bakeries",
                description="Find bakeries in a specified city in Germany.",
                func=self.search_bakeries,
            )
        ]

    def search_bakeries(self, city):
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=bakeries+in+{city}&key={self.api_key}"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and data.get("results"):
            places = [f"{place['name']} ({place['formatted_address']})" for place in data["results"][:5]]
            return "\n".join(places)
        else:
            return "No bakery information found for this city."
