import json
from core.ai_client import call_claude
from prompts.simulator_prompt import (
    build_question_generation_prompt,
    build_evaluation_prompt,
    build_report_prompt
)


def clean_json_response(raw_response):
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        if start != -1 and end != 0:
            cleaned = cleaned[start:end]
    return cleaned


def generate_questions(role, experience_level):
    # Build prompt and call AI
    prompt = build_question_generation_prompt(role, experience_level)
    raw_response = call_claude(prompt, max_tokens=2000)

    if raw_response is None:
        print("ERROR: AI call failed in generate_questions")
        return None

    cleaned = clean_json_response(raw_response)

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"ERROR: Could not parse JSON in generate_questions: {e}")
        return None

    if "questions" not in result:
        print("ERROR: 'questions' key missing from response")
        return None

    return result["questions"]


def evaluate_answer(question, user_answer, role):
    # If user left answer blank, give a default low score
    if not user_answer or not user_answer.strip():
        return {
            "score": 1,
            "score_reason": "No answer was provided",
            "what_was_good": "N/A",
            "what_was_missing": "A complete answer addressing the question",
            "improved_answer": "Please attempt to answer even if unsure",
            "keywords_missed": []
        }

    prompt = build_evaluation_prompt(question, user_answer, role)
    raw_response = call_claude(prompt, max_tokens=1000)

    if raw_response is None:
        print("ERROR: AI call failed in evaluate_answer")
        return None

    cleaned = clean_json_response(raw_response)

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"ERROR: Could not parse JSON in evaluate_answer: {e}")
        return None

    # Make sure score is a valid number between 1-10
    try:
        result["score"] = int(result["score"])
        result["score"] = max(1, min(10, result["score"]))
    except (ValueError, TypeError):
        result["score"] = 5

    return result


def generate_report(questions, answers, evaluations, role):
    prompt = build_report_prompt(questions, answers, evaluations, role)
    raw_response = call_claude(prompt, max_tokens=2000)

    if raw_response is None:
        print("ERROR: AI call failed in generate_report")
        return None

    cleaned = clean_json_response(raw_response)

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"ERROR: Could not parse JSON in generate_report: {e}")
        return None

    # Validate overall_score is in range
    try:
        result["overall_score"] = int(result["overall_score"])
        result["overall_score"] = max(0, min(100, result["overall_score"]))
    except (ValueError, TypeError):
        result["overall_score"] = 50

    return result


if __name__ == "__main__":
    print("Testing interview simulator...\n")

    # Test 1: Generate questions
    print("--- Test 1: Generating questions ---")
    questions = generate_questions("Full Stack Developer", "Fresher")

    if questions:
        print(f"SUCCESS! Generated {len(questions)} questions:")
        for q in questions:
            print(f"  Q{q['id']} [{q['difficulty']}][{q['category']}]: {q['question']}")
    else:
        print("FAILED — could not generate questions")

    print("\n--- Test 2: Evaluating a sample answer ---")
    if questions:
        test_question = questions[0]["question"]
        test_answer = "I would use React hooks like useState and useEffect to manage state and side effects. For the backend I would build REST APIs with Node.js and Express."

        evaluation = evaluate_answer(test_question, test_answer, "Full Stack Developer")

        if evaluation:
            print(f"SUCCESS! Score: {evaluation['score']}/10")
            print(f"Feedback: {evaluation['score_reason']}")
        else:
            print("FAILED — could not evaluate answer")

    print("\n--- Test 3: Generating final report ---")
    if questions and evaluation:
        # Use the same answer and evaluation for all questions as a test
        test_answers = [test_answer] * len(questions)
        test_evaluations = [evaluation] * len(questions)

        report = generate_report(questions, test_answers, test_evaluations, "Full Stack Developer")

        if report:
            print(f"SUCCESS! Overall score: {report['overall_score']}/100")
            print(f"Grade: {report['grade']}")
            print(f"Verdict: {report['hire_verdict']}")
        else:
            print("FAILED — could not generate report")