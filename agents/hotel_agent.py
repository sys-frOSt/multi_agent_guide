from __future__ import annotations

import json


from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from graph.state import TravelState

from tools.tavily_tools import search_hotels

def hotel_agent(state: TravelState):
    query = f"Best hotels for {state['user_query']}"
    hotel_data = search_hotels.invoke(query)
    return {
        "hotel_results": hotel_data,
        "messages": [
            AIMessage(content="Hotel results fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


