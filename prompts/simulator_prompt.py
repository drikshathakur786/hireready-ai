def build_question_generation_prompt(role, experience_level):
    prompt = f"""You are a senior technical interviewer at a top tech company.

You are about to conduct a mock interview for a {experience_level} candidate 
applying for a {role} position.

Generate exactly 8 interview questions for this mock interview.

Question mix required:
- 4 Technical questions (core skills for {role})
- 2 Behavioural questions (teamwork, problem solving, conflict)
- 2 Role-specific questions (day to day responsibilities of {role})

Difficulty mix:
- 2 Easy questions (confidence builders)
- 4 Medium questions (core assessment)
- 2 Hard questions (differentiation)

INSTRUCTIONS:
- Questions must feel like a real interview, not a quiz
- Return ONLY valid JSON. No extra text. No markdown. No backticks.
- Your entire response must start with {{ and end with }}

Return exactly this JSON structure:
{{
    "questions": [
        {{
            "id": 1,
            "question": "<the interview question>",
            "category": "<exactly one of: Technical, Behavioural, Role-specific>",
            "difficulty": "<exactly one of: Easy, Medium, Hard>",
            "what_interviewer_wants": "<what a strong answer should demonstrate>"
        }}
    ]
}}"""
    return prompt


def build_evaluation_prompt(question, user_answer, role):
    prompt = f"""You are a senior technical interviewer evaluating a candidate's 
answer during a mock interview for a {role} position.

INTERVIEW QUESTION:
{question}

CANDIDATE'S ANSWER:
{user_answer}

Evaluate this answer honestly and constructively.

INSTRUCTIONS:
- Score out of 10. Be realistic — a perfect answer is rare.
- 1-3: Poor. Missing the point entirely.
- 4-5: Below average. Some relevant points but major gaps.
- 6-7: Average. Decent answer but room for improvement.
- 8-9: Strong. Clear, structured, with good examples.
- 10: Exceptional. Rarely given.
- Return ONLY valid JSON. No extra text. No markdown. No backticks.
- Your entire response must start with {{ and end with }}

Return exactly this JSON structure:
{{
    "score": <number from 1 to 10>,
    "score_reason": "<one sentence explaining the score>",
    "what_was_good": "<what the candidate did well>",
    "what_was_missing": "<what was lacking or could be improved>",
    "improved_answer": "<how a top candidate would answer this question>",
    "keywords_missed": ["<keyword1>", "<keyword2>"]
}}"""
    return prompt


def build_report_prompt(questions, answers, evaluations, role):
    # Build a summary of the full interview to send to AI
    interview_summary = ""
    for i, (q, a, e) in enumerate(zip(questions, answers, evaluations), 1):
        interview_summary += f"""
Question {i} [{q.get('category', '')}]: {q.get('question', '')}
Candidate Answer: {a}
Score: {e.get('score', 0)}/10
Feedback: {e.get('score_reason', '')}
"""

    prompt = f"""You are a senior hiring manager writing a performance report 
after a mock interview for a {role} position.

Here is the complete interview transcript:
{interview_summary}

Write a comprehensive but honest performance report for this candidate.

INSTRUCTIONS:
- Be constructive and encouraging but realistic
- Base everything on the actual answers given above
- Return ONLY valid JSON. No extra text. No markdown. No backticks.
- Your entire response must start with {{ and end with }}

Return exactly this JSON structure:
{{
    "overall_score": <average score out of 100>,
    "grade": "<exactly one of: A, B, C, D, F>",
    "hire_verdict": "<one sentence on hiring likelihood>",
    "technical_score": <score out of 100 for technical questions>,
    "behavioural_score": <score out of 100 for behavioural questions>,
    "top_3_strengths": ["<strength1>", "<strength2>", "<strength3>"],
    "top_3_improvements": ["<improvement1>", "<improvement2>", "<improvement3>"],
    "question_breakdown": [
        {{
            "question_id": 1,
            "score": <score>,
            "one_line_feedback": "<brief feedback>"
        }}
    ],
    "recommended_next_steps": ["<step1>", "<step2>", "<step3>"]
}}"""
    return prompt