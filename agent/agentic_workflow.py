from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.calculator import CalculatorTool
from tools.cost_estimator import CostEstimatorTool
from tools.itinerary_generator import ItineraryGeneratorTool
from tools.opening_hours_checker import OpeningHoursCheckerTool
from tools.transport_info import TransportInfoTool
from exception.customexception import handle_general_exception
from logger.logging import logger

class GraphBuilder:
    def __init__(self, model_provider="groq"):
        try:
            self.model_loader = ModelLoader(model_provider=model_provider)
            self.llm = self.model_loader.load_llm()

            self.weather_tools = WeatherInfoTool()
            self.place_search_tools = PlaceSearchTool()
            self.calculator_tools = CalculatorTool()
            self.cost_estimator_tools = CostEstimatorTool()
            self.itinerary_generator_tools = ItineraryGeneratorTool()
            self.opening_hours_checker_tools = OpeningHoursCheckerTool()
            self.transport_tools = TransportInfoTool()

            self.tools = [
                *self.weather_tools.weather_tool_list,
                *self.place_search_tools.place_search_tool_list,
                *self.calculator_tools.calculator_tool_list,
                *self.cost_estimator_tools.cost_estimator_tool_list,
                *self.itinerary_generator_tools.itinerary_generator_tool_list,
                *self.opening_hours_checker_tools.opening_hours_tool_list,
                *self.transport_tools.transport_info_tool_list,
            ]

            self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
            self.graph = None
            self.system_prompt = SYSTEM_PROMPT
        except Exception as e:
            logger.error("Failed to initialize GraphBuilder.")
            raise e

    def agent_function(self, state: MessagesState):
        try:
            user_messages = state["messages"]
            input_messages = [self.system_prompt] + user_messages
            response = self.llm_with_tools.invoke(input_messages)
            # response is AIMessage object; add to messages list
            return {"messages": user_messages + [response]}
        except Exception as e:
            return {"messages": state["messages"] + [{"role": "assistant", "content": handle_general_exception("Agent Function", e)}]}

    def build_graph(self):
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END)
        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        return self.build_graph()
