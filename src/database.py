import json

def upsert_job_listing(cur, listing) -> None:
    """Handles pure SQL execution for a single job listing."""
    cur.execute(
        """
        INSERT INTO job_listing (
            title, company, location, posted_date, employment_type,
            experience_level, salary_range, required_skills, responsibilities, url
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (url) DO UPDATE SET
            verified_at = CURRENT_TIMESTAMP,
            is_valid = TRUE;
        """,
        (
            listing.title, listing.company, listing.location, listing.posted_date,
            listing.employment_type, listing.experience_level, listing.salary_range,
            listing.required_skills, listing.responsibilities, listing.url
        )
    )

def upsert_company_profile(cur, profile) -> None:
    """Handles pure SQL execution for a corporate research profile."""
    cur.execute(
        """
        INSERT INTO company_profile (
            company, industry, size_or_stage, about, culture,
            recent_news, cover_letter_angles, resume_tailoring_notes, cautions, sources
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (company) DO UPDATE SET
            about = EXCLUDED.about,
            culture = EXCLUDED.culture,
            recent_news = EXCLUDED.recent_news,
            cover_letter_angles = EXCLUDED.cover_letter_angles,
            updated_at = CURRENT_TIMESTAMP;
        """,
        (
            profile.company, profile.industry, profile.size_or_stage,
            profile.about, profile.culture, profile.recent_news,
            json.dumps(profile.cover_letter_angles),
            profile.resume_tailoring_notes, profile.cautions, profile.sources
        )
    )

def upsert_tailored_documents(cur, letter) -> None:
    """Resolves foreign key linkages and upserts application packages."""
    cur.execute("SELECT id FROM job_listing WHERE url = %s LIMIT 1", (letter.get("url"),))
    job_row = cur.fetchone()
    
    if not job_row:
        print(f"⚠️ Could not map document to job row for URL: {letter.get('url')}")
        return
        
    job_id = job_row[0]
    
    cur.execute(
        """
        INSERT INTO cover_letter (job_listing_id, letter_text)
        VALUES (%s, %s)
        ON CONFLICT (job_listing_id) DO UPDATE SET
            letter_text = EXCLUDED.letter_text,
            created_at = CURRENT_TIMESTAMP;
        """,
        (job_id, letter.get("letter_text"))
    )
    
    if letter.get("latex_code"):
        cur.execute(
            """
            INSERT INTO resume (job_listing_id, latex_code)
            VALUES (%s, %s)
            ON CONFLICT (job_listing_id) DO UPDATE SET
                latex_code = EXCLUDED.latex_code,
                created_at = CURRENT_TIMESTAMP;
            """,
            (job_id, letter.get("latex_code"))
        )
