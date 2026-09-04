

class AgentState(TypedDict):
    queries: List[str]
    current_query: str
    search_intent: Literal["job_search", "company_research"]
    raw_search_results: List[dict]