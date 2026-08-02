#!/usr/bin/env python3
"""Build the 'Human-Skills Premium 2026' doodle deck."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# palette
INK   = RGBColor(0x22, 0x22, 0x2B)
PAPER = RGBColor(0xFB, 0xF7, 0xEF)
ACCENT= RGBColor(0xE8, 0x55, 0x3A)  # warm orange-red
BLUE  = RGBColor(0x2F, 0x6F, 0xB0)
GREEN = RGBColor(0x3B, 0x8C, 0x5A)
GREY  = RGBColor(0x8A, 0x86, 0x7E)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
W, H = prs.slide_width, prs.slide_height

def slide():
    s = prs.slides.add_slide(BLANK)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
    bg.fill.solid(); bg.fill.fore_color.rgb = PAPER
    bg.line.fill.background()
    bg.shadow.inherit = False
    s.shapes._spTree.remove(bg._element); s.shapes._spTree.insert(2, bg._element)
    return s

def txt(s, x, y, w, h, text, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, font="Comic Sans MS", line_spacing=1.05):
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.line_spacing = line_spacing
        r = p.add_run(); r.text = ln
        r.font.size = Pt(size); r.font.bold = bold
        r.font.color.rgb = color; r.font.name = font
    return tb

def doodle(s, shape, x, y, w, h, color=INK, fill=None, wdt=2.5):
    sp = s.shapes.add_shape(shape, x, y, w, h)
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid(); sp.fill.fore_color.rgb = fill
    sp.line.color.rgb = color; sp.line.width = Pt(wdt)
    sp.shadow.inherit = False
    return sp

def blob_label(s, x, y, w, h, label, num, ncolor):
    c = doodle(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, color=ncolor, fill=PAPER, wdt=3)
    doodle(s, MSO_SHAPE.OVAL, x-Inches(0.28), y-Inches(0.28), Inches(0.85), Inches(0.85),
           color=INK, fill=ncolor, wdt=2.5)
    txt(s, x-Inches(0.28), y-Inches(0.30), Inches(0.85), Inches(0.85), num, 26, PAPER,
        True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    return c

# ---------- Slide 1: title ----------
s = slide()
txt(s, Inches(0.9), Inches(1.5), Inches(11.5), Inches(1.6),
    "The Human-Skills Premium", 60, INK, True, PP_ALIGN.LEFT)
doodle(s, MSO_SHAPE.RECTANGLE, Inches(0.95), Inches(2.95), Inches(6.6), Inches(0.16),
       color=ACCENT, fill=ACCENT, wdt=1)
txt(s, Inches(0.95), Inches(3.25), Inches(11.4), Inches(1.0),
    "What to learn when AI learns everything.", 30, ACCENT, True)
txt(s, Inches(0.95), Inches(4.15), Inches(11.4), Inches(1.0),
    "2026 mid-year trend brief  ·  5-minute read  ·  19 July 2026", 20, GREY)
doodle(s, MSO_SHAPE.LIGHTNING_BOLT, Inches(10.7), Inches(1.2), Inches(1.4), Inches(2.0),
       color=ACCENT, fill=RGBColor(0xFF,0xE7,0x9c), wdt=3)
doodle(s, MSO_SHAPE.SUN, Inches(9.5), Inches(4.6), Inches(1.7), Inches(1.7),
       color=BLUE, fill=None, wdt=3)
txt(s, Inches(9.5), Inches(5.15), Inches(1.7), Inches(0.7), "AI ×\nHUMAN", 16, BLUE,
    True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

# ---------- Slide 2: the one line ----------
s = slide()
txt(s, Inches(0.9), Inches(0.6), Inches(11.5), Inches(0.8), "The one line", 34, ACCENT, True)
doodle(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.7), Inches(11.3), Inches(3.4),
       color=INK, fill=RGBColor(0xFF,0xF3,0xD9), wdt=3)
txt(s, Inches(1.5), Inches(2.0), Inches(10.3), Inches(2.9),
    "AI is not erasing the value of human skills —\nit is REPRICING them.\n\n"
    "The tasks it automates get cheaper.\nThe judgment, taste & trust it can't fake get "
    "more expensive.", 30, INK, True, PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)
txt(s, Inches(1.0), Inches(5.5), Inches(11.3), Inches(1.2),
    "The 2026 move isn’t “AI vs. human.”  It’s  AI × human.", 26, ACCENT, True, PP_ALIGN.CENTER)

# ---------- Slide 3: three forces ----------
s = slide()
txt(s, Inches(0.9), Inches(0.5), Inches(11.5), Inches(0.8),
    "Three forces on your career right now", 32, ACCENT, True)
cols = [
    (Inches(0.9),  "1", BLUE,  "DURABLE HUMAN SKILLS",
     "Critical thinking is the\n#1 skill leaders want\n(73%).\n\nJudgment · leadership ·\nEQ · human-in-the-loop"),
    (Inches(5.05), "2", ACCENT,"AI JOB-MARKET SHIFTS",
     "+62% wage premium\n(PwC, up from 57%).\n\nBut skills now expire\nin 2.5–5 years."),
    (Inches(9.2),  "3", GREEN, "NICHE / LIVED LEARNING",
     "The “skilliday” boom.\n\nLanguages, crafts,\nwellness — half of\nEurope, led by Gen Z."),
]
for x, n, col, head, body in cols:
    blob_label(s, x, Inches(1.9), Inches(3.55), Inches(3.9), head, n, col)
    txt(s, x+Inches(0.2), Inches(2.25), Inches(3.15), Inches(0.9), head, 17, col, True,
        PP_ALIGN.CENTER)
    txt(s, x+Inches(0.25), Inches(3.15), Inches(3.05), Inches(2.5), body, 15, INK)
doodle(s, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.0), Inches(6.2), Inches(7.3), Inches(0.9),
       color=INK, fill=RGBColor(0xE7,0xF0,0xE7), wdt=2.5)
txt(s, Inches(3.0), Inches(6.25), Inches(7.3), Inches(0.8),
    "META-SKILL underneath all three: learning how to learn", 20, GREEN, True,
    PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

prs.save("/home/user/my_professional_documents/weekly-briefings/2026-07-19-human-skills-vs-ai/Human_Skills_Premium_2026.pptx")
print("saved deck with", len(prs.slides._sldIdLst), "slides")
