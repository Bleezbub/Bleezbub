#!/usr/bin/env python3
"""
make_info_card.py
Generates a neofetch-style info card SVG for Bleezbub's GitHub profile.
Height matched to ASCII portrait rendered table height (~511px canvas / 385px render).
Output: info-card.svg
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "info-card.svg")

STATIC = bool(os.environ.get("STATIC"))

USERNAME = "bleezbub"
OS_LINE = "Role    : AI &amp; Automation | EE Engineer"
LINES = [
    ("Now",        "Machine Learning  &#183;  Computer Vision"),
    ("Prev",       "Industrial Automation  &#183;  PLC / HMI"),
    ("Stack",      "Python  &#183;  C++  &#183;  JavaScript  &#183;  OpenSCAD"),
    ("Tools",      "MediaPipe  &#183;  TensorFlow  &#183;  TIA Portal"),
    ("Projects",   "Real-Jarvis  &#183;  NarutoJujutsu-MediaPipe"),
    ("Highlights", "Gesture-driven ML  &#183;  EE meets AI"),
    ("Location",   "Turkey"),
    ("GitHub",     "github.com/Bleezbub"),
]

TITLEBAR_H = 30
PAD = 20
CANVAS_W = 490
CANVAS_H = 511

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"

KEY_C    = "#7ee787"
VAL_C    = "#c9d1d9"
PROMPT_C = "#f78166"
FONT     = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

def anim(i: int) -> str:
    if STATIC:
        return ""
    delay = 0.05 + i * 0.08
    dur = delay + 0.35
    key_time = delay / dur
    return (f'<animate attributeName="opacity" values="0;0;1" '
            f'keyTimes="0;{key_time:.3f};1" dur="{dur:.2f}s" fill="freeze"/>')

def make_svg() -> str:
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="{FONT}">'
    )
    parts.append('<defs>'
                 f'<linearGradient id="icbg" x1="0" y1="0" x2="0" y2="1">'
                 f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
                 f'</linearGradient></defs>')

    parts.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#icbg)"/>')
    parts.append(f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" '
                 f'fill="none" stroke="{FRAME}" stroke-width="1"/>')

    parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
    parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
                 f'text-anchor="middle">{USERNAME}@github: ~$ neofetch</text>')

    line_h = 36
    y_start = TITLEBAR_H + 48

    # Prompt + OS line
    anim_0 = anim(0)
    parts.append(
        f'<g opacity="0">{anim_0}'
        f'<text x="{PAD}" y="{y_start}" font-size="14" fill="{PROMPT_C}">></text>'
        f'<text x="{PAD + 18}" y="{y_start}" font-size="14" fill="{VAL_C}">{OS_LINE}</text>'
        f'</g>'
    )

    # Key-value rows
    curr_y = y_start + line_h + 8
    for i, (key, val) in enumerate(LINES):
        key_padded = f"{key:<11}"
        anim_i = anim(i + 1)
        parts.append(
            f'<g opacity="0">{anim_i}'
            f'<text x="{PAD}" y="{curr_y}" font-size="14" fill="{KEY_C}" font-weight="600">  {key_padded}</text>'
            f'<text x="{PAD + 125}" y="{curr_y}" font-size="14" fill="{VAL_C}">{val}</text>'
            f'</g>'
        )
        curr_y += line_h

    # Color palette bars at bottom
    curr_y += 20
    colors = ["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff", "#bf7af0", "#f78166", "#79c0ff", "#56d364"]
    for ci, col in enumerate(colors):
        cx = PAD + ci * 24
        parts.append(f'<rect x="{cx}" y="{curr_y}" width="20" height="10" fill="{col}" rx="2"/>')
        parts.append(f'<rect x="{cx}" y="{curr_y+14}" width="20" height="10" fill="{col}" opacity="0.5" rx="2"/>')

    parts.append("</svg>")
    return "".join(parts)

def main():
    svg = make_svg()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[OK] Wrote {OUT} ({len(svg)} bytes; {CANVAS_W}x{CANVAS_H})")

if __name__ == "__main__":
    main()
