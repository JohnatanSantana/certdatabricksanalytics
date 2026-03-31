from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Generator

ROOT_DIR = Path(__file__).resolve().parents[2]
DB_PATH = ROOT_DIR / "data" / "quiz_history.db"


@contextmanager
def _connect(path: Path = DB_PATH) -> Generator[sqlite3.Connection, None, None]:
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        yield conn


def init_db(path: Path = DB_PATH) -> None:
    with sqlite3.connect(path) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at  TEXT NOT NULL,
                finished_at TEXT NOT NULL,
                score       INTEGER NOT NULL,
                total       INTEGER NOT NULL,
                pct         REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS answers (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id      INTEGER NOT NULL REFERENCES sessions(id),
                question_number INTEGER NOT NULL,
                section         TEXT NOT NULL,
                chosen          TEXT,
                correct_answer  TEXT NOT NULL,
                is_correct      INTEGER NOT NULL
            );
        """)


def save_session(
    started_at: str,
    answers: dict[int, str],
    questions: list,
) -> int:
    finished_at = datetime.now().isoformat(timespec="seconds")
    score = sum(1 for idx, ch in answers.items() if ch == questions[idx].answer)
    total = len(questions)
    pct = round(score / total * 100, 1) if total else 0.0

    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO sessions (started_at, finished_at, score, total, pct) VALUES (?,?,?,?,?)",
            (started_at, finished_at, score, total, pct),
        )
        session_id = cur.lastrowid
        conn.executemany(
            "INSERT INTO answers"
            " (session_id, question_number, section, chosen, correct_answer, is_correct)"
            " VALUES (?,?,?,?,?,?)",
            [
                (
                    session_id,
                    q.number,
                    q.section,
                    answers.get(idx),
                    q.answer,
                    int(answers.get(idx) == q.answer),
                )
                for idx, q in enumerate(questions)
            ],
        )
    return session_id


def load_sessions(limit: int = 15) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, started_at, finished_at, score, total, pct"
            " FROM sessions ORDER BY finished_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


def load_section_stats(session_id: int) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT section,"
            "  SUM(is_correct) AS correct,"
            "  COUNT(*) AS total"
            " FROM answers WHERE session_id=? AND chosen IS NOT NULL"
            " GROUP BY section ORDER BY section",
            (session_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def load_session_answers(session_id: int) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT question_number, section, chosen, correct_answer, is_correct"
            " FROM answers WHERE session_id=?"
            " ORDER BY question_number",
            (session_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def load_session(session_id: int) -> dict | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, started_at, finished_at, score, total, pct"
            " FROM sessions WHERE id=?",
            (session_id,),
        ).fetchone()
    return dict(row) if row else None
