import os
from typing import TypedDict,Annotated
import operator

import psycopg
from langgraph.graph import StateGraph,START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import(
    AnyMessage,
    HumanMessage,
    SystemMessage,
    AIMessage,

)

from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from tools.tavily_tools import search_hotels
from tools.flight_tool import search_flights



llm=ChatGroq(model="llama-3.3-70b-versatile",
             temperature=0.3,)


DB_URL=os.getenv("DATABASE_URL")





