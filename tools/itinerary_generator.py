from langchain.tools import Tool

class ItineraryGeneratorTool:
    def __init__(self):
        self.itinerary_generator_tool_list = [
            Tool.from_function(
                name="generate_bakery_itinerary",
                description="Generate a simple itinerary for visiting 2-3 bakeries in a city.",
                func=self.generate_bakery_itinerary,
            )
        ]

    def generate_bakery_itinerary(self, city):
        itinerary = f"""Sample itinerary for {city}:
- 10:00 AM: Start with breakfast at a famous local bakery.
- 12:00 PM: Coffee break at a hidden gem.
- 2:00 PM: Explore a popular bakery known for special pastries.
- 4:00 PM: End with a takeaway treat.
"""
        return itinerary
