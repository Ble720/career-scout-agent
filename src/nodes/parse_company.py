import datetime
from langchain_core.runnables import RunnableConfig
from src.state import AgentState
from src.schemas import CompanyProfile

def process_and_parse_company_node(state: AgentState, config: RunnableConfig) -> dict:
    raw_results = state.get("raw_company_search_results", [])
    if not raw_results:
        print("No raw company search results found to parse. Skipping node.")
        return {}

    base_llm = config.get("configurable", {}).get("gemini_client")
    if not base_llm:
        raise ValueError(
            "Gemini client was not provided in graph configuration."
        )

    structured_llm = base_llm.with_structured_output(CompanyProfile)

    aggregated_text_blocks = []
    collected_urls = []

    for result in raw_results:
        url = result.get("url", "")
        raw_text = result.get("raw_content", "")

        if raw_text and len(raw_text.strip()) >= 50:
            aggregated_text_blocks.append(
                f"SOURCE URL: {url}\nCONTENT:\n{raw_text}"
            )
            if url:
                collected_urls.append(url)

    if not aggregated_text_blocks:
        print("No valid content found in raw results. Skipping parsing.")
        return {"raw_company_search_results": []}

    # 2. Combine all search content into a single context payload
    combined_context = "\n\n---\n\n".join(aggregated_text_blocks)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    prompt = (
        f"You are an expert corporate research analyst.\n"
        f"Synthesize the following web search snippets to extract a single, comprehensive company profile.\n"
        f"Verification Timestamp: {timestamp}\n\n"
        f"AGGREGATED WEB SEARCH CONTENT:\n{combined_context}"
    )

    try:
        profile_data: CompanyProfile = structured_llm.invoke(prompt)

        for url in collected_urls:
            if url not in profile_data.sources:
                profile_data.sources.append(url)

        print(f"Gemini Parsed Unified Profile for: {profile_data.company}")

        return {
            "extracted_company_profiles": [profile_data],
            "raw_company_search_results": [],  
        }

    except Exception as e:
        print(f"Gemini company profile synthesis failed: {e}")
        return {"raw_company_search_results": []}