from langchain_core.tools import Tool
from pydantic import BaseModel, Field
from typing import Type
import requests
import os
from exception.customexception import handle_tool_exception

class OpeningHoursInput(BaseModel):
    place_id: str = Field(description="The place_id of the location to check opening hours for.")

class OpeningHoursCheckerTool:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Missing GOOGLE_API_KEY environment variable.")
        self.opening_hours_tool_list = [
            Tool.from_function(
                name="check_opening_hours",
                description="Check the opening hours of a bakery given its place_id.",
                func=self.check_opening_hours,
                args_schema=OpeningHoursInput
            )
        ]

    def check_opening_hours(self, place_id: str):
        try:
            url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,opening_hours,business_status&key={self.api_key}"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and "result" in data:
                result = data["result"]
                hours = result.get("opening_hours", {}).get("weekday_text", [])
                business_status = result.get("business_status", "Unknown")
                if hours:
                    return f"Opening hours for {result['name']}:\n" + "\n".join(hours) + f"\nStatus: {business_status}"
                else:
                    return f"Opening hours not available. Status: {business_status}"
            else:
                return "Failed to retrieve opening hours."
        except Exception as e:
            return handle_tool_exception("OpeningHoursCheckerTool", e)

if __name__ == "__main__":
    tool = OpeningHoursCheckerTool()
    print(tool.check_opening_hours("ChIJD7fiBh9u5kcRYJSMaMOCCwQ"))  # Example place_id
