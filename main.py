# main.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient
from src.graph import graph

from psycopg_pool import ConnectionPool
from src.db_utils import bootstrap_database

load_dotenv()

db_url = os.getenv("DATABASE_URL", "postgresql://localhost/career_scout")
db_pool = ConnectionPool(conninfo=db_url, min_size=1, max_size=5)
bootstrap_database(db_pool)

live_tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

live_gemini_client = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3 # Low temperature for accurate parsing data
)

config = {
    "configurable": {
        "tavily_client": live_tavily_client,
        "gemini_client": live_gemini_client ,
        "db_pool": db_pool,
    }
}

initial_state = {
    "queries": ['"software engineer" remote jobs posted today'],
    "current_query": "",
    "seen_urls": set(),
    "raw_search_results": [],
    "extracted_jobs": [],
    "current_job_to_research": None,
    "raw_company_research_results": [],
    "final_cover_letters": []
}

if __name__ == "__main__":
    print("Starting Automated Job Search & Research Agent...")
    final_state = graph.invoke(initial_state, config=config)
    print(f"Finished!")
