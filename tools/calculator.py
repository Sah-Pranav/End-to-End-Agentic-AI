from langchain_core.tools import Tool
from exception.customexception import handle_tool_exception
import ast

class CalculatorTool:
    def __init__(self):
        self.calculator_tool_list = [
            Tool.from_function(
                name="basic_calculator",
                description="Simple calculator for addition, subtraction, multiplication, and division.",
                func=self.basic_calculator,
            )
        ]

    def safe_eval(self, expression: str):
        try:
            # Parse expression safely
            node = ast.parse(expression, mode='eval')
            for n in ast.walk(node):
                if not isinstance(n, (ast.Expression, ast.BinOp, ast.UnaryOp,
                                      ast.Num, ast.Load, ast.operator, ast.unaryop)):
                    raise ValueError("Unsafe expression")
            return eval(compile(node, '<string>', 'eval'))
        except Exception:
            raise ValueError("Invalid or unsafe expression.")

    def basic_calculator(self, expression: str):
        try:
            result = self.safe_eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return handle_tool_exception("CalculatorTool", e)

if __name__ == "__main__":
    tool = CalculatorTool()
    print(tool.basic_calculator("2 + 3 * 4"))
