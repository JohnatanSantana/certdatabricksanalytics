from __future__ import annotations

from collections import defaultdict

import streamlit as st

import database.repository as db
from schema.models import Question
from state.session import reset_quiz


def render_sidebar(questions: list[Question]) -> None:
    total = len(questions)
    answered = len(st.session_state["answers"])
    correct = sum(
        1
        for idx, ch in st.session_state["answers"].items()
        if ch == questions[idx].answer
    )

    st.sidebar.title("Databricks Quiz")
    c1, c2, c3 = st.sidebar.columns(3)
    c1.metric("Done", f"{answered}/{total}")
    c2.metric("Correct", correct)
    c3.metric("Score", f"{round(correct / total * 100) if answered else 0}%")
    st.sidebar.progress(answered / total if total else 0.0)

    if st.sidebar.button("Restart quiz", use_container_width=True, type="secondary"):
        reset_quiz(total)
        st.rerun()

    st.sidebar.divider()
    st.sidebar.caption("Quick navigation")

    n_cols = 5
    for row_start in range(0, total, n_cols):
        cols = st.sidebar.columns(n_cols)
        for offset, col in enumerate(cols):
            idx = row_start + offset
            if idx >= total:
                break
            q = questions[idx]
            if idx in st.session_state["submitted"]:
                is_correct = st.session_state["answers"][idx] == q.answer
                label = f"{'✓' if is_correct else '✗'}{q.number:02d}"
            elif idx in st.session_state["answers"]:
                label = f"·{q.number:02d}"
            else:
                label = f"{q.number:02d}"

            is_current = idx == st.session_state["current_question"]
            if col.button(
                label,
                key=f"nav_{idx}",
                use_container_width=True,
                type="primary" if is_current else "secondary",
            ):
                st.session_state["current_question"] = idx
                st.session_state["needs_scroll"] = True
                st.rerun()

    st.sidebar.divider()
    with st.sidebar.expander("Progress by section", expanded=False):
        section_totals: dict[str, dict] = defaultdict(
            lambda: {"total": 0, "correct": 0, "answered": 0}
        )
        for idx, q in enumerate(questions):
            section_totals[q.section]["total"] += 1
            if idx in st.session_state["answers"]:
                section_totals[q.section]["answered"] += 1
                if st.session_state["answers"][idx] == q.answer:
                    section_totals[q.section]["correct"] += 1
        for section, stats in section_totals.items():
            short = section.split("–")[-1].strip() if "–" in section else section[:30]
            pct = round(stats["correct"] / stats["answered"] * 100) if stats["answered"] else 0
            st.caption(f"**{short}**")
            st.caption(f"{stats['correct']}/{stats['answered']} answered · {pct}% correct")

    st.sidebar.divider()
    with st.sidebar.expander("Recent history", expanded=False):
        sessions = db.load_sessions(limit=8)
        if not sessions:
            st.caption("No sessions saved yet.")
        else:
            for s in sessions:
                date = s["finished_at"][:10]
                st.caption(f"{date} — {s['score']}/{s['total']} ({s['pct']}%)")
