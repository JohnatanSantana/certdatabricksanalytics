from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

QUIZ_FILES = {
    "Standard (40 questions)": ROOT_DIR / "data" / "quiz-data-analyst-associate.md",
    "Advanced (40 questions)": ROOT_DIR / "data" / "quiz-advanced.md",
}


@dataclass
class Question:
    number: int
    section: str
    objective: str
    prompt: str
    options: dict[str, str]
    answer: str
    concept: str
