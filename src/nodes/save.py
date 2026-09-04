

def init_db(conn) -> None:
    """Creates the production schemas once using the active connection."""
    with conn.cursor() as cur:
        # 1. Job Listings Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS job_listing (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                posted_date TIMESTAMPTZ,
                employment_type TEXT,
                experience_level TEXT,
                salary_range TEXT,
                required_skills TEXT[],
                responsibilities TEXT[],
                url TEXT NOT NULL UNIQUE,
                is_valid BOOLEAN NOT NULL DEFAULT TRUE,
                verified_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_job_leads_posted_date ON job_listing(posted_date)")
        
        # 2. Company Profiles Table (Bug Fixes Applied)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS company_profile (
                company TEXT PRIMARY KEY,
                industry TEXT,
                size_or_stage TEXT,
                about TEXT NOT NULL,
                culture TEXT[] NOT NULL,
                recent_news TEXT[] NOT NULL,
                cover_letter_angles JSONB NOT NULL, -- Fixed syntax constraint
                resume_tailoring_notes TEXT[] NOT NULL,
                cautions TEXT[] NOT NULL,
                sources TEXT[] NOT NULL,
                updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_company_profile_name ON company_profile(company)")

        # 3. Resume Table (Linked explicitly to job listing IDs)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS resume (
                job_listing_id INT PRIMARY KEY REFERENCES job_listing(id) ON DELETE CASCADE,
                latex_code TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 4. Cover Letter Table 
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cover_letter (
                job_listing_id INT PRIMARY KEY REFERENCES job_listing(id) ON DELETE CASCADE,
                letter_text TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)