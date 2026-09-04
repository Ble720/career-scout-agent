-- init.sql
-- Database initialization script for the LangGraph Job Search and Research Agent.

-- Job Listings Table
-- Uses the unique job URL to prevent duplicate postings.
CREATE TABLE IF NOT EXISTS job_listing (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT,
    posted_date TIMESTAMPTZ,
    employment_type TEXT,
    experience_level TEXT,
    salary_range TEXT,
    required_skills TEXT[] NOT NULL DEFAULT '{}', -- Native Postgres string arrays
    responsibilities TEXT[] NOT NULL DEFAULT '{}',
    url TEXT NOT NULL UNIQUE,                      -- Enforces deduplication on the unique URL link
    is_valid BOOLEAN NOT NULL DEFAULT TRUE,
    verified_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index to optimize querying or sorting job trends by time
CREATE INDEX IF NOT EXISTS idx_job_listing_posted_date ON job_listing(posted_date);


-- Company Profiles Table
-- Stores dense background information extracted by Gemini.
CREATE TABLE IF NOT EXISTS company_profile (
    company TEXT PRIMARY KEY,                       -- Company name serves as the natural primary key
    industry TEXT,
    size_or_stage TEXT,
    about TEXT NOT NULL,
    culture TEXT[] NOT NULL DEFAULT '{}',
    recent_news TEXT[] NOT NULL DEFAULT '{}',
    cover_letter_angles JSONB NOT NULL DEFAULT '[]', -- JSONB handles arrays of complex reasoning hooks beautifully
    resume_tailoring_notes TEXT[] NOT NULL DEFAULT '{}',
    cautions TEXT[] NOT NULL DEFAULT '{}',
    sources TEXT[] NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_company_profile_name ON company_profile(company);


-- Tailored Resumes Table
-- Links explicitly to the exact job listing via a foreign key.
CREATE TABLE IF NOT EXISTS resume (
    job_listing_id INT PRIMARY KEY REFERENCES job_listing(id) ON DELETE CASCADE,
    latex_code TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Tailored Cover Letters Table
-- Links explicitly to the exact job listing via a foreign key.
CREATE TABLE IF NOT EXISTS cover_letter (
    job_listing_id INT PRIMARY KEY REFERENCES job_listing(id) ON DELETE CASCADE,
    letter_text TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
