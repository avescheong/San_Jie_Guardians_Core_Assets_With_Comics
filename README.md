# Hero Kai × San Jie Guardians — Core Asset Repository

Core production asset repository for **Hero Kai × San Jie Guardians (三捷班)** — covering the **17 Student Guardians**, **18 Guardian Pets**, **12-Chapter Bilingual Graphic Novel**, **Interactive Web Hubs**, **Collector Posters**, **Animations**, and the **Zero-Drift Story & Visual Engine**.

This repository serves as the single source of truth (SSOT) for developing:
- **San Jie Comics** (A4 bilingual print PDFs & 800px Webtoon vertical strips)
- **Websites & Interactive Hubs** (Gift Hub, Dual-Edition 3D Flip Gallery, Unified Comic Reader)
- **Future Products** (keepsake books, collector posters, animated shorts, banners, and merchandise)

---

## Key Root Documents & Interactive Hubs

| File | Description |
| :--- | :--- |
| [`AGENT.md`](./AGENT.md) | Workspace router & cold-start protocol |
| [`HANDOVER_CURRENT.md`](./HANDOVER_CURRENT.md) | Current production baseline & next steps |
| [`ASSET_INVENTORY_INDEX.md`](./ASSET_INVENTORY_INDEX.md) | Folder-by-folder inventory & gap tracker |
| [`SanJie_Pet_Evolution_Index_And_Kai_Gift_Hub_v7.html`](./SanJie_Pet_Evolution_Index_And_Kai_Gift_Hub_v7.html) | Interactive Pet Evolution & Gift Hub |
| [`SanJie_17_Guardians_Dual_Edition_Flip_Gallery.html`](./SanJie_17_Guardians_Dual_Edition_Flip_Gallery.html) | Interactive 3D Flip Gallery (Series A ↔ Series B) |
| [`SanJie_17_Guardians_Unified_Comic_Reader_v4.html`](./SanJie_17_Guardians_Unified_Comic_Reader_v4.html) | Unified Bilingual Comic Reader (Prologue + Ch. 01–12) |
| [`SanJie_17_Guardians_Enhanced_Manga_Story_Bible_v2.pdf`](./SanJie_17_Guardians_Enhanced_Manga_Story_Bible_v2.pdf) | Enhanced Manga Story Bible (v2) |
| [`SanJie_Class_July2026_HeroKai_18_Guardians_Keepsake_Book_A4.pdf`](./SanJie_Class_July2026_HeroKai_18_Guardians_Keepsake_Book_A4.pdf) | Printable A4 Keepsake & Activity Book |

### Master Plans & Playbooks
- [`00_MASTER_PLAN_SAN_JIE_PETS_GIFT_AND_EVOLUTION.md`](./00_MASTER_PLAN_SAN_JIE_PETS_GIFT_AND_EVOLUTION.md)
- [`02_PET_PROPS_AND_RELICS_MASTER_PLAN.md`](./02_PET_PROPS_AND_RELICS_MASTER_PLAN.md)
- [`03_DIGIMON_PYTHON_MANGA_MASTER_STORY_PLAN_17_GUARDIANS.md`](./03_DIGIMON_PYTHON_MANGA_MASTER_STORY_PLAN_17_GUARDIANS.md)
- [`05_SANJIE_COMIC_PROBLEMS_SOLUTIONS_AND_QUALITY_PLAYBOOK.md`](./05_SANJIE_COMIC_PROBLEMS_SOLUTIONS_AND_QUALITY_PLAYBOOK.md)

---

## Repository Structure

| Folder | Contents |
| :--- | :--- |
| `00_Original_Hand_Drawn_Drawings/` | Original kids' hand-drawn scans & reference name cards |
| `00_SAN_JIE_ZERO_DRIFT_ENGINE_SSOT/` | Locked master boards, story state JSON, registry, and zero-drift engine scripts |
| `01_Hero_Kai_Story_Keyframes/` | Hero Kai keyframe illustrations |
| `02_Pet_Evolution_Sheets_All_18/` | Evolution sheets for all 18 guardian pets |
| `03_Pet_Turnaround_Sheets_All_18/` | 3-stage pet turnaround sheets (54 sheets) |
| `04_Student_Spellcaster_Cast_All_18/` | Student spellcaster cast master boards |
| `05_Hero_Kai_SanJie_Bilingual_Comic/` | Bilingual comic episodes, 387 raw panels, compositing scripts, PDFs & Webtoon strips |
| `06_Student_Individual_Turnarounds_All_17/` | Individual character turnarounds for all 17 students |
| `07_Pet_Props_And_Relics_Boards_All_18/` | Bilingual props & relics reference boards |
| `08_New_Saga_NPC_Turnarounds/` | New saga NPC turnaround sheets |
| `09_SeriesA_Editorial_Champion_Posters_All_17/` | Series A editorial champion posters (JPGs + A4 PDF) |
| `10_SeriesB_Cinematic_Ultimate_Posters_All_17/` | Series B cinematic ultimate posters (JPGs + A4 PDF) |
| `11_Animation/` | Cinema A4 `.mp4` animations for Series B |
| `12_Personalised_Banners_Trainer_S1_S2_S3_All_17/` | 21:9 panoramic banners (text-free masters + bilingual editions) |
| `13_Workspace_Skills_Used/` | Agent skill definitions & pipeline documentation |
| `99_Archive_Superseded/` | *(Gitignored)* Superseded drafts, duplicates, and converted `.md.docx` originals |

---

## Notes for GitHub & Future Development
- **Privacy:** This repository contains student names, keepsake books, and original class drawings. Keep the GitHub repository **Private** unless you have explicit permission to publish them.
- **Large Media:** `99_Archive_Superseded/` is excluded via `.gitignore` to keep the repository under GitHub's 1 GB soft limit. If you add more `.mp4` animations or high-res PDFs, consider enabling **Git LFS** (`git lfs track "*.mp4"`).
