#!/usr/bin/env python3
"""
Hero Kai's Pythonia Adventure — Manga/Webtoon Lettering & Dynamic Layout Engine v5.2
Non-destructive compositor: reads untouched text-free raw panels + structured JSON script,
and renders true Webtoon/Manhwa lettering with:
  - Embedded local Comic Neue (dialogue) + Bangers (SFX) via @font-face (exact reference typography)
  - 6 SVG Balloon Styles: speech, shout (spiky starburst), thought (cloud), whisper (dashed),
    glitch (jagged villain), narration (crisp white/drop-shadow box)
  - Exact Coordinate-Targeted Curved Bezier Tails pointing directly to (tx%, ty%)
  - Stacked-SVG Hand-Lettered SFX (Giongo) & Floating Mood Cues (Gitaigo) with crisp white halo
  - 9 Dynamic Webtoon Layout Modes:
      framed, full_bleed, inset_reaction,
      tall_portrait (3:4 / 2:3 vertical reveal), portrait_bleed (edge-to-edge tall splash),
      eye_strip (narrow manga eye-slit crop), floating_beat (centered quiet/comedy micro-panel),
      zoom_cascade (2- or 3-step staggered zoom-in/zoom-out sequence),
      split_duo (side-by-side straight or diagonal clash panels)
  - Optional Radial Manga Speedlines & Inline Python Spellbook Code Trays (0% art overlap)
  - Retina-safe JPEG compression to keep mobile Webtoon PDFs <= 6.35 MB
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


def font_face_css() -> str:
    """Embed local Comic Neue & Bangers TTFs if present in ./fonts or ~/.local/share/fonts."""
    candidates = [
        ("Comic Neue", "400", "normal", ["fonts/ComicNeue-Regular.ttf", "fonts/Comic_Neue/ComicNeue-Regular.ttf", os.path.expanduser("~/.local/share/fonts/ComicNeue-Regular.ttf")]),
        ("Comic Neue", "700", "normal", ["fonts/ComicNeue-Bold.ttf", "fonts/Comic_Neue/ComicNeue-Bold.ttf", os.path.expanduser("~/.local/share/fonts/ComicNeue-Bold.ttf")]),
        ("Comic Neue", "700", "italic", ["fonts/ComicNeue-BoldItalic.ttf", "fonts/Comic_Neue/ComicNeue-BoldItalic.ttf", os.path.expanduser("~/.local/share/fonts/ComicNeue-BoldItalic.ttf")]),
        ("Bangers", "400", "normal", ["fonts/Bangers/Bangers-Regular.ttf", "fonts/Bangers-Regular.ttf", os.path.expanduser("~/.local/share/fonts/Bangers-Regular.ttf")]),
        ("Bangers", "700", "normal", ["fonts/Bangers/Bangers-Regular.ttf", "fonts/Bangers-Regular.ttf", os.path.expanduser("~/.local/share/fonts/Bangers-Regular.ttf")]),
    ]
    rules = []
    for fam, weight, style, paths in candidates:
        for p in paths:
            if os.path.isfile(p):
                uri = Path(p).resolve().as_uri()
                rules.append(
                    f'@font-face {{ font-family: "{fam}"; src: url("{uri}") format("truetype"); '
                    f'font-weight: {weight}; font-style: {style}; }}'
                )
                break
    return "\n".join(rules)


def svg_spiky_starburst(cx, cy, rx, ry, spikes=14, seed_offset=0.2):
    pts = []
    n = spikes * 2
    for i in range(n):
        ang = (2 * math.pi * i / n) + seed_offset
        if i % 2 == 0:
            mod = 1.15 + 0.10 * math.sin(i * 1.7)
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


def svg_curved_tail(bx, by, tx, ty, base_half=13):
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


def render_balloon_svg(b, panel_x, panel_y, panel_w, panel_h):
    btype = b.get("type", "speech")
    text = b["text"].upper()
    bx = panel_x + panel_w * b["bx"] / 100.0
    by = panel_y + panel_h * b["by"] / 100.0
    max_chars = b.get("max_chars", 28 if btype == "narration" else 19)
    lines = wrap_comic_lines(text, max_chars=max_chars)
    font_size = b.get("font_size", 17.5 if btype != "narration" else 16.5)
    line_h = font_size * 1.24

    if btype == "narration":
        box_w = b.get("width", max(290, min(690, max(len(l) for l in lines) * font_size * 0.60 + 52)))
        box_h = len(lines) * line_h + 26
        x0 = max(24, min(800 - 24 - box_w, bx - box_w / 2))
        y0 = by - box_h / 2
        fill = b.get("fill", "#FFFFFF")
        stroke = b.get("stroke", "#18181B")
        text_svg = []
        start_y = y0 + 20 + font_size * 0.72
        for idx, ln in enumerate(lines):
            ty = start_y + idx * line_h
            text_svg.append(
                f'<text x="{x0 + box_w/2:.1f}" y="{ty:.1f}" text-anchor="middle" '
                f'font-family="Comic Neue, Inter, sans-serif" font-weight="700" '
                f'font-size="{font_size}" fill="#141418" letter-spacing="0.45">{esc(ln)}</text>'
            )
        svg = f'''
        <g>
          <rect x="{x0+4:.1f}" y="{y0+5:.1f}" width="{box_w:.1f}" height="{box_h:.1f}" fill="rgba(0,0,0,0.14)"/>
          <rect x="{x0:.1f}" y="{y0:.1f}" width="{box_w:.1f}" height="{box_h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="2.2"/>
          {"".join(text_svg)}
        </g>
        '''
        return svg, y0, y0 + box_h + 8

    # Generous airy Comic Neue oval padding matching reference
    est_w = max(len(l) for l in lines) * font_size * 0.58
    rx = b.get("rx", max(100, est_w * 0.68 + 32))
    ry = b.get("ry", max(46, len(lines) * line_h * 0.70 + 21))
    bx = max(rx + 16, min(800 - rx - 16, bx))

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
                    f'<circle cx="{cx_t:.1f}" cy="{cy_t:.1f}" r="{rad}" fill="#FFFFFF" stroke="#18181B" stroke-width="2.1"/>'
                )
            tail_svg = "".join(circles)
        else:
            t_path = svg_curved_tail(bx, by, tx, ty, base_half=13)
            tail_fill = "#1B1028" if btype == "glitch" else "#FFFFFF"
            tail_stroke = "#A855F7" if btype == "glitch" else "#18181B"
            tail_svg = (
                f'<path d="{t_path}" fill="{tail_fill}" stroke="{tail_stroke}" '
                f'stroke-width="2.3" stroke-linejoin="round"/>'
            )

    if btype == "shout":
        d_path = svg_spiky_starburst(bx, by, rx * 1.15, ry * 1.18, spikes=14)
        body_svg = f'<path d="{d_path}" fill="#FFFFFF" stroke="#18181B" stroke-width="2.3" stroke-linejoin="round"/>'
        mask_svg = f'<path d="{d_path}" fill="#FFFFFF" stroke="none"/>'
        text_color = "#111116"
        top_ext, bot_ext = by - ry * 1.42, by + ry * 1.42
    elif btype == "glitch":
        d_path = svg_glitch_balloon(bx, by, rx * 1.12, ry * 1.14, teeth=18)
        body_svg = f'<path d="{d_path}" fill="#1B1028" stroke="#A855F7" stroke-width="2.8" stroke-linejoin="miter"/>'
        mask_svg = f'<path d="{d_path}" fill="#1B1028" stroke="none"/>'
        text_color = "#F3E8FF"
        top_ext, bot_ext = by - ry * 1.34, by + ry * 1.34
    elif btype == "whisper":
        body_svg = (
            f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
            f'fill="#FFFFFF" stroke="#52525B" stroke-width="2.0" stroke-dasharray="6,4"/>'
        )
        mask_svg = f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{rx-2:.1f}" ry="{ry-2:.1f}" fill="#FFFFFF"/>'
        text_color = "#3F3F46"
        top_ext, bot_ext = by - ry - 6, by + ry + 6
    else:
        body_svg = (
            f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
            f'fill="#FFFFFF" stroke="#18181B" stroke-width="2.3"/>'
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
            f'font-family="Comic Neue, Inter, sans-serif" font-weight="700" '
            f'font-size="{font_size}" fill="{text_color}" letter-spacing="0.4">{esc(ln)}</text>'
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
    t = esc(text)
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'transform="rotate({rot} {x:.1f} {y:.1f})" '
        f'font-family="{font_fam}" font-size="{size}" font-weight="400" letter-spacing="{letter_sp}" '
        f'fill="none" stroke="{stroke}" stroke-width="{stroke_w}" stroke-linejoin="round">{t}</text>'
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'transform="rotate({rot} {x:.1f} {y:.1f})" '
        f'font-family="{font_fam}" font-size="{size}" font-weight="400" letter-spacing="{letter_sp}" '
        f'fill="{fill}" stroke="none">{t}</text>'
    )


def render_sfx_svg(sfx, panel_x, panel_y, panel_w, panel_h):
    kind = sfx.get("kind", "sfx")
    sx = panel_x + panel_w * sfx["x"] / 100.0
    sy = panel_y + panel_h * sfx["y"] / 100.0
    rot = sfx.get("rotate", -8)
    size = sfx.get("size", 54 if kind == "sfx" else 28)
    fill = sfx.get("fill", "#EA580C")
    stroke = sfx.get("stroke", "#FFFFFF")
    stroke_w = sfx.get("stroke_width", 10 if kind == "sfx" else 7)
    font_fam = "Bangers, Liberation Sans Narrow, sans-serif"
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
        r'\b(for|in|while|if|elif|else|def|return|True|False|None|and|or|not)\b',
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


def build_split_duo_section_html(sec, downloads_dir: Path):
    """Side-by-side straight or diagonal 2-panel manga clash / banter beat."""
    W = 800
    top_pad = sec.get("top_gutter", 72)
    bot_pad = sec.get("bottom_gutter", 32)
    ph = sec.get("height", 310)
    diagonal = sec.get("diagonal", True)
    slant = 28 if diagonal else 0
    gap = 16
    left_spec = sec["left"]
    right_spec = sec["right"]

    l_uri = img_to_b64_data_uri(str(downloads_dir / left_spec["file"]), crop_box=left_spec.get("crop"), max_w=540, quality=82)
    r_uri = img_to_b64_data_uri(str(downloads_dir / right_spec["file"]), crop_box=right_spec.get("crop"), max_w=540, quality=82)

    py = top_pad
    x_mid = W / 2.0
    cid_l = f"clip_{sec['id']}_L"
    cid_r = f"clip_{sec['id']}_R"

    # Left polygon & right polygon
    lp = f"36,{py} {x_mid + slant - gap/2:.1f},{py} {x_mid - slant - gap/2:.1f},{py+ph} 36,{py+ph}"
    rp = f"{x_mid + slant + gap/2:.1f},{py} 764,{py} 764,{py+ph} {x_mid - slant + gap/2:.1f},{py+ph}"

    balloon_svgs = []
    min_y, max_y = 0, top_pad + ph + bot_pad
    for b in sec.get("balloons", []):
        svg, t_y, b_y = render_balloon_svg(b, 36, py, 728, ph)
        balloon_svgs.append(svg)
        min_y = min(min_y, t_y - 12)
        max_y = max(max_y, b_y + 18)

    shift_y = -min_y if min_y < 0 else 0
    py_adj = py + shift_y
    if shift_y > 0:
        lp = f"36,{py_adj} {x_mid + slant - gap/2:.1f},{py_adj} {x_mid - slant - gap/2:.1f},{py_adj+ph} 36,{py_adj+ph}"
        rp = f"{x_mid + slant + gap/2:.1f},{py_adj} 764,{py_adj} 764,{py_adj+ph} {x_mid - slant + gap/2:.1f},{py_adj+ph}"
        balloon_svgs = []
        max_y = py_adj + ph + bot_pad
        for b in sec.get("balloons", []):
            svg, _, b_y = render_balloon_svg(b, 36, py_adj, 728, ph)
            balloon_svgs.append(svg)
            max_y = max(max_y, b_y + 18)

    sfx_svgs = [render_sfx_svg(s, 36, py_adj, 728, ph) for s in sec.get("sfx", [])]
    total_h = int(math.ceil(max_y))

    return f'''
    <div class="wt-block">
      <div class="wt-section" style="width:{W}px; height:{total_h}px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{total_h}" viewBox="0 0 {W} {total_h}">
          <defs>
            <clipPath id="{cid_l}"><polygon points="{lp}"/></clipPath>
            <clipPath id="{cid_r}"><polygon points="{rp}"/></clipPath>
          </defs>
          <rect x="0" y="0" width="{W}" height="{total_h}" fill="#FFFFFF"/>
          <image href="{l_uri}" x="36" y="{py_adj}" width="420" height="{ph}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid_l})"/>
          <image href="{r_uri}" x="344" y="{py_adj}" width="420" height="{ph}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid_r})"/>
          <polygon points="{lp}" fill="none" stroke="#18181B" stroke-width="3.0"/>
          <polygon points="{rp}" fill="none" stroke="#18181B" stroke-width="3.0"/>
          {"".join(sfx_svgs)}
          {"".join(balloon_svgs)}
        </svg>
      </div>
    </div>
    '''


def build_zoom_cascade_section_html(sec, downloads_dir: Path):
    """2- or 3-step staggered zoom-in or zoom-out manga cascade."""
    W = 800
    top_pad = sec.get("top_gutter", 68)
    bot_pad = sec.get("bottom_gutter", 34)
    steps = sec["steps"]  # list of {file, crop, x, y_off, w, h, sfx?}
    py = top_pad

    # First compute bounding height
    max_step_bot = 0
    for st in steps:
        max_step_bot = max(max_step_bot, py + st["y_off"] + st["h"])

    balloon_svgs = []
    min_y, max_y = 0, max_step_bot + bot_pad
    for b in sec.get("balloons", []):
        svg, t_y, b_y = render_balloon_svg(b, 36, py, 728, max_step_bot - py)
        balloon_svgs.append(svg)
        min_y = min(min_y, t_y - 12)
        max_y = max(max_y, b_y + 18)

    shift_y = -min_y if min_y < 0 else 0
    py_adj = py + shift_y
    if shift_y > 0:
        balloon_svgs = []
        max_y = max_step_bot + shift_y + bot_pad
        for b in sec.get("balloons", []):
            svg, _, b_y = render_balloon_svg(b, 36, py_adj, 728, max_step_bot - py)
            balloon_svgs.append(svg)
            max_y = max(max_y, b_y + 18)

    panels_svg = []
    sfx_svgs = [render_sfx_svg(s, 36, py_adj, 728, max_step_bot - py) for s in sec.get("sfx", [])]
    for idx, st in enumerate(steps):
        uri = img_to_b64_data_uri(str(downloads_dir / st["file"]), crop_box=st.get("crop"), max_w=780, quality=82)
        sx, sy, sw, sh = st["x"], py_adj + st["y_off"], st["w"], st["h"]
        cid = f"clip_{sec['id']}_s{idx}"
        panels_svg.append(f'''
          <defs><clipPath id="{cid}"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh}"/></clipPath></defs>
          <rect x="{sx+5}" y="{sy+6}" width="{sw}" height="{sh}" fill="rgba(0,0,0,0.14)"/>
          <image href="{uri}" x="{sx}" y="{sy}" width="{sw}" height="{sh}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid})"/>
          <rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="none" stroke="#18181B" stroke-width="3.0"/>
        ''')
        for s in st.get("sfx", []):
            sfx_svgs.append(render_sfx_svg(s, sx, sy, sw, sh))

    total_h = int(math.ceil(max_y))
    return f'''
    <div class="wt-block">
      <div class="wt-section" style="width:{W}px; height:{total_h}px;">
        <svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{total_h}" viewBox="0 0 {W} {total_h}">
          <rect x="0" y="0" width="{W}" height="{total_h}" fill="#FFFFFF"/>
          {"".join(panels_svg)}
          {"".join(sfx_svgs)}
          {"".join(balloon_svgs)}
        </svg>
      </div>
    </div>
    '''


def build_webtoon_section_html(sec, downloads_dir: Path):
    layout = sec.get("layout", "framed")
    if layout == "split_duo":
        return build_split_duo_section_html(sec, downloads_dir)
    if layout == "zoom_cascade":
        return build_zoom_cascade_section_html(sec, downloads_dir)

    W = 800
    top_pad = sec.get("top_gutter", 92)
    bot_pad = sec.get("bottom_gutter", 36)
    img_path = str(downloads_dir / sec["file"])
    crop_box = sec.get("crop")
    data_uri = img_to_b64_data_uri(img_path, crop_box=crop_box, max_w=880, quality=80)

    if layout == "full_bleed":
        px, pw, ph = 0, 800, sec.get("height", 440)
    elif layout == "portrait_bleed":
        px, pw, ph = 0, 800, sec.get("height", 1040)
    elif layout == "tall_portrait":
        pw = sec.get("width", 680)
        px = (W - pw) // 2
        ph = sec.get("height", 920)
    elif layout == "eye_strip":
        px, pw, ph = 36, 728, sec.get("height", 190)
    elif layout == "floating_beat":
        pw = sec.get("width", 440)
        ph = sec.get("height", 360)
        px = sec.get("x", (W - pw) // 2)
    elif layout == "inset_reaction":
        px, pw, ph = 26, 560, sec.get("height", 330)
    else:
        px, pw, ph = 36, 728, sec.get("height", 405)

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
        ins_path = str(downloads_dir / ins.get("file", sec["file"]))
        ins_uri = img_to_b64_data_uri(ins_path, crop_box=ins["crop"], max_w=512, quality=86)
        ix, iy, iw, ih = ins.get("x", 545), py_adj + ins.get("y_off", 145), ins.get("w", 226), ins.get("h", 226)
        max_y = max(max_y, iy + ih + 26)
        inset_svg = f'''
        <g>
          <rect x="{ix+5}" y="{iy+6}" width="{iw}" height="{ih}" fill="rgba(0,0,0,0.18)"/>
          <image href="{ins_uri}" x="{ix}" y="{iy}" width="{iw}" height="{ih}" preserveAspectRatio="xMidYMid slice"/>
          <rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" fill="none" stroke="#18181B" stroke-width="3.2"/>
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
        if layout in ("full_bleed", "portrait_bleed")
        else f'<rect x="{px}" y="{py_adj}" width="{pw}" height="{ph}" fill="none" stroke="#18181B" stroke-width="3.0"/>'
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


def compile_webtoon(script_path: str, downloads_dir: str, out_pdf: str, out_png_dir: str):
    with open(script_path, "r", encoding="utf-8") as f:
        script = json.load(f)

    dl_dir = Path(downloads_dir)
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

    ff_css = font_face_css()
    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  {ff_css}
  @page {{
    size: 800px 1460px;
    margin: 0;
  }}
  body {{
    margin: 0;
    padding: 0;
    width: 800px;
    background: #FFFFFF;
    font-family: "Comic Neue", "Inter", sans-serif;
  }}
  .wt-header {{
    width: 800px;
    padding: 40px 40px 32px 40px;
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
    margin-bottom: 10px;
  }}
  .wt-title {{
    font-family: "Bangers", sans-serif;
    font-size: 52px;
    letter-spacing: 2.5px;
    color: #FFFFFF;
    margin-bottom: 8px;
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
    padding: 4px 36px 26px 36px;
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
  .ct-dots {{ display: flex; gap: 6px; }}
  .ct-dots span {{ display: inline-block; width: 9px; height: 9px; border-radius: 50%; }}
  .ct-dots .d1 {{ background: #F87171; }}
  .ct-dots .d2 {{ background: #FBBF24; }}
  .ct-dots .d3 {{ background: #34D399; }}
  .ct-badge {{ font-size: 13px; font-weight: 700; letter-spacing: 1.5px; color: #FCD34D; text-transform: uppercase; }}
  .code-tray-villain .ct-badge {{ color: #E879F9; }}
  .ct-concept {{ font-size: 12px; font-weight: 700; color: #94A3B8; }}
  .ct-code {{ margin: 0; padding: 12px 18px; font-size: 14.5px; line-height: 1.48; color: #F1F5F9; white-space: pre-wrap; }}
  .py-kw {{ color: #C084FC; font-weight: 700; }}
  .py-str {{ color: #86EFAC; }}
  .py-fn {{ color: #38BDF8; font-weight: 700; }}
  .py-num {{ color: #FCD34D; }}
  .py-com {{ color: #94A3B8; font-style: italic; }}
  .ct-out {{ padding: 7px 18px 9px 18px; background: rgba(56, 189, 248, 0.10); border-top: 1px solid rgba(255, 255, 255, 0.10); font-size: 13.5px; color: #E0F2FE; }}
  .code-tray-villain .ct-out {{ background: rgba(168, 85, 247, 0.14); color: #F3E8FF; }}
  .ct-out-lbl {{ color: #FBBF24; font-weight: 700; margin-right: 6px; }}
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
  .wt-f-kicker {{ font-size: 14px; letter-spacing: 3px; color: #FCD34D; font-weight: 700; margin-bottom: 8px; }}
  .wt-f-title {{ font-family: "Bangers", sans-serif; font-size: 40px; letter-spacing: 2.5px; color: #FFFFFF; margin-bottom: 6px; }}
  .wt-f-sub {{ font-size: 15px; color: #CBD5E1; }}
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
    for i in range(len(pdf)):
        bmp = pdf[i].render(scale=1.2).to_pil()
        p_out = os.path.join(out_png_dir, f"page_{i+1:02d}.png")
        bmp.save(p_out)
        rendered.append(p_out)
    sz = os.path.getsize(out_pdf)
    print(f"Rendered {len(rendered)} mobile Webtoon pages -> {out_pdf} ({sz:,} bytes / {sz/1048576:.2f} MB)")
    return rendered


if __name__ == "__main__":
    compile_webtoon(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
