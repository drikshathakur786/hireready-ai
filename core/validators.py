def validate_resume_text(resume_text):
    # Check resume text is not None or empty
    if not resume_text:
        return False, "No resume text found. Please upload a valid PDF."

    # Check it has enough content to be a real resume
    # A real resume should have at least 100 characters
    if len(resume_text.strip()) < 100:
        return False, "Resume text is too short. The PDF may be a scanned image or empty."

    # Check it looks like a resume — has at least some common resume words
    resume_keywords = [
        "experience", "education", "skills", "project",
        "work", "university", "college", "internship",
        "developer", "engineer", "student", "bachelor"
    ]
    text_lower = resume_text.lower()
    matches = sum(1 for word in resume_keywords if word in text_lower)

    if matches < 2:
        return False, "This doesn't look like a resume. Please upload your resume PDF."

    return True, "Resume is valid."


def validate_jd_text(jd_text):
    # Check JD is not empty
    if not jd_text or not jd_text.strip():
        return False, "Job description is empty. Please paste a job description."

    # Check it has enough content
    if len(jd_text.strip()) < 50:
        return False, "Job description is too short. Please paste the full job description."

    return True, "Job description is valid."


def validate_inputs(resume_text, jd_text):
    # Validate both inputs together
    # Returns (is_valid, error_message)
    resume_valid, resume_msg = validate_resume_text(resume_text)
    if not resume_valid:
        return False, resume_msg

    jd_valid, jd_msg = validate_jd_text(jd_text)
    if not jd_valid:
        return False, jd_msg

    return True, "All inputs valid."


if __name__ == "__main__":
    # Test with fake data
    fake_resume = """
    Priya Mehta — Software Developer
    Education: BE Computer Science, Pune University
    Skills: Python, React, Node.js
    Experience: Frontend Intern at TechStartup
    Projects: Built a web application using React
    """

    fake_jd = "Looking for a Full Stack Developer with React and Node.js experience."

    print("Testing validators...")

    is_valid, msg = validate_inputs(fake_resume, fake_jd)
    print(f"Result: {is_valid} — {msg}")

    # Test with empty inputs
    is_valid2, msg2 = validate_inputs("", "")
    print(f"Empty test: {is_valid2} — {msg2}")

    # Test with too short resume
    is_valid3, msg3 = validate_inputs("hi", fake_jd)
    print(f"Short resume test: {is_valid3} — {msg3}")