# Agent Guidelines for multi-agent-guide

## Setup
- Install dependencies: `uv sync` or `pip install -e .`
- Environment variables: ensure .env contains GROQ_API, AVIATION_API_KEY, TAVILY_API_KEY (see .env)

## Running
- Start the travel planner: `python main.py` (uses sample request)
- Custom request: `python main.py --request "your request text"`

## Dependencies
- Core: langchain, langgraph, streamlit, tavily, python-dotenv
- Aviation API via aviationstack (key in .env)

## Notes
- The graph is defined in `graph.state.graph`; agents are in `agents/`.
- No test suite currently; verify by running the script and checking output.
- Code style follows typical Python conventions; no enforced formatter.
