#!/usr/bin/env python3
"""Build the September 2026 Government AI Navigator PDF from index.html product data."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Frame,
    KeepTogether,
    ListFlowable,
    ListItem,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Flowable,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from navigator_pdf_copy import GENERIC_QUESTIONS, QUESTIONS, RATIONALE

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
LOGO_SRC = ROOT / "avero-logo.png"
# Write outside the static site root. DigitalOcean publishes the repo as-is;
# a PDF under public/ (or anywhere else in the tree) would be world-downloadable.
OUT_PDF = ROOT / "artifacts" / "Avero_Start-at-Zero_Government-AI-Navigator_Sep2026.pdf"
LOGO_CLEAR = Path("/tmp/avero-logo-transparent.png")

NAVY = HexColor("#0B1120")
NAVY2 = HexColor("#0F172A")
INK = HexColor("#1B2A4A")
GOLD = HexColor("#C4883C")
GOLD_SOFT = HexColor("#C9A46C")
CREAM = HexColor("#F0EBE3")
CREAM2 = HexColor("#E2D9CA")
MUTED = HexColor("#5C6B7A")
RULE = HexColor("#D4CBBC")
PALE = HexColor("#F7F4EE")
GREEN = HexColor("#0F766E")
BLUE = HexColor("#1D4E89")

LENS_META = {
    "readiness": {
        "title": "Readiness × Capability",
        "question": "Can I buy it, and what does it do?",
        "x": "Government readiness →",
        "y": "↑ Capability depth",
        "x_desc": "StateRAMP/FedRAMP where publicly documented, cooperative vehicles, SLED references",
        "y_desc": "Narrow point solution → broad platform",
        "labels": {
            "tl": ("High potential, high risk", "Powerful, procurement still hard for SLED"),
            "tr": ("Government-ready leaders", "Strong capability and a path to buy"),
            "bl": ("Emerging bets", "Early, thin SLED track record"),
            "br": ("Safe but limited", "Easy to buy, narrow use"),
        },
    },
    "impact": {
        "title": "Complexity × Impact",
        "question": "What will it take, and what will I get?",
        "x": "Implementation complexity →",
        "y": "↑ Mission impact",
        "x_desc": "Plug-and-play → deep integration and change management",
        "y_desc": "Staff efficiency → resident or student outcomes",
        "labels": {
            "tl": ("Quick wins", "High impact, faster to stand up"),
            "tr": ("Strategic transformers", "High impact, major investment"),
            "bl": ("Easy adds", "Simple deploy, incremental value"),
            "br": ("Heavy lifts", "Hard to implement, limited payoff"),
        },
    },
    "independence": {
        "title": "Independence × Maturity",
        "question": "Am I getting locked in?",
        "x": "Vendor independence →",
        "y": "↑ Gov market maturity",
        "x_desc": "Proprietary / hard to leave → portable data and alternatives",
        "y_desc": "Emerging → established at SLED scale",
        "labels": {
            "tl": ("Established but locked", "Proven, expensive to unwind"),
            "tr": ("Open and proven", "Mature with a realistic exit"),
            "bl": ("Risky bets", "New and proprietary"),
            "br": ("Flexible but unproven", "Open, thin SLED history"),
        },
    },
}

QUAD_COLOR = {
    "tl": HexColor("#1D4E89"),
    "tr": HexColor("#0F766E"),
    "bl": HexColor("#B45309"),
    "br": HexColor("#9A3412"),
}


def register_fonts() -> None:
    base = Path("/usr/share/fonts/truetype/macos")
    pdfmetrics.registerFont(TTFont("Inter", str(base / "Inter-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Inter-Med", str(base / "Inter-Medium.ttf")))
    pdfmetrics.registerFont(TTFont("Inter-Semi", str(base / "Inter-SemiBold.ttf")))
    pdfmetrics.registerFont(TTFont("Inter-Bold", str(base / "Inter-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Inter-Italic", str(base / "Inter-Italic.ttf")))
    pdfmetrics.registerFontFamily(
        "Inter",
        normal="Inter",
        bold="Inter-Bold",
        italic="Inter-Italic",
        boldItalic="Inter-Bold",
    )


def extract_tools() -> list[dict]:
    js = r"""
const fs = require('fs');
const html = fs.readFileSync(process.argv[1], 'utf8');
const m = html.match(/const TOOLS = (\[[\s\S]*?\n    \];)/);
if (!m) { process.stderr.write('TOOLS not found\n'); process.exit(1); }
const tools = new Function('return ' + m[1])();
process.stdout.write(JSON.stringify(tools));
"""
    proc = subprocess.run(
        ["node", "-e", js, str(INDEX)],
        check=True,
        capture_output=True,
        text=True,
    )
    tools = json.loads(proc.stdout)
    if len(tools) != 43:
        raise SystemExit(f"Expected 43 products, found {len(tools)}")
    missing_q = [t["name"] for t in tools if t["name"] not in QUESTIONS]
    if missing_q:
        raise SystemExit(f"Missing procurement questions for: {missing_q}")
    return tools


def prepare_logo() -> str:
    im = PILImage.open(LOGO_SRC).convert("RGBA")
    pixels = im.load()
    width, height = im.size
    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            if r < 40 and g < 40 and b < 40:
                pixels[x, y] = (r, g, b, 0)
    im.save(LOGO_CLEAR)
    return str(LOGO_CLEAR)


def quad_key(x: float, y: float) -> str:
    return ("t" if y >= 50 else "b") + ("l" if x < 50 else "r")


def placement_name(lens_id: str, x: float, y: float) -> str:
    return LENS_META[lens_id]["labels"][quad_key(x, y)][0]


def default_rationale(tool: dict) -> str:
    r = placement_name("readiness", *tool["pos"]["readiness"])
    i = placement_name("impact", *tool["pos"]["impact"])
    n = placement_name("independence", *tool["pos"]["independence"])
    return (
        f"Avero places {tool['name']} in “{r}” on readiness × capability, "
        f"“{i}” on complexity × impact, and “{n}” on independence × maturity. "
        f"{tool['notes']['independence']}"
    )


def styles() -> dict:
    ss = getSampleStyleSheet()
    s = {}
    s["kicker"] = ParagraphStyle(
        "kicker", parent=ss["Normal"], fontName="Inter-Semi", fontSize=8.5,
        textColor=GOLD, tracking=1.4, leading=12, spaceAfter=4,
    )
    s["h1"] = ParagraphStyle(
        "h1", parent=ss["Normal"], fontName="Inter-Bold", fontSize=22,
        textColor=INK, leading=26, spaceAfter=10, spaceBefore=2,
    )
    s["h2"] = ParagraphStyle(
        "h2", parent=ss["Normal"], fontName="Inter-Bold", fontSize=14.5,
        textColor=INK, leading=18, spaceBefore=12, spaceAfter=6,
    )
    s["h3"] = ParagraphStyle(
        "h3", parent=ss["Normal"], fontName="Inter-Semi", fontSize=11,
        textColor=INK, leading=14, spaceBefore=8, spaceAfter=4,
    )
    s["body"] = ParagraphStyle(
        "body", parent=ss["Normal"], fontName="Inter", fontSize=9.6,
        textColor=INK, leading=13.4, alignment=TA_JUSTIFY, spaceAfter=7,
    )
    s["bodyleft"] = ParagraphStyle(
        "bodyleft", parent=s["body"], alignment=TA_LEFT,
    )
    s["small"] = ParagraphStyle(
        "small", parent=ss["Normal"], fontName="Inter", fontSize=8.4,
        textColor=MUTED, leading=11.4, spaceAfter=4,
    )
    s["caption"] = ParagraphStyle(
        "caption", parent=ss["Normal"], fontName="Inter-Med", fontSize=8,
        textColor=MUTED, leading=10.5,
    )
    s["prod"] = ParagraphStyle(
        "prod", parent=ss["Normal"], fontName="Inter-Bold", fontSize=15,
        textColor=INK, leading=18, spaceAfter=1,
    )
    s["cat"] = ParagraphStyle(
        "cat", parent=ss["Normal"], fontName="Inter-Semi", fontSize=8,
        textColor=GOLD, leading=11, spaceAfter=6,
    )
    s["note_lbl"] = ParagraphStyle(
        "note_lbl", parent=ss["Normal"], fontName="Inter-Bold", fontSize=8.5,
        textColor=BLUE, leading=11, spaceBefore=4, spaceAfter=1,
    )
    s["note"] = ParagraphStyle(
        "note", parent=ss["Normal"], fontName="Inter", fontSize=9,
        textColor=INK, leading=12.4, spaceAfter=4, alignment=TA_LEFT,
    )
    s["q"] = ParagraphStyle(
        "q", parent=ss["Normal"], fontName="Inter", fontSize=9,
        textColor=INK, leading=12.2,
    )
    s["toc"] = ParagraphStyle(
        "toc", parent=ss["Normal"], fontName="Inter", fontSize=10.5,
        textColor=INK, leading=16, leftIndent=8,
    )
    s["center"] = ParagraphStyle(
        "center", parent=ss["Normal"], fontName="Inter", fontSize=10,
        textColor=CREAM, leading=14, alignment=TA_CENTER,
    )
    s["cell"] = ParagraphStyle(
        "cell", parent=ss["Normal"], fontName="Inter", fontSize=8.2,
        textColor=INK, leading=11,
    )
    s["cellb"] = ParagraphStyle(
        "cellb", parent=ss["Normal"], fontName="Inter-Semi", fontSize=8.2,
        textColor=INK, leading=11,
    )
    s["cellhdr"] = ParagraphStyle(
        "cellhdr", parent=ss["Normal"], fontName="Inter-Semi", fontSize=8,
        textColor=CREAM, leading=11,
    )
    s["newbadge"] = ParagraphStyle(
        "newbadge", parent=ss["Normal"], fontName="Inter-Bold", fontSize=7.5,
        textColor=HexColor("#1E40AF"), leading=10,
    )
    s["callout"] = ParagraphStyle(
        "callout", parent=ss["Normal"], fontName="Inter", fontSize=9.2,
        textColor=INK, leading=12.8, alignment=TA_LEFT,
    )
    s["cover_sub"] = ParagraphStyle(
        "cover_sub", parent=ss["Normal"], fontName="Inter", fontSize=12,
        textColor=CREAM, leading=17, alignment=TA_LEFT,
    )
    return s


class GoldRule(Flowable):
    def __init__(self, width=None, stroke=GOLD, thickness=1.1):
        super().__init__()
        self._width = width
        self.stroke = stroke
        self.thickness = thickness
        self.height = 8

    def wrap(self, aw, ah):
        self.width = self._width or aw
        return self.width, self.height

    def draw(self):
        self.canv.setStrokeColor(self.stroke)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 4, self.width, 4)


class Callout(Flowable):
    def __init__(self, title: str, body: str, width_hint: float = 7.1 * inch):
        super().__init__()
        self.title = title
        self.body = body
        self.width_hint = width_hint
        self._content = None

    def wrap(self, aw, ah):
        self.width = aw
        inner = aw - 16
        st = styles()
        title_p = Paragraph(self.title, st["h3"])
        body_p = Paragraph(self.body, st["callout"])
        tw, th = title_p.wrap(inner, ah)
        bw, bh = body_p.wrap(inner, ah)
        self._content = (title_p, body_p, th, bh)
        self.height = th + bh + 20
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(HexColor("#FBF6EC"))
        c.setStrokeColor(GOLD)
        c.setLineWidth(1)
        c.roundRect(0, 0, self.width, self.height, 5, fill=1, stroke=1)
        c.setFillColor(GOLD)
        c.rect(0, 0, 4, self.height, fill=1, stroke=0)
        title_p, body_p, th, bh = self._content
        title_p.drawOn(c, 12, self.height - 10 - th)
        body_p.drawOn(c, 12, 8)


class MiniQuad(Flowable):
    """Small 2×2 with a dot for one lens."""

    def __init__(self, lens_id: str, xy: list, label: str):
        super().__init__()
        self.lens_id = lens_id
        self.xy = xy
        self.label = label
        self.width = 2.3 * inch
        self.height = 1.55 * inch

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c = self.canv
        meta = LENS_META[self.lens_id]
        x, y = self.xy
        pad = 14
        plot = 72
        left = 18
        bottom = 22
        fills = {
            "tl": Color(0.12, 0.31, 0.54, alpha=0.12),
            "tr": Color(0.06, 0.46, 0.43, alpha=0.12),
            "bl": Color(0.71, 0.33, 0.04, alpha=0.10),
            "br": Color(0.60, 0.20, 0.07, alpha=0.10),
        }
        half = plot / 2
        c.setFillColor(fills["tl"])
        c.rect(left, bottom + half, half, half, fill=1, stroke=0)
        c.setFillColor(fills["tr"])
        c.rect(left + half, bottom + half, half, half, fill=1, stroke=0)
        c.setFillColor(fills["bl"])
        c.rect(left, bottom, half, half, fill=1, stroke=0)
        c.setFillColor(fills["br"])
        c.rect(left + half, bottom, half, half, fill=1, stroke=0)
        c.setStrokeColor(HexColor("#C5BBAE"))
        c.setLineWidth(0.6)
        c.rect(left, bottom, plot, plot, fill=0, stroke=1)
        c.setDash(2, 2)
        c.line(left + half, bottom, left + half, bottom + plot)
        c.line(left, bottom + half, left + plot, bottom + half)
        c.setDash()
        dx = left + (x / 100) * plot
        dy = bottom + (y / 100) * plot
        c.setFillColor(GOLD)
        c.circle(dx, dy, 4.2, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.circle(dx, dy, 2.2, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Inter-Semi", 7)
        c.drawString(left, bottom + plot + 6, meta["title"])
        c.setFillColor(MUTED)
        c.setFont("Inter", 6.2)
        c.drawCentredString(left + plot / 2, bottom - 10, meta["x"].replace("→", "").strip())
        qk = quad_key(x, y)
        c.setFillColor(QUAD_COLOR[qk])
        c.setFont("Inter-Semi", 6.4)
        c.drawString(left + plot + 8, bottom + plot - 10, meta["labels"][qk][0])


class QuadRow(Flowable):
    def __init__(self, tool: dict):
        super().__init__()
        self.tool = tool
        self.kids = [
            MiniQuad("readiness", tool["pos"]["readiness"], "R"),
            MiniQuad("impact", tool["pos"]["impact"], "I"),
            MiniQuad("independence", tool["pos"]["independence"], "N"),
        ]

    def wrap(self, aw, ah):
        self.width = aw
        self.height = 1.55 * inch
        return self.width, self.height

    def draw(self):
        gap = (self.width - 3 * self.kids[0].width) / 2
        x = 0
        for kid in self.kids:
            kid.canv = self.canv
            self.canv.saveState()
            self.canv.translate(x, 0)
            kid.draw()
            self.canv.restoreState()
            x += kid.width + gap


def draw_cover(c: Canvas, doc) -> None:
    w, h = letter
    c.setFillColor(NAVY)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    # cream brand band
    c.setFillColor(CREAM)
    c.rect(0, h - 1.35 * inch, w, 1.35 * inch, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, h - 1.35 * inch - 4, w, 4, fill=1, stroke=0)
    logo = str(LOGO_CLEAR)
    c.drawImage(logo, 0.7 * inch, h - 1.22 * inch, width=2.15 * inch, height=1.02 * inch,
                mask="auto", preserveAspectRatio=True, anchor="c")
    c.setFillColor(INK)
    c.setFont("Inter-Semi", 9)
    c.drawRightString(w - 0.7 * inch, h - 0.62 * inch, "Start at Zero")
    c.setFont("Inter", 8)
    c.setFillColor(HexColor("#5A4A32"))
    c.drawRightString(w - 0.7 * inch, h - 0.82 * inch, "Buyer-side advisory")

    y = h - 2.15 * inch
    c.setFillColor(GOLD)
    c.setFont("Inter-Semi", 9)
    c.drawString(0.7 * inch, y, "SEPTEMBER 2026  ·  43 PRODUCTS")
    y -= 36
    c.setFillColor(white)
    c.setFont("Inter-Bold", 28)
    c.drawString(0.7 * inch, y, "Government AI Navigator")
    y -= 28
    c.setFont("Inter", 13)
    c.setFillColor(CREAM)
    c.drawString(0.7 * inch, y, "Independent map for state and local leaders")
    y -= 22
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(0.7 * inch, y, 2.6 * inch, y)
    y -= 28
    c.setFont("Inter", 11)
    c.setFillColor(HexColor("#D6D3CD"))
    for line in [
        "Three lenses every government leader needs before investing in AI:",
        "readiness, impact, and lock-in.",
    ]:
        c.drawString(0.7 * inch, y, line)
        y -= 16
    y -= 10
    boxes = [
        ("01", "Can I buy it,", "and what does it do?"),
        ("02", "What will it take,", "and what will I get?"),
        ("03", "Am I getting", "locked in?"),
    ]
    bx = 0.7 * inch
    for num, a, b in boxes:
        c.setFillColor(NAVY2)
        c.setStrokeColor(HexColor("#2A3344"))
        c.roundRect(bx, y - 58, 2.2 * inch, 72, 6, fill=1, stroke=1)
        c.setFillColor(GOLD)
        c.setFont("Inter-Bold", 9)
        c.drawString(bx + 12, y + 2, num)
        c.setFillColor(white)
        c.setFont("Inter-Semi", 9)
        c.drawString(bx + 12, y - 18, a)
        c.drawString(bx + 12, y - 32, b)
        bx += 2.38 * inch

    y -= 88
    c.setFillColor(GOLD_SOFT)
    c.setFont("Inter-Semi", 9)
    c.drawString(0.7 * inch, y, "Buyer-side. No vendor money.")
    y -= 16
    c.setFillColor(HexColor("#94A3B8"))
    c.setFont("Inter", 9)
    c.drawString(0.7 * inch, y, "Caliber is Avero methodology — beta, not sold or licensed, not a dot on the map.")

    # Contents strip
    band_h = 1.72 * inch
    c.setFillColor(HexColor("#151C2C"))
    c.roundRect(0.7 * inch, 0.78 * inch, w - 1.4 * inch, band_h, 8, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.roundRect(0.7 * inch, 0.78 * inch, w - 1.4 * inch, band_h, 8, fill=0, stroke=1)
    c.setFillColor(GOLD)
    c.setFont("Inter-Semi", 8)
    c.drawString(0.92 * inch, 0.78 * inch + band_h - 18, "INSIDE THIS EDITION")
    c.setFillColor(CREAM)
    c.setFont("Inter", 9)
    lines = [
        "How to read the three lenses  ·  scoring notes, placement rationale, and procurement questions",
        "Full directory of 43 products  ·  Caliber methodology rail (not a vendor SKU)",
        "File:  Avero_Start-at-Zero_Government-AI-Navigator_Sep2026.pdf",
        "Interactive map:  govai.averoadvisors.com",
    ]
    ly = 0.78 * inch + band_h - 38
    for line in lines:
        c.drawString(0.92 * inch, ly, line)
        ly -= 15

    c.setFillColor(HexColor("#64748B"))
    c.setFont("Inter", 8)
    c.drawString(0.7 * inch, 0.48 * inch, "Avero Advisors  ·  Independent analysis  ·  Not affiliated with any vendor listed")
    c.setFont("Inter", 7.5)
    c.drawString(0.7 * inch, 0.32 * inch, "© 2026 Avèro Advisors")


def draw_interior(c: Canvas, doc) -> None:
    w, h = letter
    if doc.page == 1:
        return
    c.setFillColor(CREAM)
    c.rect(0, h - 0.42 * inch, w, 0.42 * inch, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, h - 0.42 * inch - 2, w, 2, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Inter-Semi", 8)
    c.drawString(0.7 * inch, h - 0.28 * inch, "Government AI Navigator")
    c.setFillColor(MUTED)
    c.setFont("Inter", 8)
    c.drawRightString(w - 0.7 * inch, h - 0.28 * inch, "September 2026  ·  43 products")
    c.setFillColor(CREAM)
    c.rect(0, 0, w, 0.42 * inch, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, 0.42 * inch, w, 1.5, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont("Inter", 7.2)
    c.drawString(0.7 * inch, 0.22 * inch, "Avero Advisors  ·  Independent analysis  ·  Not affiliated with any vendor listed")
    c.setFont("Inter-Semi", 8)
    c.setFillColor(INK)
    c.drawRightString(w - 0.7 * inch, 0.22 * inch, str(doc.page))
    c.setFont("Inter", 6.5)
    c.setFillColor(HexColor("#8A8074"))
    c.drawCentredString(w / 2, 0.08 * inch, "© 2026 Avèro Advisors  ·  Positions are an independent read — verify compliance claims on the vendor’s current public page")


def bookmark(canvas, title, key):
    canvas.bookmarkPage(key)
    canvas.addOutlineEntry(title, key, 0, 0)


class Bookmark(Flowable):
    def __init__(self, title: str, key: str, level: int = 0):
        super().__init__()
        self.title = title
        self.key = key
        self.level = level
        self.width = 0
        self.height = 0

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        self.canv.bookmarkPage(self.key)
        self.canv.addOutlineEntry(self.title, self.key, self.level, 0)


def product_block(tool: dict, st: dict) -> list:
    name = tool["name"]
    cat = tool["category"]
    new = bool(tool.get("added"))
    header_bits = [Paragraph(name, st["prod"])]
    catline = cat.upper() + ("  ·  NEW THIS EDITION" if new else "")
    header_bits.append(Paragraph(catline, st["cat"]))
    header_bits.append(GoldRule(thickness=0.8))
    header_bits.append(Spacer(1, 6))
    header_bits.append(QuadRow(tool))
    header_bits.append(Spacer(1, 8))

    rows = [["Lens", "Placement", "X", "Y"]]
    for lens_id, xlabel, ylabel in [
        ("readiness", "Readiness", "Capability"),
        ("impact", "Complexity", "Impact"),
        ("independence", "Independence", "Maturity"),
    ]:
        x, y = tool["pos"][lens_id]
        rows.append([
            Paragraph(LENS_META[lens_id]["title"], st["cellb"]),
            Paragraph(placement_name(lens_id, x, y), st["cell"]),
            Paragraph(f"{x:.0f}", st["cell"]),
            Paragraph(f"{y:.0f}", st["cell"]),
        ])
    table = Table(rows, colWidths=[2.35 * inch, 3.15 * inch, 0.7 * inch, 0.7 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("TEXTCOLOR", (0, 0), (-1, 0), CREAM),
        ("FONTNAME", (0, 0), (-1, 0), "Inter-Semi"),
        ("FONTSIZE", (0, 0), (-1, 0), 7.5),
        ("BACKGROUND", (0, 1), (-1, -1), PALE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.3, RULE),
        ("ALIGN", (2, 1), (-1, -1), "CENTER"),
    ]))
    header_bits.append(table)
    header_bits.append(Spacer(1, 8))
    header_bits.append(Paragraph("Placement rationale", st["h3"]))
    header_bits.append(Paragraph(RATIONALE.get(name, default_rationale(tool)), st["bodyleft"]))

    rest = []
    rest.append(Paragraph("Scoring notes", st["h3"]))
    rest.append(Paragraph("Readiness × capability", st["note_lbl"]))
    rest.append(Paragraph(tool["notes"]["readiness"], st["note"]))
    rest.append(Paragraph("Complexity × impact", st["note_lbl"]))
    rest.append(Paragraph(tool["notes"]["impact"], st["note"]))
    rest.append(Paragraph("Independence × maturity", st["note_lbl"]))
    rest.append(Paragraph(tool["notes"]["independence"], st["note"]))
    rest.append(Paragraph("Procurement questions", st["h3"]))
    qs = QUESTIONS.get(name, GENERIC_QUESTIONS)
    items = [ListItem(Paragraph(q, st["q"]), leftIndent=8, value="•") for q in qs]
    rest.append(ListFlowable(items, bulletType="bullet", start="•", leftIndent=12, spaceBefore=0, spaceAfter=6))
    rest.append(Paragraph(
        "Scores are 0–100 Avero placements on each axis, not vendor grades. "
        "Verify every compliance claim on the vendor’s current public page before you buy.",
        st["small"],
    ))
    rest.append(Spacer(1, 10))
    return [Bookmark(name, f"p-{name}", 1), KeepTogether(header_bits), *rest]


def build() -> Path:
    register_fonts()
    prepare_logo()
    tools = extract_tools()
    st = styles()
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)

    doc = BaseDocTemplate(
        str(OUT_PDF),
        pagesize=letter,
        title='"Start at Zero" Government AI Navigator — September 2026',
        author="Avero Advisors",
        subject="Independent map of 43 AI products for state and local leaders. Buyer-side. No vendor money.",
        creator="Avero Advisors / Start at Zero",
    )
    cover_frame = Frame(0, 0, letter[0], letter[1], 0, 0, 0, 0, id="cover")
    interior_frame = Frame(
        0.7 * inch, 0.55 * inch, letter[0] - 1.4 * inch, letter[1] - 1.12 * inch,
        0, 0, 0, 0, id="body",
    )
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=draw_cover),
        PageTemplate(id="interior", frames=[interior_frame], onPage=draw_interior),
    ])

    story = []
    story.append(NextPageTemplate("interior"))
    story.append(PageBreak())

    # Contents / how to use
    story.append(Bookmark("How to use this report", "toc"))
    story.append(Paragraph("HOW TO USE THIS REPORT", st["kicker"]))
    story.append(Paragraph("A buyer’s map, not a vendor catalog", st["h1"]))
    story.append(GoldRule())
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "This September 2026 edition of the Government AI Navigator is the printable companion "
        "to the interactive map at govai.averoadvisors.com. It is written for state, local, "
        "and education leaders who are being sold “AI” faster than procurement, records, and "
        "policy can absorb it. Avero sits on the buyer’s side. No vendor paid for placement. "
        "Caliber is Avero methodology — not a product on the map.",
        st["body"],
    ))
    story.append(Paragraph(
        "The live site plots <b>43 products</b> across three lenses. This PDF adds what the "
        "scatter cannot hold: scoring notes, placement rationale, and procurement questions "
        "for every product, plus an honest Caliber methodology section (beta, not sold or licensed).",
        st["body"],
    ))
    story.append(Paragraph("What’s inside", st["h2"]))
    for line in [
        "How to read the three lenses — the same axes as the interactive map.",
        "What’s new in this edition — 11 net-new products and the OpenAI split.",
        "Product directory — scoring notes, rationale, and questions, grouped by category.",
        "Caliber — how Avero scores engagements, and what it is not.",
        "Before you buy — Phase Zero, from Start at Zero.",
    ]:
        story.append(Paragraph("•  " + line, st["toc"]))
    story.append(Spacer(1, 8))
    story.append(Callout(
        "How to read a score",
        "Each axis is 0–100. They are Avero’s independent September 2026 placements, not "
        "benchmarks, not lab tests, and not a substitute for your own due diligence. "
        "A product in “Government-ready leaders” can still be the wrong buy for your estate. "
        "A product in “Emerging bets” can still be the right narrow tool. Use the questions.",
    ))

    story.append(PageBreak())
    story.append(Bookmark("How to read the three lenses", "lenses"))
    story.append(Paragraph("THE THREE LENSES", st["kicker"]))
    story.append(Paragraph("How to read the map", st["h1"]))
    story.append(GoldRule())
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Every product is placed on three independent 2×2s. Clicking a dot on the website "
        "pins the same notes printed here. Caliber is not on any scatter — it is the rail "
        "Avero uses to score work, described later in this report.",
        st["body"],
    ))

    for lens_id in ("readiness", "impact", "independence"):
        meta = LENS_META[lens_id]
        story.append(Paragraph(f"{meta['question']}", st["h2"]))
        story.append(Paragraph(f"<b>{meta['title']}</b>  ·  X: {meta['x_desc']}.  Y: {meta['y_desc']}.", st["bodyleft"]))
        qrows = [[Paragraph("Quadrant", st["cellhdr"]), Paragraph("Meaning", st["cellhdr"])]]
        for key in ("tl", "tr", "bl", "br"):
            title, desc = meta["labels"][key]
            qrows.append([Paragraph(title, st["cellb"]), Paragraph(desc, st["cell"])])
        qt = Table(qrows, colWidths=[2.6 * inch, 4.5 * inch])
        qt.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), INK),
            ("TEXTCOLOR", (0, 0), (-1, 0), CREAM),
            ("BACKGROUND", (0, 1), (-1, -1), PALE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("GRID", (0, 0), (-1, -1), 0.3, RULE),
        ]))
        story.append(qt)

    story.append(Spacer(1, 10))
    story.append(Callout(
        "Compliance claims in this edition",
        "FedRAMP, GovRAMP, StateRAMP, IL5, and cooperative-vehicle language in this PDF is "
        "copied from the live site product notes (public pages as of this edition). We do not "
        "invent additional authorizations. Cooperative purchase is not FedRAMP. “Progressing” "
        "is not authorized. Confirm the SKU, cloud, and boundary on the vendor’s current "
        "public page and your own authorizing official’s review before you buy.",
    ))

    story.append(PageBreak())
    story.append(Bookmark("What’s new this edition", "new"))
    story.append(Paragraph("SEPTEMBER 2026", st["kicker"]))
    story.append(Paragraph("What’s new in this edition", st["h1"]))
    story.append(GoldRule())
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "The interactive map already shows September 2026 / 43 products, with Caliber as a "
        "methodology rail rather than a vendor dot. This report matches that inventory.",
        st["body"],
    ))
    story.append(Paragraph("Relabels and splits (existing products, not dropped)", st["h2"]))
    story.append(Paragraph(
        "<b>OpenAI split.</b> ChatGPT Enterprise (FedRAMP Moderate SaaS, FR2533155773) is "
        "separate from ChatGPT Gov (customer-hosted on Azure / Azure Government — the High / "
        "IL5 / CJIS path is the agency ATO, not OpenAI-managed High SaaS). "
        "<b>Google Gemini</b> is relabeled Gemini for Government. "
        "<b>Salesforce GovCloud</b> notes include Agentforce; IL5 on Missionforce National "
        "Security (5 Aug 2026) is a national-security path, not treated as a SLED FedRAMP claim. "
        "<b>Darwin AI</b> readiness is raised on Carahsoft + NASPO/TIPS/OMNIA (Apr 2026) — still "
        "not a FedRAMP claim.",
        st["body"],
    ))
    story.append(Paragraph("Net-new on the scatter", st["h2"]))
    added = [t for t in tools if t.get("added")]
    for t in added:
        story.append(Paragraph(f"<b>{t['name']}</b>  ·  {t['category']}", st["h3"]))
        story.append(Paragraph(t["notes"]["readiness"], st["note"]))
    story.append(Callout(
        "Caliber is not new-as-a-product",
        "Caliber remains Avero’s scoring rail. It is not one of the 43. It is not plotted. "
        "See the methodology section. Agencies get the benefit by engaging Avero; there is "
        "no SKU and no cooperative contract.",
    ))

    story.append(PageBreak())
    story.append(Bookmark("Product directory", "dir"))
    story.append(Paragraph("DIRECTORY", st["kicker"]))
    story.append(Paragraph("43 products — scoring notes, rationale, questions", st["h1"]))
    story.append(GoldRule())
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Grouped in the same order as the live map. “New this edition” matches the chips on "
        "govai.averoadvisors.com. Mini-plots below match the three website lenses; the gold "
        "dot is this product.",
        st["body"],
    ))

    grouped = []
    seen = []
    for t in tools:
        if t["category"] not in seen:
            seen.append(t["category"])
            grouped.append((t["category"], []))
        grouped[seen.index(t["category"])][1].append(t)

    for cat, items in grouped:
        story.append(CondPageBreak(2.2 * inch))
        story.append(Bookmark(cat, f"cat-{cat}", 0))
        story.append(Paragraph(cat.upper(), st["kicker"]))
        story.append(Paragraph(f"{cat}", st["h2"]))
        story.append(Paragraph(f"{len(items)} product{'s' if len(items) != 1 else ''} in this edition.", st["small"]))
        for tool in items:
            story.append(CondPageBreak(3.4 * inch))
            story.extend(product_block(tool, st))

    # Caliber
    story.append(PageBreak())
    story.append(Bookmark("Caliber methodology", "caliber"))
    story.append(Paragraph("HOW WE SCORE ENGAGEMENTS", st["kicker"]))
    story.append(Paragraph("Caliber — Avero methodology, not a vendor product", st["h1"]))
    story.append(GoldRule())
    story.append(Spacer(1, 8))
    story.append(Callout(
        "Buyer honesty",
        "<b>Beta. Not sold or licensed.</b> There is no SKU and no cooperative contract. "
        "Caliber is the buyer-side advisory rail Avero uses to run discovery, requirements, "
        "scorecards, and implementation health. Agencies get the benefit by engaging Avero; "
        "work product belongs to the agency. It is not plotted on the product matrix so it "
        "cannot be mistaken for a paid placement.",
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Earlier Navigator editions risked looking as if Caliber were a 32nd (or 37th) vendor "
        "dot. This edition removes that ambiguity. On the live site, Caliber is a gold "
        "methodology rail above the scatter, with a link to averocaliber.averoadvisors.com. "
        "This PDF keeps the same rule: Caliber is how Avero works, not what Avero is selling "
        "as software.",
        st["body"],
    ))
    story.append(Paragraph("What Caliber is for", st["h2"]))
    story.append(Paragraph(
        "Government AI failures are usually not model failures. They are discovery, "
        "requirements, procurement, data, and change-management failures. Caliber is the "
        "internal method Avero uses so those steps are explicit: what “done” looks like, "
        "who owns the record, which vehicle you can actually use, and whether implementation "
        "health is drifting. It is a scoring rail for engagements — not a chatbot, not an "
        "ERP, and not a listing you can piggyback.",
        st["body"],
    ))
    story.append(Paragraph("What Caliber is not", st["h2"]))
    for line in [
        "Not a vendor product on this map, and not competing with the 43.",
        "Not generally available software you can license from a cooperative.",
        "Not a substitute for your authorizing official, counsel, or records officer.",
        "Not a paid placement. Avero did not take vendor money to put anything on this map.",
    ]:
        story.append(Paragraph("•  " + line, st["toc"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "If a salesperson tells you Caliber is “on the Navigator as a leading platform,” "
        "they are misreading the map. Send them to the methodology rail and to this page.",
        st["body"],
    ))
    story.append(Paragraph(
        "Public site: <b>averocaliber.averoadvisors.com</b>",
        st["bodyleft"],
    ))

    story.append(PageBreak())
    story.append(Bookmark("Before you buy — Phase Zero", "phasezero"))
    story.append(Paragraph("START AT ZERO", st["kicker"]))
    story.append(Paragraph("Before you buy any of these tools", st["h1"]))
    story.append(GoldRule())
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Have you completed <b>Phase Zero</b>? Data, policy, procurement vehicles, and an "
        "executive sponsor beat another pilot. The playbook is in <i>Start at Zero</i> "
        "(startatzero.averoadvisors.com). This Navigator tells you where products sit; "
        "Phase Zero tells you whether you should be shopping yet.",
        st["body"],
    ))
    story.append(Paragraph("A short sequence", st["h2"]))
    for n, line in enumerate([
        "Name the job to be done in citizen or staff outcomes, not in model names.",
        "Inventory data classification, records schedules, and the actual vehicle you can use.",
        "Place candidate products on these three lenses — then run the questions in this PDF.",
        "Require human review, logging, and an exit clause before go-live, especially on public safety, HHS, and ERP.",
        "Fund change management. Copilots fail quietly when nobody changes how work is done.",
    ], 1):
        story.append(Paragraph(f"<b>{n}.</b>  {line}", st["toc"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Keep going on the buyer’s side: Start at Zero on Substack (avavero.substack.com) "
        "and the book at startatzero.averoadvisors.com.",
        st["body"],
    ))

    story.append(Paragraph("Notes and limits", st["h2"]))
    story.append(Paragraph(
        "This is independent analysis by Avero Advisors as of September 2026. It is not "
        "legal, procurement, or compliance advice and is not affiliated with any vendor "
        "listed. Product names are the vendors’ marks. Positions will move as public "
        "authorizations, vehicles, and SLED references change — check the live map and the "
        "vendor’s current page. File: "
        "<b>Avero_Start-at-Zero_Government-AI-Navigator_Sep2026.pdf</b>.",
        st["body"],
    ))
    story.append(Paragraph(
        "© 2026 Avèro Advisors. Interactive edition: govai.averoadvisors.com.",
        st["small"],
    ))

    doc.build(story)
    return OUT_PDF


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path} ({path.stat().st_size} bytes)")
