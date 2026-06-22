import streamlit as st
from core.pdf_parser import extract_text_from_pdf

st.set_page_config(
    page_title="HireReady AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── GLOBAL STYLES ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── ROOT & TOKENS ── */
:root {
    --bg-base: #06080D;
    --bg-surface: rgba(12, 16, 24, 0.7);
    --glass: rgba(255,255,255,0.025);
    --glass-border: rgba(255,255,255,0.06);
    --glass-hover: rgba(255,255,255,0.045);
    --accent-cyan: #22D3EE;
    --accent-violet: #A78BFA;
    --accent-emerald: #34D399;
    --accent-rose: #FB7185;
    --accent-amber: #FBBF24;
    --accent-blue: #60A5FA;
    --text-primary: #F1F5F9;
    --text-secondary: #94A3B8;
    --text-tertiary: #475569;
    --text-muted: #334155;
    --radius-lg: 20px;
    --radius-md: 14px;
    --radius-sm: 10px;
    --radius-pill: 100px;
    --shadow-glow: 0 0 80px -20px;
    --transition-smooth: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

/* ── BACKGROUND ── */
.stApp {
    background: var(--bg-base) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    overflow-x: hidden;
}

/* Animated aurora mesh */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 10% 20%, rgba(34,211,238,0.08) 0%, transparent 50%),
        radial-gradient(ellipse 60% 60% at 80% 10%, rgba(167,139,250,0.07) 0%, transparent 50%),
        radial-gradient(ellipse 50% 70% at 60% 90%, rgba(52,211,153,0.05) 0%, transparent 50%),
        radial-gradient(ellipse 40% 40% at 30% 70%, rgba(96,165,250,0.04) 0%, transparent 50%);
    animation: auroraPulse 12s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

@keyframes auroraPulse {
    0% {
        filter: blur(0px);
        opacity: 1;
    }
    50% {
        filter: blur(20px);
        opacity: 0.8;
    }
    100% {
        filter: blur(0px);
        opacity: 1;
    }
}

/* Floating accent orb */
.stApp::after {
    content: '';
    position: fixed;
    top: 50%;
    left: 50%;
    width: 600px;
    height: 600px;
    background: conic-gradient(
        from 0deg,
        rgba(34,211,238,0.06),
        rgba(167,139,250,0.06),
        rgba(52,211,153,0.04),
        rgba(34,211,238,0.06)
    );
    border-radius: 50%;
    transform: translate(-50%, -50%);
    animation: orbRotate 25s linear infinite;
    pointer-events: none;
    z-index: 0;
    filter: blur(100px);
}

@keyframes orbRotate {
    0% { transform: translate(-50%, -50%) rotate(0deg) scale(1); }
    50% { transform: translate(-50%, -50%) rotate(180deg) scale(1.15); }
    100% { transform: translate(-50%, -50%) rotate(360deg) scale(1); }
}

/* ── FADE-IN ANIMATION CLASSES ── */
@keyframes fadeInUp {
    0% { opacity: 0; transform: translateY(16px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    0% { opacity: 0; }
    100% { opacity: 1; }
}

@keyframes slideInLeft {
    0% { opacity: 0; transform: translateX(-12px); }
    100% { opacity: 1; transform: translateX(0); }
}

@keyframes scaleIn {
    0% { opacity: 0; transform: scale(0.92); }
    100% { opacity: 1; transform: scale(1); }
}

@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.fade-in-up {
    animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.fade-in-up-delayed {
    animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.15s both;
}

.fade-in-up-delayed-2 {
    animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.3s both;
}

.scale-in {
    animation: scaleIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: rgba(8, 10, 16, 0.85) !important;
    border-right: 1px solid rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(40px) saturate(150%) !important;
    -webkit-backdrop-filter: blur(40px) saturate(150%) !important;
}

[data-testid="stSidebar"] > div {
    padding: 2rem 1.5rem !important;
}

/* ── TYPOGRAPHY ── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.025em !important;
    font-weight: 700 !important;
}

p, span, div, label {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-secondary) !important;
}

/* ── GLASS CARD ── */
.glass-card {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    padding: 1.75rem;
    backdrop-filter: blur(20px) saturate(130%);
    -webkit-backdrop-filter: blur(20px) saturate(130%);
    transition: var(--transition-smooth);
    position: relative;
    overflow: hidden;
}

/* Subtle top-edge highlight */
.glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 20%;
    right: 20%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
    pointer-events: none;
}

.glass-card:hover {
    background: var(--glass-hover);
    transform: translateY(-3px);
    box-shadow: 0 20px 50px -15px rgba(0,0,0,0.4);
}

/* ── LOGO ── */
.logo-container {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 2.5rem;
    animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.logo-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    overflow: hidden;
    flex-shrink: 0;
}

.logo-icon img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.logo-text {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.6rem !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.03em !important;
}

.logo-sub {
    font-size: 0.78rem !important;
    color: var(--text-tertiary) !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* ── SECTION LABEL ── */
.section-label {
    font-size: 0.78rem;
    color: var(--text-tertiary);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    margin-bottom: 0.6rem;
}

/* ── METRIC CARDS ── */
.metric-card {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: var(--transition-smooth);
    backdrop-filter: blur(16px);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 20%;
    right: 20%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
}

.metric-card:hover {
    transform: translateY(-4px);
    background: var(--glass-hover);
    box-shadow: 0 16px 40px -12px rgba(0,0,0,0.3);
}

.metric-number {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--text-primary), var(--text-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}

.metric-label {
    font-size: 0.78rem;
    color: var(--text-tertiary);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 8px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
}

/* ── SKILL PILLS ── */
.skill-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 5px 14px;
    border-radius: var(--radius-pill);
    font-size: 0.88rem;
    font-weight: 500;
    margin: 3px;
    letter-spacing: 0.01em;
    font-family: 'Inter', sans-serif;
    transition: var(--transition-smooth);
}

.skill-pill:hover {
    transform: translateY(-1px);
}

.skill-have {
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.2);
    color: var(--accent-emerald);
}

.skill-have::before {
    content: '✓';
    font-size:1.18rem;
}

.skill-missing {
    background: rgba(251,113,133,0.08);
    border: 1px solid rgba(251,113,133,0.2);
    color: var(--accent-rose);
}

.skill-missing::before {
    content: '○';
    font-size: 0.88rem;
}

/* ── STATUS DOT ── */
.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
}

.status-dot.active {
    background: var(--accent-emerald);
    box-shadow: 0 0 8px rgba(52,211,153,0.5);
    animation: pulse 2s ease-in-out infinite;
}

.status-dot.inactive {
    background: var(--text-muted);
}

/* ── BUTTONS ── */
.stButton > button {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    border-radius: var(--radius-md) !important;
    padding: 0.65rem 1.5rem !important;
    transition: var(--transition-smooth) !important;
    backdrop-filter: blur(8px) !important;
    position: relative;
    overflow: hidden;
}

.stButton > button:hover {
    background: rgba(255,255,255,0.06) !important;
    border-color: rgba(255,255,255,0.15) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.2) !important;
}

/* Primary button — multiple selectors to catch all Streamlit variants */
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"],
.stButton > button.st-emotion-cache-primary,
[data-testid="stBaseButton-primary"],
button[kind="primaryFormSubmit"],
button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet)) !important;
    border: none !important;
    color: #FFFFFF !important;
    box-shadow: 0 8px 24px rgba(34,211,238,0.2) !important;
    font-weight: 700 !important;
}

/* Force white on ALL text inside primary buttons */
.stButton > button[kind="primary"] p,
.stButton > button[kind="primary"] span,
.stButton > button[kind="primary"] div,
[data-testid="stBaseButton-primary"] p,
[data-testid="stBaseButton-primary"] span,
[data-testid="stBaseButton-primary"] div,
button[kind="primary"] p,
button[kind="primary"] span {
    color: #FFFFFF !important;
}

.stButton > button[kind="primary"]:hover,
[data-testid="stBaseButton-primary"]:hover,
button[kind="primary"]:hover {
    box-shadow: 0 12px 32px rgba(34,211,238,0.35) !important;
    transform: translateY(-2px) !important;
    filter: brightness(1.08);
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.015) !important;
    border: 1px dashed rgba(255,255,255,0.1) !important;
    border-radius: var(--radius-md) !important;
    padding: 1.2rem !important;
    transition: var(--transition-smooth) !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--accent-cyan) !important;
    background: rgba(34,211,238,0.02) !important;
    box-shadow: 0 0 40px rgba(34,211,238,0.05) !important;
}

/* ── TEXT AREA ── */
.stTextArea textarea {
    background: rgba(0,0,0,0.3) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 1rem !important;
    transition: var(--transition-smooth) !important;
}

.stTextArea textarea:focus {
    border-color: rgba(34,211,238,0.4) !important;
    box-shadow: 0 0 0 3px rgba(34,211,238,0.08) !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,0,0,0.25) !important;
    border-radius: 16px !important;
    padding: 5px !important;
    border: 1px solid rgba(255,255,255,0.04) !important;
    gap: 4px !important;
    backdrop-filter: blur(12px) !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-tertiary) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    letter-spacing: 0.01em !important;
    transition: var(--transition-smooth) !important;
    padding: 0.55rem 1.2rem !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-secondary) !important;
    background: rgba(255,255,255,0.03) !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(255,255,255,0.08) !important;
    color: var(--text-primary) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
}

.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* ── SELECTBOX ── */
.stSelectbox > div > div {
    background: rgba(0,0,0,0.3) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    transition: var(--transition-smooth) !important;
}

.streamlit-expanderHeader:hover {
    background: rgba(255,255,255,0.04) !important;
    border-color: rgba(255,255,255,0.1) !important;
}

.streamlit-expanderContent {
    background: rgba(0,0,0,0.15) !important;
    border: 1px solid rgba(255,255,255,0.04) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
}

/* ── ALERTS ── */
.stSuccess {
    background: rgba(52,211,153,0.04) !important;
    border: 1px solid rgba(52,211,153,0.15) !important;
    border-left: 3px solid var(--accent-emerald) !important;
    border-radius: var(--radius-sm) !important;
}

.stWarning {
    background: rgba(251,191,36,0.04) !important;
    border: 1px solid rgba(251,191,36,0.15) !important;
    border-left: 3px solid var(--accent-amber) !important;
    border-radius: var(--radius-sm) !important;
}

.stInfo {
    background: rgba(34,211,238,0.04) !important;
    border: 1px solid rgba(34,211,238,0.15) !important;
    border-left: 3px solid var(--accent-cyan) !important;
    border-radius: var(--radius-sm) !important;
}

.stError {
    background: rgba(251,113,133,0.04) !important;
    border: 1px solid rgba(251,113,133,0.15) !important;
    border-left: 3px solid var(--accent-rose) !important;
    border-radius: var(--radius-sm) !important;
}

/* ── PROGRESS BAR ── */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-violet)) !important;
    border-radius: var(--radius-pill) !important;
}

.stProgress > div {
    background: rgba(255,255,255,0.04) !important;
    border-radius: var(--radius-pill) !important;
    overflow: hidden;
}

/* ── DIVIDER ── */
hr {
    border-color: rgba(255,255,255,0.04) !important;
    margin: 2rem 0 !important;
}

/* ── SPINNER ── */
.stSpinner > div {
    border-top-color: var(--accent-cyan) !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-lg) !important;
    overflow: hidden !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: var(--radius-pill); }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.15); }

/* ── HIDE STREAMLIT DEFAULTS ── */
#MainMenu { visibility: hidden; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }
[data-testid="stLogoSpacer"] { display: none !important; }
div[class*="stLogoSpacer"] { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
section[data-testid="stSidebar"] {
    min-width: 340px !important;
    width: 340px !important;
    transform: none !important;
    left: 0 !important;
    visibility: visible !important;
    display: block !important;
}
section[data-testid="stSidebar"] > div {
    width: 340px !important;
}
.stActionButton { display: none !important; }
.st-emotion-cache-ujm5ma { display: none !important; }
.st-emotion-cache-pkm19r { display: none !important; }
span[data-testid="stIconMaterial"] { display: none !important; }
button[data-testid="baseButton-headerNoPadding"] { display: none !important; }
iframe[title="keyboard_shortcut"] { display: none !important; }
div[class*="keyboard"] { display: none !important; }
button[aria-label*="keyboard"] { display: none !important; }
button[aria-label*="shortcuts"] { display: none !important; }
.st-emotion-cache-czk5ss { display: none !important; }
.st-emotion-cache-1dp5vir { display: none !important; }
footer { visibility: hidden; }
header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)
# Kill the keyboard shortcut floating element
st.components.v1.html("""
<script>
function removeKeyboardOverlay() {
    const allElements = document.querySelectorAll('*');
    allElements.forEach(el => {
        if (el.children.length === 0 &&
            el.textContent.trim().toLowerCase().includes('keyboard')) {
            el.style.display = 'none';
        }
    });
    const spacers = document.querySelectorAll('[data-testid="stLogoSpacer"]');
    spacers.forEach(el => el.style.display = 'none');
    const headers = document.querySelectorAll('header');
    headers.forEach(el => el.style.display = 'none');
}
removeKeyboardOverlay();
setTimeout(removeKeyboardOverlay, 500);
setTimeout(removeKeyboardOverlay, 1500);
setTimeout(removeKeyboardOverlay, 3000);
</script>
""", height=0)

# ── SESSION STATE ─────────────────────────────────────────────────
defaults = {
    "resume_text": None,
    "jd_text": "",
    "analysis_result": None,
    "questions": None,
    "bullet_rewrites": {},
    "extracted_bullets": [],
    "simulator_stage": "setup",
    "simulator_role": None,
    "simulator_questions": [],
    "simulator_current_index": 0,
    "simulator_answers": [],
    "simulator_evaluations": [],
    "simulator_report": None,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    import base64, os
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        logo_src = f"data:image/png;base64,{logo_b64}"
    else:
        logo_src = ""

    st.markdown(f"""
    <div class='logo-container'>
        <div class='logo-icon'><img src='{logo_src}' alt='HireReady AI'/></div>
        <div>
            <div class='logo-text'>HireReady AI</div>
            <div class='logo-sub'>Career Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Resume</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        extracted = extract_text_from_pdf(uploaded_file)
        if extracted:
            st.session_state.resume_text = extracted
            st.markdown("""
            <div style='display:flex;align-items:center;gap:8px;padding:8px 14px;
            background:rgba(52,211,153,0.06);border:1px solid rgba(52,211,153,0.15);
            border-radius:10px;margin-top:8px;animation:fadeInUp 0.4s ease both;'>
                <span class='status-dot active'></span>
                <span style='color:#34d399;font-size:0.82rem;font-weight:500;'>Resume parsed successfully</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Could not read PDF.")

    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Job Description</div>", unsafe_allow_html=True)

    st.session_state.jd_text = st.text_area(
        "JD",
        value=st.session_state.jd_text,
        height=170,
        placeholder="Paste job description here...",
        label_visibility="collapsed"
    )

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    analyse_button = st.button("Analyse Now", use_container_width=True, type="primary")

    # Status indicators
    st.markdown("<div style='margin-top:2.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Status</div>", unsafe_allow_html=True)

    resume_ready = st.session_state.resume_text is not None
    jd_ready = bool(st.session_state.jd_text.strip())
    analysis_ready = st.session_state.analysis_result is not None

    r_dot = "background:#34d399;box-shadow:0 0 8px rgba(52,211,153,0.5);" if resume_ready else "background:#334155;"
    r_text = "Loaded" if resume_ready else "Waiting"
    r_color = "#34d399" if resume_ready else "#334155"

    j_dot = "background:#34d399;box-shadow:0 0 8px rgba(52,211,153,0.5);" if jd_ready else "background:#334155;"
    j_text = "Ready" if jd_ready else "Waiting"
    j_color = "#34d399" if jd_ready else "#334155"

    a_dot = "background:#34d399;box-shadow:0 0 8px rgba(52,211,153,0.5);" if analysis_ready else "background:#334155;"
    a_text = "Complete" if analysis_ready else "Pending"
    a_color = "#34d399" if analysis_ready else "#334155"

    st.markdown(f"""
    <div style='display:flex;flex-direction:column;gap:2px;'>
        <div style='display:flex;justify-content:space-between;align-items:center;padding:6px 0;'>
            <span style='font-size:0.82rem;color:#475569;font-weight:500;'>Resume</span>
            <div style='display:flex;align-items:center;gap:6px;'>
                <span style='width:6px;height:6px;border-radius:50%;display:inline-block;{r_dot}'></span>
                <span style='font-size:0.78rem;color:{r_color};font-weight:500;font-family:JetBrains Mono,monospace;'>{r_text}</span>
            </div>
        </div>
        <div style='display:flex;justify-content:space-between;align-items:center;padding:6px 0;'>
            <span style='font-size:0.82rem;color:#475569;font-weight:500;'>Job Description</span>
            <div style='display:flex;align-items:center;gap:6px;'>
                <span style='width:6px;height:6px;border-radius:50%;display:inline-block;{j_dot}'></span>
                <span style='font-size:0.78rem;color:{j_color};font-weight:500;font-family:JetBrains Mono,monospace;'>{j_text}</span>
            </div>
        </div>
        <div style='display:flex;justify-content:space-between;align-items:center;padding:6px 0;'>
            <span style='font-size:0.82rem;color:#475569;font-weight:500;'>Analysis</span>
            <div style='display:flex;align-items:center;gap:6px;'>
                <span style='width:6px;height:6px;border-radius:50%;display:inline-block;{a_dot}'></span>
                <span style='font-size:0.78rem;color:{a_color};font-weight:500;font-family:JetBrains Mono,monospace;'>{a_text}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── MAIN TABS ─────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "  Analysis  ",
    "  Predictor  ",
    "  Batch  ",
    "  Interview  "
])

# ══════════════════════════════════════════════════════════════════
# TAB 1 — RESUME ANALYSIS
# ══════════════════════════════════════════════════════════════════
with tab1:
    if analyse_button:
        if not st.session_state.resume_text:
            st.error("Upload your resume PDF first.")
        elif not st.session_state.jd_text.strip():
            st.error("Paste a job description first.")
        else:
            from features.resume_analyzer import analyse_resume
            from features.bullet_rewriter import extract_bullets

            with st.spinner("Running AI analysis..."):
                result = analyse_resume(st.session_state.resume_text, st.session_state.jd_text)

            if result:
                st.session_state.analysis_result = result
                st.session_state.extracted_bullets = extract_bullets(st.session_state.resume_text)
            else:
                st.error("Analysis failed. Try again.")

    if st.session_state.analysis_result:
        from utils.formatters import display_skills, display_bullet_rewrite
        from features.bullet_rewriter import rewrite_bullet

        r = st.session_state.analysis_result
        score = r["match_score"]

        # Determine glow color based on score
        if score >= 70:
            glow_color = "rgba(52,211,153,0.35)"
            score_color = "#34d399"
            ring_gradient = "linear-gradient(135deg, #34d399, #22d3ee)"
        elif score >= 50:
            glow_color = "rgba(251,191,36,0.35)"
            score_color = "#fbbf24"
            ring_gradient = "linear-gradient(135deg, #fbbf24, #fb923c)"
        else:
            glow_color = "rgba(251,113,133,0.35)"
            score_color = "#fb7185"
            ring_gradient = "linear-gradient(135deg, #fb7185, #f43f5e)"

        # Hero score section with animated entrance
        st.markdown(f"""
        <div class='fade-in-up' style='text-align:center;padding:3rem 1rem 2rem;'>
            <div style='font-size:1.18rem;color:var(--text-tertiary);text-transform:uppercase;
            letter-spacing:0.2em;margin-bottom:1.2rem;font-weight:600;'>Match Score</div>
            <div style='position:relative;display:inline-block;'>
                <div style='font-size:7rem;font-weight:800;font-family:"Plus Jakarta Sans",sans-serif;
                background:{ring_gradient};
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                background-clip:text;line-height:1;
                filter:drop-shadow(0 0 40px {glow_color});
                letter-spacing:-0.04em;'>{score}</div>
            </div>
            <div style='font-size:1.47rem;color:var(--text-muted);margin-top:0.5rem;font-weight:500;'>out of 100</div>
        </div>
        """, unsafe_allow_html=True)

        # Recommendation badge
        rec = r["hiring_recommendation"]
        rec_colors = {
            "Strong Yes": ("#34d399", "rgba(52,211,153,0.08)", "rgba(52,211,153,0.2)"),
            "Yes": ("#34d399", "rgba(52,211,153,0.06)", "rgba(52,211,153,0.15)"),
            "Maybe": ("#fbbf24", "rgba(251,191,36,0.06)", "rgba(251,191,36,0.15)"),
            "No": ("#fb7185", "rgba(251,113,133,0.06)", "rgba(251,113,133,0.15)")
        }
        rc, rbg, rborder = rec_colors.get(rec, ("#fff", "rgba(255,255,255,0.03)", "rgba(255,255,255,0.08)"))

        st.markdown(f"""
        <div class='fade-in-up-delayed' style='text-align:center;margin-bottom:2.5rem;'>
            <span style='background:{rbg};border:1px solid {rborder};color:{rc};
            padding:7px 22px;border-radius:var(--radius-pill);font-size:1.41rem;font-weight:700;
            letter-spacing:0.04em;font-family:"Plus Jakarta Sans",sans-serif;
            display:inline-block;'>{rec}</span>
            <div style='color:var(--text-tertiary);font-size:1.47rem;margin-top:1rem;
            max-width:500px;margin-left:auto;margin-right:auto;line-height:1.6;'>{r["recommendation_reason"]}</div>
        </div>
        """, unsafe_allow_html=True)

        # Three metric cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class='metric-card fade-in-up-delayed'>
                <div class='metric-number'>{score}</div>
                <div class='metric-label'>Match Score</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='metric-card fade-in-up-delayed'>
                <div class='metric-number' style='font-size:2.74rem;'>{r["experience_match"]}</div>
                <div class='metric-label'>Experience</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class='metric-card fade-in-up-delayed-2'>
                <div class='metric-number' style='font-size:2.74rem;'>{r["education_match"]}</div>
                <div class='metric-label'>Education</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin:2.5rem 0;'></div>", unsafe_allow_html=True)

        # Skills section
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class='glass-card fade-in-up-delayed'>
                <div class='section-label' style='margin-bottom:1rem;'>Skills You Have</div>
            """, unsafe_allow_html=True)
            if r["matched_skills"]:
                pills = "".join([f"<span class='skill-pill skill-have'>{s}</span>" for s in r["matched_skills"]])
                st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:2px;'>{pills}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:var(--text-muted);font-size:1.47rem;'>None found</p></div>", unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class='glass-card fade-in-up-delayed-2'>
                <div class='section-label' style='margin-bottom:1rem;'>Skills to Learn</div>
            """, unsafe_allow_html=True)
            if r["missing_skills"]:
                pills = "".join([f"<span class='skill-pill skill-missing'>{s}</span>" for s in r["missing_skills"]])
                st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:2px;'>{pills}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:var(--text-muted);font-size:1.47rem;'>None missing</p></div>", unsafe_allow_html=True)

        # Feedback
        st.markdown("<div style='margin:1.5rem 0;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='glass-card fade-in-up-delayed-2'>
            <div class='section-label' style='margin-bottom:0.8rem;'>AI Feedback</div>
            <p style='color:var(--text-secondary);font-size:1.61rem;line-height:1.8;margin:0;'>{r["overall_feedback"]}</p>
        </div>
        """, unsafe_allow_html=True)

        # Bullet rewriter
        st.markdown("<div style='margin:2.5rem 0 1rem;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-label'>Bullet Rewriter</div>", unsafe_allow_html=True)

        bullets = st.session_state.extracted_bullets
        if not bullets:
            st.markdown("<p style='color:var(--text-muted);font-size:1.47rem;'>No bullets detected in your resume.</p>", unsafe_allow_html=True)
        else:
            for i, bullet in enumerate(bullets):
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"""
                    <div style='background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);
                    border-radius:var(--radius-sm);padding:12px 16px;font-size:1.53rem;
                    color:var(--text-secondary);font-family:"JetBrains Mono",monospace;line-height:1.6;'>
                    {bullet}</div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("Rewrite", key=f"rewrite_{i}"):
                        with st.spinner("Rewriting..."):
                            res = rewrite_bullet(bullet, st.session_state.jd_text)
                        if res:
                            st.session_state.bullet_rewrites[i] = res

                if i in st.session_state.bullet_rewrites:
                    rw = st.session_state.bullet_rewrites[i]
                    st.markdown(f"""
                    <div style='background:rgba(52,211,153,0.04);border:1px solid rgba(52,211,153,0.12);
                    border-radius:var(--radius-sm);padding:14px 18px;margin-top:6px;margin-bottom:14px;
                    border-left:3px solid rgba(52,211,153,0.4);'>
                        <div style='font-size:1.13rem;color:rgba(52,211,153,0.5);text-transform:uppercase;
                        letter-spacing:0.12em;margin-bottom:8px;font-weight:600;'>✓ Rewritten</div>
                        <div style='font-size:1.57rem;color:var(--text-secondary);
                        font-family:"JetBrains Mono",monospace;line-height:1.7;'>{rw.get("rewritten","")}</div>
                    </div>
                    """, unsafe_allow_html=True)

    else:
        # Empty state
        st.markdown("""
        <div class='fade-in-up' style='text-align:center;padding:6rem 2rem;'>
            <div style='width:64px;height:64px;margin:0 auto 1.5rem;border-radius:18px;
            background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);
            display:flex;align-items:center;justify-content:center;'>
                <svg width='28' height='28' viewBox='0 0 24 24' fill='none' stroke='rgba(255,255,255,0.15)' stroke-width='1.5' stroke-linecap='round'>
                    <path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/>
                    <polyline points='14 2 14 8 20 8'/>
                    <line x1='16' y1='13' x2='8' y2='13'/>
                    <line x1='16' y1='17' x2='8' y2='17'/>
                    <polyline points='10 9 9 9 8 9'/>
                </svg>
            </div>
            <div style='font-size:1.76rem;color:var(--text-tertiary);font-weight:600;
            font-family:"Plus Jakarta Sans",sans-serif;letter-spacing:-0.01em;'>Upload your resume & paste a job description</div>
            <div style='font-size:1.41rem;color:var(--text-muted);margin-top:0.5rem;'>
            Then click <span style='color:var(--accent-cyan);font-weight:600;'>Analyse Now</span> in the sidebar</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# TAB 2 — INTERVIEW PREDICTOR
# ══════════════════════════════════════════════════════════════════
with tab2:
    if not st.session_state.analysis_result:
        st.markdown("""
        <div class='fade-in-up' style='text-align:center;padding:6rem 2rem;'>
            <div style='width:64px;height:64px;margin:0 auto 1.5rem;border-radius:18px;
            background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);
            display:flex;align-items:center;justify-content:center;'>
                <svg width='28' height='28' viewBox='0 0 24 24' fill='none' stroke='rgba(255,255,255,0.15)' stroke-width='1.5' stroke-linecap='round'>
                    <circle cx='12' cy='12' r='10'/><path d='M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3'/><line x1='12' y1='17' x2='12.01' y2='17'/>
                </svg>
            </div>
            <div style='font-size:1.76rem;color:var(--text-tertiary);font-weight:600;
            font-family:"Plus Jakarta Sans",sans-serif;'>Complete Resume Analysis first</div>
            <div style='font-size:1.41rem;color:var(--text-muted);margin-top:0.5rem;'>Run an analysis to unlock interview predictions</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='fade-in-up' style='margin-bottom:1.5rem;'>
            <div class='section-label' style='margin-bottom:0.4rem;'>Interview Predictor</div>
            <div style='font-size:1.61rem;color:var(--text-tertiary);font-weight:500;'>AI predicts the exact questions you'll be asked</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])
        with col1:
            experience_level = st.selectbox("Experience Level", ["Fresher", "1-2 years", "3-5 years"])
        with col2:
            st.markdown("<div style='padding-top:1.8rem;'></div>", unsafe_allow_html=True)
            predict_btn = st.button("Predict", use_container_width=True, type="primary")

        if predict_btn:
            from features.interview_predictor import predict_questions
            with st.spinner("Predicting your questions..."):
                result = predict_questions(st.session_state.resume_text, st.session_state.jd_text, experience_level)
            if result:
                st.session_state.questions = result
            else:
                st.error("Could not predict questions. Try again.")

        if st.session_state.questions:
            from utils.formatters import display_question_card
            qdata = st.session_state.questions
            st.markdown(f"""
            <div class='fade-in-up' style='display:flex;align-items:center;justify-content:space-between;margin:1.5rem 0 1rem;'>
                <div style='font-size:1.41rem;color:var(--text-tertiary);font-weight:500;'>
                    Role: <span style='color:var(--accent-cyan);font-weight:600;'>{qdata.get("role","")}</span>
                </div>
                <div style='font-size:1.27rem;color:var(--text-muted);font-weight:500;
                font-family:"JetBrains Mono",monospace;'>{len(qdata["questions"])} questions</div>
            </div>
            """, unsafe_allow_html=True)

            cat_colors = {
                "Technical": "var(--accent-blue)",
                "Behavioural": "var(--accent-violet)",
                "Role-specific": "var(--accent-emerald)",
                "Culture": "var(--accent-amber)"
            }

            for i, q in enumerate(qdata["questions"], 1):
                cat = q.get("category", "General")
                cc = cat_colors.get(cat, "#fff")
                with st.expander(f"Q{i}  —  {q['question'][:70]}..."):
                    st.markdown(f"""
                    <span style='background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                    color:{cc};padding:3px 12px;border-radius:var(--radius-pill);font-size:1.27rem;
                    letter-spacing:0.04em;font-weight:600;'>{cat}</span>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <p style='color:var(--text-tertiary);font-size:1.47rem;font-style:italic;
                    margin-top:0.8rem;line-height:1.6;'>Why you'll be asked this: {q.get("why_asked","")}</p>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style='background:rgba(34,211,238,0.04);border:1px solid rgba(34,211,238,0.12);
                    border-radius:var(--radius-sm);padding:14px;margin-top:0.5rem;border-left:3px solid rgba(34,211,238,0.3);'>
                        <div style='font-size:1.13rem;color:rgba(34,211,238,0.5);text-transform:uppercase;
                        letter-spacing:0.12em;margin-bottom:8px;font-weight:600;'>How to Answer</div>
                        <p style='color:var(--text-secondary);font-size:1.53rem;margin:0;line-height:1.7;'>
                        {q.get("answer_framework","")}</p>
                    </div>
                    <div style='background:rgba(52,211,153,0.04);border:1px solid rgba(52,211,153,0.1);
                    border-radius:var(--radius-sm);padding:14px;margin-top:0.5rem;border-left:3px solid rgba(52,211,153,0.3);'>
                        <div style='font-size:1.13rem;color:rgba(52,211,153,0.5);text-transform:uppercase;
                        letter-spacing:0.12em;margin-bottom:8px;font-weight:600;'>Strong Answer Example</div>
                        <p style='color:var(--text-secondary);font-size:1.53rem;margin:0;line-height:1.7;'>
                        {q.get("sample_strong_answer","")}</p>
                    </div>
                    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# TAB 3 — BATCH SCREENER
# ══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div class='fade-in-up' style='margin-bottom:1.5rem;'>
        <div class='section-label' style='margin-bottom:0.4rem;'>Batch Screener</div>
        <div style='font-size:1.61rem;color:var(--text-tertiary);font-weight:500;'>Screen multiple resumes against one job description</div>
    </div>
    """, unsafe_allow_html=True)

    batch_files = st.file_uploader("Upload Resumes", type=["pdf"], accept_multiple_files=True)
    batch_jd = st.text_area("Job Description", height=120, placeholder="Paste JD here...")

    if st.button("Screen All", use_container_width=True, type="primary"):
        if not batch_files:
            st.error("Upload at least one PDF.")
        elif not batch_jd.strip():
            st.error("Paste a job description.")
        else:
            from features.batch_screener import screen_resumes
            with st.spinner(f"Screening {len(batch_files)} resumes..."):
                df = screen_resumes(batch_files, batch_jd)

            if df is not None and len(df) > 0:
                total = len(df)
                recommended = len(df[df["Recommendation"].isin(["Strong Yes", "Yes"])])

                st.markdown(f"""
                <div class='fade-in-up' style='display:flex;gap:1rem;margin-bottom:1.5rem;'>
                    <div class='metric-card' style='flex:1;'>
                        <div class='metric-number'>{total}</div>
                        <div class='metric-label'>Total Screened</div>
                    </div>
                    <div class='metric-card' style='flex:1;'>
                        <div class='metric-number' style='background:linear-gradient(135deg,#34d399,#22d3ee);-webkit-background-clip:text;background-clip:text;'>{recommended}</div>
                        <div class='metric-label'>Recommended</div>
                    </div>
                    <div class='metric-card' style='flex:1;'>
                        <div class='metric-number' style='background:linear-gradient(135deg,#fb7185,#f43f5e);-webkit-background-clip:text;background-clip:text;'>{total - recommended}</div>
                        <div class='metric-label'>Not Recommended</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.dataframe(df, use_container_width=True)
                st.download_button(
                    "Download CSV",
                    df.to_csv(index=False),
                    "screening_results.csv",
                    "text/csv",
                    use_container_width=True
                )

# ══════════════════════════════════════════════════════════════════
# TAB 4 — MOCK INTERVIEW
# ══════════════════════════════════════════════════════════════════
with tab4:
    from features.interview_simulator import generate_questions, evaluate_answer, generate_report

    # ── SETUP STAGE ──
    if st.session_state.simulator_stage == "setup":
        st.markdown("""
        <div class='fade-in-up' style='text-align:center;padding:2.5rem 1rem 3rem;'>
            <div style='width:64px;height:64px;margin:0 auto 1.5rem;border-radius:18px;
            background:linear-gradient(135deg, rgba(34,211,238,0.1), rgba(167,139,250,0.1));
            border:1px solid rgba(255,255,255,0.08);
            display:flex;align-items:center;justify-content:center;'>
                <svg width='28' height='28' viewBox='0 0 24 24' fill='none' stroke='rgba(34,211,238,0.6)' stroke-width='1.5' stroke-linecap='round'>
                    <path d='M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'/>
                </svg>
            </div>
            <div class='section-label' style='text-align:center;margin-bottom:1rem;'>AI Interviewer</div>
            <div style='font-size:2.35rem;font-weight:700;color:var(--text-primary);
            font-family:"Plus Jakarta Sans",sans-serif;letter-spacing:-0.02em;'>Mock Interview</div>
            <div style='font-size:1.47rem;color:var(--text-tertiary);margin-top:0.5rem;font-weight:500;'>
            8 questions · instant feedback · full report</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            sim_role = st.selectbox("Role", ["Full Stack Developer", "Frontend Developer",
                "Backend Developer", "Data Analyst", "ML Engineer", "DevOps Engineer"])
        with col2:
            sim_exp = st.selectbox("Level", ["Fresher", "1-2 years", "3-5 years"])

        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

        if st.button("Begin Interview", use_container_width=True, type="primary"):
            with st.spinner("Preparing your interview..."):
                questions = generate_questions(sim_role, sim_exp)
            if questions:
                st.session_state.simulator_questions = questions
                st.session_state.simulator_role = sim_role
                st.session_state.simulator_stage = "in_progress"
                st.session_state.simulator_current_index = 0
                st.session_state.simulator_answers = []
                st.session_state.simulator_evaluations = []
                st.rerun()
            else:
                st.error("Could not generate questions. Try again.")

    # ── IN PROGRESS STAGE ──
    elif st.session_state.simulator_stage == "in_progress":
        questions = st.session_state.simulator_questions
        idx = st.session_state.simulator_current_index
        total = len(questions)
        q = questions[idx]

        # Progress
        progress_pct = idx / total
        st.markdown(f"""
        <div class='fade-in-up' style='display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;'>
            <div style='font-size:1.27rem;color:var(--text-tertiary);text-transform:uppercase;
            letter-spacing:0.1em;font-weight:600;'>Question {idx+1} of {total}</div>
            <div style='font-size:1.27rem;color:var(--accent-cyan);font-family:"JetBrains Mono",monospace;font-weight:500;'>
            {int(progress_pct*100)}% complete</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(progress_pct)
        st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)

        diff_colors = {"Easy": "var(--accent-emerald)", "Medium": "var(--accent-amber)", "Hard": "var(--accent-rose)"}
        cat_colors2 = {"Technical": "var(--accent-blue)", "Behavioural": "var(--accent-violet)", "Role-specific": "var(--accent-emerald)"}
        dc = diff_colors.get(q.get("difficulty", "Medium"), "#fff")
        cc = cat_colors2.get(q.get("category", "Technical"), "#fff")

        st.markdown(f"""
        <div class='glass-card fade-in-up' style='margin-bottom:1.5rem;'>
            <div style='display:flex;gap:8px;margin-bottom:1.2rem;'>
                <span style='background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);
                color:{cc};padding:3px 12px;border-radius:var(--radius-pill);font-size:1.22rem;font-weight:600;letter-spacing:0.04em;'>{q.get("category","")}</span>
                <span style='background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);
                color:{dc};padding:3px 12px;border-radius:var(--radius-pill);font-size:1.22rem;font-weight:600;letter-spacing:0.04em;'>{q.get("difficulty","")}</span>
            </div>
            <div style='font-size:2.06rem;font-weight:600;color:var(--text-primary);
            font-family:"Plus Jakarta Sans",sans-serif;line-height:1.6;letter-spacing:-0.01em;'>
            {q["question"]}</div>
            <div style='font-size:1.41rem;color:var(--text-muted);margin-top:0.8rem;font-style:italic;line-height:1.5;'>
            {q.get("what_interviewer_wants","")}</div>
        </div>
        """, unsafe_allow_html=True)

        # Show last eval
        if st.session_state.simulator_evaluations:
            last = st.session_state.simulator_evaluations[-1]
            score_val = last.get("score", 0)
            sc = "#34d399" if score_val >= 7 else "#fbbf24" if score_val >= 5 else "#fb7185"
            with st.expander(f"Previous answer — {score_val}/10"):
                st.markdown(f"""
                <div style='display:flex;gap:1rem;margin-bottom:1rem;'>
                    <div style='font-size:3.92rem;font-weight:800;color:{sc};font-family:"Plus Jakarta Sans",sans-serif;'>{score_val}/10</div>
                </div>
                <p style='color:var(--text-tertiary);font-size:1.47rem;line-height:1.6;'>{last.get("score_reason","")}</p>
                <div style='background:rgba(52,211,153,0.04);border:1px solid rgba(52,211,153,0.1);
                border-radius:var(--radius-sm);padding:12px;margin-top:8px;border-left:3px solid rgba(52,211,153,0.3);'>
                    <div style='font-size:1.13rem;color:rgba(52,211,153,0.5);margin-bottom:6px;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;'>WHAT WORKED</div>
                    <p style='color:var(--text-secondary);font-size:1.47rem;margin:0;line-height:1.6;'>{last.get("what_was_good","")}</p>
                </div>
                <div style='background:rgba(251,191,36,0.04);border:1px solid rgba(251,191,36,0.1);
                border-radius:var(--radius-sm);padding:12px;margin-top:8px;border-left:3px solid rgba(251,191,36,0.3);'>
                    <div style='font-size:1.13rem;color:rgba(251,191,36,0.5);margin-bottom:6px;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;'>WHAT WAS MISSING</div>
                    <p style='color:var(--text-secondary);font-size:1.47rem;margin:0;line-height:1.6;'>{last.get("what_was_missing","")}</p>
                </div>
                """, unsafe_allow_html=True)

        user_answer = st.text_area("Your Answer", height=180,
            placeholder="Take your time. Think out loud if needed...",
            key=f"ans_{idx}")

        if st.button("Submit Answer  →", use_container_width=True, type="primary"):
            if not user_answer.strip():
                st.warning("Type your answer before submitting.")
            else:
                with st.spinner("Evaluating..."):
                    ev = evaluate_answer(q["question"], user_answer, st.session_state.simulator_role)
                if ev:
                    st.session_state.simulator_answers.append(user_answer)
                    st.session_state.simulator_evaluations.append(ev)
                    if idx + 1 >= total:
                        with st.spinner("Generating your report..."):
                            report = generate_report(
                                st.session_state.simulator_questions,
                                st.session_state.simulator_answers,
                                st.session_state.simulator_evaluations,
                                st.session_state.simulator_role
                            )
                        st.session_state.simulator_report = report
                        st.session_state.simulator_stage = "complete"
                    else:
                        st.session_state.simulator_current_index += 1
                    st.rerun()
                else:
                    st.error("Evaluation failed. Try again.")

    # ── COMPLETE STAGE ──
    elif st.session_state.simulator_stage == "complete":
        report = st.session_state.simulator_report

        if not report:
            st.error("Report failed. Restart the interview.")
        else:
            overall = report.get("overall_score", 0)
            grade = report.get("grade", "?")

            if grade in ["A"]:
                grade_gradient = "linear-gradient(135deg, #34d399, #22d3ee)"
                grade_glow = "rgba(52,211,153,0.3)"
            elif grade in ["B", "C"]:
                grade_gradient = "linear-gradient(135deg, #fbbf24, #fb923c)"
                grade_glow = "rgba(251,191,36,0.3)"
            else:
                grade_gradient = "linear-gradient(135deg, #fb7185, #f43f5e)"
                grade_glow = "rgba(251,113,133,0.3)"

            st.markdown(f"""
            <div class='fade-in-up' style='text-align:center;padding:3rem 1rem 2.5rem;'>
                <div class='section-label' style='text-align:center;margin-bottom:1rem;'>Interview Complete</div>
                <div style='font-size:10.78rem;font-weight:800;font-family:"Plus Jakarta Sans",sans-serif;
                background:{grade_gradient};
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                background-clip:text;line-height:1;
                filter:drop-shadow(0 0 40px {grade_glow});letter-spacing:-0.04em;'>{grade}</div>
                <div style='font-size:1.96rem;color:var(--text-tertiary);margin-top:0.5rem;font-weight:600;'>{overall}/100</div>
                <div style='font-size:1.53rem;color:var(--text-muted);margin-top:0.8rem;
                font-style:italic;max-width:400px;margin-left:auto;margin-right:auto;line-height:1.5;'>{report.get("hire_verdict","")}</div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class='glass-card fade-in-up-delayed'>
                    <div class='section-label' style='margin-bottom:1rem;'>Top Strengths</div>
                    {''.join([f'<div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:10px;"><span style="color:var(--accent-emerald);font-size:1.47rem;font-weight:700;margin-top:1px;">+</span><span style="color:var(--text-secondary);font-size:1.53rem;line-height:1.6;">{s}</span></div>' for s in report.get("top_3_strengths",[])])}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class='glass-card fade-in-up-delayed-2'>
                    <div class='section-label' style='margin-bottom:1rem;'>Areas to Improve</div>
                    {''.join([f'<div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:10px;"><span style="color:var(--accent-amber);font-size:1.47rem;font-weight:700;margin-top:1px;">→</span><span style="color:var(--text-secondary);font-size:1.53rem;line-height:1.6;">{s}</span></div>' for s in report.get("top_3_improvements",[])])}
                </div>
                """, unsafe_allow_html=True)

            # Question breakdown
            st.markdown("<div style='margin:2rem 0 1rem;'></div>", unsafe_allow_html=True)
            st.markdown("<div class='section-label'>Question Breakdown</div>", unsafe_allow_html=True)

            for i, (q, e) in enumerate(zip(st.session_state.simulator_questions, st.session_state.simulator_evaluations), 1):
                sc_val = e.get("score", 0)
                sc = "#34d399" if sc_val >= 7 else "#fbbf24" if sc_val >= 5 else "#fb7185"
                with st.expander(f"Q{i}  ·  {sc_val}/10  —  {q['question'][:60]}..."):
                    st.markdown(f"""
                    <p style='color:var(--text-muted);font-size:1.47rem;font-style:italic;
                    margin-bottom:0.8rem;line-height:1.6;'>Your answer: {st.session_state.simulator_answers[i-1][:200]}...</p>
                    <div style='font-size:1.53rem;color:{sc};font-weight:700;margin-bottom:0.5rem;
                    font-family:"Plus Jakarta Sans",sans-serif;'>{sc_val}/10 — {e.get("score_reason","")}</div>
                    <p style='color:var(--text-tertiary);font-size:1.47rem;line-height:1.6;'>{e.get("improved_answer","")}</p>
                    """, unsafe_allow_html=True)

            # Next steps
            st.markdown("<div style='margin:2rem 0 1rem;'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='glass-card fade-in-up-delayed-2'>
                <div class='section-label' style='margin-bottom:1rem;'>Recommended Next Steps</div>
                {''.join([f'<div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:10px;"><span style="color:var(--accent-cyan);font-weight:700;">→</span><span style="color:var(--text-secondary);font-size:1.53rem;line-height:1.6;">{s}</span></div>' for s in report.get("recommended_next_steps",[])])}
            </div>
            """, unsafe_allow_html=True)

            # Report text for download
            report_text = f"""HIREREADY AI — MOCK INTERVIEW REPORT
Role: {st.session_state.simulator_role}
Overall Score: {overall}/100  |  Grade: {grade}
Verdict: {report.get('hire_verdict','')}

TOP STRENGTHS:
{chr(10).join(['• ' + s for s in report.get('top_3_strengths',[])])}

AREAS TO IMPROVE:
{chr(10).join(['• ' + s for s in report.get('top_3_improvements',[])])}

QUESTION BREAKDOWN:
{''.join([f"Q{i}: {q['question']}{chr(10)}Answer: {a}{chr(10)}Score: {e['score']}/10 — {e['score_reason']}{chr(10)}{chr(10)}" for i,(q,a,e) in enumerate(zip(st.session_state.simulator_questions, st.session_state.simulator_answers, st.session_state.simulator_evaluations),1)])}

NEXT STEPS:
{chr(10).join(['• ' + s for s in report.get('recommended_next_steps',[])])}
"""
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("Download Report", report_text,
                    "interview_report.txt", "text/plain", use_container_width=True)
            with col2:
                if st.button("New Interview", use_container_width=True):
                    for key in ["simulator_stage","simulator_questions","simulator_current_index",
                                "simulator_answers","simulator_evaluations","simulator_report"]:
                        st.session_state[key] = "setup" if key == "simulator_stage" else [] if isinstance(st.session_state[key], list) else None
                    st.rerun()
