from __future__ import annotations

import streamlit as st

import database.repository as db
from quiz.loader import load_quiz
from schema.models import QUIZ_FILES
from state.session import init_state
from ui.navigation import render_navigation
from ui.question import render_question
from ui.results import render_results
from ui.sidebar import render_sidebar
from ui.styles import inject_global_css


def main() -> None:
    st.set_page_config(
        page_title="Databricks Quiz",
        page_icon=":bar_chart:",
        layout="wide",
    )
    inject_global_css()
    db.init_db()

    selected_quiz = st.sidebar.selectbox(
        "Quiz",
        options=list(QUIZ_FILES.keys()),
        key="selected_quiz_name",
    )
    quiz_file = QUIZ_FILES[selected_quiz]

    if st.session_state.get("_loaded_quiz") != selected_quiz:
        st.session_state["_loaded_quiz"] = selected_quiz
        for key in list(st.session_state.keys()):
            if key not in ("selected_quiz_name", "_loaded_quiz"):
                del st.session_state[key]
        st.rerun()

    try:
        questions = load_quiz(quiz_file)
    except Exception as exc:
        st.title("Practice Quiz — Databricks Certified Data Analyst Associate")
        st.error(f"Failed to load quiz: {exc}")
        st.stop()

    init_state(len(questions))
    render_sidebar(questions)

    if not st.session_state["show_results"]:
        difficulty = "Advanced" if "Advanced" in selected_quiz else "Standard"
        st.title(f"Practice Quiz — Databricks Data Analyst Associate · {difficulty}")
        current_index = st.session_state["current_question"]
        render_question(questions[current_index], current_index, len(questions))
        st.divider()
        render_navigation(len(questions))
    else:
        render_results(questions)


if __name__ == "__main__":
    main()
