from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
from dotenv import load_dotenv
from logger.logging import logger
from exception.customexception import handle_fastapi_exception
import os
import json
import asyncio
from typing import Optional

load_dotenv()

app = FastAPI()

# Singleton Graph Initialization
try:
    graph_builder = GraphBuilder(model_provider="groq")
    agentic_graph = graph_builder()
    logger.info("Graph initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize graph: {e}")
    raise e

# CORS Configuration
origins = [
    "http://localhost:8501",  # Streamlit default port
    "http://127.0.0.1:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    thread_id: Optional[str] = "default_thread"

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        logger.info(f"Received query: {query.question} (Thread: {query.thread_id})")
        
        config = {"configurable": {"thread_id": query.thread_id}}
        state = {"messages": [{"role": "user", "content": query.question}]}
        
        # Invoke the graph
        final_state = await agentic_graph.ainvoke(state, config=config)
        
        last_message = final_state["messages"][-1]
        final_output = last_message.content if hasattr(last_message, "content") else str(last_message)
        
        return {"answer": final_output}

    except Exception as e:
        return handle_fastapi_exception("Query Endpoint", e)

@app.post("/chat/stream")
async def chat_stream(query: QueryRequest):
    try:
        logger.info(f"Received streaming query: {query.question} (Thread: {query.thread_id})")
        
        config = {"configurable": {"thread_id": query.thread_id}}
        state = {"messages": [{"role": "user", "content": query.question}]}

        async def event_generator():
            try:
                # Stream events from the graph
                async for event in agentic_graph.astream(state, config=config, stream_mode="updates"):
                    # Convert event to a serializable format
                    # 'event' is a dict like {'agent': {'messages': [AIMessage(...)]}}
                    # We need to serialize the messages
                    serializable_event = {}
                    for node, content in event.items():
                        serializable_event[node] = {}
                        if "messages" in content:
                            serializable_event[node]["messages"] = [
                                m.dict() if hasattr(m, "dict") else str(m) for m in content["messages"]
                            ]
                        else:
                            serializable_event[node] = str(content)

                    yield f"data: {json.dumps(serializable_event)}\n\n"
                    
                # Yield a final done message
                yield "data: [DONE]\n\n"
            except Exception as e:
                logger.error(f"Streaming error: {e}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except Exception as e:
        return handle_fastapi_exception("Streaming Endpoint", e)

