#!/usr/bin/env python3
"""
Entroly Demo Video Generator
=============================

Generates an animated terminal recording as SVG and interactive HTML.
Shows a real OpenClaw workspace benchmark — the kind of output `entroly demo`
produces on an actual workspace.

Usage:
    python docs/generate_demo.py              # Generate both SVG and HTML
    python docs/generate_demo.py --format svg # Generate SVG only
    python docs/generate_demo.py --format html # Generate HTML only

Output is saved to docs/assets/.
"""

from __future__ import annotations

import argparse
from pathlib import Path

# ── Terminal Theme (neutral dark — VS Code default style) ──
COLORS = {
    "bg": "#1e1e2e",
    "bg_tab": "#2d2d3f",
    "fg": "#d4d4d4",
    "green": "#6ee7b7",
    "cyan": "#67e8f9",
    "yellow": "#fde68a",
    "red": "#f87171",
    "purple": "#a78bfa",
    "orange": "#fbbf24",
    "gray": "#6b7280",
    "muted": "#9ca3af",
    "bright": "#e5e7eb",
    "border": "#374151",
    "white": "#ffffff",
}

# ── Storyboard ──
# Each frame is (delay_ms, lines) where lines are (text, color, bold, indent)
# Content matches real `entroly demo` output on an OpenClaw workspace.
FRAMES = [
    # Frame 0: Command prompt
    (600, [
        ("~/openclaw $ entroly demo", "bright", True, 0),
    ]),
    # Frame 1: Indexing
    (1000, [
        ("", None, False, 0),
        ("Indexing workspace...", "gray", False, 0),
    ]),
    # Frame 2: Indexed result
    (800, [
        ("✓ 24 files indexed (2,348 tokens) in 0.05ms", "green", False, 0),
    ]),
    # Frame 3: WITHOUT section
    (1000, [
        ("", None, False, 0),
        ("Without Entroly", "red", True, 0),
        ("  Budget: 2,048 tokens", "muted", False, 0),
        ("  Files loaded: 15 of 24    (9 files invisible)", "muted", False, 0),
        ("  Tokens used:  2,031 / 2,048  (99.2% of budget)", "muted", False, 0),
    ]),
    # Frame 4: Missing files
    (1200, [
        ("  Missing:", "gray", False, 0),
        ("    ✗ skills/system.md         — can't manage Docker", "red", False, 0),
        ("    ✗ tools/search_emails.json — can't search inbox", "red", False, 0),
        ("    ✗ tools/send_email.json    — can't send email", "red", False, 0),
        ("    ✗ tools/run_tests.json     — can't run tests", "red", False, 0),
        ("    ... and 5 more", "gray", False, 0),
    ]),
    # Frame 5: WITH section
    (1200, [
        ("", None, False, 0),
        ("With Entroly", "green", True, 0),
        ("  Budget: 2,048 tokens", "muted", False, 0),
        ("  Files loaded: 24 of 24   (100% coverage)", "bright", False, 0),
        ("  Tokens used:  1,812 / 2,048  (88.5% — 22.7% saved)", "bright", False, 0),
    ]),
    # Frame 6: Compression breakdown
    (1000, [
        ("  Compression:", "gray", False, 0),
        ("    SOUL.md, MEMORY.md              → full", "fg", False, 0),
        ("    daily/2024-03-20.md +1 more     → skeleton", "fg", False, 0),
        ("    tools/*.json (9 files)           → reference", "fg", False, 0),
    ]),
    # Frame 7: Summary
    (1200, [
        ("", None, False, 0),
        ("✓ All 24 files visible. 22.7% fewer tokens. 0.05ms.", "green", True, 0),
    ]),
    # Frame 8: Next step
    (1500, [
        ("", None, False, 0),
        ("  Start now:  pip install entroly && entroly proxy", "gray", False, 0),
    ]),
]

LINE_HEIGHT = 18
FONT_SIZE = 13
PADDING_X = 40
PADDING_Y = 56
TERMINAL_WIDTH = 840
TAB_BAR_HEIGHT = 32


def _escape_xml(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def generate_svg() -> str:
    """Generate an animated SVG terminal recording."""

    all_lines: list[tuple[str, str, bool, float]] = []
    t = 0.0
    for delay_ms, lines in FRAMES:
        t += delay_ms / 1000.0
        for text, color, bold, indent in lines:
            all_lines.append((text, color or "fg", bold, t))
            t += 0.06

    total_lines = len(all_lines)
    terminal_height = PADDING_Y + (total_lines * LINE_HEIGHT) + 30
    total_height = terminal_height + 32  # outer padding

    parts = []

    # SVG header
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TERMINAL_WIDTH} {total_height}" width="{TERMINAL_WIDTH}" height="{total_height}">')
    parts.append(f"""  <defs>
    <style>
      .t {{ font-family: 'SF Mono', 'Cascadia Code', 'Consolas', monospace; font-size: {FONT_SIZE}px; }}
      .b {{ font-weight: 700; }}
    </style>
  </defs>""")

    # White outer background
    parts.append(f'  <rect width="{TERMINAL_WIDTH}" height="{total_height}" fill="#ffffff"/>')

    # Terminal frame
    parts.append(f'  <rect x="24" y="16" width="{TERMINAL_WIDTH - 48}" height="{terminal_height}" rx="8" fill="{COLORS["bg"]}" stroke="{COLORS["border"]}" stroke-width="1"/>')

    # Tab bar
    parts.append(f'  <rect x="24" y="16" width="{TERMINAL_WIDTH - 48}" height="{TAB_BAR_HEIGHT}" rx="8" fill="{COLORS["bg_tab"]}"/>')
    parts.append(f'  <rect x="24" y="40" width="{TERMINAL_WIDTH - 48}" height="8" fill="{COLORS["bg_tab"]}"/>')

    # Active tab
    parts.append(f'  <rect x="32" y="22" width="140" height="24" rx="4" fill="{COLORS["bg"]}"/>')
    parts.append(f'  <circle cx="42" cy="34" r="3" fill="{COLORS["green"]}"/>')
    parts.append(f'  <text x="52" y="38" class="t" fill="{COLORS["muted"]}" font-size="11">Terminal — zsh</text>')

    # Animated text lines
    for i, (text, color, bold, appear_time) in enumerate(all_lines):
        if not text:
            continue

        y = PADDING_Y + (i * LINE_HEIGHT) + 14
        color_hex = COLORS.get(color, COLORS["fg"])
        bold_class = " b" if bold else ""
        escaped = _escape_xml(text)

        parts.append(f'  <g opacity="0">')
        parts.append(f'    <animate attributeName="opacity" from="0" to="1" begin="{appear_time:.2f}s" dur="0.2s" fill="freeze"/>')
        parts.append(f'    <text x="{PADDING_X}" y="{y}" class="t{bold_class}" fill="{color_hex}">{escaped}</text>')
        parts.append(f'  </g>')

    # Blinking cursor
    last_y = PADDING_Y + (total_lines * LINE_HEIGHT) + 2
    cursor_appear = all_lines[-1][3] + 0.4 if all_lines else 1.0
    parts.append(f'  <rect x="{PADDING_X}" y="{last_y}" width="7" height="14" fill="{COLORS["bright"]}" opacity="0">')
    parts.append(f'    <animate attributeName="opacity" from="0" to="1" begin="{cursor_appear:.2f}s" dur="0.01s" fill="freeze"/>')
    parts.append(f'    <animate attributeName="opacity" values="1;1;0;0" dur="1s" begin="{cursor_appear:.2f}s" repeatCount="indefinite"/>')
    parts.append(f'  </rect>')

    parts.append('</svg>')
    return '\n'.join(parts)


def generate_html() -> str:
    """Generate an interactive HTML page with the terminal animation."""

    all_entries: list[tuple[str, str, bool, int]] = []
    t = 0
    for delay_ms, lines in FRAMES:
        t += delay_ms
        for text, color, bold, indent in lines:
            all_entries.append((text, color or "fg", bold, t))
            t += 50

    lines_json = []
    for text, color, bold, delay in all_entries:
        color_hex = COLORS.get(color, COLORS["fg"])
        escaped = text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        lines_json.append(f'    {{t:"{escaped}",c:"{color_hex}",b:{str(bold).lower()},d:{delay}}}')

    lines_str = ",\n".join(lines_json)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Entroly — Demo</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;700&display=swap');
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #f9fafb;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 24px;
    font-family: 'Inter', system-ui, sans-serif;
  }}
  .wrapper {{
    max-width: 840px;
    width: 100%;
  }}
  .terminal {{
    background: {COLORS["bg"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.12);
  }}
  .tab-bar {{
    background: {COLORS["bg_tab"]};
    height: 36px;
    display: flex;
    align-items: center;
    padding: 0 12px;
    gap: 8px;
  }}
  .tab {{
    background: {COLORS["bg"]};
    border-radius: 4px;
    padding: 4px 12px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .tab-dot {{
    width: 6px; height: 6px; border-radius: 50%;
    background: {COLORS["green"]};
  }}
  .tab-text {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: {COLORS["muted"]};
  }}
  .content {{
    padding: 16px 20px 24px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    line-height: 1.5;
    min-height: 420px;
  }}
  .line {{
    opacity: 0;
    transform: translateY(3px);
    transition: opacity 0.2s ease, transform 0.2s ease;
    white-space: pre;
  }}
  .line.show {{
    opacity: 1;
    transform: translateY(0);
  }}
  .cursor {{
    display: inline-block;
    width: 7px; height: 14px;
    background: {COLORS["bright"]};
    animation: blink 1s step-end infinite;
    vertical-align: text-bottom;
    opacity: 0;
  }}
  .cursor.show {{ opacity: 1; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .controls {{
    display: flex;
    justify-content: center;
    gap: 8px;
    padding: 12px;
    background: {COLORS["bg_tab"]};
    border-top: 1px solid {COLORS["border"]};
  }}
  .controls button {{
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 12px;
    background: {COLORS["bg"]};
    color: {COLORS["bright"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 4px;
    padding: 6px 16px;
    cursor: pointer;
    transition: background 0.15s;
  }}
  .controls button:hover {{ background: {COLORS["border"]}; }}
</style>
</head>
<body>
<div class="wrapper">
<div class="terminal">
  <div class="tab-bar">
    <div class="tab">
      <span class="tab-dot"></span>
      <span class="tab-text">Terminal — zsh</span>
    </div>
  </div>
  <div class="content" id="content"></div>
  <div class="controls">
    <button onclick="replay()">Replay</button>
    <button onclick="skipToEnd()">Skip to End</button>
  </div>
</div>
</div>
<script>
const L=[
{lines_str}
];
const content=document.getElementById('content');
let timeouts=[];
function clear(){{ timeouts.forEach(clearTimeout); timeouts=[]; content.innerHTML=''; }}
function play() {{
  clear();
  L.forEach((l,i) => {{
    const div=document.createElement('div');
    div.className='line';
    if(l.b) div.style.fontWeight='700';
    div.style.color=l.c;
    div.textContent=l.t||'\\u00a0';
    content.appendChild(div);
    timeouts.push(setTimeout(()=>div.classList.add('show'), l.d));
  }});
  const cur=document.createElement('span');
  cur.className='cursor';
  content.appendChild(cur);
  const lastDelay=L[L.length-1].d+400;
  timeouts.push(setTimeout(()=>cur.classList.add('show'), lastDelay));
}}
function replay() {{ play(); }}
function skipToEnd() {{
  clear();
  L.forEach(l => {{
    const div=document.createElement('div');
    div.className='line show';
    if(l.b) div.style.fontWeight='700';
    div.style.color=l.c;
    div.textContent=l.t||'\\u00a0';
    content.appendChild(div);
  }});
  const cur=document.createElement('span');
  cur.className='cursor show';
  content.appendChild(cur);
}}
play();
</script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate Entroly demo animation")
    parser.add_argument("--format", choices=["svg", "html", "both"], default="both",
                        help="Output format (default: both)")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory (default: docs/assets/)")
    args = parser.parse_args()

    output_dir = Path(args.output_dir) if args.output_dir else Path(__file__).parent / "assets"
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.format in ("svg", "both"):
        svg_path = output_dir / "demo_animated.svg"
        svg_path.write_text(generate_svg(), encoding="utf-8")
        print(f"  \033[38;5;82m✓\033[0m SVG saved: {svg_path}")

    if args.format in ("html", "both"):
        html_path = output_dir / "demo.html"
        html_path.write_text(generate_html(), encoding="utf-8")
        print(f"  \033[38;5;82m✓\033[0m HTML saved: {html_path}")

    print(f"\n  Tip: Open the HTML file in a browser for the interactive version.")


if __name__ == "__main__":
    main()
