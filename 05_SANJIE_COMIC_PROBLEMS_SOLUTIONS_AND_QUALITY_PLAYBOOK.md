# San Jie Class (July 2026) — Hero Kai × 17 Guardians: Comic Production Problems, Proven Solutions & v5.3 Quality Playbook
Last Updated: 2026-11-23
Workspace Root: Hero_Kai_San_Jie_Guardians (1tyHf-nXF2-HcUMLD2comNcR1uupw8qQ9)
Current Quality Standard: Full-Page Manga & Webtoon v5.3 (Comic Neue Bold + Bangers, 9 dynamic layout modes, 88–99% vertical page fill, 0% face overlap, <= 6.35 MB mobile PDFs)
Archived Workspace Skills Folder: 13_Workspace_Skills_Used (1Dhddt2EJrCHNeoMBIxCdkcbFgdkP0h2o)
Active Handover & SSOT References: HANDOVER_CURRENT.md, AGENT.md, ASSET_INVENTORY_INDEX.md, and 00_SAN_JIE_ZERO_DRIFT_ENGINE_SSOT
# 1. Current Production Baseline (v5.3 Snapshot)
This document records every major visual, narrative, lettering, layout, and infrastructure problem encountered while building the Hero Kai × 17 Guardians comic, paired with the exact proven solutions that produced the latest v5.3 quality standard. Follow this playbook on remaining chapters and all future comic projects to reproduce the same quality without repeating past mistakes.

Raw Panel Master Vault (00_Raw_Panels_Tracked_For_Edit): 387/387 Zero-Drift Director's Cut panels (342 visually audited baseline panels + 45 Director's Cut expansion panels) plus bespoke 3:4 portrait panels added per chapter for v5.3 full-page pacing.
v5.3 Full-Page Webtoon Rollout (05_Hero_Kai_SanJie_Bilingual_Comic): 9 of 13 chapters complete (Act 1 & Act 2 100% done — Batches 1–3: CH00 through CH08, achieving 87.1%–99.4% vertical page fill and all PDFs under 6.35 MB). Batches 4–5 (CH09–CH12) are currently on v5.1 and ready for v5.3 upgrade (with Teacher Cheong's 4-view turnaround locked for the CH12 reveal).
Production Engine & Permanent Offline Fonts: manga_compositor_v5.py, ComicNeue-Bold.ttf, and Bangers-Regular.ttf.
Companion Zero-Drift Deliverables: 17-page Series A Editorial Champion Posters PDF (5.81 MB, 16/16 flagged posters remediated), 17-page Series B Cinematic Ultimate Posters PDF (5.91 MB, 9/17 S3_Grand posters remediated), and 34 personalised 21:9 banners in 12_Personalised_Banners_Trainer_S1_S2_S3_All_17.
# 2. Master Problems & Proven Solutions Playbook
## Domain A — Character, Pet & Roster Visual Drift

| Problem Faced | Root Cause | Proven Solution & Locked Standard | Canonical Reference |
| :--- | :--- | :--- | :--- |
| Severe face, hair, glasses, and outfit drift on students and pets | Passing multi-character collage boards (MASTER_BOARD_01/02) into image generation (tiny faces) or prompting pets from text nicknames alone | Anti-Collage Rule + Zero-Reupload Drive Retrieval: Never pass collage boards into image_gen. Always retrieve individual full-res turnarounds directly from Drive via context_service_agent:get_context (1:1 individual student + stage-matched pet turnaround). Run a 1–2 panel pilot gate before scaling batches. | 06_Student_Individual_Turnarounds_All_17, 03_Pet_Turnaround_Sheets_All_18 |
| Excluded roster members or wrong glasses/hair creeping into panels | Stale 18-student drafts and unconstrained hair/glasses generation | Strict 17-Student & DNA Lock: Strictly 17 students (#01 Ng Shuang – #17 Uvincc Long); #18 Ko Zi Xing and Tan Jie Khe Jacob permanently excluded. 100% black hair on all 17 students; glasses ONLY on #01, #09, #10, #13, #14, #15. Core cast locks: Hero Kai 4.0H sword-free, Ember 1 head/2 wings/1 tail, Lord Malcode 6 limbs. | sanjie_zero_drift_engine.py, 08_New_Saga_NPC_Turnarounds |
| Generation-turn self-checks missed subtle defects (30 Act 1 panels, 9/17 Series B posters, 16/17 Series A posters) | Confirmation bias during generation turns; subtle errors (extra limbs/tails, wrong boots, pet species swaps like Sticky -> mermaid or Sky-Pup -> Golden Retriever) slipped through | Fresh Read-Only Parallel Visual Drift Audit Gate: Never trust generation-turn self-checks. Fan out parallel read-only audit subagents (1 per chapter/Act) inspecting every panel at full resolution via view_file against canonical turnarounds using the 6-Point Zero-Tolerance Matrix. | 2026-11-23 Graft Learning Note, visual-drift-auditor skill |
| Regenerating border-only defects introduced fresh character drift | Re-rolling an otherwise on-model panel just to remove white/cream outer margins | Lossless PIL Border Cropping: For on-model panels with outer white/paper frames, apply lossless PIL cropping (or crop: [0.03, 0.02, 0.97, 0.98] in JSON) instead of regenerating the artwork. | webtoon-manga-lettering-engine & visual-drift-auditor skills |
| Crowd drift, character clones, outfit bleeding, and uneven screentime in 17-kid group scenes | Image generators cannot reliably hold 15–17 distinct faces in one frame | Ensemble-Split Anti-Crowd-Drift Rule: Cap frames at 4–5 locked individual turnarounds with explicit left-to-right positional mapping. Split all-17 arrival, battle, feast, and lantern scenes into sequential 4–5 student squad panels, verified by a 3-Act Cast-Inclusion Audit (+45 Director's Cut panels). | HANDOVER_CURRENT.md |

## Domain B — Story Pacing, Evolution Continuity & World Canon

| Problem Faced | Root Cause | Proven Solution & Locked Standard | Canonical Reference |
| :--- | :--- | :--- | :--- |
| Premature Stage 2 evolutions & rushed 1-panel snap-cut transformations | Early 3–5 page mini-episodes compressed 6 story beats into 12 panels with no narrative breathing room or automated stage gating | Act-Gated Evolution Lock + Digimon-Style 4-Panel Slow Evolution: Hard-lock Act 1 (CH00–CH04) to S1_Baby only; unlock S2_Site in Act 2 (CH05–CH08) and S3_Grand in Act 3 (CH09–CH12). Every evolution uses a 4-panel sequence: Relic Resonance -> Luminous Cocoon -> Slow-Motion Unfurling -> Bonded Reveal, enforced programmatically by sanjie_story_engine.py. | 04_SANJIE_17_GUARDIANS_30PP_MASTER_STORY_REPLAN_AND_ENGINE_SPEC, sanjie_story_engine.py |
| Dual-villain canon split (Bug King II vs. Vex) & flat mid-season stakes | Unbridged antagonist lore between Volume 1 and the San Jie saga | Unified Rival Redemption Arc & Humanitarian Stakes: Establish Vex/Alias-0 as a lonely coder whose unsafe override unlocked Lord Malcode (Bug King II), leading to Vex's Act 3 redemption and Teacher Cheong's CH12 reveal inside Malcode's cracking armor. Lock 100% plant-based food and non-lethal debugging/purification magic. | SanJie_17_Guardians_Enhanced_Manga_Story_Bible_v2.pdf |

## Domain C — Typography, Lettering & Face-Overlap Defects (v4 to v5.3)

| Problem Faced | Root Cause | Proven Solution & Locked Standard | Canonical Reference |
| :--- | :--- | :--- | :--- |
| AI-baked text broke Traditional Chinese, prevented edits, and leaked garbled runes (TG4A, RPK) onto stones/scrolls | Asking image generators to draw text or leaving uninspected flat surfaces (bridges, rune cubes, scrolls, lanterns) | 100% Text-Free Raw Art + Non-Destructive SVG Compositing: Keep raw art permanently untouched and text-free. Render all dialogue, SFX, and Python Spellbook trays deterministically from JSON scripts via manga_compositor_v5.py. Zoom-inspect flat surfaces during visual QA. |  |
| Generic fallback fonts (DejaVu) looked stiff and non-comic | Offline sandbox VM has no outbound internet access to download Google Fonts | Permanent Offline Drive Font Vault: Stored ComicNeue-Bold.ttf (dialogue/narration) and Bangers-Regular.ttf (tilted SFX/titles) in Drive and loaded them locally via @font-face in manga_compositor_v5.py. |  |
| WeasyPrint SVG paint-order="stroke" rendering defects & broken vertical CJK spines | WeasyPrint SVG engine limitations on single-pass stroked text and CSS vertical writing modes | Two-Pass Stacked Stroked SVG & Explicit CJK <br/> Stacks: Render crisp white-halo SFX using _stacked_stroked_text() (stroke pass first, fill pass second). Render vertical Chinese poster spines (三捷班) using explicit <br/> character stacks. |  |
| Speech balloons, shout spikes, tail tips, or bold SFX covered Hero Kai's or NPCs' faces | Estimating balloon coordinates blindly without grid mapping or placing balloons inside upper-third character art | Zero Face-Overlap Iron Law: Overlay 0–100% X/Y coordinate grids on 2x2 contact sheets before authoring JSON. Lift upper-third balloons cleanly into the white top gutter (by: -14 to -26, top_gutter: 95–122), stop curved Bezier tail tips outside head silhouettes, place SFX in open sky/spark pockets, and visually inspect 4-up rendered QA contact sheets of every page. |  |

## Domain D — Page Rhythm, Portrait Variety & Half-Blank Page Voids (v5.1 to v5.3 Breakthrough)

| Problem Faced | Root Cause | Proven Solution & Locked Standard | Canonical Reference |
| :--- | :--- | :--- | :--- |
| Monotonous stacked landscape rectangles & 30–60% empty white voids at page bottoms | Relying solely on 16:9 landscape panels in a vertical 800×1460px mobile scroll format | v5.3 Full-Page Packing Law & 9 Dynamic Layout Modes: Mix ~35–40% native 2:3/3:4 Portrait (portrait_bleed, tall_portrait, portrait_duo), ~35–40% Landscape (full_bleed, framed), and ~20–25% zero-cost Micro-Zooms (eye_strip, split_duo, zoom_cascade, inset_reaction, floating_beat). Pack every page to 88–99% vertical fill WITHOUT shrinking art — generate 2–6 bespoke portrait/story panels per chapter to fill natural story beats, monitored by the built-in <72% fill diagnostic in manga_compositor_v5.py. | CH06 v5.3 PDF, CH07 v5.3 PDF, CH08 v5.3 PDF |

## Domain E — Posters, Banners, Drive Size Ceilings & Custody Governance

| Problem Faced | Root Cause | Proven Solution & Locked Standard | Canonical Reference |
| :--- | :--- | :--- | :--- |
| White-patch cutout halos on dark poster backgrounds & nameplate collisions on 21:9 banners | Flood-filling white turnaround backgrounds onto colored scenes; letting art crowd the bottom-left corner of banners | Unified Painted Scenes & Reserved Safe Zones: Generate unified painted compositions directly on #F6F3EA parchment (Series A) or inside full-bleed habitats (Series B). For 21:9 banners (Student + S1 + S2 + S3), pass all 4 turnarounds together, reserve a clean bottom-left nameplate safe zone, and ship paired Text-Free + Bilingual editions. | 09_SeriesA_Editorial_Champion_Posters_All_17, 12_Personalised_Banners_Trainer_S1_S2_S3_All_17 |
| Google Drive 10 MB upload failures & stripped base64 images in HTML apps | Raw high-DPI PDFs exceeding Drive's 10 MB payload ceiling; text/html conversion stripping <img> tags | Size Ceiling & Binary MIME Discipline: Keep compiled mobile/A4 PDFs <= 6.35 MB (175 DPI for 17-page A4 posters; max_w=880, quality=80 JPEG for Webtoon PDFs). Upload standalone HTML apps with mime_type: "application/octet-stream". Auto-split >9.5 MB bundles into <5 MB SHA-256 chunks with reassemble_*.py. | vm-drive-reconciliation skill |
| Lost earlier versions, upstream/website desync, & cold-start context drift across sessions | Overwriting files directly or updating only one workspace without syncing handovers | Archive-Never-Delete Custody + Root Orientation Suite: Always move superseded files into 99_Archive_Superseded (never delete). Mirror updated posters atomically to both upstream and website folders, record always_follow: true rules in Graft Memory, and update HANDOVER_CURRENT.md after every milestone. | 99_Archive_Superseded, HANDOVER_CURRENT.md |

# 3. Repeatable 6-Step Formula for Future Chapters & New Comics (v5.3 Quality Gate)
Use this exact sequence for Batches 4–5 (CH09–CH12) and any future comic volume:

Cold-Start & Canon Lock: Load san-jie-guardians-zero-drift-sdk + webtoon-manga-lettering-engine, read HANDOVER_CURRENT.md, and download manga_compositor_v5.py, ComicNeue-Bold.ttf, and Bangers-Regular.ttf into ./fonts/.
Audit Raw Art & Generate Bespoke Portraits: Verify all chapter raw panels are 100% text-free and on-model against individual Drive turnarounds (never collages). Generate 2–6 native 2:3/3:4 portrait panels (anchored via context_service_agent:get_context) and visually inspect every generated image with view_file before uploading.
Overlay 0–100% Coordinate Grids: Stitch chapter panels into 2x2 coordinate-grid contact sheets (10% grid lines) and inspect every sheet with view_file to lock exact (bx, by, tx, ty) coordinates, open SFX pockets, and micro-zoom crop boxes (eye_strip, split_duo, zoom_cascade, inset_reaction).
Author JSON Script & Enforce Layout Mix: Balance ~35–40% Portrait, ~35–40% Landscape, and ~20–25% Micro-Zoom beats. Lift balloons into top gutters (by: -14 to -26) to guarantee 0% face/hair overlap, and add inline Python Spellbook trays on coding beats.
Compile & Visual QA Every Page: Run manga_compositor_v5.py, stitch rendered PNG pages into 4-up QA contact sheets, and verify with view_file: (a) real Comic Neue + Bangers rendered, (b) 0% face/eye/helmet overlap, (c) 88–99% vertical fill on every non-final page without shrinking artwork, and (d) final PDF <= 6.35 MB.
Custody & Handover: Move any superseded PDFs/panels to 99_Archive_Superseded, upload the verified JSON + PDF to 05_Hero_Kai_SanJie_Bilingual_Comic, and update HANDOVER_CURRENT.md.
# 4. Workspace Skills Used to Build This Comic
All 8 workspace skills used across the San Jie Guardians comic pipeline (plus the bundled manga_compositor_v5.py script) are backed up verbatim in 13_Workspace_Skills_Used so future sessions or team members can inspect or re-import the exact toolkit:


| # | Workspace Skill | Role in Comic Production |
| :--- | :--- | :--- |
| 1 | san-jie-guardians-zero-drift-sdk | Primary project SDK: 17-student + 18-pet visual DNA table, Drive SSOT IDs, zero-reupload protocol, stage-locked pet anchors, and 4-panel evolution rules. |
| 2 | webtoon-manga-lettering-engine | Full-Page Manga v5.3 SVG/WeasyPrint engine (Comic Neue + Bangers, 9 dynamic layout modes, 95–99% full-page fill, Zero Face-Overlap Iron Law, plus manga_compositor_v5.py). |
| 3 | visual-drift-auditor | Zero-tolerance 6-Point Visual QA gate, parallel chapter audit fan-out, Ensemble-Split Anti-Crowd-Drift Rule, lossless PIL border cropping, and remediation custody. |
| 4 | hero-kai-character-sdk | Hero Kai Genome v5.0 SSOT (Normal 4.0H proportions, cobalt-blue eyes, Tzu Chi buckle, sword-free lock, Anti-Collage Rule, and Normal vs. Chibi track isolation). |
| 5 | kai-webtoon-comic-pipeline | End-to-end Hero Kai bilingual comic & Webtoon production workflow (JSON script structure, text-free raw art rules, dual A4 print + 800px Webtoon exports). |
| 6 | pythonia-world-assets-sdk | Upstream read-only SSOT router for 001_Kai_Assets / Hero_Kai_Core_Assets (Hero Kai, Bug King hexapod lock, 100% plant-based world lock, canonical turnarounds). |
| 7 | graft-code-steward | Persistent engineering learnings vault (000_Graft_Memory/learnings/), always_follow: true invariants, and pipeline blast-radius code mapping. |
| 8 | vm-drive-reconciliation | Archive-Never-Delete custody (99_Archive_Superseded), SHA-256 parity checks, <5 MB auto-chunking / <= 6.35 MB PDF discipline, and handover synchronization. |
