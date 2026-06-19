"""AI Mock Interview Engine — generates tailored questions, evaluates answers, provides feedback."""

import json
import logging
from typing import Optional

import httpx

from config import config

logger = logging.getLogger(__name__)

DEEPSEEK_URL = config["deepseek_base_url"].rstrip("/")
API_KEY = config["deepseek_api_key"]
MODEL = "deepseek-v4-pro[1m]"


async def _chat(system: str, user: str, api_key: str = "") -> str:
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


INTERVIEWER_SYSTEM = """你是一位资深面试官，拥有10年以上技术/管理面试经验，面试过5000+候选人。
你熟悉各类面试形式：结构化面试、行为面试（STAR）、技术面试、案例分析、压力面试。

【面试题设计原则】
1. 行为面试用STAR追问——不只问"你遇到过什么困难"，还要追问"你具体做了什么""结果怎么衡量的"
2. 技术面试要有层次——从基础概念 → 实践应用 → 系统设计 → 踩坑经验
3. 加入压力测试题和陷阱题——考察临场反应
4. 产品/业务题要有场景感——给出具体的业务困境，让候选人提出方案
5. 每道题标注考察意图（考察什么能力）"""


async def generate_questions(
    job_description: str = "",
    interview_type: str = "mixed",
    difficulty: str = "medium",
    question_count: int = 8,
    language: str = "zh",
    api_key: str = "",
) -> dict:
    """Generate tailored interview questions based on job description.

    interview_type: mixed / technical / behavioral / case / stress
    difficulty: junior / medium / senior / staff
    """
    lang_hint = "用中文出题，如果JD中的职位需要英语则中英混合出题" if language == "zh" else "All questions in English"
    type_hints = {
        "mixed": "混合题（40%行为面试 + 40%技术/专业 + 20%压力/场景题）",
        "technical": "纯技术面试题（算法、系统设计、专业技术深度）",
        "behavioral": "纯行为面试题（STAR法则、领导力、冲突处理、团队协作）",
        "case": "纯案例分析题（业务问题、产品决策、战略分析）",
        "stress": "压力面试风格（质疑、打断、时间压力、矛盾问题）",
    }

    system = f"""{INTERVIEWER_SYSTEM}
{lang_hint}
面试类型：{type_hints.get(interview_type, type_hints['mixed'])}
难度：{difficulty}
出题数量：{question_count}道

输出JSON格式：
{{
  "interview_config": {{
    "type": "面试类型",
    "difficulty": "难度",
    "estimated_duration_min": 预计时长分钟数
  }},
  "questions": [
    {{
      "id": 1,
      "question": "面试题",
      "category": "behavioral/technical/case/stress",
      "intent": "这道题考察什么能力",
      "expected_points": ["好的回答应该包含的要点1", "要点2"],
      "follow_up": "如果候选人回答得好，追问什么；回答不好，如何引导",
      "difficulty_level": "easy/medium/hard",
      "estimated_time_min": 回答预计用时
    }}
  ]
}}"""
    user = f"""请根据以下JD生成{question_count}道面试题：

{job_description if job_description else '通用面试（无特定JD）'}

难度：{difficulty}
类型：{type_hints.get(interview_type, type_hints['mixed'])}"""

    result = await _chat(system, user, api_key)
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {"raw_questions": result}


async def evaluate_answer(
    question: str,
    answer: str,
    question_intent: str = "",
    expected_points: list = None,
    language: str = "zh",
    api_key: str = "",
) -> dict:
    """Evaluate a candidate's answer to an interview question."""
    lang_hint = "用中文评价" if language == "zh" else "Evaluate in English"
    intent_line = f"考察意图：{question_intent}" if question_intent else ""
    points_line = f"期望要点：{json.dumps(expected_points, ensure_ascii=False)}" if expected_points else ""

    system = f"""你是资深面试官。{lang_hint}。对候选人的回答进行专业评估。
评分标准：
- 10分：完美的回答，有深度有结构有实例，超出预期
- 8-9分：很好的回答，覆盖了关键点，有实际案例
- 6-7分：合格，回答了问题但缺乏深度或结构
- 4-5分：勉强及格，有内容但不完整或逻辑不清
- 1-3分：不及格，跑题、空洞或错误

输出JSON格式：
{{
  "score": 0,
  "score_breakdown": {{
    "content_relevance": 0,
    "structure_logic": 0,
    "depth_expertise": 0,
    "example_quality": 0,
    "delivery_confidence": 0
  }},
  "strengths": ["做得好的点"],
  "weaknesses": ["需要改进的点"],
  "improved_answer_example": "一个更好的回答范例",
  "key_takeaway": "这道题最关键的面试技巧"
}}"""
    user = f"""面试题：{question}
{intent_line}
{points_line}

候选人回答：{answer}

请评分并给出详细反馈。"""

    result = await _chat(system, user, api_key)
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {"raw_evaluation": result}


async def full_mock_interview(
    job_description: str,
    interview_type: str = "mixed",
    difficulty: str = "medium",
    language: str = "zh",
    api_key: str = "",
) -> dict:
    """Run a complete mock interview simulation — generates questions with model answers."""
    system = f"""你是模拟面试官。根据JD进行一轮完整模拟面试（5道题），
每道题包含：题目、考察点、满分回答范例、评分标准。

输出JSON：
{{
  "interview_title": "面试标题（如：字节跳动高级产品经理模拟面试）",
  "total_duration_min": 预计总时长,
  "rounds": [
    {{
      "round_number": 1,
      "round_name": "轮次名称（如：自我介绍与破冰 / 技术深度 / 行为面试 / 案例分析 / 反问环节）",
      "questions": [
        {{
          "question": "题目",
          "intent": "考察意图",
          "model_answer": "满分回答范例",
          "scoring_rubric": "评分标准",
          "common_mistakes": ["常见错误1", "常见错误2"]
        }}
      ]
    }}
  ]
}}"""
    user = f"""JD：{job_description}
类型：{interview_type}
难度：{difficulty}
语言：{'中文' if language == 'zh' else 'English'}

请生成完整模拟面试。"""

    result = await _chat(system, user, api_key)
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {"raw_interview": result}


async def interview_feedback_report(
    all_qa: list,  # [{"question": str, "answer": str}, ...]
    language: str = "zh",
    api_key: str = "",
) -> dict:
    """Generate a comprehensive interview feedback report from multiple Q&A pairs."""
    lang_hint = "用中文写报告" if language == "zh" else "Write report in English"
    qa_text = "\n\n".join(
        f"Q{i+1}: {qa['question']}\nA{i+1}: {qa['answer']}"
        for i, qa in enumerate(all_qa)
    )

    system = f"""你是资深面试官，现在出具一份完整的面试评估报告。{lang_hint}。

输出JSON：
{{
  "overall_rating": "通过/待定/不通过",
  "overall_score": 0,
  "summary": "3句话总结面试表现",
  "strength_areas": ["优势领域1", "优势领域2"],
  "weakness_areas": ["薄弱领域1", "薄弱领域2"],
  "hiring_recommendation": "是否建议录用及理由",
  "level_assessment": "候选人级别评估（初级/中级/高级/专家）",
  "salary_suggestion": "建议薪资范围（基于表现）",
  "development_plan": ["入职后3个月培养建议1", "建议2"],
  "per_question_feedback": [
    {{"question_index": 1, "score": 0, "one_line": "一句话点评"}}
  ]
}}"""
    user = f"面试记录：\n{qa_text}\n\n请写完整评估报告。"

    result = await _chat(system, user, api_key)
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {"raw_report": result}
