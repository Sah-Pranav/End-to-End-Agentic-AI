import pytest
from tools.place_search_tool import PlaceSearchTool
from tools.calculator import CalculatorTool
import os

# Mock environment variable for testing if not present
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "dummy_key"

def test_calculator_tool():
    tool = CalculatorTool()
    # Access the function directly from the tool list
    calc_func = tool.calculator_tool_list[0].func
    
    assert "Result: 5" in calc_func("2 + 3")
    assert "Result: 6" in calc_func("2 * 3")
    assert "Invalid" in calc_func("import os")  # Security check

def test_place_search_tool_init():
    # Test initialization
    tool = PlaceSearchTool()
    assert len(tool.place_search_tool_list) == 1
    assert tool.place_search_tool_list[0].name == "search_places"
