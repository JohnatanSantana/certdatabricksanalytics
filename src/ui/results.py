from __future__ import annotations

from collections import defaultdict

import streamlit as st

import database.repository as db
from schema.models import Question
from ui.styles import scroll_to_top


def render_results(questions: list[Question]) -> None:
    if st.session_state.pop("needs_scroll", False):
        scroll_to_top()

    total = len(questions)
    answers = st.session_state["answers"]
    answered = len(answers)
    correct = sum(1 for idx, ch in answers.items() if ch == questions[idx].answer)
    score_pct = correct / total * 100

    if not st.session_state["session_saved"]:
        sid = db.save_session(st.session_state["started_at"], answers, questions)
        st.session_state["session_id"] = sid
        st.session_state["session_saved"] = True

    st.title("Results")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score", f"{correct}/{total}")
    col2.metric("Percentage", f"{score_pct:.1f}%")
    col3.metric("Answered", f"{answered}/{total}")
    col4.metric("Pass (≥70%)", "✓ Yes" if score_pct >= 70 else "✗ No")

    st.progress(score_pct / 100)

    unanswered = [q.number for idx, q in enumerate(questions) if idx not in answers]
    if unanswered:
        st.warning("Unanswered: " + ", ".join(str(n) for n in unanswered))

    tab_summary, tab_review, tab_history = st.tabs(
        ["Section breakdown", "Question review", "History"]
    )

    with tab_summary:
        section_stats: dict[str, dict] = defaultdict(
            lambda: {"total": 0, "correct": 0, "answered": 0}
        )
        for idx, q in enumerate(questions):
            section_stats[q.section]["total"] += 1
            if idx in answers:
                section_stats[q.section]["answered"] += 1
                if answers[idx] == q.answer:
                    section_stats[q.section]["correct"] += 1

        for section, stats in section_stats.items():
            pct = stats["correct"] / stats["answered"] * 100 if stats["answered"] else 0
            short = section.split("–")[-1].strip() if "–" in section else section
            st.markdown(f"**{short}**")
            st.progress(
                pct / 100,
                text=f"{stats['correct']}/{stats['answered']} correct ({pct:.0f}%)"
                + (
                    f" — {stats['total'] - stats['answered']} unanswered"
                    if stats["answered"] < stats["total"]
                    else ""
                ),
            )

    with tab_review:
        for idx, question in enumerate(questions):
            chosen = answers.get(idx, "—")
            is_correct = chosen == question.answer
            status = "✓" if is_correct else ("✗" if idx in answers else "○")

            with st.expander(
                f"{status} Q{question.number} — {question.objective[:60]}...",
                expanded=not is_correct and idx in answers,
            ):
                st.markdown(question.prompt)
                st.markdown(f"**Your answer:** `{chosen}` · **Correct:** `{question.answer}`")
                st.caption(f"Key concept: {question.concept}")
                if st.button("Go to question", key=f"goto_result_{idx}"):
                    st.session_state["show_results"] = False
                    st.session_state["current_question"] = idx
                    st.session_state["needs_scroll"] = True
                    st.rerun()

    with tab_history:
        sessions = db.load_sessions(limit=15)
        if not sessions:
            st.info("No previous sessions found.")
        else:
            current_id = st.session_state.get("session_id")
            for s in sessions:
                tag = " ← this session" if s["id"] == current_id else ""
                date = s["finished_at"].replace("T", " ")
                badge = "🟢" if s["pct"] >= 70 else "🔴"
                st.markdown(
                    f"{badge} **{date}**{tag}  \n"
                    f"Score: {s['score']}/{s['total']} · {s['pct']}%"
                )
                st.divider()

    st.markdown("")
    if st.button("← Back to quiz", use_container_width=True):
        st.session_state["show_results"] = False
        st.session_state["needs_scroll"] = True
        st.rerun()
