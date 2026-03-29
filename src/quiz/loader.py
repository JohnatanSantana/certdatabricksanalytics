from __future__ import annotations

import re
from pathlib import Path

from schema.models import Question


def load_quiz(markdown_path: Path) -> list[Question]:
    content = markdown_path.read_text(encoding="utf-8")
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    questions_part, answer_key_part = content.split("# Answer Key", maxsplit=1)

    answer_rows = re.findall(
        r"\|\s*(\d+)\s*\|\s*([A-D])\s*\|\s*(.*?)\s*\|",
        answer_key_part,
    )
    answer_key = {int(n): (a, c) for n, a, c in answer_rows}

    sections = re.split(r"\n## ", questions_part)
    parsed: list[Question] = []

    for raw_section in sections:
        if not raw_section.strip():
            continue
        lines = raw_section.splitlines()
        if lines[0].startswith("# "):
            continue
        section_title = lines[0].strip()
        body = "\n".join(lines[1:])
        chunks = re.split(r"\n---\n\s*(?=\*\*Question \d+\*\*)", body)

        for chunk in chunks:
            number_match = re.search(r"\*\*Question (\d+)\*\*", chunk)
            objective_match = re.search(r"\*Objective: (.*?)\*", chunk, flags=re.DOTALL)
            if not number_match or not objective_match:
                continue

            number = int(number_match.group(1))
            objective = " ".join(objective_match.group(1).split())
            body_after = chunk[objective_match.end():].strip()

            option_positions = list(re.finditer(r"(?m)^(A|B|C|D)\.\s?", body_after))
            if len(option_positions) != 4:
                continue

            prompt = body_after[: option_positions[0].start()].strip()
            options: dict[str, str] = {}
            for pos, opt in enumerate(option_positions):
                letter = opt.group(1)
                start = opt.end()
                end = (
                    option_positions[pos + 1].start()
                    if pos + 1 < len(option_positions)
                    else len(body_after)
                )
                options[letter] = body_after[start:end].strip()

            answer, concept = answer_key[number]
            parsed.append(
                Question(
                    number=number,
                    section=section_title,
                    objective=objective,
                    prompt=prompt,
                    options=options,
                    answer=answer,
                    concept=concept,
                )
            )

    if not parsed:
        raise ValueError(
            f"No questions loaded from {markdown_path.name}. Check the Markdown format."
        )
    return parsed
