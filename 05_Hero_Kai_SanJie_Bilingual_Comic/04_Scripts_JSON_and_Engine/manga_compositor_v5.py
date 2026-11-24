#!/usr/bin/env python3
"""
Hero Kai x San Jie 17 Guardians — Manga/Webtoon Lettering & Layout Engine v5.3
Non-destructive compositor: reads untouched text-free raw panels + structured JSON script,
and renders true Webtoon/Manhwa lettering with:
  - Embedded @font-face Typography: Comic Neue Bold (dialogue/narration) & Bangers (tilted SFX)
  - 6 SVG Balloon Styles: speech (+12% breathing room, 2.2px outline), shout (spiky starburst),
    thought (cloud), whisper (dashed), glitch (jagged villain), narration (drop-shadow box)
  - Exact Coordinate-Targeted Curved Bezier Tails pointing directly to (target_x%, target_y%)
  - Stacked-SVG Hand-Lettered SFX (Giongo, 9px white halo) & Floating Mood Cues (Gitaigo)
  - 8 Dynamic Landscape + Portrait + Micro-Zoom Manga Layouts (Zero Half-Blank Pages):
      * full_bleed (800x440)
      * framed (728x415)
      * inset_reaction (560x330 + zoomed reaction inset)
      * portrait_tall / tall_portrait (700x980 — fills a full 800x1460 mobile page!)
      * portrait_bleed / portrait_cinematic (800x1100 — edge-to-edge full-page vertical splash!)
      * portrait_duo / split_duo (two side-by-side 352x520 vertical panels with 24px gutter)
      * eye_strip (728x195 dramatic horizontal eye/glare slit)
      * floating_beat (460x380 centered micro-panel with deliberate breathing space)
      * zoom_cascade (2- or 3-step diagonal staggered zoom-in/zoom-out)
  - Inline Python Spellbook Code Trays on coding / spell-cast panels (0% art overlap)
  - Built-in Page-Fill Diagnostic (flags any non-final page < 72% filled!)
"""
import base64
import html as html_lib
import io
import json
import math
import os
import re
import sys
from pathlib import Path
from PIL import Image
import weasyprint
import pypdfium2 as pdfium


def esc(s: str) -> str:
    return html_lib.escape(s, quote=True)


def find_font_file(filename: str, extra_dirs=None) -> str:
    search_dirs = []
    if extra_dirs:
        search_dirs.extend(extra_dirs)
    here = Path(__file__).resolve().parent
    search_dirs.extend([
        here,
        here / "fonts",
        Path.cwd() / "downloads",
        Path.cwd() / "work" / "fonts",
        Path.cwd() / "work" / "fonts" / "bangers_bundle" / "Bangers",
        Path.cwd() / "work" / "fonts" / "bangers_bundle" / "Comic_Neue",
        Path.cwd() / "work" / "fonts" / "comic_neue",
        Path.home() / ".local" / "share" / "fonts",
    ])
    for d in search_dirs:
        p = Path(d) / filename
        if p.exists():
            return p.resolve().as_uri()
    return ""


def build_font_face_css(extra_dirs=None) -> str:
    parts = []
    cn_bold = find_font_file("ComicNeue-Bold.ttf", extra_dirs)
    cn_reg = find_font_file("ComicNeue-Regular.ttf", extra_dirs) or cn_bold
    bangers = find_font_file("Bangers-Regular.ttf", extra_dirs)
    if cn_reg:
        parts.append(f"""
        @font-face {{
          font-family: 'Comic Neue';
          src: url('{cn_reg}') format('truetype');
          font-weight: 400;
          font-style: normal;
        }}""")
    if cn_bold:
        parts.append(f"""
        @font-face {{
          font-family: 'Comic Neue';
          src: url('{cn_bold}') format('truetype');
          font-weight: 700;
          font-style: normal;
        }}""")
    if bangers:
        parts.append(f"""
        @font-face {{
          font-family: 'Bangers';
          src: url('{bangers}') format('truetype');
          font-weight: 400;
          font-style: normal;
        }}
        @font-face {{
          font-family: 'Bangers';
          src: url('{bangers}') format('truetype');
          font-weight: 700;
          font-style: normal;
        }}""")
    if not (cn_bold and bangers):
        print(f"WARNING: Missing local TTF font(s) — ComicNeue-Bold={bool(cn_bold)}, Bangers={bool(bangers)}")
    return "\n".join(parts)


def img_to_b64_data_uri(path: str, crop_box=None, max_w: int = 880, quality: int = 80) -> str:
    img = Image.open(path).convert("RGB")
    if crop_box:
        w, h = img.size
        x0, y0, x1, y1 = crop_box
        img = img.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))
    if max_w and img.width > max_w:
        nh = int(img.height * (max_w / img.width))
        img = img.resize((max_w, nh), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{b64}"


def svg_spiky_starburst(cx, cy, rx, ry, spikes=14, seed_offset=0.2):
    pts = []
    n = spikes * 2
    for i in range(n):
        ang = (2 * math.pi * i / n) + seed_offset
        if i % 2 == 0:
            mod = 1.14 + 0.10 * math.sin(i * 1.7)
            r_x, r_y = rx * mod, ry * mod
        else:
            mod = 0.88 + 0.04 * math.cos(i * 2.3)
            r_x, r_y = rx * mod, ry * mod
        pts.append((cx + r_x * math.cos(ang), cy + r_y * math.sin(ang)))
    d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f} "
    for i in range(0, n, 2):
        p_valley = pts[(i + 1) % n]
        p_next = pts[(i + 2) % n]
        d += f"Q {p_valley[0]:.1f},{p_valley[1]:.1f} {p_next[0]:.1f},{p_next[1]:.1f} "
    d += "Z"
    return d


def svg_glitch_balloon(cx, cy, rx, ry, teeth=18):
    pts = []
    n = teeth * 2
    for i in range(n):
        ang = 2 * math.pi * i / n
        mod = (1.13 + 0.07 * math.sin(i * 3.1)) if i % 2 == 0 else (0.91 - 0.04 * math.cos(i * 2.1))
        pts.append((cx + rx * mod * math.cos(ang), cy + ry * mod * math.sin(ang)))
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def svg_curved_tail(bx, by, tx, ty, base_half=12):
    dx, dy = tx - bx, ty - by
    dist = math.hypot(dx, dy) or 1.0
    ux, uy = dx / dist, dy / dist
    px, py = -uy, ux
    p1x, p1y = bx + px * base_half, by + py * base_half
    p2x, p2y = bx - px * base_half, by - py * base_half
    bend = 16 if dx >= 0 else -16
    mx, my = (bx + tx) / 2 + px * bend * 0.45, (by + ty) / 2 + py * bend * 0.45
    return (
        f"M {p1x:.1f},{p1y:.1f} Q {mx + px*4:.1f},{my + py*4:.1f} {tx:.1f},{ty:.1f} "
        f"Q {mx - px*4:.1f},{my - py*4:.1f} {p2x:.1f},{p2y:.1f} Z"
    )


def svg_speedlines(x, y, w, h, cx_pct=50, cy_pct=50, color="#FFFFFF", opacity=0.45, count=56):
    cx = x + w * cx_pct / 100.0
    cy = y + h * cy_pct / 100.0
    max_r = math.hypot(w, h)
    lines = []
    for i in range(count):
        ang = (2 * math.pi * i / count) + 0.03 * math.sin(i * 2.7)
        inner_r = min(w, h) * (0.30 + 0.12 * math.sin(i * 3.3))
        x1 = cx + inner_r * math.cos(ang)
        y1 = cy + inner_r * math.sin(ang)
        x2 = cx + max_r * math.cos(ang)
        y2 = cy + max_r * math.sin(ang)
        sw = 1.6 + (i % 3) * 1.1
        lines.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{sw:.1f}" stroke-opacity="{opacity}"/>'
        )
    return "\n".join(lines)


def wrap_comic_lines(text: str, max_chars: int = 20):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > max_chars:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def render_balloon_svg(b, panel_x, panel_y, panel_w, panel_h, clamp_min_x=18, clamp_max_x=782):
    btype = b.get("type", "speech")
    text = b["text"].upper()
    bx = panel_x + panel_w * b["bx"] / 100.0
    by = panel_y + panel_h * b["by"] / 100.0
    max_chars = b.get("max_chars", 26 if btype == "narration" else 19)
    lines = wrap_comic_lines(text, max_chars=max_chars)
    font_size = b.get("font_size", 16.5 if btype != "narration" else 16.0)
    line_h = font_size * 1.24

    if btype == "narration":
        max_avail = max(180, clamp_max_x - clamp_min_x - 12)
        box_w = b.get("width", max(220, min(max_avail, max(len(l) for l in lines) * font_size * 0.60 + 48)))
        box_h = len(lines) * line_h + 24
        x0 = max(clamp_min_x, min(clamp_max_x - box_w, bx - box_w / 2))
        y0 = by - box_h / 2
        fill = b.get("fill", "#FFFFFF")
        stroke = b.get("stroke", "#18181B")
        text_svg = []
        start_y = y0 + 19 + font_size * 0.72
        for idx, ln in enumerate(lines):
            ty = start_y + idx * line_h
            text_svg.append(
                f'<text x="{x0 + box_w/2:.1f}" y="{ty:.1f}" text-anchor="middle" '
                f'font-family="Comic Neue, Comic Sans MS, sans-serif" font-weight="700" '
                f'font-size="{font_size}" fill="#141418" letter-spacing="0.5">{esc(ln)}</text>'
            )
        svg = f'''
        <g>
          <rect x="{x0+4:.1f}" y="{y0+5:.1f}" width="{box_w:.1f}" height="{box_h:.1f}" fill="rgba(0,0,0,0.16)"/>
          <rect x="{x0:.1f}" y="{y0:.1f}" width="{box_w:.1f}" height="{box_h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="2.2"/>
          {"".join(text_svg)}
        </g>
        '''
        return svg, y0, y0 + box_h + 8

    # +12% horizontal breathing room per v5.2/v5.3 reference polish
    est_w = max(len(l) for l in lines) * font_size * 0.60
    max_rx = (clamp_max_x - clamp_min_x) / 2.0 - 4
    rx = min(max_rx, b.get("rx", max(92, est_w * 0.72 + 28)))
    ry = b.get("ry", max(42, len(lines) * line_h * 0.68 + 18))
    bx = max(clamp_min_x + rx, min(clamp_max_x - rx, bx))

    tail_svg = ""
    if "tx" in b and "ty" in b:
        tx = panel_x + panel_w * b["tx"] / 100.0
        ty = panel_y + panel_h * b["ty"] / 100.0
        if btype == "thought":
            circles = []
            for frac, rad in [(0.52, 8), (0.72, 5.5), (0.88, 3.5)]:
                cx_t = bx + (tx - bx) * frac
                cy_t = by + (ty - by) * frac
                circles.append(
                    f'<circle cx="{cx_t:.1f}" cy="{cy_t:.1f}" r="{rad}" fill="#FFFFFF" stroke="#18181B" stroke-width="2.0"/>'
                )
            tail_svg = "".join(circles)
        else:
            t_path = svg_curved_tail(bx, by, tx, ty, base_half=12)
            tail_fill = "#1B1028" if btype == "glitch" else "#FFFFFF"
            tail_stroke = "#A855F7" if btype == "glitch" else "#18181B"
            tail_sw = "2.8" if btype == "glitch" else "2.2"
            tail_svg = (
                f'<path d="{t_path}" fill="{tail_fill}" stroke="{tail_stroke}" '
                f'stroke-width="{tail_sw}" stroke-linejoin="round"/>'
            )

    if btype == "shout":
        d_path = svg_spiky_starburst(bx, by, rx * 1.12, ry * 1.15, spikes=14)
        body_svg = f'<path d="{d_path}" fill="#FFFFFF" stroke="#18181B" stroke-width="2.3" stroke-linejoin="round"/>'
        mask_svg = f'<path d="{d_path}" fill="#FFFFFF" stroke="none"/>'
        text_color = "#111116"
        top_ext, bot_ext = by - ry * 1.38, by + ry * 1.38
    elif btype == "glitch":
        d_path = svg_glitch_balloon(bx, by, rx * 1.11, ry * 1.13, teeth=18)
        body_svg = f'<path d="{d_path}" fill="#1B1028" stroke="#A855F7" stroke-width="2.8" stroke-linejoin="miter"/>'
        mask_svg = f'<path d="{d_path}" fill="#1B1028" stroke="none"/>'
        text_color = "#F3E8FF"
        top_ext, bot_ext = by - ry * 1.30, by + ry * 1.30
    elif btype == "whisper":
        body_svg = (
            f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
            f'fill="#FFFFFF" stroke="#52525B" stroke-width="1.9" stroke-dasharray="6,4"/>'
        )
        mask_svg = f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{rx-2:.1f}" ry="{ry-2:.1f}" fill="#FFFFFF"/>'
        text_color = "#3F3F46"
        top_ext, bot_ext = by - ry - 6, by + ry + 6
    else:
        body_svg = (
            f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
            f'fill="#FFFFFF" stroke="#18181B" stroke-width="2.2"/>'
        )
        mask_svg = f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{rx-2:.1f}" ry="{ry-2:.1f}" fill="#FFFFFF"/>'
        text_color = "#141418"
        top_ext, bot_ext = by - ry - 6, by + ry + 6

    total_th = len(lines) * line_h
    start_y = by - total_th / 2 + font_size * 0.85
    text_svg = []
    for idx, ln in enumerate(lines):
        ty = start_y + idx * line_h
        text_svg.append(
            f'<text x="{bx:.1f}" y="{ty:.1f}" text-anchor="middle" '
            f'font-family="Comic Neue, Comic Sans MS, sans-serif" font-weight="700" '
            f'font-size="{font_size}" fill="{text_color}" letter-spacing="0.5">{esc(ln)}</text>'
        )

    svg = f'''
    <g>
      {body_svg}
      {tail_svg}
      {mask_svg}
      {"".join(text_svg)}
    </g>
    '''
    return svg, top_ext, bot_ext


def _stacked_stroked_text(x, y, text, rot, font_fam, size, letter_sp, fill, stroke, stroke_w, anchor="middle"):
    """Two-pass SVG text so WeasyPrint renders a crisp white outer halo BEHIND the colored/black fill."""
    t = esc(text)
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'transform="rotate({rot} {x:.1f} {y:.1f})" '
        f'font-family="{font_fam}" font-size="{size}" font-weight="700" letter-spacing="{letter_sp}" '
        f'fill="none" stroke="{stroke}" stroke-width="{stroke_w}" stroke-linejoin="round">{t}</text>'
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'transform="rotate({rot} {x:.1f} {y:.1f})" '
        f'font-family="{font_fam}" font-size="{size}" font-weight="700" letter-spacing="{letter_sp}" '
        f'fill="{fill}" stroke="none">{t}</text>'
    )


def render_sfx_svg(sfx, panel_x, panel_y, panel_w, panel_h):
    kind = sfx.get("kind", "sfx")
    sx = panel_x + panel_w * sfx["x"] / 100.0
    sy = panel_y + panel_h * sfx["y"] / 100.0
    rot = sfx.get("rotate", -8)
    size = sfx.get("size", 52 if kind == "sfx" else 28)
    fill = sfx.get("fill", "#111116")
    stroke = sfx.get("stroke", "#FFFFFF")
    stroke_w = sfx.get("stroke_width", 9.0 if kind == "sfx" else 6.5)
    font_fam = "Bangers, sans-serif"
    letter_sp = "2.5" if kind == "sfx" else "1.6"
    text = sfx.get("text", "").upper()

    if "cascade" in sfx:
        parts = []
        step_x = sfx.get("step_x", 48)
        step_y = sfx.get("step_y", 52)
        for i, word in enumerate(sfx["cascade"]):
            wx = sx + i * step_x
            wy = sy + i * step_y
            parts.append(
                _stacked_stroked_text(
                    wx, wy, word.upper(), rot, font_fam, size, letter_sp, fill, stroke, stroke_w, anchor="start"
                )
            )
        return "<g>" + "".join(parts) + "</g>"

    return (
        "<g>"
        + _stacked_stroked_text(sx, sy, text, rot, font_fam, size, letter_sp, fill, stroke, stroke_w, anchor="middle")
        + "</g>"
    )


def highlight_python_line(line: str) -> str:
    comment_part = ""
    code_part = line
    in_str = False
    str_ch = ""
    for i, ch in enumerate(line):
        if ch in ('"', "'") and (i == 0 or line[i - 1] != "\\"):
            if not in_str:
                in_str, str_ch = True, ch
            elif ch == str_ch:
                in_str = False
        elif ch == "#" and not in_str:
            code_part = line[:i]
            comment_part = line[i:]
            break

    s = esc(code_part)
    str_tokens = []

    def _stash_str(m):
        idx = len(str_tokens)
        str_tokens.append(f'<span class="py-str">{m.group(0)}</span>')
        return f"@@STR{idx}@@"

    s = re.sub(r'(&quot;.*?&quot;|&#x27;.*?&#x27;)', _stash_str, s)
    s = re.sub(
        r'\b(for|in|while|if|elif|else|def|return|try|except|break|True|False|None|and|or|not)\b',
        r'<span class="py-kw">\1</span>',
        s,
    )
    s = re.sub(r'\b(\d+)\b', r'<span class="py-num">\1</span>', s)
    s = re.sub(r'\b([a-zA-Z_][a-zA-Z0-9_]*)(?=\()', r'<span class="py-fn">\1</span>', s)
    for idx, tok in enumerate(str_tokens):
        s = s.replace(f"@@STR{idx}@@", tok)
    if comment_part:
        s += f'<span class="py-com">{esc(comment_part)}</span>'
    return s


def render_code_tray_html(tray: dict) -> str:
    theme = tray.get("theme", "hero")
    cls = "code-tray code-tray-villain" if theme == "villain" else "code-tray code-tray-hero"
    badge = esc(tray.get("badge", "PYTHON SPELLBOOK"))
    concept = esc(tray.get("concept", ""))
    lines_html = "\n".join(highlight_python_line(ln) for ln in tray.get("lines", []))
    output = tray.get("output", "")
    out_html = (
        f'<div class="ct-out"><span class="ct-out-lbl">&gt;&gt;</span> {esc(output)}</div>'
        if output
        else ""
    )
    return f'''
    <div class="wt-code-wrap">
      <div class="{cls}">
        <div class="ct-head">
          <div class="ct-dots"><span class="d1"></span><span class="d2"></span><span class="d3"></span></div>
          <div class="ct-badge">{badge}</div>
          <div class="ct-concept">{concept}</div>
        </div>
        <pre class="ct-code">{lines_html}</pre>
        {out_html}
      </div>
    </div>
    '''


def build_portrait_duo_html(sec, downloads_dir: Path):
    """Side-by-side two-column vertical manga panels (default 352x520 each, 24px center gutter)."""
    W = 800
    top_pad = sec.get("top_gutter", 96)
    bot_pad = sec.get("bottom_gutter", 34)
    ph = sec.get("height", 520)
    slots = [
        ("left", sec["left"], 36, 352, 16, 396),
        ("right", sec["right"], 412, 352, 404, 784),
    ]

    py = top_pad
    min_y, max_y = 0, top_pad + ph + bot_pad
    for _, side, px, pw, cmin, cmax in slots:
        for b in side.get("balloons", []):
            _, t_y, b_y = render_balloon_svg(b, px, py, pw, ph, clamp_min_x=cmin, clamp_max_x=cmax)
            min_y = min(min_y, t_y - 12)
            max_y = max(max_y, b_y + 18)

    shift_y = -min_y if min_y < 0 else 0
    py_adj = py + shift_y
    max_y = max(max_y + shift_y, py_adj + ph + bot_pad)

    defs_parts, img_parts, fx_parts, border_parts, sfx_parts, balloon_parts = [], [], [], [], [], []
    for key, side, px, pw, cmin, cmax in slots:
        clip_id = f"clip_{sec['id']}_{key}"
        img_path = str(downloads_dir / side["file"])
        data_uri = img_to_b64_data_uri(img_path, crop_box=side.get("crop"), max_w=640, quality=80)
        defs_parts.append(f'<clipPath id="{clip_id}"><rect x="{px}" y="{py_adj}" width="{pw}" height="{ph}"/></clipPath>')
        img_parts.append(
            f'<image href="{data_uri}" x="{px}" y="{py_adj}" width="{pw}" height="{ph}" '
            f'preserveAspectRatio="xMidYMid slice" clip-path="url(#{clip_id})"/>'
        )
        if side.get("speedlines"):
            sl = side["speedlines"]
            fx_parts.append(
                f'<g clip-path="url(#{clip_id})">'
                f'{svg_speedlines(px, py_adj, pw, ph, cx_pct=sl.get("cx", 50), cy_pct=sl.get("cy", 50), color=sl.get("color", "#FFFFFF"), opacity=sl.get("opacity", 0.42))}'
                f'</g>'
            )
        border_parts.append(f'<rect x="{px}" y="{py_adj}" width="{pw}" height="{ph}" fill="none" stroke="#18181B" stroke-width="2.8"/>')
        for s in side.get("sfx", []):
            sfx_parts.append(render_sfx_svg(s, px, py_adj, pw, ph))
        for b in side.get("balloons", []):
            svg, _, b_y = render_balloon_svg(b, px, py_adj, pw, ph, clamp_min_x=cmin, clamp_max_x=cmax)
            balloon_parts.append(svg)
            max_y = max(max_y, b_y + 18)

    total_h = int(math.ceil(max_y))
    code_tray_html = render_code_tray_html(sec["code_tray"]) if "code_tray" in sec else ""

    return f'''
    <div class="wt-block">
      <div class="wt-section" style="width:{W}px; height:{total_h}px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{total_h}" viewBox="0 0 {W} {total_h}">
          <defs>{"".join(defs_parts)}</defs>
          <rect x="0" y="0" width="{W}" height="{total_h}" fill="#FFFFFF"/>
          {"".join(img_parts)}
          {"".join(fx_parts)}
          {"".join(border_parts)}
          {"".join(sfx_parts)}
          {"".join(balloon_parts)}
        </svg>
      </div>
      {code_tray_html}
    </div>
    '''


def build_zoom_cascade_html(sec, downloads_dir: Path):
    """2- or 3-step diagonal staggered zoom-in / zoom-out panels."""
    W = 800
    steps = sec["steps"]
    n = len(steps)
    top_pad = sec.get("top_gutter", 72)
    bot_pad = sec.get("bottom_gutter", 30)
    box_w = 390 if n == 2 else 340
    box_h = 250 if n == 2 else 210
    step_dx = (728 - box_w) // max(1, n - 1)
    step_dy = 215 if n == 2 else 175

    defs_parts, img_parts, border_parts, sfx_parts, balloon_parts = [], [], [], [], []
    max_y = top_pad + box_h + (n - 1) * step_dy + bot_pad
    for idx, st in enumerate(steps):
        px = 36 + idx * step_dx
        py = top_pad + idx * step_dy
        clip_id = f"clip_{sec['id']}_st{idx}"
        img_path = str(downloads_dir / st["file"])
        data_uri = img_to_b64_data_uri(img_path, crop_box=st.get("crop"), max_w=640, quality=80)
        defs_parts.append(f'<clipPath id="{clip_id}"><rect x="{px}" y="{py}" width="{box_w}" height="{box_h}"/></clipPath>')
        img_parts.append(f'<rect x="{px+5}" y="{py+6}" width="{box_w}" height="{box_h}" fill="rgba(0,0,0,0.16)"/>')
        img_parts.append(
            f'<image href="{data_uri}" x="{px}" y="{py}" width="{box_w}" height="{box_h}" '
            f'preserveAspectRatio="xMidYMid slice" clip-path="url(#{clip_id})"/>'
        )
        border_parts.append(f'<rect x="{px}" y="{py}" width="{box_w}" height="{box_h}" fill="none" stroke="#18181B" stroke-width="2.8"/>')
        for s in st.get("sfx", []):
            sfx_parts.append(render_sfx_svg(s, px, py, box_w, box_h))
        for b in st.get("balloons", []):
            svg, _, b_y = render_balloon_svg(b, px, py, box_w, box_h)
            balloon_parts.append(svg)
            max_y = max(max_y, b_y + 18)

    total_h = int(math.ceil(max_y))
    return f'''
    <div class="wt-block">
      <div class="wt-section" style="width:{W}px; height:{total_h}px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{total_h}" viewBox="0 0 {W} {total_h}">
          <defs>{"".join(defs_parts)}</defs>
          <rect x="0" y="0" width="{W}" height="{total_h}" fill="#FFFFFF"/>
          {"".join(img_parts)}
          {"".join(border_parts)}
          {"".join(sfx_parts)}
          {"".join(balloon_parts)}
        </svg>
      </div>
    </div>
    '''


def build_webtoon_section_html(sec, downloads_dir: Path):
    layout = sec.get("layout", "framed")
    if layout in ("portrait_duo", "split_duo"):
        return build_portrait_duo_html(sec, downloads_dir)
    if layout == "zoom_cascade":
        return build_zoom_cascade_html(sec, downloads_dir)

    W = 800
    top_pad = sec.get("top_gutter", 92)
    bot_pad = sec.get("bottom_gutter", 34)
    img_path = str(downloads_dir / sec["file"])
    data_uri = img_to_b64_data_uri(img_path, crop_box=sec.get("crop"), max_w=880, quality=80)

    if layout == "full_bleed":
        px, pw, ph = 0, 800, sec.get("height", 440)
    elif layout == "inset_reaction":
        px, pw, ph = 26, 560, sec.get("height", 340)
    elif layout in ("portrait_tall", "tall_portrait"):
        # Full-page tall portrait (700x980) — fills the entire 800x1460 mobile page cleanly!
        px, pw, ph = 50, 700, sec.get("height", 980)
    elif layout in ("portrait_bleed", "portrait_cinematic"):
        # Edge-to-edge full-page vertical splash (800x1100)
        px, pw, ph = 0, 800, sec.get("height", 1100)
    elif layout == "eye_strip":
        px, pw, ph = 36, 728, sec.get("height", 195)
    elif layout == "floating_beat":
        px, pw, ph = 170, 460, sec.get("height", 380)
    else:
        px, pw, ph = 36, 728, sec.get("height", 415)

    py = top_pad
    total_h = top_pad + ph + bot_pad
    clip_id = f"clip_{sec['id']}"

    balloon_svgs = []
    min_y, max_y = 0, total_h
    for b in sec.get("balloons", []):
        svg, t_y, b_y = render_balloon_svg(b, px, py, pw, ph)
        balloon_svgs.append(svg)
        min_y = min(min_y, t_y - 12)
        max_y = max(max_y, b_y + 18)

    shift_y = -min_y if min_y < 0 else 0
    py_adj = py + shift_y
    if shift_y > 0:
        balloon_svgs = []
        max_y = py_adj + ph + bot_pad
        for b in sec.get("balloons", []):
            svg, _, b_y = render_balloon_svg(b, px, py_adj, pw, ph)
            balloon_svgs.append(svg)
            max_y = max(max_y, b_y + 20)
    else:
        max_y = max(max_y, py_adj + ph + bot_pad)

    inset_svg = ""
    sfx_svgs = [render_sfx_svg(s, px, py_adj, pw, ph) for s in sec.get("sfx", [])]

    if layout == "inset_reaction" and "inset" in sec:
        ins = sec["inset"]
        ins_uri = img_to_b64_data_uri(img_path, crop_box=ins["crop"], max_w=512, quality=84)
        ix, iy, iw, ih = ins.get("x", 545), py_adj + ins.get("y_off", 145), ins.get("w", 226), ins.get("h", 226)
        max_y = max(max_y, iy + ih + 26)
        inset_svg = f'''
        <g>
          <rect x="{ix+5}" y="{iy+6}" width="{iw}" height="{ih}" fill="rgba(0,0,0,0.18)"/>
          <image href="{ins_uri}" x="{ix}" y="{iy}" width="{iw}" height="{ih}" preserveAspectRatio="xMidYMid slice"/>
          <rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" fill="none" stroke="#18181B" stroke-width="2.8"/>
        </g>
        '''
        for s in ins.get("sfx", []):
            sfx_svgs.append(render_sfx_svg(s, ix, iy, iw, ih))

    total_h = int(math.ceil(max_y))

    fx_svg = ""
    if sec.get("speedlines"):
        sl = sec["speedlines"]
        fx_svg = f'''
        <g clip-path="url(#{clip_id})">
          {svg_speedlines(px, py_adj, pw, ph, cx_pct=sl.get("cx", 50), cy_pct=sl.get("cy", 50),
                          color=sl.get("color", "#FFFFFF"), opacity=sl.get("opacity", 0.45))}
        </g>
        '''

    panel_border = (
        ""
        if layout in ("full_bleed", "portrait_bleed", "portrait_cinematic")
        else f'<rect x="{px}" y="{py_adj}" width="{pw}" height="{ph}" fill="none" stroke="#18181B" stroke-width="2.8"/>'
    )

    code_tray_html = render_code_tray_html(sec["code_tray"]) if "code_tray" in sec else ""

    return f'''
    <div class="wt-block">
      <div class="wt-section" style="width:{W}px; height:{total_h}px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{total_h}" viewBox="0 0 {W} {total_h}">
          <defs>
            <clipPath id="{clip_id}">
              <rect x="{px}" y="{py_adj}" width="{pw}" height="{ph}"/>
            </clipPath>
          </defs>
          <rect x="0" y="0" width="{W}" height="{total_h}" fill="#FFFFFF"/>
          <image href="{data_uri}" x="{px}" y="{py_adj}" width="{pw}" height="{ph}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{clip_id})"/>
          {fx_svg}
          {panel_border}
          {inset_svg}
          {"".join(sfx_svgs)}
          {"".join(balloon_svgs)}
        </svg>
      </div>
      {code_tray_html}
    </div>
    '''


def measure_page_fill_pct(pil_img: Image.Image) -> float:
    """Returns % of vertical page height down to the lowest non-white pixel."""
    g = pil_img.convert("L")
    w, h = g.size
    px = g.load()
    lowest = 0
    for y in range(h - 1, -1, -2):
        row_has_ink = False
        for x in range(0, w, 4):
            if px[x, y] < 248:
                row_has_ink = True
                break
        if row_has_ink:
            lowest = y + 1
            break
    return 100.0 * lowest / h


def compile_webtoon(script_path: str, downloads_dir: str, out_pdf: str, out_png_dir: str):
    with open(script_path, "r", encoding="utf-8") as f:
        script = json.load(f)

    dl_dir = Path(downloads_dir)
    font_css = build_font_face_css([dl_dir, Path(script_path).resolve().parent])

    sections_html = [f'''
    <div class="wt-header">
      <div class="wt-kicker">{esc(script["kicker"])}</div>
      <div class="wt-title">{esc(script["title"])}</div>
      <div class="wt-sub">{esc(script["subtitle"])}</div>
    </div>
    ''']

    for sec in script["sections"]:
        sections_html.append(build_webtoon_section_html(sec, dl_dir))

    if "end_banner" in script:
        eb = script["end_banner"]
        sections_html.append(f'''
        <div class="wt-footer">
          <div class="wt-f-kicker">{esc(eb.get("kicker", ""))}</div>
          <div class="wt-f-title">{esc(eb.get("title", ""))}</div>
          <div class="wt-f-sub">{esc(eb.get("subtitle", ""))}</div>
        </div>
        ''')

    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  {font_css}
  @page {{
    size: 800px 1460px;
    margin: 0;
  }}
  body {{
    margin: 0;
    padding: 0;
    width: 800px;
    background: #FFFFFF;
    font-family: "Comic Neue", sans-serif;
  }}
  .wt-header {{
    width: 800px;
    padding: 36px 40px 28px 40px;
    box-sizing: border-box;
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    color: #F8FAFC;
    border-bottom: 5px solid #F59E0B;
    text-align: center;
  }}
  .wt-kicker {{
    font-size: 15px;
    letter-spacing: 3px;
    color: #FCD34D;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 8px;
  }}
  .wt-title {{
    font-family: "Bangers", sans-serif;
    font-size: 50px;
    letter-spacing: 2.5px;
    color: #FFFFFF;
    margin-bottom: 6px;
  }}
  .wt-sub {{
    font-size: 16px;
    color: #CBD5E1;
  }}
  .wt-block {{
    page-break-inside: avoid;
    break-inside: avoid;
    display: block;
    margin: 0;
    padding: 0;
  }}
  .wt-section {{
    display: block;
    margin: 0;
    padding: 0;
  }}
  .wt-code-wrap {{
    width: 800px;
    padding: 4px 36px 24px 36px;
    box-sizing: border-box;
    background: #FFFFFF;
  }}
  .code-tray {{
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 5px 14px rgba(15, 23, 42, 0.22);
    font-family: "DejaVu Sans Mono", "Courier New", monospace;
  }}
  .code-tray-hero {{
    background: #0F172A;
    border: 2.5px solid #38BDF8;
  }}
  .code-tray-villain {{
    background: #1B1028;
    border: 2.5px solid #A855F7;
  }}
  .ct-head {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 7px 14px;
    background: rgba(255, 255, 255, 0.06);
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    font-family: "Comic Neue", sans-serif;
  }}
  .ct-dots {{
    display: flex;
    gap: 6px;
  }}
  .ct-dots span {{
    display: inline-block;
    width: 9px;
    height: 9px;
    border-radius: 50%;
  }}
  .ct-dots .d1 {{ background: #F87171; }}
  .ct-dots .d2 {{ background: #FBBF24; }}
  .ct-dots .d3 {{ background: #34D399; }}
  .ct-badge {{
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #FCD34D;
    text-transform: uppercase;
  }}
  .code-tray-villain .ct-badge {{
    color: #E879F9;
  }}
  .ct-concept {{
    font-size: 12px;
    font-weight: 700;
    color: #94A3B8;
  }}
  .ct-code {{
    margin: 0;
    padding: 11px 18px;
    font-size: 14.5px;
    line-height: 1.46;
    color: #F1F5F9;
    white-space: pre-wrap;
  }}
  .py-kw {{ color: #C084FC; font-weight: 700; }}
  .py-str {{ color: #86EFAC; }}
  .py-fn {{ color: #38BDF8; font-weight: 700; }}
  .py-num {{ color: #FCD34D; }}
  .py-com {{ color: #94A3B8; font-style: italic; }}
  .ct-out {{
    padding: 7px 18px 9px 18px;
    background: rgba(56, 189, 248, 0.10);
    border-top: 1px solid rgba(255, 255, 255, 0.10);
    font-size: 13.5px;
    color: #E0F2FE;
  }}
  .code-tray-villain .ct-out {{
    background: rgba(168, 85, 247, 0.14);
    color: #F3E8FF;
  }}
  .ct-out-lbl {{
    color: #FBBF24;
    font-weight: 700;
    margin-right: 6px;
  }}
  .wt-footer {{
    width: 800px;
    padding: 34px 40px 38px 40px;
    box-sizing: border-box;
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    color: #F8FAFC;
    border-top: 5px solid #F59E0B;
    text-align: center;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  .wt-f-kicker {{
    font-size: 14px;
    letter-spacing: 3px;
    color: #FCD34D;
    font-weight: 700;
    margin-bottom: 8px;
  }}
  .wt-f-title {{
    font-family: "Bangers", sans-serif;
    font-size: 38px;
    letter-spacing: 2px;
    color: #FFFFFF;
    margin-bottom: 6px;
  }}
  .wt-f-sub {{
    font-size: 15px;
    color: #CBD5E1;
  }}
</style>
</head>
<body>
  {"".join(sections_html)}
</body>
</html>'''

    os.makedirs(Path(out_pdf).parent, exist_ok=True)
    os.makedirs(out_png_dir, exist_ok=True)
    weasyprint.HTML(string=html).write_pdf(out_pdf)

    pdf = pdfium.PdfDocument(out_pdf)
    rendered = []
    underfilled = []
    for i in range(len(pdf)):
        bmp = pdf[i].render(scale=1.2).to_pil()
        p_out = os.path.join(out_png_dir, f"page_{i+1:02d}.png")
        bmp.save(p_out)
        rendered.append(p_out)
        fill = measure_page_fill_pct(bmp)
        flag = "  <-- LOW FILL!" if (i < len(pdf) - 1 and fill < 72.0) else ""
        if flag:
            underfilled.append((i + 1, round(fill, 1)))
        print(f"  Page {i+1:02d}: fill={fill:5.1f}%{flag}")
    sz = os.path.getsize(out_pdf)
    print(f"Rendered {len(rendered)} mobile Webtoon pages -> {out_pdf} ({sz:,} bytes / {sz/1048576:.2f} MB)")
    if underfilled:
        print(f"UNDERFILLED PAGES (<72%): {underfilled}")
    else:
        print("PAGE-FILL AUDIT: 100% PASS (Zero half-blank pages!)")
    return rendered


if __name__ == "__main__":
    compile_webtoon(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
