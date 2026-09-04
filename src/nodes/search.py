from tavily import TavilyClient
from langchain_core.runnables import RunnableConfig

def tavily_search_node(state: AgentState, config: RunnableConfig) -> dict:
    """Pops the next query and performs a free content-rich search."""
    tavily_client = config.get("configurable", {}).get("tavily_client")
    state_destination_key = config.get("configurable", {}).get("destination_key", "raw_search_results")
    max_results_limit = config.get("configurable", {}).get("max_results", 5) # Default fallback is 5

    queries = state["queries"].copy()
    if not queries:
        return {"raw_search_results": []}

    if not tavily_client:
        raise ValueError("Tavily client was not provided in graph configuration.")
        
    next_query = queries.pop(0)
    print(f"🕵️ Searching Tavily for: '{next_query}'")
    
    # Executes single-credit search containing raw_content
    response = tavily_client.search(
        query=next_query,
        search_depth="advanced",
        max_results=max_results_limit,
        include_raw_content=True
    )
    
    return {
        "queries": queries,
        "current_query": next_query,
        "raw_search_results": response.get('results', [])
    }