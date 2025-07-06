from langchain.tools import Tool

class TransportInfoTool:
    def __init__(self):
        self.transport_info_tool_list = [
            Tool.from_function(
                name="get_transport_options",
                description="Provide available transport modes for a bakery visit in a given city.",
                func=self.get_transport_options,
            )
        ]

    def get_transport_options(self, city):
        options = {
            "Berlin": "U-Bahn, S-Bahn, Bus, Tram, Taxi, Bike rentals.",
            "Munich": "U-Bahn, S-Bahn, Bus, Tram, Taxi, Bike sharing.",
            "Hamburg": "S-Bahn, U-Bahn, Ferry, Bus, Taxi.",
        }
        return options.get(city, "Public transport, taxi, bike rentals available.")
