from tavily import TavilyClient
from src.state import AgentState
from langchain_core.runnables import RunnableConfig

def tavily_search_node(state: AgentState, config: RunnableConfig) -> dict:
    """Pops the next query and performs a free content-rich search."""
    tavily_client = config.get("configurable", {}).get("tavily_client")
    state_destination_key = config.get("configurable", {}).get("destination_key", "raw_search_results")
    max_results_limit = config.get("configurable", {}).get("max_results", 20)

    queries = state["queries"].copy()
    if not queries:
        return {state_destination_key: []}

    if not tavily_client:
        raise ValueError("Tavily client was not provided in graph configuration.")
        
    next_query = queries.pop(0)
    print(f"Searching Tavily for: '{next_query}' (Requesting max {max_results_limit} results)")
    
    response = tavily_client.search(
        query=next_query,
        search_depth="advanced",
        max_results=max_results_limit,
        include_raw_content=True
    )
    
    return {
        "queries": queries,
        "current_query": next_query,
        state_destination_key: response.get('results', [])
    }