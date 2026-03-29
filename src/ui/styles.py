from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

OPTION_STYLE: dict[str, str] = {
    "correct": (
        "background:#d4edda;border-left:4px solid #28a745;"
        "padding:10px 14px;border-radius:6px;margin:5px 0;color:#155724"
    ),
    "wrong": (
        "background:#f8d7da;border-left:4px solid #dc3545;"
        "padding:10px 14px;border-radius:6px;margin:5px 0;color:#721c24"
    ),
    "neutral": (
        "background:#f8f9fa;border-left:4px solid #ced4da;"
        "padding:10px 14px;border-radius:6px;margin:5px 0;color:#495057"
    ),
}


def inject_global_css() -> None:
    st.markdown(
        """
        <style>
        .stMarkdown p, .stMarkdown li { line-height: 1.6; overflow-wrap: anywhere; }
        div[data-testid="stMetricValue"] { font-size: 1.3rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def scroll_to_anchor(anchor_id: str) -> None:
    components.html(
        f"""
        <script>
        (function() {{
            var main = window.parent.document.querySelector('[data-testid="stMain"]')
                    || window.parent.document.querySelector('.main');
            if (!main) return;
            function doScroll() {{
                var el = window.parent.document.getElementById('{anchor_id}');
                if (!el) return;
                var elTop  = el.getBoundingClientRect().top;
                var mainTop = main.getBoundingClientRect().top;
                main.scrollTop = main.scrollTop + elTop - mainTop - 8;
            }}
            setTimeout(doScroll, 80);
        }})();
        </script>
        """,
        height=0,
    )


def scroll_to_top() -> None:
    components.html(
        """
        <script>
        (function() {
            var el = window.parent.document.querySelector('[data-testid="stMain"]')
                  || window.parent.document.querySelector('.main');
            if (el) el.scrollTop = 0;
        })();
        </script>
        """,
        height=0,
    )
