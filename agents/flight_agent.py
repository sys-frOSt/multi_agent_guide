from __future__ import annotations

import json


from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from graph.state import TravelState

from tools.flight_tool import search_flights


def flight_agent(state: TravelState):
    query = state["user_query"]
    flight_data = search_flights.invoke(query)
    return {
        "flight_results": flight_data,
        "messages": [
            AIMessage(content="Flight results fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }

