from langchain.tools import Tool

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
        """Takes comma-separated expenses like '10,20,5' and returns the total."""
        try:
            amounts = [float(x.strip()) for x in expenses.split(",")]
            return f"Estimated total expense: {sum(amounts)} EUR"
        except Exception as e:
            return f"Failed to calculate expenses: {e}"
