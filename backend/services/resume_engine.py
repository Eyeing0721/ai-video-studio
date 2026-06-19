"""AI Resume Optimization Engine — generates tailored resumes, cover letters, and analyzes job descriptions.

Uses DeepSeek via Anthropic-compatible API (same pattern as deepseek_client.py).
"""

import json
import logging
from typing import Optional

import httpx

from config import config

logger = logging.getLogger(__name__)

DEEPSEEK_URL = config["deepseek_base_url"].rstrip("/")
API_KEY = config["deepseek_api_key"]
MODEL = "deepseek-v4-pro[1m]"

RESUME_SYSTEM = """你是一位资深HR和职业规划师，拥有10年以上简历筛选和面试官经验，同时精通ATS（申请人追踪系统）的筛选规则。

你的任务是帮用户优化简历。你必须做到：
1. 量化成就——所有描述必须有数字支撑（提升了X%、节省了Y万、管理了Z人团队）
2. 关键词优化——根据目标岗位的JD，在简历中自然融入行业关键词和技能术语
3. STAR法则——每个项目经历用 Situation-Task-Action-Result 框架重写
4. 去废话——删除"负责""参与"等弱动词，替换为"主导""搭建""从0到1""优化至"
5. 排版干净——不使用特殊符号、表格、图形（会被ATS误读）
6. 个性化——根据JD调整简历侧重点，突出匹配度最高的经历

【简历格式规范】
- 使用 Markdown 格式输出
- 结构：个人信息 → 求职意向 → 核心技能 → 工作经历 → 项目经历 → 教育背景 → 证书/其他
- 工作经历中每段经历3-5个bullet point
- 每个bullet point必须有量化数据

输出纯文本，不要加"```"代码块标记。"""


async def _chat(system: str, user: str, api_key: str = "") -> str:
    """Send a chat completion request to DeepSeek."""
    key = api_key or API_KEY
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Anthropic-Version": "2023-06-01",
    }
    body = {
        "model": MODEL,
        "max_tokens": 8192,
        "temperature": 0.7,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(
            f"{DEEPSEEK_URL}/messages",
            headers=headers,
            json=body,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["content"][0]["text"]


async def optimize_resume(
    job_description: str,
    user_background: str,
    target_position: str = "",
    language: str = "zh",
    api_key: str = "",
) -> str:
    """Generate an optimized resume based on job description and user background."""
    lang_hint = "请用中文输出简历。" if language == "zh" else "Please output the resume in English."
    user_msg = f"""【目标岗位】{target_position or '见JD'}

【招聘JD】
{job_description}

【我的背景】
{user_background}

{lang_hint}

请输出一份针对该岗位的优化后简历。严格遵循STAR法则，所有经历必须有量化数据。"""

    return await _chat(RESUME_SYSTEM, user_msg, api_key)


async def generate_cover_letter(
    job_description: str,
    resume: str,
    company_name: str = "",
    language: str = "zh",
    api_key: str = "",
) -> str:
    """Generate a tailored cover letter / 求职信."""
    lang_hint = "用中文写" if language == "zh" else "Write in English"
    company_hint = f"投递公司：{company_name}" if company_name else ""

    system = f"""你是一位资深求职顾问，擅长撰写打动人心的求职信。{lang_hint}。
规则：
- 开头直击痛点——展示你对公司和岗位的理解，不要废话
- 中间用1-2个具体成就证明你的能力
- 结尾表达真诚的兴趣和行动呼吁
- 全文300-500字，不要超过一页A4
- 语气专业但不死板，有温度但不油腻"""
    user = f"""【招聘JD】
{job_description}

{company_hint}

【我的简历】
{resume}

请根据以上信息写一封求职信。"""

    return await _chat(system, user, api_key)


async def analyze_jd(job_description: str, api_key: str = "") -> dict:
    """Analyze a job description to extract key requirements, skills, and hidden expectations."""
    system = """你是资深HR。分析JD并输出JSON。
返回格式：
{
  "position": "岗位名称",
  "hard_skills": ["硬技能1", "硬技能2"],
  "soft_skills": ["软技能1", "软技能2"],
  "years_required": "要求年限",
  "education": "学历要求",
  "key_responsibilities": ["核心职责1", "核心职责2"],
  "hidden_requirements": ["隐性要求1（JD没写但实际看重）"],
  "salary_hint": "薪资范围暗示",
  "company_culture_clues": "从JD措辞推断的公司文化",
  "resume_keywords": ["必须在简历中出现的词"],
  "interview_focus": ["面试最可能问的方向"]
}"""
    user = f"请分析以下招聘JD：\n\n{job_description}"

    result = await _chat(system, user, api_key)
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {"raw_analysis": result}


async def score_resume(
    resume: str,
    job_description: str = "",
    language: str = "zh",
    api_key: str = "",
) -> dict:
    """Score a resume against best practices and optionally against a specific JD."""
    lang_hint = "用中文回复" if language == "zh" else "Reply in English"
    jd_context = f"\n\n【目标岗位JD】\n{job_description}" if job_description else ""

    system = f"""你是资深HR和简历评审专家。{lang_hint}。
对简历进行五维评分（每项1-10分），并给出具体修改建议。
输出JSON格式：
{{
  "overall_score": 0,
  "dimensions": {{
    "quantified_impact": {{"score": 0, "comment": "具体评价"}},
    "keyword_match": {{"score": 0, "comment": "具体评价"}},
    "structure_clarity": {{"score": 0, "comment": "具体评价"}},
    "star_format": {{"score": 0, "comment": "具体评价"}},
    "ats_friendly": {{"score": 0, "comment": "具体评价"}}
  }},
  "top_strengths": ["优点1", "优点2", "优点3"],
  "critical_fixes": ["必须改的问题1", "必须改的问题2"],
  "optimization_tips": ["优化建议1", "优化建议2"]
}}"""
    user = f"请评审以下简历：\n\n{resume}{jd_context}"

    result = await _chat(system, user, api_key)
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {"raw_score": result}
