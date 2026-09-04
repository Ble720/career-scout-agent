import datetime

def process_and_parse_node(state: AgentState) -> dict:
    new_jobs = []
    seen = state["seen_urls"].copy()
    
    for result in state["raw_search_results"]:
        url = result.get('url', '')
        raw_text = result.get('raw_content', '')
        
        if url in seen or not raw_text or len(raw_text.strip()) < 100:
            continue
            
        try:
            # Build the mapping prompt
            prompt = (
                f"Extract details for this job listing. URL: {url}. "
                f"Verification Timestamp: {datetime.datetime.utcnow().isoformat()}Z. \n\n"
                f"RAW WEBPAGE CONTENT:\n{raw_text}"
            )
            
            # Gemini handles the validation against your JobListing BaseModel automatically
            job_data: JobListing = llm.invoke(prompt)
            
            new_jobs.append(job_data)
            seen.add(url)
            print(f"✅ Gemini Parsed: {job_data.title} @ {job_data.company}")
            
        except Exception as e:
            print(f"❌ Gemini validation failed for {url}: {e}")
            
    return {"extracted_jobs": new_jobs, "seen_urls": seen, "raw_search_results": 0}