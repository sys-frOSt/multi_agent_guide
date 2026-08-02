from __future__ import annotations

import json


from langchain_core.messages import HumanMessage, SystemMessage

from graph.state import TravelState
from agents.llm import llm

def itinerary_agent(state: TravelState):
    prompt=f"""
    Create a travel iterary.
    User query: {state['user_query']}
    Flight results: {state['flight_results']}
    Hotel results: {state['hotel_results']}
    """

    response = llm.invoke([SystemMessage(content="" \
    "You are a expert travel agent."),
    HumanMessage(content=prompt)])
    return{
        "iterary": response.content,
        "messages":[response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }