from langchain_core.runnables import RunnableConfig
from src.state import AgentState

from src.database import (
    upsert_job_listing, 
    upsert_company_profile, 
    upsert_tailored_documents
)

def save_all_artifacts_node(state: AgentState, config: RunnableConfig) -> dict:
    """Unified conductor node that flushes active state artifacts to PostgreSQL."""
    db_pool = config.get("configurable", {}).get("db_pool")
    if not db_pool:
        raise ValueError("Database connection pool was not provided in graph configuration.")

    extracted_jobs = state.get("extracted_jobs", [])
    profile_data = state.get("current_company_profile")
    final_letters = state.get("final_cover_letters", [])
    
    with db_pool.connection() as conn:
        with conn.cursor() as cur:
            for listing in extracted_jobs:
                upsert_job_listing(cur, listing)
                
            if profile_data:
                upsert_company_profile(cur, profile_data)
                
            for letter in final_letters:
                upsert_tailored_documents(cur, letter)
                
        print("Database synchronization transaction completed successfully.")
        
    return {}
