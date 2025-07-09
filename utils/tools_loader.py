from tools.calculator import CalculatorTool
from tools.cost_estimator import CostEstimatorTool
from tools.itinerary_generator import ItineraryGeneratorTool
from tools.opening_hours_checker import OpeningHoursCheckerTool
from tools.place_search_tool import PlaceSearchTool
from tools.transport_info import TransportInfoTool
from tools.weather_info import WeatherInfoTool

def get_all_tools():
    tools = []
    tools.extend(CalculatorTool().calculator_tool_list)
    tools.extend(CostEstimatorTool().cost_estimator_tool_list)
    tools.extend(ItineraryGeneratorTool().itinerary_generator_tool_list)
    tools.extend(OpeningHoursCheckerTool().opening_hours_tool_list)
    tools.extend(PlaceSearchTool().place_search_tool_list)
    tools.extend(TransportInfoTool().transport_info_tool_list)
    tools.extend(WeatherInfoTool().weather_tool_list)
    return tools

if __name__ == "__main__":
   pass