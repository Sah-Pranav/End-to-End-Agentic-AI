from langchain_core.tools import Tool
from pydantic import BaseModel, Field
from exception.customexception import handle_tool_exception

class ItineraryGeneratorInput(BaseModel):
    city: str = Field(description="The city name to generate an itinerary for.")

class ItineraryGeneratorTool:
    def __init__(self):
        self.itinerary_generator_tool_list = [
            Tool.from_function(
                name="generate_bakery_itinerary",
                description="Generate a simple itinerary for visiting 2-3 bakeries in a city.",
                func=self.generate_bakery_itinerary,
                args_schema=ItineraryGeneratorInput
            )
        ]

    def generate_bakery_itinerary(self, city: str):
        try:
            itinerary = f"""Sample itinerary for {city}:
- 10:00 AM: Start with breakfast at a famous local bakery.
- 12:00 PM: Coffee break at a hidden gem.
- 2:00 PM: Visit a popular bakery known for its signature pastries.
- 4:00 PM: End with a takeaway treat.
"""
            return itinerary
        except Exception as e:
            return handle_tool_exception("ItineraryGeneratorTool", e)

if __name__ == "__main__":
    tool = ItineraryGeneratorTool()
    print(tool.generate_bakery_itinerary("Berlin"))
