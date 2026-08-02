from agents.itinerary_agent import itinerary_agent
from agents.flight_agent import flight_agent
from agents.hotel_agent import hotel_agent
from agents.final_agent import final_agent
from graph.state import TravelState
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, StateGraph,START
from dotenv import load_dotenv
import os
from psycopg.rows import dict_row



builder=StateGraph(TravelState)

builder.add_node("flight", flight_agent)
builder.add_node("hotel", hotel_agent)
builder.add_node("itinerary", itinerary_agent)
builder.add_node("final", final_agent)



builder.add_edge(START, "flight")
builder.add_edge("flight", "hotel")
builder.add_edge("hotel", "itinerary")
builder.add_edge("itinerary", "final")
builder.add_edge("final", END)
