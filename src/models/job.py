import datetime
from typing import Optional, Literal
from pydantic import ConfigDict
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

class JobListing(SQLModel, table=True):
    __tablename__ = "job_listings"
    
    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    
    title: str = Field(description="Job title.")
    company: str = Field(description="Company name.")
    company_site_url: str | None = Field(
        default=None,
        description="The company's official branded careers URL (e.g., stripe.com/careers/...)."
    )
    location: str = Field(description="City, State, or 'Remote'.")
    
    employment_type: Literal["Full-time", "Part-time", "Contract", "Internship"] | None = Field(
        default=None, 
        description="The type of employment contract."
    )
    experience_level: str | None = Field(
        default=None, 
        description="Target experience level or years of experience required."
    )
    salary_range: str | None = Field(
        default=None, 
        description="Salary or hourly rate compensation range if listed on the page."
    )
    description: str = Field(
        default="", 
        description="Full text or core summary of the job posting."
    )
    required_skills: list[str] = Field(
        default_factory=list, 
        sa_column=Column(JSONB), 
        description="Key technical or soft skills extracted from the description."
    )
    posted_date: str | None = Field(
        default=None, 
        description="Date job was posted or relative time text (e.g., '3 days ago')."
    )
    responsibilities: list[str] = Field(
        default_factory=list, 
        sa_column=Column(JSONB), 
        description="The top 3 to 5 core day-to-day responsibilities or tasks for this role."
    )
    url: str = Field(
        description="Job application URL.",
        unique=True,
        index=True)
    is_valid: bool = Field(
        default=True,
        description="Job listing is still actively accepting applications."
    )
    verified_at: str = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat(),
        description="Most recent ISO timestamp this listing was verified."
    )
    embedding: list[float] | None = Field(
        default=None,
        sa_column=Column(Vector(768)),
        description="Vector embedding generated from job title, description, and required skills."
    )
    