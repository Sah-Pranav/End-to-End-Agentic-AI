from langchain_core.tools import Tool
from pydantic import BaseModel, Field
from exception.customexception import handle_tool_exception

class TransportInfoInput(BaseModel):
    city: str = Field(description="The city name to get transport options for.")

class TransportInfoTool:
    def __init__(self):
        self.transport_info_tool_list = [
            Tool.from_function(
                name="get_transport_options",
                description="Provide available transport modes for a bakery visit in a city.",
                func=self.get_transport_options,
                args_schema=TransportInfoInput
            )
        ]
        self.transport_options = {
            "Berlin": "U-Bahn, S-Bahn, Bus, Tram, Taxi, Bike rentals.",
            "Munich": "U-Bahn, S-Bahn, Bus, Tram, Taxi, Bike sharing.",
            "Hamburg": "S-Bahn, U-Bahn, Ferry, Bus, Taxi.",
        }

    def get_transport_options(self, city: str):
        try:
            return self.transport_options.get(city, "Public transport, taxi, bike rentals available.")
        except Exception as e:
            return handle_tool_exception("TransportInfoTool", e)

if __name__ == "__main__":
    tool = TransportInfoTool()
    print(tool.get_transport_options("Berlin"))
