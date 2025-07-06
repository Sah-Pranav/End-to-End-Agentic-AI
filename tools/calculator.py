from langchain.tools import Tool

class CalculatorTool:
    def __init__(self):
        self.calculator_tool_list = [
            Tool.from_function(
                name="basic_calculator",
                description="Simple calculator for addition, subtraction, multiplication, and division.",
                func=self.basic_calculator,
            )
        ]

    def basic_calculator(self, expression: str):
        try:
            result = eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Error calculating expression: {e}"
