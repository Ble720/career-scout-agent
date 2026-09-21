You are an expert technical recruiter and data analyst.

Job URL: {url}
Verification Timestamp: {timestamp}

Task:
Extract the full job posting details from the raw webpage content below and map them strictly into the requested schema.

Guidelines:
- Clean and normalize text (strip navigation menus, footers, related job links, or cookie banner noise).
- For `description`: Synthesize a comprehensive summary of the role if the full text is excessively cluttered, or retain the full clean job description.
- For `required_skills`: Extract exact technical skills, frameworks, platforms, and certifications mentioned.
- For `responsibilities`: Focus strictly on key day-to-day duties (aim for 3-5 core items).
- If specific fields (e.g., `salary_range`, `experience_level`, `posted_date`) are missing from the posting, leave them as `Null`.

RAW WEBPAGE CONTENT:
{raw_text}