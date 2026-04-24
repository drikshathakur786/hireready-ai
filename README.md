# HireReady AI — Job Readiness Platform

> Upload your resume. Paste a JD. Know exactly where you stand.

[![Live App](https://img.shields.io/badge/Live%20App-%20hireready--ai-00C853?style=for-the-badge)](https://hireready-ai.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3-F55036?style=for-the-badge)](https://console.groq.com)
[![License](https://img.shields.io/badge/License-MIT-22223B?style=for-the-badge)](https://github.com/drikshathakur786/hireready-ai/blob/main/LICENSE)

---

## What it does

| # | Feature | Description |
|---|---|---|
| 01 | 📄 Resume Analysis | Match score, skills gap analysis, and hiring recommendation |
| 02 | ✏️ Bullet Rewriter | Rewrites weak resume bullets into STAR format |
| 03 | 🎯 Interview Predictor | 10 tailored questions based on your resume + JD |
| 04 | 🎤 Mock Interview | 8-round AI interview with per-round scoring and full report |
| 05 | 📊 Batch Screener | Screen multiple resumes against one JD, export as CSV |

---

## Getting Started

### Prerequisites
- Python 3.11+
- A free Groq API key → [console.groq.com](https://console.groq.com)

### Installation

```bash
git clone https://github.com/drikshathakur786/hireready-ai.git
cd hireready-ai
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > .env
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| UI | Streamlit |
| AI Engine | Groq · LLaMA 3.3-70B |
| PDF Parsing | pdfplumber |
| Data Handling | pandas |

---

## Project Structure

```
hireready-ai/
├── app.py                  # Streamlit frontend
├── core/                   # AI client, PDF parser, validators
├── features/               # Analyzer, rewriter, predictor, simulator
├── prompts/                # AI prompt builders
└── utils/                  # Display formatters
```

---

## License

[MIT](https://github.com/drikshathakur786/hireready-ai/blob/main/LICENSE) © 2026 Driksha Thakur