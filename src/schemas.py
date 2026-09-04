from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

class JobListing(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True
    )
    
    title: str = Field(description="Job title.")
    company: str = Field(description="Company name.")
    company_site_url: str | None = Field(
        default=None,
        description="The company's official branded careers URL (e.g., stripe.com/careers/...)."
    )
    location: str = Field(description="City, State, or 'Remote'.")
    
    employment_type: Literal["Full-time", "Part-time", "Contract", "Internship"] | None = Field(
        default=None, description="The type of employment contract."
    )
    experience_level: str | None = Field(
        default=None, description="Target experience level or years of experience required."
    )
    salary_range: str | None = Field(
        default=None, description="Salary or hourly rate compensation range if listed on the page."
    )
    required_skills: list[str] = Field(
        default_factory=list, description="Key technical or soft skills extracted from the description."
    )
    posted_date: str | None = Field(
        default=None, description="Date job was posted or relative time text (e.g., '3 days ago')."
    )
    responsibilities: list[str] = Field(
        default_factory=list, 
        description="The top 3 to 5 core day-to-day responsibilities or tasks for this role."
    )
    url: str = Field(description="Job application URL.")
    is_valid: bool = Field(description="Job listing is still actively accepting applications.")
    verified_at: str = Field(description="Most recent ISO timestamp this listing was verified.")

class CompanyProfile(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True
    )
    
    company: str = Field(description="Company name.")
    industry: str | None = Field(default=None, description="The primary market vertical or sector.")
    size_or_stage: str | None = Field(
        default=None, description="Approximate employee headcount or funding stage (e.g., Series B, Public)."
    )
    about: str = Field(description="Comprehensive summary of what the company does and its products/services.")
    culture: list[str] = Field(description="Company mission, values, and cultural principles.")
    
    recent_news: list[str] = Field(
        default_factory=list, description="Recent major events, product launches, or news articles."
    )
    cover_letter_angles: list[str] = Field(
        description="Specific personal/professional angles a candidate could address in a cover letter."
    )
    resume_tailoring_notes: list[str] = Field(
        description="Resume themes, skills, or outcomes worth emphasizing for this company."
    )
    cautions: list[str] = Field(description="Facts to verify, potential red flags, or claims to avoid overstating.")
    sources: list[str] = Field(description="Source URLs used to construct this company profile.")

class TailoredLatexResume(BaseModel):
    job_listing_id: str
    latex_code: str = Field(description="The complete compilable LaTeX document string.")
    created_at: str

class TailoredCoverLetter(BaseModel):
    job_listing_id: str
    letter_text: str = Field(description="The complete text of cover letter")
    created_at: str

class SearchQualityCheck(BaseModel):
    is_good_job_search: bool = Field(
        description="True if snippets show actual direct job postings for candidates to apply to. False if snippets are articles, blogs, forums, or resume templates."
    )
    reason: str = Field(
        description="A concise 1-sentence explanation of why the query results were classified this way."
    )