# src/graph.py
from langgraph.graph import StateGraph, START, END
from src.state import AgentState
from src.nodes.search import generalized_search_node


def route_search_results(state: AgentState) -> Literal["parse_jobs", "extract_company_profile"]:
    """Routes the generalized search data to the correct LLM parser based on intent."""
    if state["search_intent"] == "job_hunting":
        return "parse_jobs"  # Routes to Gemini with the JobListing schema
        
    if state["search_intent"] == "company_research":
        return "extract_company_profile"  # Routes to Gemini with the CompanyProfile schema


builder = StateGraph(AgentState)

# 1. Bind configuration properties to create two unique operational stations
job_hunter_station = generalized_search_node.bind_config(
    configurable={"destination_key": "raw_search_results", "max_results": 20}
)

company_researcher_station = generalized_search_node.bind_config(
    configurable={"destination_key": "company_research_raw", "max_results": 3}
)

# 2. Add them as distinct node addresses inside your LangGraph blueprints
builder.add_node("job_search", job_hunter_station)
builder.add_node("company_research", company_researcher_station)
