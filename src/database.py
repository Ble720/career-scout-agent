import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.models import JobListing, CompanyProfile, TailoredCoverLetter, TailoredLatexResume

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:postgres@localhost:5432/career_scout"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

async_session_factory = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session

async def upsert_job_listing(session: AsyncSession, listing_data: dict) -> None:
    """
    Upserts a JobListing using SQLModel ORM. 
    Updates listing if URL exists, otherwise creates a new record.
    """
    statement = select(JobListing).where(JobListing.url == listing_data.url)
    result = await session.exec(statement)
    existing_job = result.first()

    if existing_job:
        # Update existing record
        for key, value in listing_data.model_dump(exclude_unset=True).items():
            if key not in ("id", "created_at"):
                setattr(existing_job, key, value)
    else:
        # Add new listing
        session.add(listing_data)

    await session.commit()

async def upsert_company_profile(session: AsyncSession, profile_data) -> None:
    """
    Upserts a CompanyProfile using SQLModel ORM.
    Updates profile if company name exists, otherwise creates a new record.
    """
    statement = select(CompanyProfile).where(CompanyProfile.company == profile_data.company)
    result = await session.exec(statement)
    existing_profile = result.first()

    if existing_profile:
        for key, value in profile_data.model_dump(exclude_unset=True).items():
            if key not in ("id", "created_at"):
                setattr(existing_profile, key, value)
    else:
        session.add(profile_data)

    await session.commit()

async def save_tailored_documents(
    session: AsyncSession, 
    job_url: str, 
    cover_letter_text: str | None = None, 
    latex_code: str | None = None
) -> None:
    """Finds job_listing_id by URL and saves associated Cover Letter and LaTeX Resume."""
    statement = select(JobListing.id).where(JobListing.url == job_url)
    result = await session.exec(statement)
    job_id = result.first()

    if not job_id:
        print(f"⚠️ Could not map document to job row for URL: {job_url}")
        return

    if cover_letter_text:
        letter_stmt = select(TailoredCoverLetter).where(TailoredCoverLetter.job_listing_id == job_id)
        letter_res = await session.exec(letter_stmt)
        existing_letter = letter_res.first()

        if existing_letter:
            existing_letter.letter_text = cover_letter_text
        else:
            session.add(TailoredCoverLetter(job_listing_id=job_id, letter_text=cover_letter_text))

    if latex_code:
        resume_stmt = select(TailoredLatexResume).where(TailoredLatexResume.job_listing_id == job_id)
        resume_res = await session.exec(resume_stmt)
        existing_resume = resume_res.first()

        if existing_resume:
            existing_resume.latex_code = latex_code
        else:
            session.add(TailoredLatexResume(job_listing_id=job_id, latex_code=latex_code))

    await session.commit()
