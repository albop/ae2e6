#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tutorials/session_1/index_correction.qmd"
SUBJECT = ROOT / "tutorials/session_1/index.qmd"

OPEN_DIV_RE = re.compile(r"^:::\s*\{([^}]*)\}\s*$")
CORRECTION_CLASS = "correction-only"
SUBJECT_CLASS = "subject-only"


def split_front_matter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("Source file must start with YAML front matter.")

    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("Could not find end of YAML front matter.")

    front = text[4:end]
    body = text[end + 5 :]
    return front, body


def set_title(front: str, title: str) -> str:
    lines = front.splitlines()
    out = []
    replaced = False
    for line in lines:
        if line.startswith("title:"):
            out.append(f'title: "{title}"')
            replaced = True
        else:
            out.append(line)
    if not replaced:
        out.insert(0, f'title: "{title}"')
    return "\n".join(out)


def _parse_open_div(line: str) -> str | None:
    match = OPEN_DIV_RE.match(line.strip())
    if not match:
        return None

    attrs = match.group(1)
    classes = {token[1:] for token in attrs.split() if token.startswith(".")}

    if CORRECTION_CLASS in classes:
        return CORRECTION_CLASS
    if SUBJECT_CLASS in classes:
        return SUBJECT_CLASS
    return "other"


def render_profile(body: str, profile: str) -> str:
    if profile not in {"subject", "correction"}:
        raise ValueError("profile must be either 'subject' or 'correction'.")

    lines = body.splitlines(keepends=True)
    out: list[str] = []

    block_stack: list[str] = []

    for line in lines:
        stripped = line.strip()
        div_class = _parse_open_div(line)

        # Handle markdown fenced div markers.
        if div_class is not None:
            block_stack.append(div_class)
            if div_class in {CORRECTION_CLASS, SUBJECT_CLASS}:
                # Marker wrappers are removed in outputs.
                continue

        elif stripped == ":::" and block_stack:
            closed = block_stack.pop()
            if closed in {CORRECTION_CLASS, SUBJECT_CLASS}:
                continue

        in_subject_only = SUBJECT_CLASS in block_stack
        in_correction_only = CORRECTION_CLASS in block_stack

        # Profile-specific visibility.
        if profile == "subject" and in_correction_only:
            continue
        if profile == "correction" and in_subject_only:
            continue

        out.append(line)

    rendered = "".join(out)
    if profile == "subject":
        rendered = ensure_nonempty_python_cells(rendered)
    return rendered


def ensure_nonempty_python_cells(text: str) -> str:
    """Add a no-op statement to python fences that only contain Quarto options.

    Quarto option-only cells (e.g. only '#| echo: true') can disappear in ipynb
    export because they are effectively empty code cells.
    """
    lines = text.splitlines(keepends=True)
    out: list[str] = []

    in_py = False
    block_lines: list[str] = []

    for line in lines:
        stripped = line.strip()

        if not in_py and stripped.startswith("```{python"):
            in_py = True
            out.append(line)
            block_lines = []
            continue

        if in_py and stripped == "```":
            has_code = any(
                ln.strip() and not ln.lstrip().startswith("#|") for ln in block_lines
            )
            out.extend(block_lines)
            if not has_code:
                out.append("# TODO\n")
            out.append(line)
            in_py = False
            block_lines = []
            continue

        if in_py:
            block_lines.append(line)
        else:
            out.append(line)

    # If an unterminated python fence exists, flush buffered lines as-is.
    if in_py:
        out.extend(block_lines)

    return "".join(out)


def strip_leading_html_comments(text: str) -> str:
    lines = text.splitlines(keepends=True)
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith("<!--") and stripped.endswith("-->"):
            i += 1
            continue
        break

    return "".join(lines[i:])


def write_qmd(path: Path, front: str, body: str, note: str) -> None:
    clean_body = strip_leading_html_comments(body).lstrip()
    content = f"---\n{front}\n---\n\n<!-- {note} -->\n\n{clean_body}"
    path.write_text(content, encoding="utf-8")


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    front, body = split_front_matter(source_text)

    subject_front = set_title(front, "Bases de Python et processus VAR - Sujet")

    subject_body = render_profile(body, "subject")

    write_qmd(
        SUBJECT,
        subject_front,
        subject_body,
        "Auto-generated from tutorials/session_1/index_correction.qmd (subject version).",
    )


if __name__ == "__main__":
    main()
