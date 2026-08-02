from dotenv import load_dotenv
import os
from typing import Any, cast

from langgraph.checkpoint.postgres import PostgresSaver

from graph.builder import builder
from langchain_core.messages import HumanMessage

load_dotenv()



def main():
    db_url = os.getenv("DATABASE_URL")

    if db_url is None:
        raise ValueError("DATABASE_URL not found in .env")

    with PostgresSaver.from_conn_string(db_url) as checkpointer:
        checkpointer.setup()

        # Read user input and build the payload inline (matches screenshot)
        user_input = input("Enter travel request: ")

        payload: Any = {
            "messages": [HumanMessage(content=user_input)],
            "user_query": user_input,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0,
        }

        app = builder.compile(checkpointer=checkpointer)

        config = {"configurable": {"thread_id": "user_aviraj"}}

        result = app.invoke(payload, config=cast(Any, config))

        print("\nFINAL RESPONSE:\n")

        for msg in result.get("messages", []):
            content = getattr(msg, "content", msg)
            print(content)

        print("\nLLM Calls:", result.get("llm_calls", 0))


if __name__ == "__main__":
    main()