#!/usr/bin/env python3
"""Render the assignment's Markdown into a printable, bookmarked PDF."""

from __future__ import annotations

import re
from html import escape
from pathlib import Path

import reportlab
from markdown_it import MarkdownIt
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak,
    HRFlowable,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "assignment-handbook.md"
OUTPUT = ROOT / "docs" / "assignment-handbook.pdf"
NAVY = colors.HexColor("#172B4D")
TEAL = colors.HexColor("#087F8C")
INK = colors.HexColor("#253348")
MUTED = colors.HexColor("#586779")


def make_styles():
    """Use ReportLab's bundled fonts so no system fonts are required."""
    font_dir = Path(reportlab.__file__).parent / "fonts"
    for name, filename in (
        ("Guide", "Vera.ttf"),
        ("Guide-Bold", "VeraBd.ttf"),
        ("Guide-Italic", "VeraIt.ttf"),
        ("Guide-BoldItalic", "VeraBI.ttf"),
    ):
        pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
    pdfmetrics.registerFontFamily(
        "Guide",
        normal="Guide",
        bold="Guide-Bold",
        italic="Guide-Italic",
        boldItalic="Guide-BoldItalic",
    )
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            "Body",
            fontName="Guide",
            fontSize=9.5,
            leading=13,
            textColor=INK,
            spaceAfter=6,
            splitLongWords=True,
            allowWidows=0,
            allowOrphans=0,
        )
    )
    styles.add(
        ParagraphStyle(
            "Chapter",
            parent=styles["Body"],
            fontName="Guide-Bold",
            fontSize=19,
            leading=24,
            textColor=NAVY,
            spaceAfter=12,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            "Section",
            parent=styles["Body"],
            fontName="Guide-Bold",
            fontSize=11,
            leading=14,
            textColor=TEAL,
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            "CodeBlock",
            fontName="Courier",
            fontSize=7.8,
            leading=10,
            textColor=NAVY,
            backColor=colors.HexColor("#F0F4F8"),
            borderPadding=8,
            spaceBefore=5,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            "ListBody", parent=styles["Body"], spaceAfter=3, leading=12.5
        )
    )
    styles.add(
        ParagraphStyle(
            "CoverTitle",
            parent=styles["Chapter"],
            fontSize=42,
            leading=48,
            spaceAfter=20,
        )
    )
    styles.add(
        ParagraphStyle(
            "CoverSubtitle",
            parent=styles["Body"],
            fontSize=19,
            leading=27,
            spaceAfter=18,
        )
    )
    styles.add(
        ParagraphStyle(
            "Label",
            parent=styles["Body"],
            fontName="Guide-Bold",
            fontSize=9,
            textColor=TEAL,
            spaceAfter=15,
        )
    )
    styles.add(
        ParagraphStyle(
            "ContentsEntry",
            parent=styles["Body"],
            fontSize=10,
            leading=15,
            spaceBefore=3,
            spaceAfter=0,
            leftIndent=0,
            firstLineIndent=0,
        )
    )
    return styles


def linked_text(text: str) -> str:
    parts = re.split(r"(https?://[^\s]+)", text)
    result = []
    for part in parts:
        if part.startswith(("https://", "http://")):
            url = part.rstrip(".,;")
            suffix = part[len(url) :]
            result.append(
                f'<link href="{escape(url, quote=True)}" color="#087F8C">'
                f"{escape(url)}</link>{escape(suffix)}"
            )
        else:
            result.append(escape(part))
    return "".join(result)


def inline(tokens) -> str:
    pieces = []
    in_link = False
    for token in tokens or []:
        kind = token.type
        if kind == "text":
            pieces.append(escape(token.content) if in_link else linked_text(token.content))
        elif kind == "code_inline":
            pieces.append(f'<font name="Courier" size="9">{escape(token.content)}</font>')
        elif kind == "strong_open":
            pieces.append("<b>")
        elif kind == "strong_close":
            pieces.append("</b>")
        elif kind == "em_open":
            pieces.append("<i>")
        elif kind == "em_close":
            pieces.append("</i>")
        elif kind == "link_open":
            href = escape(token.attrGet("href") or "", quote=True)
            pieces.append(f'<link href="{href}" color="#087F8C">')
            in_link = True
        elif kind == "link_close":
            pieces.append("</link>")
            in_link = False
        elif kind == "softbreak":
            pieces.append(" ")
        elif kind == "hardbreak":
            pieces.append("<br/>")
        else:
            raise ValueError(f"Unsupported inline Markdown token: {kind}")
    return "".join(pieces)


class MarkdownRenderer:
    def __init__(self, styles):
        self.styles = styles
        self.seen_chapter = False

    def blocks(self, tokens, index=0, stop=None, in_list=False):
        result = []
        while index < len(tokens):
            token = tokens[index]
            kind = token.type
            if kind == stop:
                return result, index + 1
            if kind == "heading_open":
                chapter = token.tag == "h1"
                if chapter and self.seen_chapter:
                    result.extend([CondPageBreak(3.5 * inch), Spacer(1, 16)])
                if chapter:
                    self.seen_chapter = True
                style = self.styles["Chapter" if chapter else "Section"]
                result.append(Paragraph(inline(tokens[index + 1].children), style))
                index += 3
            elif kind == "paragraph_open":
                style = self.styles["ListBody" if in_list else "Body"]
                result.append(Paragraph(inline(tokens[index + 1].children), style))
                index += 3
            elif kind in ("fence", "code_block"):
                result.append(Preformatted(token.content.rstrip("\n"), self.styles["CodeBlock"]))
                index += 1
            elif kind in ("bullet_list_open", "ordered_list_open"):
                ordered = kind == "ordered_list_open"
                close = "ordered_list_close" if ordered else "bullet_list_close"
                start = int(token.attrGet("start") or "1") if ordered else "bulletchar"
                items = []
                index += 1
                while tokens[index].type != close:
                    if tokens[index].type != "list_item_open":
                        raise ValueError("Expected a Markdown list item")
                    item, index = self.blocks(tokens, index + 1, "list_item_close", True)
                    items.append(ListItem(item))
                result.append(
                    ListFlowable(
                        items,
                        bulletType="1" if ordered else "bullet",
                        start=start,
                        leftIndent=18,
                        bulletFontName="Guide",
                        bulletFontSize=9,
                        bulletColor=TEAL,
                        spaceAfter=6,
                    )
                )
                index += 1
            elif kind == "hr":
                result.append(HRFlowable(width="100%", color=TEAL, spaceAfter=10))
                index += 1
            else:
                raise ValueError(f"Unsupported block Markdown token: {kind}")
        if stop is not None:
            raise ValueError(f"Unclosed Markdown block: {stop}")
        return result, index


class HandbookDocument(SimpleDocTemplate):
    def beforeDocument(self):
        self.chapter_number = 0

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == "Chapter":
            title = flowable.getPlainText()
            self.chapter_number += 1
            key = f"chapter-{self.chapter_number}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title, key, level=0)
            self.notify("TOCEntry", (0, title, self.page, key))


def page_furniture(canvas, doc):
    canvas.saveState()
    width, height = letter
    canvas.setTitle("tiny-kv: Rust Storage Engine Assignment Handbook")
    canvas.setAuthor("tiny-kv learning project")
    canvas.setSubject("A staged Rust, persistence, recovery, and performance assignment")
    if doc.page == 1:
        canvas.setFillColor(TEAL)
        canvas.rect(0, height - 0.22 * inch, width, 0.22 * inch, fill=1, stroke=0)
    else:
        canvas.setFont("Guide-Bold", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(doc.leftMargin, height - 0.38 * inch, "TINY-KV / ASSIGNMENT HANDBOOK")
        canvas.setStrokeColor(colors.HexColor("#D6E0E8"))
        canvas.line(doc.leftMargin, 0.48 * inch, width - doc.rightMargin, 0.48 * inch)
        canvas.setFont("Guide", 7.5)
        canvas.drawString(doc.leftMargin, 0.3 * inch, "Learn Rust. Build storage. Explain the evidence.")
        canvas.drawRightString(width - doc.rightMargin, 0.3 * inch, str(doc.page))
    canvas.restoreState()


def main():
    styles = make_styles()
    text = SOURCE.read_text(encoding="utf-8")
    tokens = MarkdownIt("commonmark").parse(text)
    body, _ = MarkdownRenderer(styles).blocks(tokens)
    contents = TableOfContents()
    contents.levelStyles = [styles["ContentsEntry"]]
    contents.dotsMinLevel = 0
    story = [
        Spacer(1, 0.75 * inch),
        Paragraph("SELF-DIRECTED SYSTEMS PROGRAMMING LAB", styles["Label"]),
        Paragraph("tiny-kv", styles["CoverTitle"]),
        Paragraph("Build a Persistent<br/>Key-Value Store in Rust", styles["CoverSubtitle"]),
        HRFlowable(width="25%", thickness=3, color=TEAL, hAlign="LEFT", spaceAfter=23),
        Paragraph(
            "A college-style assignment for learning Rust through a small, "
            "correct, durable, and measurable storage engine.",
            styles["Body"],
        ),
        Spacer(1, 0.3 * inch),
        Paragraph("THE LEARNING PATH", styles["Label"]),
        Paragraph(
            "Rust foundations / in-memory store / file persistence / "
            "append-only log / crash recovery / compaction / "
            "profiling and Linux / Mini-LSM",
            styles["Body"],
        ),
        Spacer(1, 0.45 * inch),
        Paragraph("19 sections / 7 assignments / 100-point rubric", styles["Body"]),
        Paragraph("Version 1.0 | October 15, 2026", styles["Body"]),
        Paragraph(
            "Start with the first-session checklist in section 18. "
            "Your first major milestone is file-backed put/get/delete.",
            styles["Body"],
        ),
        PageBreak(),
        Paragraph("Contents", styles["CoverSubtitle"]),
        Paragraph("Click a section title or use the PDF bookmarks to navigate.", styles["Body"]),
        contents,
        PageBreak(),
        *body,
    ]
    doc = HandbookDocument(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        pageCompression=1,
    )
    doc.multiBuild(story, onFirstPage=page_furniture, onLaterPages=page_furniture)
    pdf = PdfReader(OUTPUT)
    chapter_count = sum(t.type == "heading_open" and t.tag == "h1" for t in tokens)
    if len(pdf.outline) != chapter_count:
        raise RuntimeError("Generated PDF is missing chapter bookmarks")
    extracted = "\n".join(page.extract_text() or "" for page in pdf.pages)
    for heading in ("Project brief", "Assignment 7", "Final storage format", "Attribution"):
        if heading not in extracted:
            raise RuntimeError(f"Generated PDF is missing expected content: {heading}")
    if any(not (page.extract_text() or "").strip() for page in pdf.pages):
        raise RuntimeError("Generated PDF contains an empty page")
    print(f"Built {OUTPUT.relative_to(ROOT)}")
    print(f"{len(pdf.pages)} pages; {chapter_count} bookmarks; {OUTPUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
