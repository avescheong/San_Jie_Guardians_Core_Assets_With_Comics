## name: webtoon-manga-lettering-engine description: Non-destructive Full-Page Manga and Webtoon SVG lettering, Comic Neue + Bangers typography, portrait/landscape rhythm, zoom micro-panels, balloon, SFX, and vertical-scroll layout engine (v5.3) for text-free raw comic panels. Use whenever the user asks to letter raw comic or manga panels, add expressive speech balloons, spiky shout starbursts, curved Bezier tails, narration boxes, cascading SFX (Giongo), floating mood cues (Gitaigo), speedlines, tall portrait splashes, eye-strips, diagonal split-duos, zoom cascades, zoomed reaction insets, or inline code/spellbook trays to any Webtoon, manhwa, or comic chapter (such as Hero Kai Volume 1/2, San Jie Guardians, or any new illustrated project). allowed-tools: default_api drive google
# Webtoon & Manga Lettering Engine (v5.3 — Full-Page Portrait & Micro-Zoom Standard)
Non-destructive SVG + WeasyPrint lettering and full-page vertical-scroll Webtoon compositor (scripts/manga_compositor_v5.py). Transforms untouched, text-free raw panels into expressive, magazine-tight Manga/Manhwa/Webtoon pages (800x1460px mobile PDFs, <= 6.35 MB) with Comic Neue + Bangers typography, mixed portrait/landscape rhythm, zero face overlap, and 95–99% full-page vertical fill.
## When to Use
Converting text-free raw comic, manga, or Webtoon panels into a finished mobile-friendly vertical-scroll Webtoon PDF (pure English or pure Traditional Chinese editions).
Upgrading static landscape-only chapters into dynamic Manga v5.3 episodes combining full-bleed tall portraits (2:3/3:4), landscape action/dialogue panels, and zero-cost micro-zoom beats (eye_strip, zoom_cascade, split_duo, inset_reaction, floating_beat).
Adding expressive balloons, gutter-bleeding curved Bezier tails, straddling narration boxes, two-pass white-halo Bangers SFX (Giongo), floating mood cues (Gitaigo), radial speedlines, and optional inline Python Spellbook code trays.
## Canonical Typography Lock (Comic Neue + Bangers)
Always match the exact studio lettering stack:

Dialogue & Narration: Comic Neue (Bold, all-caps, airy rx/ry oval padding, crisp 2.2–2.3px strokes).
SFX (Giongo), Mood Cues (Gitaigo), & Episode Titles: Bangers with two-pass white halo stroke (_stacked_stroked_text()).
Offline Font Vault on Drive: Download ComicNeue-Bold.ttf (15Bbdqw17qGYOxTroBnvNs6WYh-KpGk3y) and Bangers-Regular.ttf (1lREJr364ejRPYOVZ-LBessBZSY5pVgSX) from Hero_Kai_Comic/00_fonts (1PkNXws3RDPq-lyO7U5edFyaSx2SB2Ivk) into ./fonts/ (or ~/.local/share/fonts/) before rendering. manga_compositor_v5.py auto-loads them via @font-face.
## The 9 Dynamic Layout Modes & Full-Page Packing Law
Never stack 3+ identical landscape rectangles or leave 30–60% blank white space at the bottom of a page. Target ~35–40% Portrait, ~35–40% Landscape, ~20–25% Micro-Zoom per chapter, packing every 800x1460px page to 95–99% full height WITHOUT shrinking artwork:

portrait_bleed (800px full-bleed width, 830–1040px height): Edge-to-edge vertical reveals (2:3/3:4 native portrait art) for portal drops, towering villains, spell awakenings, and sweeping finales. Pair with one 410–430px landscape panel or 240–260px split_duo so the page totals ~1410–1445px.
tall_portrait (660–700px framed width, 860–960px height): Framed vertical character reveal or emotional beat.
full_bleed (800px wide, 410–445px height): Edge-to-edge landscape action, magic clash, or panoramic vista.
framed (728px wide, 380–425px height): Crisp bordered dialogue/storytelling beat. Three framed/full-bleed panels (~420px + gutters) pack one full 1460px page cleanly.
eye_strip (728x170–190px narrow horizontal slit): Zero-cost smart crop (crop: [x0, y0, x1, y1]) focused on eyes, widening pupils, or subtle realization.
split_duo (diagonal: true|false, 230–265px height): Side-by-side 2-panel clash or rapid banter beat (left: {file, crop}, right: {file, crop}).
zoom_cascade (steps: [{file, crop, x, y_off, w, h, sfx}, ...]): Staggered 2- or 3-step zoom-in (e.g., kicking boot -> wide bush crash; hugging hands -> determined smile) or zoom-out sequence.
inset_reaction (main panel + inset: {crop, x, y_off, w, h, sfx}): Main beat paired with an overlapping zoomed reaction box (e.g., lonely pixel friend, wobbling boots).
floating_beat (440x340px centered micro-panel): Quiet touching pause or deadpan comedy beat framed by deliberate white space (ma).

Full-Page Fill Rule (Never Shrink Existing Art): If a page has >25% empty bottom void after pairing portraits with micro-zooms, do not shrink panels to squeeze more in; instead, generate 1–3 additional fun, emotional, or native 2:3/3:4 portrait panels to fill the exact story beat naturally.
## The 4 Core Lettering Elements + Optional Trays
Expressive Balloons & Curved Bezier Tails: speech (organic oval), shout (spiky starburst), thought (oval + dot trail), whisper (dashed oval), glitch (jagged dark violet villain balloon), and narration (crisp white drop-shadowed box straddling top/bottom edges).
Two-Pass White-Halo SFX (Giongo): Bold tilted Bangers text (POOF!!, SKIIIID!!, KRA-KOOM!!, or cascade: ["VWHOO—", "OOOSH!!"]).
Floating Mood Cues (Gitaigo): Smaller angled white-outlined cues (tap... tap..., sigh..., ping!, ba-dump..., chirp! chirp!).
Optional Speedlines & Inline Python Spellbook Trays: Clipped radial speedlines: {cx, cy, color, opacity} and dark-mode code_tray: {theme: "hero"|"villain", badge, concept, lines, output} with 0% art overlap.
## Workflow Steps
### 1. Preserve Raw Artwork & Fetch Fonts
Never paint text onto master raw art. Download ComicNeue-Bold.ttf and Bangers-Regular.ttf from 00_fonts (1PkNXws3RDPq-lyO7U5edFyaSx2SB2Ivk) into ./fonts/ and keep raw panels in a dedicated read-only folder.
### 2. Plan Portrait/Landscape/Zoom Mix & Generate Needed Art
Audit the chapter's existing raw panels. Generate 4–6 native 2:3/3:4 portrait panels (plus any fun/emotional bridge panels needed for 95–99% full-page fill) anchored to canonical 4.0H character turnarounds, visually QA them, and upload to the chapter's Drive folder.
### 3. Inspect 0–100% Coordinate Grids Before Scripting
Overlay 0–100% X/Y grids (every 10%) onto 2x2 contact sheets of all chapter panels and inspect every sheet with view_file to lock exact (bx, by, tx, ty) coordinates, open SFX pockets, and eye_strip/split_duo/zoom_cascade crop boxes.
### 4. Author JSON, Compile, Visually QA Every Page & Snap to 95–99% Fill
Run:

python3 scripts/manga_compositor_v5.py chapter_script.json raw_panels_dir output_chapter.pdf qa_pages_dir

Stitch qa_pages_dir/page_*.png into 4-up contact sheets and inspect every single page with view_file:

Verify 0% face/hair overlap from balloons or tail tips.
Verify Comic Neue + Bangers rendered cleanly (never DejaVu fallback).
Verify every page is 95–99% full (tighten 15–35px overflows so no panel kicks an orphan onto the next page, and no page ends with >25% blank white void).
Verify final mobile PDF is <= 6.35 MB.
## Zero Face-Overlap Iron Law (Mandatory QA Gate)
NEVER cover any Hero or NPC face, eyes, nose, mouth, mustache, or helmet/head silhouette with speech/thought/shout balloons, shout spikes, tail tips, or SFX (Giongo/Gitaigo).
When characters sit in the upper third of a panel (especially split_duo or close-ups), always lift balloons cleanly into the white top gutter (by: -18 to -26 with top_gutter: 95–112) and stop tail tips cleanly outside/above the head silhouette (never dipping onto eyes, cheeks, or mustaches).
Place bold Bangers SFX in open sky, background, or spark/impact zones—never across a character's eyes or face.
## Gotchas
Never use single-pass paint-order="stroke" in WeasyPrint SVG: Always use _stacked_stroked_text() (stroke pass first, fill pass second).
Trim natural watercolor borders on portrait art: If a generated portrait has a thin cream paper frame, pass crop: [0.03, 0.02, 0.97, 0.98] in JSON so portrait_bleed is truly edge-to-edge.
Keep pure-language editions separate: Render English-only (EN) and Traditional Chinese-only (ZH_TW) editions as separate JSON scripts/PDFs.
