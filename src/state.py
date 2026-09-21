from __future__ import annotations
from typing import Any, List, Literal, Optional
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages
from typing import Annotated

class AgentState(BaseModel):
    """
    State model for Career Scout using Pydantic BaseModel.
    """
    messages: Annotated[List[Any], add_messages] = Field(default_factory=list)

    initial_user_input: Optional[str] = Field(
        default=None,
        description="The original unparsed search request from the user"
    )
    queries: List[str] = Field(
        default_factory=list,
        description="List of candidate search queries generated for selection"
    )
    previous_queries: List[str] = Field(
        default_factory=list,
        description="History of previously offered queries to avoid repeating options during refinement"
    )
    user_feedback: Optional[str] = Field(
        default=None,
        description="User critique/instructions provided during query refinement"
    )
    current_query: Optional[str] = Field(
        default=None,
        description="The active search query being executed"
    )

    raw_job_search_results: List[dict] = Field(
        default_factory=list,
        description="Raw JSON results returned from web search or API tools"
    )
    raw_company_search_results: List[dict] = Field(
        default_factory=list,
        description="Raw JSON results returned from company research queries"
    )

    unseen_companies: List[str] = Field(
        default_factory=list,
        description="Companies extracted from job listings that do not exist in the DB yet"
    )

    thread_id: Optional[str] = Field(
        default=None,
        description="Session ID mapping to Redis `chat:{thread_id}`"
    )
    search_query_hash: Optional[str] = Field(
        default=None,
        description="SHA-256 hash for Redis `search:{query_hash}` cache lookups"
    )
    cache_hit: bool = Field(
        default=False,
        description="Flag indicating if results were populated from Redis"
    )