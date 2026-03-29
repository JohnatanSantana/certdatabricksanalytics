from __future__ import annotations

import streamlit as st

from schema.models import Question
from ui.styles import OPTION_STYLE, scroll_to_anchor


def render_question(question: Question, index: int, total_questions: int) -> None:
    st.markdown('<span id="question-top"></span>', unsafe_allow_html=True)
    if st.session_state.pop("needs_scroll", False):
        scroll_to_anchor("question-top")

    st.progress(
        (index + 1) / total_questions,
        text=f"Question {index + 1} of {total_questions}",
    )

    st.caption(question.section)
    st.subheader(f"Q{question.number}. {question.objective}")
    st.markdown(question.prompt)

    selected = st.session_state.get(f"choice_{index}")
    is_submitted = index in st.session_state["submitted"]

    st.markdown("**Options**")

    if is_submitted:
        chosen = st.session_state["answers"][index]
        for letter, text in question.options.items():
            if letter == question.answer:
                style, icon = OPTION_STYLE["correct"], "✓"
            elif letter == chosen:
                style, icon = OPTION_STYLE["wrong"], "✗"
            else:
                style, icon = OPTION_STYLE["neutral"], "○"
            st.markdown(
                f'<div style="{style}"><strong>{letter}.</strong> {icon} {text}</div>',
                unsafe_allow_html=True,
            )
    else:
        for letter, text in question.options.items():
            select_col, text_col = st.columns([1, 14], vertical_alignment="top")
            with select_col:
                if st.button(
                    "◉" if selected == letter else "○",
                    key=f"select_{index}_{letter}",
                    use_container_width=True,
                ):
                    st.session_state[f"choice_{index}"] = letter
                    st.rerun()
            with text_col:
                st.markdown(f"**{letter}.** {text}")

    st.markdown("")
    if not is_submitted:
        if st.button("Submit answer", type="primary", use_container_width=True):
            if not selected:
                st.warning("Select an option before submitting.")
            else:
                st.session_state["answers"][index] = selected
                st.session_state["submitted"][index] = True
                st.rerun()
    else:
        chosen_letter = st.session_state["answers"][index]
        if chosen_letter == question.answer:
            st.success(f"Correct! Answer: **{question.answer}**")
        else:
            st.error(
                f"Incorrect. Your answer: **{chosen_letter}** · Correct: **{question.answer}**"
            )
        st.info(f"**Key concept:** {question.concept}")
