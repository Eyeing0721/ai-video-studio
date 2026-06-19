"""API routes for AI Resume + Mock Interview services."""

import logging
from fastapi import APIRouter

from services.resume_engine import (
    optimize_resume,
    generate_cover_letter,
    analyze_jd,
    score_resume,
)
from services.interview_engine import (
    generate_questions,
    evaluate_answer,
    full_mock_interview,
    interview_feedback_report,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/career", tags=["career"])


# ── Resume ─────────────────────────────────────────────

@router.post("/resume/optimize")
async def api_optimize_resume(data: dict):
    """Generate optimized resume from job description + user background."""
    result = await optimize_resume(
        job_description=data.get("job_description", ""),
        user_background=data.get("user_background", ""),
        target_position=data.get("target_position", ""),
        language=data.get("language", "zh"),
        api_key=data.get("api_key", ""),
    )
    return {"resume": result}


@router.post("/resume/cover-letter")
async def api_cover_letter(data: dict):
    """Generate tailored cover letter."""
    result = await generate_cover_letter(
        job_description=data.get("job_description", ""),
        resume=data.get("resume", ""),
        company_name=data.get("company_name", ""),
        language=data.get("language", "zh"),
        api_key=data.get("api_key", ""),
    )
    return {"cover_letter": result}


@router.post("/resume/analyze-jd")
async def api_analyze_jd(data: dict):
    """Analyze a job description to extract key info."""
    result = await analyze_jd(
        job_description=data.get("job_description", ""),
        api_key=data.get("api_key", ""),
    )
    return result


@router.post("/resume/score")
async def api_score_resume(data: dict):
    """Score a resume with detailed feedback."""
    result = await score_resume(
        resume=data.get("resume", ""),
        job_description=data.get("job_description", ""),
        language=data.get("language", "zh"),
        api_key=data.get("api_key", ""),
    )
    return result


# ── Interview ──────────────────────────────────────────

@router.post("/interview/questions")
async def api_generate_questions(data: dict):
    """Generate tailored interview questions."""
    result = await generate_questions(
        job_description=data.get("job_description", ""),
        interview_type=data.get("interview_type", "mixed"),
        difficulty=data.get("difficulty", "medium"),
        question_count=data.get("question_count", 8),
        language=data.get("language", "zh"),
        api_key=data.get("api_key", ""),
    )
    return result


@router.post("/interview/evaluate")
async def api_evaluate_answer(data: dict):
    """Evaluate a single interview answer."""
    result = await evaluate_answer(
        question=data.get("question", ""),
        answer=data.get("answer", ""),
        question_intent=data.get("question_intent", ""),
        expected_points=data.get("expected_points", None),
        language=data.get("language", "zh"),
        api_key=data.get("api_key", ""),
    )
    return result


@router.post("/interview/full")
async def api_full_interview(data: dict):
    """Run a complete mock interview simulation."""
    result = await full_mock_interview(
        job_description=data.get("job_description", ""),
        interview_type=data.get("interview_type", "mixed"),
        difficulty=data.get("difficulty", "medium"),
        language=data.get("language", "zh"),
        api_key=data.get("api_key", ""),
    )
    return result


@router.post("/interview/report")
async def api_interview_report(data: dict):
    """Generate comprehensive interview feedback report."""
    result = await interview_feedback_report(
        all_qa=data.get("qa_pairs", []),
        language=data.get("language", "zh"),
        api_key=data.get("api_key", ""),
    )
    return result


# ── Combined workflow ─────────────────────────────────

@router.post("/full-package")
async def api_full_package(data: dict):
    """One-shot: analyze JD → generate resume → cover letter → interview prep.

    Best for 闲鱼 delivery: user sends JD + background, gets everything back.
    """
    jd = data.get("job_description", "")
    bg = data.get("user_background", "")
    position = data.get("target_position", "")
    company = data.get("company_name", "")
    lang = data.get("language", "zh")
    key = data.get("api_key", "")

    # Run JD analysis, resume, and cover letter in parallel
    import asyncio
    jd_analysis_task = analyze_jd(jd, key)
    resume_task = optimize_resume(jd, bg, position, lang, key)

    jd_analysis, resume = await asyncio.gather(jd_analysis_task, resume_task)
    cover_letter = await generate_cover_letter(jd, resume, company, lang, key)
    interview = await full_mock_interview(jd, "mixed", "medium", lang, key)
    score = await score_resume(resume, jd, lang, key)

    return {
        "jd_analysis": jd_analysis,
        "resume": resume,
        "cover_letter": cover_letter,
        "mock_interview": interview,
        "resume_score": score,
    }
