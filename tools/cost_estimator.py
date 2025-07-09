from langchain.tools import Tool
from exception.customexception import handle_tool_exception

class CostEstimatorTool:
    def __init__(self):
        self.cost_estimator_tool_list = [
            Tool.from_function(
                name="estimate_expenses",
                description="Estimate total expense for visiting bakeries including transport, food and extras.",
                func=self.estimate_expenses,
            )
        ]

    def estimate_expenses(self, expenses: str):
        try:
            amounts = [float(x.strip()) for x in expenses.split(",")]
            total = sum(amounts)
            return f"Estimated total expense: {total} EUR"
        except Exception as e:
            return handle_tool_exception("CostEstimatorTool", e)

if __name__ == "__main__":
    tool = CostEstimatorTool()
    print(tool.estimate_expenses("10, 20, 5.5"))
