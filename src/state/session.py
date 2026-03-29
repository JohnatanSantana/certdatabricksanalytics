from __future__ import annotations

from datetime import datetime

import streamlit as st


def init_state(total_questions: int) -> None:
    st.session_state.setdefault("current_question", 0)
    st.session_state.setdefault("answers", {})
    st.session_state.setdefault("submitted", {})
    st.session_state.setdefault("show_results", False)
    st.session_state.setdefault("session_saved", False)
    st.session_state.setdefault("session_id", None)
    st.session_state.setdefault("needs_scroll", False)
    st.session_state.setdefault(
        "started_at", datetime.now().isoformat(timespec="seconds")
    )
    for index in range(total_questions):
        st.session_state.setdefault(f"choice_{index}", None)


def reset_quiz(total_questions: int) -> None:
    st.session_state["current_question"] = 0
    st.session_state["answers"] = {}
    st.session_state["submitted"] = {}
    st.session_state["show_results"] = False
    st.session_state["session_saved"] = False
    st.session_state["session_id"] = None
    st.session_state["needs_scroll"] = False
    st.session_state["started_at"] = datetime.now().isoformat(timespec="seconds")
    for index in range(total_questions):
        st.session_state[f"choice_{index}"] = None
