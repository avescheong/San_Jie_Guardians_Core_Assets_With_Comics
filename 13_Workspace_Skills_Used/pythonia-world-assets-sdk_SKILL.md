## name: pythonia-world-assets-sdk description: Single Source of Truth (SSOT) router and zero-drift visual lock for the entire Hero Kai and Scrolls of Pythonia world asset vault (001_Kai_Assets / Hero_Kai_Core_Assets, 1vLC13sHopidqHhvoQZFQxuNWXLDC8gjg). Covers O(1) Drive ID lookup for all 17 Volume 1 cast/companions/spirits (Normal 4.0H and Chibi 2.0H-2.2H turnarounds), all 8 Volume 2/3 NPCs, Hero Kai 20-sheet Studio Bibles, sprites/VFX/illustrations, world lore, and programmatic v5.4.0 genomes. Auto-activates whenever auditing comic panels, generating or verifying any Pythonia NPC, spirit, companion, villain, prop, or scene, or pulling canonical character turnarounds and world assets from Drive. allowed-tools: drive context_service_agent image_gen default_api
# Pythonia World Assets SDK
Enforce zero-drift generation, reuse, and visual auditing across the full Hero Kai and Scrolls of Pythonia universe using the read-only upstream SSOT vault 001_Kai_Assets / Hero_Kai_Core_Assets (1vLC13sHopidqHhvoQZFQxuNWXLDC8gjg).
## When to Use
Auditing comic panels, storybooks, covers, or webtoons in Hero_Kai_Comic (04_panel_art_approved or 03_panel_art_raw) against canonical cast and world references.
Retrieving exact Normal 4.0H or Chibi 2.0H-2.2H turnaround sheets for any of the 17 Volume 1 characters/spirits or 8 Volume 2/3 NPCs.
Reusing sealed sprites, combat/magic VFX, approved illustrations, video keyframes, or world lore from 001_Kai_Assets before generating new assets.
Enforcing Pythonia world canon guardrails (Zero Ember, plant-based food, Blacksmith disambiguation, Bug King hexapod lock, NPC glasses/headgear locks).
## Steps
### 1. Follow Read-Only Upstream SSOT & Zero-Reupload Retrieval
Never mutate or delete files inside 001_Kai_Assets (1vLC13sHopidqHhvoQZFQxuNWXLDC8gjg), and never ask the user to re-upload canonical turnarounds already stored in Drive.

For image_gen:generate_image inputs: Call context_service_agent:get_context with the exact canonical filename or Drive URL to obtain a verbatim file_reference token. (drive:download_file_content saves to VM for visual inspection but does not produce a file_reference.)
For visual audits (view_file): Download the target panels and the individual canonical turnaround sheets via drive:download_file_content and inspect them side-by-side at full resolution.
Anti-Collage Rule: Full-cast Master QA Boards (12_FULL_CAST_AND_SPIRITS_MASTER_QA_BOARD.jpg 1M0BoEeIlQbqnv0-5by9kAhmbhsBS3azo, 06_CHIBI_SUPPORTING_CAST_MASTER_QA_BOARD.jpg 1xG7ZRGby7l8LabJV0cv_D3XY4D9hp49-, 13_VOL2_VOL3_8_NPC_FULL_CAST_MASTER_QA_BOARD_4K_CAPTAIN_SIMON.jpg 1CRAETk-LZVb1V1JebTC7tFRWW9O3uJ9D) are for rapid human/auditor overview only. NEVER pass collage boards into image_gen; always pass individual full-res 4-view turnarounds.
Strict Track Isolation: Never mix Normal 4.0H comic/storybook turnarounds with Chibi 2.0H-2.2H game-sprite turnarounds.
### 2. O(1) Pythonia Vault Routing Map
Jump directly to the exact folder or file ID without broad Drive searches:


| Domain / Asset Category | Path inside 001_Kai_Assets | Drive ID |
| :--- | :--- | :--- |
| Master Vault Root | 001_Kai_Assets/ (Hero_Kai_Core_Assets) | 1vLC13sHopidqHhvoQZFQxuNWXLDC8gjg |
| Master Routing & Inventory | agent.md | 10kzyqjcRJ4gXhM9CkGXAW-piq3dXaKw73mXDUgU88hs |
| Workflow & Style Bible | 00_MUST_READ_KAI_WORKFLOW_STYLE_AND_PREFERENCES.md | 1at0MoNCxoAL12rbzTcp6NkSilPLOnx1FrfWL_uCn_E8 |
| Hero Kai Canonical Anchors & Logos | 01_Character_Sheets/00_Canonical_Master_Anchors_and_Logos/ | 1-gwCTME0eFHBQhaNjPFfEnBOs8DLhriG |
| Hero Kai Normal 4.0H Bible (03-10) | 01_Character_Sheets/01_Normal_4H_Studio_Bible/ | 16vnUvAwcx2ZielaPDbShWjtRNgFhvkKH |
| Hero Kai Chibi 2H Bible (13-19) | 01_Character_Sheets/02_Chibi_2H_Studio_Bible/ | 1NyGSsoHzxJc0R67zkfZWcykkXqKhOsYd |
| Supporting Cast & Spirits (4.0H) | 01_Character_Sheets/03_Supporting_Cast_Normal_4H/ | 1Cv8PQ-QoEnqEfMLVnzYMH0SEFc4T_dGE |
| Supporting Cast & Spirits (Chibi) | 01_Character_Sheets/04_Supporting_Cast_Chibi_2H/ | 1BBsBH7paqUuNUDEOpr0_slg6krUYX5oS |
| Legacy Source Assets (Read-Only) | 01_Character_Sheets/05_Legacy_Source_Assets_ReadOnly/ | 1acNei6P4hvjfYO9ohNquzw-m1yiI9veL |
| Sprites, VFX & Scenes Root | 02_Sprites_VFX_and_Scenes/ | 17dPnYf4kaxSxbHCia2tY8BorNH8UUB5e |
| Sealed Chibi Assets | 02_Sprites_VFX_and_Scenes/01_Sealed_Chibi_Assets/ | 1_xqMlKMXQoYXDWhXnlGLCumi3Hg-dY6W |
| Combat & Magic VFX | 02_Sprites_VFX_and_Scenes/02_New_Combat_and_Magic_VFX/ | 145vCwKe8-yBUxYQv8yImqctIY1f7LJUx |
| RPG Sprites | 02_Sprites_VFX_and_Scenes/Kai_RPG/ | 1bybWVZl24tdiorg5HX95JkTvOkSipnA_ |
| Generated Sprite & Scene Packs | 02_Sprites_VFX_and_Scenes/05_generated_packs/ | 1nG2O5g9LijALOEC7duNGyxiKbo8jJ7rU |
| Approved Story Illustrations | 02_Sprites_VFX_and_Scenes/Approved_Illustrations/ | 1xKOijpaS9a-IQnGAR_S9V5UdvVFE-Y9L |
| Upscaled Master Prints | 02_Sprites_VFX_and_Scenes/Upscaled_Master_Prints/ | 11rSApN03sosF_4b0CXG_mS54lSCEQ7TN |
| Video Keyframes | 02_Sprites_VFX_and_Scenes/Kai_Videos_Images/ | 1ly9tZYY9DYesFdw0St_0-bMwn_wd3KSa |
| Full Story, Bibles & Lore | 03_Full_Story_and_Lore/ | 16QIVjZnAw3HJJjzfjD7vYNyx5mm9hw8M |
| Bibles & World Docs | 03_Full_Story_and_Lore/01_Bibles_and_Docs/ | 1oBVtToj7_oCvcWojxzHtizhJuJsohcYJ |
| Image Engine & SDK Root | 04_Image_Engine_and_SDK/ | 1Wn0Pj1XVhhlaHD4z2eOb5rWlmPrTS_Ip |
| Primary SDK (00_KAI_ENGINE_SDK) | 04_Image_Engine_and_SDK/00_KAI_ENGINE_SDK/ | 1l6OYPCS0hk1iDTFpgzyoI1atZA0X8tS3 |
| Hero Kai Genome v5.0 JSON | 00_KAI_ENGINE_SDK/kai_canonical_genome_v5.json | 1K17hFaAzVh0ANYefHE_UsIibVcwWMo-t |
| Supporting Cast Genome v5.4.0 JSON | 00_KAI_ENGINE_SDK/supporting_cast_genome_v5.json | 1gvcehwB5lz2X4Wq-Q-ngE2SPT4QP65vA |
| Prompt & Rig Compiler | 00_KAI_ENGINE_SDK/kai_prompt_and_rig_compiler.py | 1d9BfjMH9CH-Yidls-3S-lCICxvPj_5W4 |
| ACVE Verifier v3 | 00_KAI_ENGINE_SDK/acve_kai_verifier_v3.py | 1kVJjXZmpJqPiFX-2tQd5bl-2-_aXOrrC |
| Paper-Doll Compositor | 00_KAI_ENGINE_SDK/kai_paperdoll_compositor.py | 1uNvuRagx8QmVZedODW5CHFp_VK2_84Rz |
| Volume 2/3 8-NPC Vault | Hero_Kai_Comic/04_panel_art_approved/00_8_NPC_MASTER_REFERENCE_VAULT/ | 15hOit7DyYHeJq-3vVewYNsM4MVlyMgZg |
| Archive (Read-Only) | 99_Archive_Docs_and_Old_Builds/ | 1BOL1XYe-PXEDdZ-G_bKK-m_F1LsrCUFS |

### 3. Complete 17-Character Volume 1 Turnaround Inventory (Normal 4.0H & Chibi 2H)
Use these exact Drive IDs to anchor generation or audit visual drift:


| # | Character & Role | Normal 4.0H Sheet ID | Chibi 2.0H-2.2H Sheet ID | Non-Negotiable Visual Locks |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Hero Kai (Protagonist) | 1P31jHSAVtBrmEzf0apbGMGNODu6yIUbR (Front: 1brhZPn-068ZBNooSde-w1Ln1CaHiazqw, Buckle: 1KhF9mkqPS8ZS1gUA61M_V-nZWcZ3fZpN) | 1QguHmW_wyBzmrqmbImzmmt1FWN6XRlws (Face: 1_uOl64q6SCPfnuhqkvVOz2HiemRhEG4Z) | 11yo boy, cobalt-blue eyes (#256BC4/#1D63B8), Tzu Chi winged-lotus Dharma ship buckle, viewer-left satchel / viewer-right 3 potions (1 ruby vial in Chibi), sword-free default |
| 2 | The Great Wizard (Mentor) | 1UhfO8Gr3ABll9qJnh07QBf1oA9RdEZuN | 16I3QYE46kuDBjKnDUJTAT5h2dhmz9vLS (Top) | 180 cm, tall pointed indigo hat, silver-white beard, starry indigo robe, gnarled staff |
| 3 | Grandma Looma (Weaver Elder) | 1PIU2v9EO5MRF7U0MMbccVAvWgyiBZ3OL | 16I3QYE46kuDBjKnDUJTAT5h2dhmz9vLS (Bottom) | 156 cm, strictly NO glasses, silver-grey low nape bun, olive vest, cream apron with wooden shuttle |
| 4 | The Bug King (Antagonist) | 1sHVzAmLObgHDLxyy1JuCTKvpeXolURmJ | 1W74_6XC1xBkBMzcwh3vA9w81t2vJEXGY (Top) | 230 cm, strict 6-limb hexapod (2 scythe-arms, 2 lower arms, 2 legs), bare obsidian carapace (NO mantle/cape), dark glossy obsidian eyes (NEVER red) |
| 5 | String (Pup Companion) | 1KKTZgQqjnQZWHmpKfkcopOkt6kKSWh8g (Top) | 1W74_6XC1xBkBMzcwh3vA9w81t2vJEXGY (Bottom Left) | Scruffy golden-tan terrier (#D89B4C), emerald neckerchief (teal str crystal collar upgrade in Ch. 8). Zero Ember rule |
| 6 | Baby Praying Mantis | 1KKTZgQqjnQZWHmpKfkcopOkt6kKSWh8g (Bottom) | 1W74_6XC1xBkBMzcwh3vA9w81t2vJEXGY (Bottom Right) | Emerald-green (#2ECC71) 6-limb hatchling with translucent wings (True Spell Guardian) |
| 7 | Ch. 3 Iron Outpost Blacksmith | 1TZ9vjd0G02Wk3vAzgLYovp7MM2GOpZqC | 1GUaIHGI7DzVmuLvjV-belLBq3B-cXrBK (Top) | 150 cm, 2-horned riveted steel helmet, triple-braided silver beard, bare muscular arms |
| 8 | Ch. 9 Master Grimsby | 1f0zLIDh2UiPg-pwsD3aXU_tgxeyBjcV- | 1GUaIHGI7DzVmuLvjV-belLBq3B-cXrBK (Bottom) | 145 cm, strictly hatless, brass forehead goggles, fiery ginger twin-forked beard with brass rings |
| 9 | The Forest Spirit (Ch. 4) | 1vAXcJLaWf2k4ty3ZzvjiB6V_YCdrz4Vq | 1VUSFCh-4dlyhs2fGYEVMoJryAmKp1MEo | Spectral aqua elfin maiden, floating barefoot, leafy laurel crown, mossy lantern staff |
| 10 | The Ghost Librarian (Ch. 7) | 1RKzYBJSn9RPnSj3T9jiNjtxMBUzosZsR | 14En-JB-RNT43LXrpm2tiVq-zcFrNMbMD | Spectral elder woman, strictly NO headscarf, low bun, round spectacles, wispy hem, 1 glowing quill |
| 11 | The Sleeping Red Dragon (Ch. 7) | 1Nx_bron4h3lpewvDI8-P-TH8sGno-Do5 | 1hKi_POHE36z0eRcw35flSU55VkfkVfHP | Ruby-red scales, cream-tan segmented belly, curved golden horns, folded ruby wings |
| 12 | Stone Block Golem (int, Ch. 8) | 1Nk2yVwVQHDEFb04RIh-yXbGLM-dqm-aV (Left) | 1dD9ZN_7DQIJujHF40k6QyQiVXQ92Y2Mx (Top Left) | Blocky mossy stone golem with glowing amber eyes |
| 13 | Water Droplet Spirit (float, Ch. 8) | 1Nk2yVwVQHDEFb04RIh-yXbGLM-dqm-aV (Center) | 1dD9ZN_7DQIJujHF40k6QyQiVXQ92Y2Mx (Top Center) | Sky-blue bouncing water droplet spirit surrounded by small bubbles |
| 14 | Flashing Truth Gem (bool, Ch. 8) | 1Nk2yVwVQHDEFb04RIh-yXbGLM-dqm-aV (Right) | 1dD9ZN_7DQIJujHF40k6QyQiVXQ92Y2Mx (Top Right) | Octagonal emerald-and-gold truth gem with sparkles |
| 15 | Barnaby the Baker (Ch. 1) | 1pw1NlmTORC1sIaBS1qMZ8eOULaNpfiNS (Left) | 1dD9ZN_7DQIJujHF40k6QyQiVXQ92Y2Mx (Bottom Left) | Stout mustachioed baker holding strictly plant-based bread basket |
| 16 | Silent Village Little Girl (Ch. 1) | 1pw1NlmTORC1sIaBS1qMZ8eOULaNpfiNS (Center) | 1dD9ZN_7DQIJujHF40k6QyQiVXQ92Y2Mx (Bottom Center) | Brown-haired pigtailed village girl in sky-blue pinafore |
| 17 | Hooded Signpost-Keeper (Ch. 11) | 1pw1NlmTORC1sIaBS1qMZ8eOULaNpfiNS (Right) | 1dD9ZN_7DQIJujHF40k6QyQiVXQ92Y2Mx (Bottom Right) | Slate-indigo hooded cloak, glowing eyes in shadow, gnarled amber lantern staff |

### 4. Volume 2 & 3 Locked 8-NPC Turnaround Inventory (00_8_NPC_MASTER_REFERENCE_VAULT)
Always pull individual 4-view sheets from 15hOit7DyYHeJq-3vVewYNsM4MVlyMgZg (never the 4K overview board):

NPC-01 Sir Cedric: NPC01_SIR_CEDRIC_4VIEW.jpg (1p57HFKw7VMfi7hP9vQGUW7XOVi62FZme) - silver armor, strictly NO helmet plume.
NPC-02 Mira the Baker: NPC02_MIRA_THE_BAKER_4VIEW.jpg (1n126bdigKGGjnvWIm9dExp67l8UyeJjO).
NPC-03 Old Tomas: NPC03_OLD_TOMAS_4VIEW.jpg (18In9Wfj1FgCgVJFODQSTV8HprgJpKzz4).
NPC-04 Pip the Messenger: NPC04_PIP_THE_MESSENGER_4VIEW.jpg (1f4oSwxxyZsLMIZECb8N1ozResk6GtmY7).
NPC-05 Herbalist Meilin: NPC05_HERBALIST_MEILIN_4VIEW.jpg (1mDCRDAdiNCiAuhAGCqYh-Xh49cqGzVlt).
NPC-06 Captain Simon: NPC06_CAPTAIN_SIMON_4VIEW.jpg (1Z6kG7C0STECrK_MMloSbwiHNVn6UsY-L) - permanently renamed from Barnaby; never revert.
NPC-07 Scholar Elena: NPC07_SCHOLAR_ELENA_4VIEW.jpg (1a37Zp5WPOQvI7Ll-PXx_XDdWId6z9jOC).
NPC-08 Mayor Aldous: NPC08_MAYOR_ALDOUS_4VIEW.jpg (1K1h-4_VUApeN4gfrfDevDpC1RqOGdDXb).
### 5. Pythonia World Canon Guardrails (Mandatory Audit & Generation Checks)
Verify every scene, panel, and sprite against these six world locks:

Zero Ember Rule: Companions are strictly String (golden-tan terrier) and the Baby Praying Mantis. Reject any fox or dog named Ember.
100% Plant-Based Economy: All campfire meals, bakery baskets, tea-stall dishes, and snacks must be strictly vegetarian/plant-based.
Blacksmith Disambiguation: Never swap Ch. 3 Iron Outpost Blacksmith (2-horned steel helmet, braided silver beard) with Ch. 9 Master Grimsby (hatless, forehead brass goggles, ginger twin-forked beard).
Bug King Hexapod & Eye Lock: Reject any Bug King render with 4 limbs, 8 limbs, a cape/mantle, or red glowing eyes.
100% Text-Free Raw Comic Art: Raw comic panels must contain zero speech bubbles, captions, SFX, or stray letters/digits on signs, scrolls, or walls.
Non-Destructive Archival: Move superseded assets to the project 99_ARCHIVE_SUPERSEDED folder instead of deleting them.
## Gotchas
Never pass legacy files (001. Turnaround.png with brown eyes, text-heavy 003. Equipment Callout.png, or anything in 05_Legacy_Source_Assets_ReadOnly) into image_gen.
Never confuse Barnaby the Baker (Vol 1 Ch. 1 villager, #15) with NPC-06 Captain Simon (Vol 2/3, permanently renamed from Barnaby).
In multi-character scenes, keep each generated frame to 4-5 locked individual turnarounds with explicit left-to-right placement so outfits, glasses, and headgear do not bleed across characters.
When auditing Hero_Kai_Comic panels, pair this skill with visual-drift-auditor so every panel is inspected at full resolution against the exact character sheet IDs above.
