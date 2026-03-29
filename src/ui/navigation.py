from __future__ import annotations

import streamlit as st


def render_navigation(total_questions: int) -> None:
    current = st.session_state["current_question"]
    prev_col, next_col, result_col = st.columns(3)

    with prev_col:
        if st.button("← Previous", use_container_width=True, disabled=current == 0):
            st.session_state["current_question"] -= 1
            st.session_state["needs_scroll"] = True
            st.rerun()

    with next_col:
        if st.button(
            "Next →",
            use_container_width=True,
            disabled=current == total_questions - 1,
        ):
            st.session_state["current_question"] += 1
            st.session_state["needs_scroll"] = True
            st.rerun()

    with result_col:
        if st.button("Final results", use_container_width=True, type="primary"):
            st.session_state["show_results"] = True
            st.session_state["needs_scroll"] = True
            st.rerun()
