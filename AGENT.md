# AGENT.md — San Jie Class (July 2026) Hero Kai × 18 Guardians Workspace Router (v2.0)

- **Workspace Root (`08_Kids_Hand_Drawn_Version`):** `1tyHf-nXF2-HcUMLD2comNcR1uupw8qQ9`
- **Parent Project (`05_Kai_Comic`):** `1KKFiiPSA8wz7Ng8g2fEP0s6m9i04ctnr`
- **Upstream Hero Kai Canon SSOT (Read-Only, `001_Kai_Assets`):** `1vLC13sHopidqHhvoQZFQxuNWXLDC8gjg`
- **Dedicated Zero-Drift Skill:** `san-jie-guardians-zero-drift-sdk` (load first in every new session!)
- **Master Inventory & Gap Tracker:** `ASSET_INVENTORY_INDEX.md` (at root)
- **Active Handover:** `HANDOVER_CURRENT.md` (at root)

## Cold-Start Protocol (Read in 30 Seconds)

1. Activate skill `san-jie-guardians-zero-drift-sdk` for all 17 students' 1:1 visual DNA, all 18 pets' Stage 0-3 specs, relics, habitats, and locked negative contracts.
2. Read `HANDOVER_CURRENT.md` and `ASSET_INVENTORY_INDEX.md` at this root.
3. For zero-drift visual references without asking the user to re-upload images, pull directly from `00_SAN_JIE_ZERO_DRIFT_ENGINE_SSOT` (`1skzEAMjg6NbYaVUSrNKM0gCCARze_MMU`):
   - `MASTER_BOARD_01_ALL_17_STUDENTS_1TO1_LOCK.jpg` (`1niKMw0BECT6e0jLydbiCjeiaowecyGlf`)
   - `MASTER_BOARD_02_ALL_17_PETS_EVOLUTION_LOCK.jpg` (`1STBdvBvSUOcaJboSCbZTgRTk5zFrM6Yr`)
   - `MASTER_BOARD_03_ALL_17_RELICS_AND_PROPS_LOCK.jpg` (`1v9jwvXiQ_5hRWjWeN88CSEt4EHUX3SPT`)
   - `SanJie_17_Guardians_Zero_Drift_Master_Boards_Bible.pdf` (`1e_vKspotUYep6Q0MJZDYPq5aR0M9AH7C`)
   - `sanjie_zero_drift_engine.py` (`1252OuHgMcXpr3PmyA55goQ_WdZP1Yu4p`)

## Canonical Folder Map

| Folder | Drive ID | Purpose |
| :--- | :--- | :--- |
| `00_SAN_JIE_ZERO_DRIFT_ENGINE_SSOT` | `1skzEAMjg6NbYaVUSrNKM0gCCARze_MMU` | 1:1 Master Lock Boards (01-03), Bible PDF, Zero-Drift Python Engine |
| `00_Original_Hand_Drawn_Drawings` | `196vCgrSldSpRTrbD3Hsetl8LzJQHj56v` | `Name Card.pdf` (17 photos), original student pet & Kai drawings |
| `01_Hero_Kai_Story_Keyframes` | `1sVzrHCwc0A004ykpc5Cs6sV_AbKZcggS` | 2 Canon-Locked Hero Kai story keyframes |
| `02_Pet_Evolution_Sheets_All_18` | `16-KgM3kDIovSbvwcXkr_hfLIdGfwg3xG` | 18 clean 4-stage pet evolution sheets (`EVO_01`-`EVO_18`) |
| `03_Pet_Turnaround_Sheets_All_18` | `1J6roWSMIOl6cBkGx1R1dzQg1K1b5nJwb` | 54 four-view pet turnaround sheets (18 pets x Stages 1-3) |
| `04_Student_Spellcaster_Cast_All_18` | `1Jwm-u_DhDYbsNzme6xt0wGNOBK79KBcL` | 4 cast boards (`CAST_01`-`CAST_04`) |
| `05_Hero_Kai_SanJie_Bilingual_Comic` | `11J-N2kLwRSvdkvq-rl1eYJGnGY5HmdvC` | Ep 01 v2 PDF, Ep 02 PDF, Ep 02 800px Webtoon strip, JSON scripts, raw panels |
| `06_Student_Individual_Turnarounds_All_17` | `1_z06Sn2W2eFq18vWDNV-xJmkApa4BXWR` | 17 individual named 3-view (Front/3-4/Back) student turnarounds |
| `07_Pet_Props_And_Relics_Boards_All_18` | `1lPBHbYSJ9OllrOz_noOKiVOwNus-aB_o` | 6 bilingual 3x3 Pet Props & Relics boards (`PROPS_01`-`PROPS_06`) |
| `09_SeriesA_Editorial_Champion_Posters_All_17` | `1a87k_CwQfGPSEfVwEP90Xy2xE0o9UE7C` | 17 warm-parchment Editorial Champion posters + combined A4 PDF |
| `10_SeriesB_Cinematic_Ultimate_Posters_All_17` | `1i2RoRJA8HtWMjdsxpCoTzgPOOvNAcO47` | 17 full-bleed Cinematic Habitat & Ultimate-Power posters + combined A4 PDF |
| `99_Archive_Superseded` | `10KmNhDKHj0p8YpL4bfEvSGosKBezZ3T9` | Archived superseded builds (Hub v6, cutout posters v3/v4, old handovers) |

## Locked Production Invariants

1. **Roster Lock:** Strictly 17 students have photos in `Name Card.pdf` (Tan Jie Khe Jacob excluded; Ko Zi Xing has Pet #18 only until photo is provided).
2. **Hero Kai Genome v5.0 (Normal 4.0H):** Golden-honey tousled hair, cobalt-blue eyes, forest-green hooded cloak with gold crescent clasp, cream tunic, Tzu Chi winged-lotus & white Dharma sailing ship emerald shield belt buckle, viewer-left brown pouch, viewer-right 3 glass potion vials (green/red/blue), sword-free default.
3. **Zero Ember & 100% Plant-Based World:** Companions are strictly String + Baby Praying Mantis; all food/snacks are vegetarian/plant-based.
4. **Unified Painted Art Over Cutouts:** Never cut watercolor characters out of turnaround sheets onto dark backgrounds; use turnarounds as 1:1 `image_references` to paint unified scenes on `#F3EFE6` parchment (editorial) or full-bleed habitats (cinema).
5. **100% Text-Free Raw Art + Python NotoSansCJK Compositing:** Never let AI draw captions, speech bubbles, or labels; composite all bilingual English + Traditional Chinese text deterministically.
6. **Binary HTML Upload Rule:** Always upload self-contained HTML files with embedded base64 images via `file://` with `mime_type: "application/octet-stream"` (never `text/html` conversion) and keep single Drive uploads under `7.0 MB` raw (`<10 MB` base64 JSON envelope).
