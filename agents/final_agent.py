from __future__ import annotations
from graph.state import TravelState
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from agents.llm import llm


import json


def final_agent(state: TravelState):
    final_prompt = f"""
    Generate a final travel response.

    Flights:
    {state['flight_results']}
    Hotels:
    {state['hotel_results']}
    Itinerary:
    {state['itinerary']}
    
    
"""
    response=llm.invoke([
        HumanMessage(content=final_prompt)
])

    return{
        "messages":[response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }
