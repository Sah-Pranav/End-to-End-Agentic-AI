from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from starlette.responses import JSONResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

app = FastAPI()

# CORS setup (restrict origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["http://localhost:3000"] or your frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        print(f"Received query: {query.question}")

        # Build Graph
        graph_builder = GraphBuilder(model_provider="groq")
        agentic_graph = graph_builder()

        # Save Graph Mermaid Diagram (optional, good for debugging)
        mermaid_png = agentic_graph.get_graph().draw_mermaid_png()
        graph_path = os.path.join(os.getcwd(), "my_graph.png")
        with open(graph_path, "wb") as f:
            f.write(mermaid_png)
        print(f"Graph diagram saved at: {graph_path}")

        # Prepare message state
        state = {"messages": [{"role": "user", "content": query.question}]}

        # Invoke the graph
        final_state = agentic_graph.invoke(state)

        # Extract final message content
        final_output = final_state["messages"][-1].content

        return {"answer": final_output}

    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})

