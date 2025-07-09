from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
from dotenv import load_dotenv
from logger.logging import logger
from exception.customexception import handle_fastapi_exception
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        logger.info(f"Received query: {query.question}")

        graph_builder = GraphBuilder(model_provider="groq")
        agentic_graph = graph_builder()

        # Create initial state with user message
        state = {"messages": [{"role": "user", "content": query.question}]}

        # Invoke the graph and get final state
        final_state = agentic_graph.invoke(state)

        # Extract the last message object
        last_message = final_state["messages"][-1]

        # Correct way to get content from AIMessage object
        final_output = last_message.content if hasattr(last_message, "content") else str(last_message)

        return {"answer": final_output}

    except Exception as e:
        return handle_fastapi_exception("Query Endpoint", e)
