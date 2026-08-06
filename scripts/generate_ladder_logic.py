"""Generate the Rev J CLICK PLUS ladder programming reference PDF.

The authoritative ladder listing lives in section 7 of
Powermatic_1200_Retrofit_Documentation_rJ.md. This script renders that section
as a shop-friendly PDF so the PDF cannot drift from the markdown source.
"""

from __future__ import annotations

from pathlib import Path
import re
import textwrap

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS = PROJECT_ROOT / "docs"
SOURCE = DOCS / "Powermatic_1200_Retrofit_Documentation_rJ.md"
OUTPUT = DOCS / "05_ladder_logic_rJ.pdf"


def section_7() -> str:
    text = SOURCE.read_text(encoding="utf-8")
    match = re.search(r"^## 7\. Ladder logic.*?^---\n", text, re.M | re.S)
    if not match:
        raise RuntimeError("Could not find section 7 ladder logic block")
    return match.group(0)


def plain(text: str) -> str:
    replacements = {
        "—": "-",
        "–": "-",
        "→": "->",
        "≥": ">=",
        "≤": "<=",
        "≈": "~",
        "¬": "NOT ",
        "∧": "AND",
        "∨": "OR",
        "─": "-",
        "│": "|",
        "┬": "+",
        "┴": "+",
        "└": "+",
        "┘": "+",
        "┤": "+",
        "├": "+",
        "↑": "UP",
        "↓": "DN",
        "…": "...",
        "§": "section ",
        "×": "x",
        "°": " deg ",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = re.sub(r"^```.*?$", "", text, flags=re.M)
    text = text.replace("`", "")
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    return text


def wrapped_lines(text: str, width: int = 96) -> list[str]:
    out: list[str] = []
    for raw in text.splitlines():
        line = raw.rstrip()
        if len(line) <= width:
            out.append(line)
            continue
        indent = len(line) - len(line.lstrip(" "))
        prefix = " " * indent
        out.extend(
            textwrap.wrap(
                line,
                width=width,
                subsequent_indent=prefix + "  ",
                break_long_words=False,
                break_on_hyphens=False,
            )
        )
    return out


def draw_pdf(lines: list[str]) -> None:
    c = canvas.Canvas(str(OUTPUT), pagesize=letter)
    width, height = letter
    left = 0.45 * inch
    top = height - 0.42 * inch
    bottom = 0.45 * inch
    line_height = 8.3
    page_no = 1

    def header() -> float:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(left, height - 0.28 * inch, "Powermatic 1200 retrofit - CLICK PLUS ladder logic")
        c.drawRightString(width - left, height - 0.28 * inch, "Rev J - generated from section 7")
        c.setFont("Courier", 7)
        return top - 0.1 * inch

    y = header()
    c.setFont("Courier", 7)
    for line in lines:
        if y < bottom:
            c.setFont("Helvetica", 7)
            c.drawRightString(width - left, 0.24 * inch, f"Sheet {page_no}")
            c.showPage()
            page_no += 1
            y = header()
            c.setFont("Courier", 7)
        c.drawString(left, y, line[:120])
        y -= line_height

    c.setFont("Helvetica", 7)
    c.drawRightString(width - left, 0.24 * inch, f"Sheet {page_no}")
    c.save()


def main() -> None:
    text = plain(section_7())
    lines = [
        "POWERMATIC 1200 RETROFIT - CLICK PLUS LADDER LOGIC",
        "",
        "Programming reference generated from Powermatic_1200_Retrofit_Documentation_rJ.md section 7.",
        "Key Rev J jog rules: any STOP press exits jog; drum OFF inhibits motion but not jog mode;",
        "the 5 s FWD entry hold is consumed by C50 and cannot command spindle motion.",
        "",
    ]
    lines.extend(wrapped_lines(text))
    draw_pdf(lines)


if __name__ == "__main__":
    main()
