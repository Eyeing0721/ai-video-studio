#!/usr/bin/env python3
"""AI Career Toolkit CLI — resume optimization + mock interview batch generator.

Usage:
  # Single resume from JD + background
  python career_cli.py resume --jd jd.txt --bg my_background.txt

  # Full package (resume + cover letter + interview prep)
  python career_cli.py full --jd jd.txt --bg my_background.txt

  # Batch: process multiple JDs for one background
  python career_cli.py batch --bg my_background.txt --jd-dir ./jobs/

  # Mock interview from JD
  python career_cli.py interview --jd jd.txt

  # Score an existing resume
  python career_cli.py score --resume my_resume.md --jd jd.txt

Output goes to ./career_output/ by default.
"""

import argparse
import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from services.resume_engine import (
    optimize_resume,
    generate_cover_letter,
    analyze_jd,
    score_resume,
)
from services.interview_engine import (
    generate_questions,
    full_mock_interview,
)

OUTPUT_DIR = Path(os.environ.get("CAREER_OUTPUT_DIR", Path(__file__).parent / "career_output"))


def read_file(path: str) -> str:
    p = Path(path)
    if p.exists():
        return p.read_text(encoding="utf-8")
    print(f"[WARN] File not found: {path}")
    return ""


def write_output(filename: str, content: str):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / filename
    out.write_text(content, encoding="utf-8")
    print(f"  -> {out}")


async def cmd_resume(args):
    jd = read_file(args.jd) if args.jd and Path(args.jd).exists() else args.jd or ""
    bg = read_file(args.bg) if args.bg and Path(args.bg).exists() else args.bg or ""

    if not jd:
        jd = input("Paste job description (end with Ctrl+Z then Enter): ")
    if not bg:
        bg = input("Paste your background/current resume: ")

    print("\n[1/3] Analyzing JD...")
    jd_analysis = await analyze_jd(jd)
    print(json.dumps(jd_analysis, ensure_ascii=False, indent=2))

    print("\n[2/3] Generating optimized resume...")
    resume = await optimize_resume(jd, bg, args.position or "", "zh")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    write_output(f"resume_{ts}.md", resume)

    print("\n[3/3] Generating cover letter...")
    cover = await generate_cover_letter(jd, resume, args.company or "", "zh")
    write_output(f"cover_letter_{ts}.md", cover)

    print("\n=== DONE ===")
    print(f"Resume: career_output/resume_{ts}.md")
    print(f"Cover Letter: career_output/cover_letter_{ts}.md")


async def cmd_full(args):
    jd = read_file(args.jd) if args.jd and Path(args.jd).exists() else args.jd or ""
    bg = read_file(args.bg) if args.bg and Path(args.bg).exists() else args.bg or ""

    if not jd:
        jd = input("Paste job description: ")
    if not bg:
        bg = input("Paste your background: ")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("\n[1/5] Analyzing JD...")
    jd_analysis = await analyze_jd(jd)

    print("[2/5] Optimizing resume...")
    resume = await optimize_resume(jd, bg, args.position or "", "zh")

    print("[3/5] Generating cover letter...")
    cover = await generate_cover_letter(jd, resume, args.company or "", "zh")

    print("[4/5] Scoring resume...")
    score = await score_resume(resume, jd, "zh")

    print("[5/5] Generating mock interview...")
    interview = await full_mock_interview(jd, "mixed", "medium", "zh")

    # Write all outputs
    write_output(f"package_{ts}_resume.md", resume)
    write_output(f"package_{ts}_cover_letter.md", cover)
    write_output(f"package_{ts}_jd_analysis.json", json.dumps(jd_analysis, ensure_ascii=False, indent=2))
    write_output(f"package_{ts}_resume_score.json", json.dumps(score, ensure_ascii=False, indent=2))
    write_output(f"package_{ts}_interview.json", json.dumps(interview, ensure_ascii=False, indent=2))

    # Combined report
    report = f"""# AI 求职全案

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> 目标岗位：{args.position or '见JD分析'}

## 1. JD 分析

{json.dumps(jd_analysis, ensure_ascii=False, indent=2)}

## 2. 优化后简历

{resume}

## 3. 求职信

{cover}

## 4. 简历评分

{json.dumps(score, ensure_ascii=False, indent=2)}

## 5. 模拟面试

{json.dumps(interview, ensure_ascii=False, indent=2)}
"""
    write_output(f"package_{ts}_FULL.md", report)

    print(f"\n=== DONE ===")
    print(f"Full package: career_output/package_{ts}_FULL.md")
    print(f"  Ready for 闲鱼 delivery!")


async def cmd_interview(args):
    jd = read_file(args.jd) if args.jd and Path(args.jd).exists() else args.jd or ""
    if not jd:
        jd = input("Paste job description: ")

    print("\nGenerating mock interview...")
    interview = await full_mock_interview(
        jd, args.type or "mixed", args.difficulty or "medium", "zh"
    )
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    write_output(f"interview_{ts}.json", json.dumps(interview, ensure_ascii=False, indent=2))
    print(f"  -> career_output/interview_{ts}.json")


async def cmd_score(args):
    resume = read_file(args.resume) if Path(args.resume).exists() else args.resume or ""
    jd = read_file(args.jd) if args.jd and Path(args.jd).exists() else args.jd or ""

    if not resume:
        resume = input("Paste your resume: ")

    print("\nScoring resume...")
    result = await score_resume(resume, jd, "zh")
    print(json.dumps(result, ensure_ascii=False, indent=2))


async def cmd_batch(args):
    bg = read_file(args.bg) if Path(args.bg).exists() else args.bg or ""
    if not bg:
        bg = input("Paste your background: ")

    jd_dir = Path(args.jd_dir)
    jd_files = list(jd_dir.glob("*.txt")) + list(jd_dir.glob("*.md"))
    if not jd_files:
        print(f"No .txt or .md files found in {jd_dir}")
        return

    print(f"\nBatch processing {len(jd_files)} JDs for 1 background...")
    for i, jf in enumerate(jd_files):
        print(f"\n[{i+1}/{len(jd_files)}] {jf.name}")
        jd = jf.read_text(encoding="utf-8")
        try:
            resume = await optimize_resume(jd, bg, "", "zh")
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = jf.stem.replace(" ", "_")
            write_output(f"batch_{name}_resume.md", resume)
        except Exception as e:
            print(f"  [ERROR] {e}")

    print(f"\n=== BATCH DONE ===")


def main():
    parser = argparse.ArgumentParser(description="AI Career Toolkit — 简历优化 + 模拟面试")
    sub = parser.add_subparsers(dest="command")

    p_resume = sub.add_parser("resume", help="Generate optimized resume")
    p_resume.add_argument("--jd", help="Job description file or text")
    p_resume.add_argument("--bg", help="Your background file or text")
    p_resume.add_argument("--position", help="Target position title")
    p_resume.add_argument("--company", help="Target company name")

    p_full = sub.add_parser("full", help="Full package (resume + cover letter + interview)")
    p_full.add_argument("--jd", help="Job description file or text")
    p_full.add_argument("--bg", help="Your background file or text")
    p_full.add_argument("--position", help="Target position title")
    p_full.add_argument("--company", help="Target company name")

    p_interview = sub.add_parser("interview", help="Generate mock interview")
    p_interview.add_argument("--jd", help="Job description file or text")
    p_interview.add_argument("--type", default="mixed", choices=["mixed", "technical", "behavioral", "case", "stress"])
    p_interview.add_argument("--difficulty", default="medium", choices=["junior", "medium", "senior", "staff"])

    p_score = sub.add_parser("score", help="Score existing resume")
    p_score.add_argument("--resume", required=True, help="Resume file or text")
    p_score.add_argument("--jd", help="Job description file or text (optional)")

    p_batch = sub.add_parser("batch", help="Batch process multiple JDs")
    p_batch.add_argument("--bg", required=True, help="Your background file or text")
    p_batch.add_argument("--jd-dir", required=True, help="Directory containing JD .txt/.md files")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    asyncio.run(globals()[f"cmd_{args.command}"](args))


if __name__ == "__main__":
    main()
