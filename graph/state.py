from __future__ import annotations
from langchain.messages import AnyMessage
from langgraph.graph import END, StateGraph,START
import os
from typing import TypedDict,Annotated,Any
import operator


class TravelState(TypedDict):
    message:Annotated[list[AnyMessage],operator.add]
    user_query:str
    flight_results:str
    hotel_results:str
    itinerary:str
    llm_calls:int
