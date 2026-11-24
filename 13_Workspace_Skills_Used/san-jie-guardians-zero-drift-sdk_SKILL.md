## name: san-jie-guardians-zero-drift-sdk description: Zero-drift character, pet, relic, poster, comic, and web-gallery SDK for the San Jie Class (July 2026) Hero Kai x 17 Guardians project (Hero_Kai_San_Jie_Guardians). Eliminates re-uploading reference images by routing directly to canonical Google Drive SSOT individual turnarounds, locked 17-student and 18-pet visual DNA, stage-locked pet evolution anchors, v4.4 Top-Band comic compositor, and proven Graft engineering invariants. Auto-activates for San Jie Class, 17 Guardians, Series A/B posters, bilingual comics, Webtoon strips, Gift Hub v7, or Flip Gallery tasks. allowed-tools: drive context_service_agent image_gen default_api google
# San Jie Guardians Zero-Drift SDK (Hero_Kai_San_Jie_Guardians)
This skill is the single operational reference for the San Jie Class (July 2026) Hero Kai x 17 Guardians project (Hero_Kai_San_Jie_Guardians, Drive ID 1tyHf-nXF2-HcUMLD2comNcR1uupw8qQ9). It prevents character and pet drift, premature pet evolution, white-patch cutout defects, Drive upload failures, and repeated reference-image uploads across sessions.
## 1. Mandatory Cold-Start & Zero-Reupload Protocol (NEVER Ask User to Re-Upload)
Before generating any new poster, comic panel, Webtoon strip, turnaround, or gallery update:

Read HANDOVER_CURRENT.md (1B1MS6Ctq3RQvbzYHQiLfUaJ5MZXdsqmk3waf4WTPnpA) inside Hero_Kai_San_Jie_Guardians (1tyHf-nXF2-HcUMLD2comNcR1uupw8qQ9) for the latest snapshot state.
Zero-Reupload file_reference Retrieval: Never ask the user to drop reference photos or drawings into chat. Call context_service_agent:get_context with the exact canonical turnaround filename (from 06_Student_Individual_Turnarounds_All_17, 03_Pet_Turnaround_Sheets_All_18, or Hero_Kai_Core_Assets) to retrieve a verbatim file_reference, and pass it into image_gen.
Anti-Collage Rule: Never pass multi-character grid/collage boards (such as MASTER_BOARD_01, MASTER_BOARD_02, or Cast Boards) into image_gen — small faces in collages cause severe drift. Always pass individual full-res turnarounds, and run a 1–2 panel pilot gate before scaling to a batch.
For any Hero Kai appearance, follow hero-kai-character-sdk (Genome v5.0, Normal 4.0H proportions, Zero Ember rule, 100% plant-based world, 00_KAI_NORMAL_4H_TURNAROUND_CLEAN.jpg 1P31jHSAVtBrmEzf0apbGMGNODu6yIUbR).
## 2. Canonical Google Drive SSOT Directory Map
Use these exact Drive IDs for O(1) retrieval (moving into Hero_Kai_* GitHub mirror root 1ltkE71xaVrIq_Rs2vusOaXqf8up210j6 preserved all IDs):

Workspace Root (Hero_Kai_San_Jie_Guardians, formerly 08_Kids_Hand_Drawn_Version): 1tyHf-nXF2-HcUMLD2comNcR1uupw8qQ9
Root Orientation Docs:
AGENT.md (v2.0): 1p52uChV9BPoALmBKuPIYtK2pU80iMdM_rfBOfIwmiAE
ASSET_INVENTORY_INDEX.md: 16xWNcImMgvojHNHZsSZvfNfw1Rvc-tWz60KFkHXmv9M
HANDOVER_CURRENT.md: 1B1MS6Ctq3RQvbzYHQiLfUaJ5MZXdsqmk3waf4WTPnpA
Zero-Drift SSOT Vault (00_SAN_JIE_ZERO_DRIFT_ENGINE_SSOT): 1skzEAMjg6NbYaVUSrNKM0gCCARze_MMU
SanJie_17_Guardians_Zero_Drift_Master_Boards_Bible.pdf: 1e_vKspotUYep6Q0MJZDYPq5aR0M9AH7C
sanjie_zero_drift_engine.py: 1252OuHgMcXpr3PmyA55goQ_WdZP1Yu4p
Original Hand-Drawn Drawings & Photos (00_Original_Hand_Drawn_Drawings): 196vCgrSldSpRTrbD3Hsetl8LzJQHj56v (Name Card.pdf: 1SeFrtXnW8CqgO2gG-3GJ6zCvyEtH_4ui)
Hero Kai Story Keyframes (01_Hero_Kai_Story_Keyframes): 1sVzrHCwc0A004ykpc5Cs6sV_AbKZcggS
Pet Evolution Sheets (02_Pet_Evolution_Sheets_All_18): 16-KgM3kDIovSbvwcXkr_hfLIdGfwg3xG
Pet Turnarounds (03_Pet_Turnaround_Sheets_All_18): 1J6roWSMIOl6cBkGx1R1dzQg1K1b5nJwb (contains S1_Baby, S2_Site, and S3_Grand 4-view sheets per pet — mandatory image_gen anchor folder for every pet)
Student Cast Boards (04_Student_Spellcaster_Cast_All_18): 1Jwm-u_DhDYbsNzme6xt0wGNOBK79KBcL
Bilingual Comics (05_Hero_Kai_SanJie_Bilingual_Comic): 11J-N2kLwRSvdkvq-rl1eYJGnGY5HmdvC
Individual Student Turnarounds (06_Student_Individual_Turnarounds_All_17): 1_z06Sn2W2eFq18vWDNV-xJmkApa4BXWR (17 named JPGs — primary image_gen anchor folder for students)
Pet Props & Relics Boards (07_Pet_Props_And_Relics_Boards_All_18): 1lPBHbYSJ9OllrOz_noOKiVOwNus-aB_o
Series A Editorial Champion Posters (09_SeriesA_Editorial_Champion_Posters_All_17): 1a87k_CwQfGPSEfVwEP90Xy2xE0o9UE7C (17-page PDF: 1ybbrpc1Bs1burtYesmNyqNkFz9T7c-LE)
Series B Cinematic Ultimate Posters (10_SeriesB_Cinematic_Ultimate_Posters_All_17): 1i2RoRJA8HtWMjdsxpCoTzgPOOvNAcO47 (17-page PDF: 1C5O9W07nJV32ksyz6QzTJu6s0X6a_ta2)
Root Interactive Web Apps:
SanJie_Pet_Evolution_Index_And_Kai_Gift_Hub_v7.html: 1kugBq96sah9ub9J2hiL5hbAXzD4537HY
SanJie_17_Guardians_Dual_Edition_Flip_Gallery.html: 1ShCF7bmWypvXNwrhr24Ogny6qi3RCP6-
Shared Comic Engines (Hero_Kai_Comic/02_sdk_and_compositor, 1J0_iVSE7OdVcAQX0jm_JyTrMwuTn10ul): comic_page_compositor_v4.py (1KBfkrm-3kmN7SujADZ245Zi4VSnbLNJY) + comic_qa_preflight_linter.py (10rXpCVUx6Ui-Ttt4TZE6bpkiBMuRt7Jx)
Superseded Archive (99_Archive_Superseded): 10KmNhDKHj0p8YpL4bfEvSGosKBezZ3T9
Graft Learnings Vault (000_Graft_Memory/learnings/): 13Zwo3E-yo9yV1oZozNIEiHqxW0kyLfgp
## 3. Roster Scope & Canon Boundaries (STRICT 17-STUDENT LOCK)
Strictly 17 Students (#01 Ng Shuang through #17 Uvincc Long): Only students #01 through #17 are in the active roster, comic reader, and storyline.
Permanently Excluded: Ko Zi Xing (#18) and Tan Jie Khe Jacob are permanently removed from the active roster, comic reader, and storyline. Never generate or re-add them.
## 4. Locked 17-Student + Partner Pet Visual DNA Table
Always lock prompts 1:1 to these exact traits (never alter glasses, hairstyles, outfit palette, pet species, or relic):


| # | Student (EN / ZH) | Locked Face, Hair & Outfit DNA | Partner Pet | Relic (EN / ZH) | Series B Habitat |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 01 | Ng Shuang (吴双) | Chin-length black bob, wispy bangs, round gold wire glasses; sky-blue/cream capelet, cream tunic, light-blue pants, tan cuffed boots | 雷冰火鹿 Tempest Stag | Aurora Prism Bell (極光稜鏡鈴) | Alpine Aurora Peak |
| 02 | Lim Dao Yang (林道羏) | Tousled black hair, feathery bangs, no glasses; crimson laced vest, cream tunic, leather cross-body satchel, brown pants, laced boots | BARKLEY | Smiley Hearth Medallion (笑臉暖爐徽章) | Sun-Forge Lantern Valley |
| 03 | Carlzen Lim Jia Tzen (林家诚) | Short cropped black hair, wide smile; aqua-teal tunic, yellow backpack, brown utility belt, brown cargo pants, dark-brown boots | Sticky | Tide-Ember Lantern Drop (潮焰提燈露) | Crystal Waterfall Grotto |
| 04 | Ong Yu Chen (洪语晨) | Black mid-high ponytail, no glasses; cream puffy-sleeve tunic, dual flame-orange/frost-blue woven scarf, brown trousers, explorer shoes | 火冰狗 Ignis-Frost Pup | Twin-Balance Bandana (冰火平衡領巾) | Glacier-Ember Canyon |
| 05 | Kua Jun Ming (葛峻铭) | Neat crew-cut black hair, steady round face; crimson-red & forest-green layered guardian tunic, leather belt with bamboo scroll, green trousers, tan boots | Javin Jr | Aegis Bamboo-Iron Scroll (竹鐵盾卷軸) | Emerald Bamboo Sanctuary |
| 06 | Ooi Yu Bhor (黄煜博) | Straight black hair with neat fringe, oval face; cobalt-blue sleeveless vest over cream laced tunic, dark-brown trousers, dark-brown boots, brass compass | DOYB | Star-Chrono Pocket Compass (星時懷錶羅盤) | Celestial Hilltop Observatory |
| 07 | Boey Yi Ren (梅译仁) | Long straight center-parted black hair; blush-pink hooded cloak, rose-pink overdress over cream tunic, petal belt pouch, cream leggings, brown boots | Poppy | Dewdrop Petal Teacup (露珠花瓣茶杯) | Cherry Blossom Sanctuary |
| 08 | Lee Khang Kok (李强国) | Thick spiky black hair, strong eyebrows; cream adventurer tunic, leather cross-strap & coiled climbing rope, khaki trousers, dark-brown cuffed boots | Bro | Iron-Heart Knapsack & Rope (鐵心行囊與攀繩) | Golden Cloud Sky-Cliffs |
| 09 | Gisele Khoo Kai Yin (邱恺音) | Low black bun, round dark-rimmed glasses, dimpled smile; berry-magenta sleeveless tunic over cream shirt, berry satchel, cream leggings, berry flats | Berrie (Berry) | Star-Berry Picnic Basket (星莓野餐籃) | Star-Berry Fairy Orchard |
| 10 | Tan Eg Siu (陈奕修) | Neat bowl-cut black hair, round dark-rimmed glasses; lime-green & golden-yellow lightning-trim tunic, brown belt with golden eggshell charm, olive trousers, brown boots | 蛋 Dan / Volt-Drake | Cracked-Shell Dynamo Core (蛋殼電能核) | Thunder-Cliff Lighthouse |
| 11 | Ooi Kai Xiang (黃楷翔) | Neat black hair with straight bangs, friendly smile; royal-blue rune-trimmed tunic, brown belt with glowing cyan-rune pouch, dark-slate trousers, brown boots | OKX | Cipher Rune Cube (密碼符文方塊) | Floating Rune Library |
| 12 | Chong Jing Cheng (张敬诚) | Short buzz-cut black hair, open smile; emerald-green long-sleeve tunic, brown leather sketch satchel, olive trousers, tall brown boots | 虛假元卡丘 Mimik-Spark | Stitch-Light Sketchbook (縫光素描本) | Twilight Atelier Courtyard |
| 13 | Lee Ming Hui (李明穗) | Low ponytail with small clip, rectangular dark glasses; sage-green & cream botanical tunic, leaf brooch, brown backpack with bedroll, forest-green leggings, brown shoes | Sylvan-Fox | Emerald Root Seed-Satchel (翡翠根種囊) | Whispering Emerald Orchard |
| 14 | Lee Qiu Rong (李秋容) | Shoulder-length layered black hair, round thin gold glasses; lavender shoulder cape with crescent clasp, mint tunic, belt with golden chime keys, dark-plum leggings, brown flats | Miku | Moon-Ribbon Chime Bow (月緞風鈴結) | Moonlit Willow Silver Lake |
| 15 | Cheah Hao Fung (谢昊峰) | Thick black hair with bangs, rectangular dark glasses; charcoal tunic with emerald-green trim, dark charcoal trousers, brown boots, blueprint pouch | Emerald-X Mecha | Eco-Rune Greatsword (生態符文巨劍) | Briar-Root Forest Canyon |
| 16 | Chan Shi Ye (陈施晔) | Chin-length black bob with full straight bangs; pastel-lavender tunic, dusty-purple trousers, rainbow-striped woven yarn pouch, brown shoes | Star-Yarn Caticorn | Rainbow Nebula Yarn Ball (彩虹星雲毛線球) | Twilight Sky Chasm |
| 17 | Uvincc Long Chieh Eik (龙学议) | Short buzz-cut black hair, calm steady face; sky-blue capelet, golden-orange tunic with sky-blue trim, brown belt with golden 8-point star-compass buckle & twin pouches, khaki trousers, dark-brown boots | 曜風天犬 Solar-Breeze Sky-Pup | Solar-Wind Star Compass (曜風星羅盤) | Golden Cumulus Sky-Ridge |

## 5. Locked Production & Graft Invariants (Non-Negotiable)
Unified Painted Scenes Over Cutout Compositing: Never isolate pets or trainers by flood-filling white (#F6F4EE) backgrounds when placing them onto dark or colored poster backgrounds. Generate a single unified painted composition directly on #F3EFE6 warm parchment (Series A) or inside a full-bleed painted habitat (Series B).
Facing & Bond Direction Lock: Trainers and partner pets must always face toward each other, look at a shared focal target, or stand side-by-side in a clear bonded pose.
100% Text-Free Raw Art + v4.4 Top-Band Compositor: All generated images must be strictly text-free. Auto-crop white borders, composite bilingual dialogue in comic_page_compositor_v4.py (Dedicated Top Dialogue Band, 0% face overlap, speaker-side dipping tails, dynamic 1–4 line code tray), and run comic_qa_preflight_linter.py before exporting.
WeasyPrint Vertical CJK Workaround: Render vertical Chinese sidebars or spine stamps using explicit <br/> character stacks.
Drive Upload Size & MIME Ceiling: Optimize compiled PDFs to under 6.35 MB and upload standalone HTML files with mime_type: "application/octet-stream".
Base64 & Visual QA Gate: Verify embedded base64 images start with valid magic bytes (/9j/ or iVBOR) and visually inspect rendered outputs before delivery.
Archive-Never-Delete Custody: Move superseded Drive files into 99_Archive_Superseded (10KmNhDKHj0p8YpL4bfEvSGosKBezZ3T9) and update HANDOVER_CURRENT.md.
Stage-Matched Pet Turnaround Anchor Lock & Pre-Crisis Baby Rule: Never generate a pet from text nicknames alone (e.g., "Golden-Pup", "Spark-Fawn"). Always pass the exact stage-matched 4-view turnaround from 03_Pet_Turnaround_Sheets_All_18 (S1_Baby, S2_Site, or S3_Grand) as an image_reference alongside the student's turnaround. Pets must remain strictly in Stage 1 Baby (S1_Baby) before the squad solves the crisis — never draw wings, star-collars, or Stage 2 features prematurely. (Guardrail: #17 Uvincc's Solar-Breeze Sky-Pup is golden-yellow & sky-blue with floppy cloud ears + sky-blue bandana in S1, and winged ears/wings + gold 8-point star-compass collar + sky-blue ankle socks + curly cloud tail in S2 — NEVER a unicorn horn, NEVER a green bandana, NEVER a generic Golden Retriever.)
Slow 3–4 Panel Magical Evolution Sequence (Digimon-Style): Whenever a pet evolves after solving a crisis, never snap-cut from Stage 1 to Stage 2 in a single panel. Dedicate a slow, magical 3–4 panel evolution sequence: (1) Relic & Digivice Virtue Resonance glow → (2) Luminous elemental cocoon / swirling ribbons lifting the Stage 1 Baby → (3) Slow-motion close-up of wings, antlers, or markings unfurling in starlight → (4) Full-frame canonical Stage 2 reveal bonded with the student.
