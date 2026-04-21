import streamlit as st


def display_match_score(score, recommendation, reason):
    # st.metric shows a big number with a label — perfect for the match score
    st.metric(label="Match Score", value=f"{score}%")

    # Color the recommendation badge based on the value
    if recommendation in ["Strong Yes", "Yes"]:
        color = "#28a745"  # green
        text_color = "#ffffff"
    elif recommendation == "Maybe":
        color = "#ffc107"  # yellow
        text_color = "#000000"
    else:
        color = "#dc3545"  # red
        text_color = "#ffffff"

    # unsafe_allow_html=True lets us use HTML for the coloured badge
    st.markdown(
        f"<span style='background-color:{color}; color:{text_color}; "
        f"padding: 4px 12px; border-radius: 12px; font-weight: bold;'>"
        f"{recommendation}</span>",
        unsafe_allow_html=True
    )

    # Show the reason in grey italic below the badge
    st.markdown(
        f"<p style='color: gray; font-style: italic; margin-top: 8px;'>{reason}</p>",
        unsafe_allow_html=True
    )


def display_skills(matched_skills, missing_skills):
    # Two columns side by side
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ✅ Skills You Have")
        if matched_skills:
            # Show each skill as a small green pill badge
            pills_html = ""
            for skill in matched_skills:
                pills_html += (
                    f"<span style='background-color:#d4edda; color:#155724; "
                    f"padding: 3px 10px; border-radius: 10px; margin: 3px; "
                    f"display: inline-block; font-size: 13px;'>{skill}</span>"
                )
            st.markdown(pills_html, unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:gray;'>None found</p>", unsafe_allow_html=True)

    with col2:
        st.markdown("#### ❌ Skills You Are Missing")
        if missing_skills:
            pills_html = ""
            for skill in missing_skills:
                pills_html += (
                    f"<span style='background-color:#f8d7da; color:#721c24; "
                    f"padding: 3px 10px; border-radius: 10px; margin: 3px; "
                    f"display: inline-block; font-size: 13px;'>{skill}</span>"
                )
            st.markdown(pills_html, unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:gray;'>None found</p>", unsafe_allow_html=True)


def display_question_card(question_dict, number):
    # Category colours
    category_colors = {
        "Technical": "#cce5ff",
        "Behavioural": "#e2d9f3",
        "Role-specific": "#d4edda",
        "Culture": "#fff3cd"
    }

    category = question_dict.get("category", "General")
    color = category_colors.get(category, "#e2e3e5")

    # Each question is inside an expander — collapsed by default
    with st.expander(f"Q{number}: {question_dict.get('question', '')}"):
        # Category badge
        st.markdown(
            f"<span style='background-color:{color}; padding: 3px 10px; "
            f"border-radius: 10px; font-size: 13px;'>{category}</span>",
            unsafe_allow_html=True
        )
        st.markdown("")

        st.markdown(f"*Why you'll be asked this:* {question_dict.get('why_asked', '')}")
        st.info(f"**How to answer:** {question_dict.get('answer_framework', '')}")
        st.success(f"**Example strong answer:** {question_dict.get('sample_strong_answer', '')}")


def display_evaluation(evaluation_dict):
    score = evaluation_dict.get("score", 0)
    st.metric(label="Answer Score", value=f"{score}/10")

    st.success(f"**What you did well:** {evaluation_dict.get('what_was_good', '')}")
    st.warning(f"**What was missing:** {evaluation_dict.get('what_was_missing', '')}")
    st.info(f"**How a top candidate would answer:** {evaluation_dict.get('improved_answer', '')}")

    keywords = evaluation_dict.get("keywords_missed", [])
    if keywords:
        st.markdown("**Keywords you missed:**")
        pills_html = ""
        for kw in keywords:
            pills_html += (
                f"<span style='background-color:#cce5ff; color:#004085; "
                f"padding: 3px 10px; border-radius: 10px; margin: 3px; "
                f"display: inline-block; font-size: 13px;'>{kw}</span>"
            )
        st.markdown(pills_html, unsafe_allow_html=True)


def display_bullet_rewrite(rewrite_dict):
    st.markdown("**Before:**")
    st.markdown(
        f"<div style='background-color:#f8f9fa; padding: 10px; "
        f"border-radius: 6px; color: #333;'>{rewrite_dict.get('original', '')}</div>",
        unsafe_allow_html=True
    )

    st.markdown("<p style='text-align:center; font-size: 20px;'>⬇️</p>", unsafe_allow_html=True)

    st.markdown("**After:**")
    st.markdown(
        f"<div style='background-color:#d4edda; padding: 10px; "
        f"border-radius: 6px; color: #155724;'>{rewrite_dict.get('rewritten', '')}</div>",
        unsafe_allow_html=True
    )

    # STAR breakdown in an expander
    star = rewrite_dict.get("star_breakdown", {})
    if star:
        with st.expander("See STAR breakdown"):
            st.markdown(f"**Situation:** {star.get('situation', '')}")
            st.markdown(f"**Task:** {star.get('task', '')}")
            st.markdown(f"**Action:** {star.get('action', '')}")
            st.markdown(f"**Result:** {star.get('result', '')}")

    keywords = rewrite_dict.get("keywords_added", [])
    if keywords:
        st.markdown("**Keywords added:**")
        pills_html = ""
        for kw in keywords:
            pills_html += (
                f"<span style='background-color:#cce5ff; color:#004085; "
                f"padding: 3px 10px; border-radius: 10px; margin: 3px; "
                f"display: inline-block; font-size: 13px;'>{kw}</span>"
            )
        st.markdown(pills_html, unsafe_allow_html=True)