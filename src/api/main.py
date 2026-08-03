import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Any, cast
from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver
from graph.builder import builder
from langchain_core.messages import HumanMessage

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

class TravelRequest(BaseModel):
    user_query: str

@app.get("/")
async def index():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))

@app.post("/plan")
async def create_travel_plan(request: TravelRequest):
    db_url = os.getenv("DATABASE_URL")
    if db_url is None:
        raise HTTPException(status_code=500, detail="DATABASE_URL not configured")
    
    # Use PostgresSaver as checkpointer
    with PostgresSaver.from_conn_string(db_url) as checkpointer:
        checkpointer.setup()
        
        payload: Any = {
            "messages": [HumanMessage(content=request.user_query)],
            "user_query": request.user_query,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0,
        }
        
        app_graph = builder.compile(checkpointer=checkpointer)
        config = {"configurable": {"thread_id": "api_user"}}  # could be dynamic
        
        result = app_graph.invoke(payload, config=cast(Any, config))
        
        return {
            "response": result.get("final_response", ""),
            "messages": [getattr(m, "content", m) for m in result.get("messages", [])],
            "llm_calls": result.get("llm_calls", 0),
        }