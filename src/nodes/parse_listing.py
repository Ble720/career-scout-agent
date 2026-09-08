import datetime
from langchain_core.runnables import RunnableConfig
from src.state import AgentState
from src.models import JobListing

def process_and_parse_node(state: AgentState, config: RunnableConfig) -> dict:
    raw_results = state.get("raw_search_results", [])
    if not raw_results:
        print("No raw search results found to parse. Skipping node.")
        return {}
    
    base_llm = config.get("configurable", {}).get("gemini_client")
    if not base_llm:
        raise ValueError("Gemini client was not provided in graph configuration.")
    
    structured_llm = base_llm.with_structured_output(JobListing)
    
    new_jobs = []
    seen = state["seen_urls"].copy()
    
    for result in state["raw_search_results"]:
        url = result.get('url', '')
        raw_text = result.get('raw_content', '')
        
        if url in seen or not raw_text or len(raw_text.strip()) < 100:
            continue
            
        try:
            timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
            
            prompt = (
                f"Extract details for this job listing. URL: {url}. "
                f"Verification Timestamp: {timestamp}. \n\n"
                f"RAW WEBPAGE CONTENT:\n{raw_text}"
            )
            
            job_data: JobListing = structured_llm.invoke(prompt)
            
            new_jobs.append(job_data)
            seen.add(url)
            print(f"Gemini Parsed: {job_data.title} @ {job_data.company}")
            
        except Exception as e:
            print(f"Gemini validation failed for {url}: {e}")
            
    return {
        "extracted_jobs": new_jobs, 
        "seen_urls": seen, 
        "raw_search_results": []
    }