# 13_Workspace_Skills_Used — San Jie Guardians Comic Production Toolkit
Archived Date: 2026-11-23
Parent Workspace: Hero_Kai_San_Jie_Guardians (1tyHf-nXF2-HcUMLD2comNcR1uupw8qQ9)
Companion Playbook: 05_SANJIE_COMIC_PROBLEMS_SOLUTIONS_AND_QUALITY_PLAYBOOK.md (1wjpAGnKh4QEtB4EpmF0lu_TWbnOTmOmF__7BAXNbhUA)

This folder stores verbatim backups of all 8 workspace skills (plus the bundled manga_compositor_v5.py script from webtoon-manga-lettering-engine) used to build the Hero Kai × San Jie 17 Guardians comic up to the Full-Page Manga v5.3 standard.
## Skills Included in This Folder

| # | File Name | Skill Name | Primary Role in Comic Production |
| :--- | :--- | :--- | :--- |
| 1 | san-jie-guardians-zero-drift-sdk_SKILL.md | san-jie-guardians-zero-drift-sdk | Core project SSOT: 17-student + 18-pet visual DNA lock, Drive folder/file IDs, zero-reupload reference protocol, stage-locked pet evolution anchors, and Graft invariants. |
| 2 | webtoon-manga-lettering-engine_SKILL.md | webtoon-manga-lettering-engine | Full-Page Manga v5.3 SVG/WeasyPrint lettering & layout engine (Comic Neue + Bangers, 9 dynamic layout modes, 95–99% full-page fill, Zero Face-Overlap Iron Law). |
| 2b | webtoon-manga-lettering-engine_manga_compositor_v5.py | (Bundled Script) | Deterministic Python SVG/WeasyPrint compositor script bundled inside webtoon-manga-lettering-engine. |
| 3 | visual-drift-auditor_SKILL.md | visual-drift-auditor | Zero-tolerance 6-Point Visual QA gate, parallel chapter audit fan-out, Ensemble-Split Anti-Crowd-Drift Rule, lossless PIL border cropping, and remediation custody. |
| 4 | hero-kai-character-sdk_SKILL.md | hero-kai-character-sdk | Hero Kai Genome v5.0 SSOT (Normal 4.0H proportions, cobalt-blue eyes, Tzu Chi buckle, sword-free lock, Anti-Collage Rule, Normal vs. Chibi track isolation). |
| 5 | kai-webtoon-comic-pipeline_SKILL.md | kai-webtoon-comic-pipeline | End-to-end Hero Kai bilingual comic & Webtoon production workflow (JSON scripts, text-free raw art, dual A4 print + 800px Webtoon exports). |
| 6 | pythonia-world-assets-sdk_SKILL.md | pythonia-world-assets-sdk | Read-only upstream SSOT router for 001_Kai_Assets / Hero_Kai_Core_Assets (Hero Kai, Bug King hexapod lock, 100% plant-based world lock, canonical turnarounds). |
| 7 | graft-code-steward_SKILL.md | graft-code-steward | Persistent engineering learnings vault (000_Graft_Memory/learnings/), always_follow: true invariants, and pipeline blast-radius code maps. |
| 8 | vm-drive-reconciliation_SKILL.md | vm-drive-reconciliation | Archive-Never-Delete custody (99_Archive_Superseded), SHA-256 verification, <5 MB auto-chunking / <= 6.35 MB PDF ceiling, and handover synchronization. |

## Recommended Execution Order for Future Chapters / Comics
Bootstrap & Canon: san-jie-guardians-zero-drift-sdk + hero-kai-character-sdk + pythonia-world-assets-sdk
Panel Generation & Visual QA: visual-drift-auditor (6-Point Matrix + Ensemble-Split Rule)
Full-Page v5.3 Lettering & PDF Export: webtoon-manga-lettering-engine (+ kai-webtoon-comic-pipeline for dual A4/Webtoon builds)
Custody, Handover & Learnings: vm-drive-reconciliation + graft-code-steward
