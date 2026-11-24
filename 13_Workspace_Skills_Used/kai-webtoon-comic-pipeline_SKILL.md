## name: kai-webtoon-comic-pipeline description: End-to-end bilingual (English and Traditional Chinese) comic book and Webtoon production pipeline for Hero Kai (05_Kai_Comic, Volume 1 expansions, Volume 2+, and 07_Webpage_Comic_Intergration). Use whenever scripting comic episodes, generating text-free comic panels, compositing bilingual speech bubbles and Python Spellbook scrolls, exporting A4 print PDFs and 800px Webtoon vertical strips or sliced WebP tiles, or updating webtoon_manifest.json.
# kai-webtoon-comic-pipeline
Produce canon-locked bilingual Hero Kai comics and Webtoon episodes from JSON scripts to dual print-ready A4 PDFs and 800px Webtoon web reader packages.
## When to Use
Scripting a new Hero Kai comic chapter, epilogue expansion, or Volume 2+ episode (e.g., VOL2_EP*_SCRIPT.json).
Generating raw clean comic panel artwork conditioned on Normal 4.0H character anchors.
Compositing English and Traditional Chinese (en + zh_TW) speech bubbles, narration boxes, and syntax-highlighted Python Spellbook scrolls onto panels.
Exporting A4 300-DPI print pages, compressed Master PDFs, 800px vertical Webtoon strips, or sliced WebP tiles and updating webtoon_manifest.json in 07_Webpage_Comic_Intergration.
## Steps
### 1. Bootstrap Canon and Workspace Layout
Read 001_Kai_Assets/agent.md, 00_MUST_READ_KAI_WORKFLOW_STYLE_AND_PREFERENCES.md (1at0MoNCxoAL12rbzTcp6NkSilPLOnx1FrfWL_uCn_E8), and 05_Kai_Comic/HANDOVER_CURRENT.md before generating or editing anything. Follow the canonical 7-folder workspace structure inside 05_Kai_Comic (1KKFiiPSA8wz7Ng8g2fEP0s6m9i04ctnr):

00_master_plan_and_bibles/: Volume outlines, cast registries (cast_reference_registry.json), and style bibles.
01_scripts_and_beatboards/: Bilingual JSON episode scripts (en + zh_TW).
02_sdk_and_compositor/: Deterministic scripts (comic_ticket_compiler.py, comic_page_compositor.py).
03_panel_art_raw/: Clean, text-free generated panels (*_RAW_CLEAN.jpg).
04_panel_art_approved/: Verified panels after visual QA.
05_composed_pages/: 300-DPI A4 composed JPEGs (PAGE_###_*.jpg).
06_exports_print_and_web/: Act PDFs, Master PDF, and full-height Webtoon episode strips.
07_Webpage_Comic_Intergration/ (1Bql9gVZ3a9YMaG1Pqy2qERIegYr_J8Wp): Website-ready 800px strips, sliced WebP tiles, episode thumbnails, webtoon_manifest.json, and portable comic.html reader.
### 2. Author Bilingual Episode JSON Script
Write structured JSON scripts containing panel IDs, scene beats, cast IDs, camera framing, bilingual dialogue (en and zh_TW), narration boxes, SFX callouts, and any Python Spellbook code snippets. Enforce lore locks:

Zero Ember rule: companions are strictly String (golden-tan terrier) and the Baby Praying Mantis Spell Guardian.
100% vegetarian / plant-based food economy across all scenes.
Correct character disambiguation (Ch. 3 Iron Outpost Blacksmith vs. hatless Master Grimsby with brass goggles; 6-limbed Bug King).
### 3. Generate 100% Text-Free Panel Art (Normal 4.0H Track)
Never ask AI image generators to render speech bubbles, captions, SFX, or Python code. Generate clean, text-free panels in sepia ink + watercolor/gouache style:

Condition Hero Kai strictly on Normal 4.0H anchors (00_KAI_NORMAL_4H_FRONT_ANCHOR.jpg, 00_KAI_NORMAL_4H_TURNAROUND_CLEAN.jpg, 00_KAI_TZU_CHI_BELT_BUCKLE_ANCHOR.jpg).
Condition supporting cast on 03_Supporting_Cast_Normal_4H/ sheets (never mix Chibi 2.0H-2.2H sheets or demoted text-heavy/brown-eyed legacy sheets).
Enforce Kai's invariants: 11-year-old 4.0H proportions, cobalt-blue irises, Tzu Chi winged-lotus emerald belt buckle, golden crescent clasp, bilateral hip asymmetry (viewer-left plain brown satchel, viewer-right 3 potion vials), and sword-free base default unless the beat calls for a tool/weapon.
Hard cap: generate at most 10 panels per batch so you can visually inspect before scaling.
### 4. Composite Lettering and Dual Exports in Python
Run deterministic Python compositors to overlay crisp bilingual speech bubbles, narration captions, and syntax-highlighted Python Spellbook scrolls:

A4 Print Master: 210 x 297 mm at 300 DPI JPEGs in 05_composed_pages/, plus a compressed <10 MB combined PDF in 06_exports_print_and_web/ for Drive sharing.
Webtoon Vertical Export: 800px wide vertical bilingual strips (EP##_*_WEBTOON_BILINGUAL.jpg), sliced WebP tiles for smooth mobile/desktop loading, and 800px episode thumbnails.
Manifest Sync: Update webtoon_manifest.json with exact episode metadata, page/tile counts, and file paths so comic.html loads new episodes automatically.
### 5. Run Stage-4 Visual Polish Pass and Handover
Inspect composed pages and Webtoon strips side-by-side for face/hair drift, eye-color drift, hip-gear inversion, text overflow, or panel gutter clipping. Fix defects surgically, archive superseded drafts to 99_Archive, upload outputs to Drive, and update 05_Kai_Comic/HANDOVER_CURRENT.md.
## Gotchas
Never let an image generator bake text or speech bubbles into raw panel art; AI lettering breaks Traditional Chinese characters and prevents bilingual edits.
Never cross-contaminate Normal 4.0H comic panels with Chibi 2.2H game sprite anchors.
Keep combined sharing PDFs under 10 MB (or split >10 MB print archives into <5 MB .part_* chunks with a SHA-256 reassemble_*.py script).
