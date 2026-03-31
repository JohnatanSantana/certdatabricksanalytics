from __future__ import annotations

from collections import defaultdict

import streamlit as st

import database.repository as db
from schema.models import Question
from ui.styles import OPTION_STYLE, scroll_to_top


def render_history_detail(questions: list[Question]) -> None:
    if st.session_state.pop("needs_scroll", False):
        scroll_to_top()

    # Build lookup by question number for O(1) access
    questions_by_number: dict[int, Question] = {q.number: q for q in questions}

    session_id = st.session_state["history_session_id"]
    session = db.load_session(session_id)
    if not session:
        st.error("Session not found.")
        _back_button()
        return

    date = session["finished_at"].replace("T", " ")
    badge = "🟢" if session["pct"] >= 70 else "🔴"
    st.title(f"{badge} Session — {date}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{session['score']}/{session['total']}")
    col2.metric("Percentage", f"{session['pct']}%")
    col3.metric("Started", session["started_at"].replace("T", " "))
    col4.metric("Pass (≥70%)", "✓ Yes" if session["pct"] >= 70 else "✗ No")

    st.progress(session["pct"] / 100)
    st.divider()

    answers = db.load_session_answers(session_id)
    if not answers:
        st.info("No answers recorded for this session.")
        _back_button()
        return

    tab_questions, tab_sections = st.tabs(["Questions", "Section breakdown"])

    with tab_questions:
        for row in answers:
            is_correct = bool(row["is_correct"])
            chosen = row["chosen"] or "—"
            icon = "✓" if is_correct else "✗"
            section_short = (
                row["section"].split("–")[-1].strip()
                if "–" in row["section"]
                else row["section"]
            )
            q = questions_by_number.get(row["question_number"])
            with st.expander(
                f"{icon} Q{row['question_number']} — {section_short}",
                expanded=not is_correct,
            ):
                if q:
                    st.caption(q.section)
                    st.markdown(f"**{q.objective}**")
                    st.markdown(q.prompt)
                    st.markdown("**Options**")
                    for letter, text in q.options.items():
                        if letter == q.answer:
                            style, icon_opt = OPTION_STYLE["correct"], "✓"
                        elif letter == chosen:
                            style, icon_opt = OPTION_STYLE["wrong"], "✗"
                        else:
                            style, icon_opt = OPTION_STYLE["neutral"], "○"
                        st.markdown(
                            f'<div style="{style}"><strong>{letter}.</strong> {icon_opt} {text}</div>',
                            unsafe_allow_html=True,
                        )
                    st.markdown("")
                    if is_correct:
                        st.success(f"Correct! Answer: **{q.answer}**")
                    else:
                        st.error(
                            f"Incorrect. Your answer: **{chosen}** · Correct: **{q.answer}**"
                        )
                    st.info(f"**Key concept:** {q.concept}")
                    st.markdown("")
                    if st.button(
                        "Go to question in quiz",
                        key=f"hist_goto_{row['question_number']}",
                        use_container_width=True,
                    ):
                        st.session_state["show_history"] = False
                        st.session_state["history_session_id"] = None
                        st.session_state["current_question"] = q.number - 1
                        st.session_state["needs_scroll"] = True
                        st.rerun()
                else:
                    col_a, col_b = st.columns(2)
                    col_a.markdown(f"**Your answer:** `{chosen}`")
                    col_b.markdown(f"**Correct answer:** `{row['correct_answer']}`")
                    if is_correct:
                        st.success("Correct")
                    else:
                        st.error(f"Incorrect — correct answer was **{row['correct_answer']}**")

    with tab_sections:
        section_stats: dict[str, dict] = defaultdict(
            lambda: {"correct": 0, "total": 0}
        )
        for row in answers:
            section_stats[row["section"]]["total"] += 1
            if row["is_correct"]:
                section_stats[row["section"]]["correct"] += 1

        for section, stats in section_stats.items():
            pct = stats["correct"] / stats["total"] * 100 if stats["total"] else 0
            short = section.split("–")[-1].strip() if "–" in section else section
            st.markdown(f"**{short}**")
            st.progress(
                pct / 100,
                text=f"{stats['correct']}/{stats['total']} correct ({pct:.0f}%)",
            )

    st.divider()
    _back_button()


def _back_button() -> None:
    if st.button("← Back to quiz", use_container_width=True):
        st.session_state["show_history"] = False
        st.session_state["history_session_id"] = None
        st.session_state["needs_scroll"] = True
        st.rerun()
