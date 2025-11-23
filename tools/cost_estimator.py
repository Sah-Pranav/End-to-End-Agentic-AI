from langchain_core.tools import Tool
from pydantic import BaseModel, Field
from exception.customexception import handle_tool_exception

class CostEstimatorInput(BaseModel):
    expenses: str = Field(description="A comma-separated list of numbers (e.g., '10, 20, 5.5') representing individual costs.")

class CostEstimatorTool:
    def __init__(self):
        self.cost_estimator_tool_list = [
            Tool.from_function(
                name="estimate_expenses",
                description="Estimate total expense. Input MUST be a comma-separated list of numbers (e.g., '10, 20, 5.5'). Do NOT input city names or text.",
                func=self.estimate_expenses,
                args_schema=CostEstimatorInput
            )
        ]

    def estimate_expenses(self, expenses: str):
        try:
            # Check if input contains letters (simple heuristic to detect city names)
            if any(c.isalpha() for c in expenses.replace(",", "").replace(".", "").strip()):
                return "Error: Input must be a list of numbers (e.g., '10, 15.5'). Please calculate the individual costs first using other tools, then pass the numbers here."

            amounts = [float(x.strip()) for x in expenses.split(",")]
            total = sum(amounts)
            return f"Estimated total expense: {total} EUR"
        except ValueError:
             return "Error: Invalid input format. Please provide a comma-separated list of numbers."
        except Exception as e:
            return handle_tool_exception("CostEstimatorTool", e)

if __name__ == "__main__":
    tool = CostEstimatorTool()
    print(tool.estimate_expenses("10, 20, 5.5"))
