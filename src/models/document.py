from typing import Optional
import datetime
from pydantic import ConfigDict
from sqlmodel import SQLModel, Field

class TailoredLatexResume(SQLModel, table=True):
    __tablename__ = "tailored_latex_resumes"

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    
    job_listing_id: int = Field(
        foreign_key="job_listings.id", 
        unique=True, 
        index=True,
        description="The ID of the job listing this resume is tailored for."
    )
    
    latex_code: str = Field(
        description="The complete compilable LaTeX document string starting with \\documentclass."
    )
    
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        description="UTC timestamp when this resume was generated."
    )


class TailoredCoverLetter(SQLModel, table=True):
    __tablename__ = "tailored_cover_letters"

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    
    job_listing_id: int = Field(
        foreign_key="job_listings.id", 
        unique=True, 
        index=True,
        description="The ID of the job listing this cover letter is tailored for."
    )
    
    letter_text: str = Field(
        description="The complete text of the generated cover letter."
    )
    
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        description="UTC timestamp when this cover letter was generated."
    )