<div align="center">
  <img src="logo.png" alt="HireReady AI Logo" width="120" />
  
  # HireReady AI
  
  **Upload your resume, paste a job description, and find out exactly where you stand — no fluff, no guesswork.**
  
  [https://hireready-ai.streamlit.app](https://hireready-ai.streamlit.app)

</div>

---

I built this because I was tired of applying to roles blind. Now I can see my skill gaps, practice with AI-generated interview questions, and actually fix my resume bullets before hitting submit.

## ✨ Features

- **Resume Analysis** — Drop your PDF and a job description. Get a match score out of 100, see which skills you have vs. what's missing, and get a hire/no-hire recommendation with reasoning.
- **Bullet Rewriter** — Picks out the bullet points from your resume and rewrites them using STAR format, tailored to the JD you're targeting.
- **Interview Predictor** — Generates 10 questions you're likely to be asked based on your resume gaps and the role requirements. Each comes with a suggested answer framework.
- **Mock Interview** — 8-question simulated interview with real-time scoring. You answer, the AI evaluates each response, tells you what worked and what didn't, and gives you a final grade + report you can download.
- **Batch Screener** — Upload multiple resumes against one JD. Ranks candidates by match score. Export results as CSV.

---

## 🚀 Run locally

You'll need Python 3.11+ and a [Groq API key](https://console.groq.com) (free tier works fine).

```bash
git clone https://github.com/drikshathakur786/hireready-ai.git
cd hireready-ai
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > .env
streamlit run app.py
```

Opens at `localhost:8501`.

---

## 🛠️ How it's built

The frontend is a single Streamlit app (`app.py`) with custom CSS — dark glassmorphic UI, Plus Jakarta Sans / Inter typography, animated aurora background. No React, no Tailwind, just raw HTML/CSS injected via `st.markdown`.

The AI layer runs on **Groq's LLaMA 3.3-70B** for speed. Each feature has its own prompt builder in `prompts/` and feature module in `features/`. PDF parsing is handled by pdfplumber.

### Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python |
| **UI** | Streamlit |
| **LLM** | Groq · LLaMA 3.3-70B |
| **PDF** | pdfplumber |
| **Data** | pandas |

### Project Structure

```text
app.py                  ← UI + routing
core/
  ai_client.py          ← Groq API wrapper
  pdf_parser.py         ← PDF text extraction
  validators.py         ← Response parsing + validation
features/
  resume_analyzer.py    ← Match scoring + skill gap
  bullet_rewriter.py    ← STAR format rewriting
  interview_predictor.py ← Question generation
  interview_simulator.py ← Mock interview + evaluation
  batch_screener.py     ← Multi-resume screening
prompts/                ← Prompt templates for each feature
utils/formatters.py     ← Display helpers
```

---

<div align="center">
  MIT License — <a href="https://github.com/drikshathakur786">Driksha Thakur</a>
</div>