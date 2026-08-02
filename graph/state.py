from __future__ import annotations
from langchain_core.messages import AnyMessage

import os
from typing import TypedDict,Annotated,Any
import operator


class TravelState(TypedDict):
    messages:Annotated[list[AnyMessage],operator.add]
    user_query:str
    flight_results:str
    hotel_results:str
    itinerary:str
    final_response: str
    llm_calls:int
