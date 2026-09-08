from typing import Optional
from pydantic import ConfigDict
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

class CompanyProfile(SQLModel, table=True):
    __tablename__ = "company_profiles"

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    company: str = Field(description="Company name.", index=True)
    industry: str | None = Field(default=None, description="The primary market vertical or sector.")
    size_or_stage: str | None = Field(
        default=None, description="Approximate employee headcount or funding stage (e.g., Series B, Public)."
    )
    about: str = Field(description="Comprehensive summary of what the company does and its products/services.")
    
    culture: list[str] = Field(
        default_factory=list, 
        sa_column=Column(JSONB), 
        description="Company mission, values, and cultural principles."
    )
    recent_news: list[str] = Field(
        default_factory=list, 
        sa_column=Column(JSONB), 
        description="Recent major events, product launches, or news articles."
    )
    cover_letter_angles: list[str] = Field(
        default_factory=list, 
        sa_column=Column(JSONB), 
        description="Specific personal/professional angles a candidate could address in a cover letter."
    )
    resume_tailoring_notes: list[str] = Field(
        default_factory=list, 
        sa_column=Column(JSONB), 
        description="Resume themes, skills, or outcomes worth emphasizing for this company."
    )
    cautions: list[str] = Field(
        default_factory=list, 
        sa_column=Column(JSONB), 
        description="Facts to verify, potential red flags, or claims to avoid overstating."
    )
    sources: list[str] = Field(
        default_factory=list, 
        sa_column=Column(JSONB), 
        description="Source URLs used to construct this company profile."
    )
    embedding: list[float] | None = Field(
        default=None,
        sa_column=Column(Vector(768)),
        description="Vector embedding generated from company name, about summary, culture, and market sector."
    )