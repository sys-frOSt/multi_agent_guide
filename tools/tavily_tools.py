from __future__ import annotations
import os
from typing import Any
from langchain_core.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv


load_dotenv()


def _client() -> TavilyClient:##api checking
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        raise RuntimeError("TAVILY_API_KEY is not set in the environment")
    return TavilyClient(api_key=key)


@tool
def search_hotels(query: str) -> str:
    """Search hotels via Tavily and return a human-readable string matching the screenshot.

    Each entry is numbered and shows a bold title, the URL, and a truncated snippet (max 300 chars).
    """
    try:
        response = _client().search(query=query, max_results=5)
    except Exception as exc:
        return f"tavily request failed: {exc}"

    results: list[str] = []
    for i, r in enumerate(response.get("results", []) or [], 1):
        title = r.get("title", "Unknown")
        url = r.get("url", "")
        snippet = (r.get("content") or "").strip()
        if len(snippet) > 300:
            snippet = snippet[:300].rsplit(" ", 1)[0] + "..."

        results.append(f"{i}. **{title}**\n{url}\n{snippet}")

    return "\n\n".join(results)
