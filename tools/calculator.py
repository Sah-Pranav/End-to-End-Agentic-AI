from langchain_core.tools import Tool
from pydantic import BaseModel, Field
import ast
import operator
from exception.customexception import handle_tool_exception

class CalculatorInput(BaseModel):
    expression: str = Field(description="The mathematical expression to evaluate (e.g., '2 + 2', '100 * 0.15').")

class CalculatorTool:
    def __init__(self):
        self.calculator_tool_list = [
            Tool.from_function(
                name="calculate",
                description="Perform basic mathematical calculations.",
                func=self.calculate,
                args_schema=CalculatorInput
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

    def calculate(self, expression: str):
        try:
            result = self.safe_eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return handle_tool_exception("CalculatorTool", e)

if __name__ == "__main__":
    tool = CalculatorTool()
    print(tool.calculate("2 + 3 * 4"))
