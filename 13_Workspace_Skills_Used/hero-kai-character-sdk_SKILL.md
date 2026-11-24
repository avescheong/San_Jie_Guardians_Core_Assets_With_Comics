## name: hero-kai-character-sdk description: Enforces zero-drift Hero Kai and 8-NPC supporting cast consistency using 001_Kai_Assets, Genome v5.0 SSOT (00_KAI_ENGINE_SDK), direct Drive file_reference retrieval (zero user re-uploads), and strict Normal (4.0H) vs. Chibi (2.0H-2.2H) reference isolation. Auto-activates whenever generating, compositing, or verifying Hero Kai or Pythonia NPC sprites, Chibi sheets, paper-doll gear, magic VFX, comics, or storybook art for Scrolls of Pythonia, Pythonia Game Maker Studio, Kai_Capybara_GO, or Kai Love & Earth Studio. allowed-tools: drive context_service_agent image_gen execute_bash write_to_file view_file
# Hero Kai Character DNA & Sprite SDK (Genome v5.0 SSOT)
Enforce zero-drift Hero Kai & Pythonia cast generation and code-driven compositing using 001_Kai_Assets (1vLC13sHopidqHhvoQZFQxuNWXLDC8gjg), 00_KAI_ENGINE_SDK (1l6OYPCS0hk1iDTFpgzyoI1atZA0X8tS3), and 00_8_NPC_MASTER_REFERENCE_VAULT (15hOit7DyYHeJq-3vVewYNsM4MVlyMgZg).
## When to Use
Generating any new Hero Kai or Pythonia NPC sprite sheet, Chibi action sheet, comic panel, or 16:9 storybook illustration.
Equipping Kai with new weapons, eco-tools, outfits, or accessories across Normal (4.0H) or Chibi (2.0H–2.2H) tracks.
Adding new elemental, Pythonic, or Love & Earth VFX over Kai's casting poses.
Auditing or post-processing any Hero Kai PNG sprite sheet or comic panel.
## Steps
### 0. Zero-Reupload Drive Reference Retrieval (MANDATORY — NEVER Ask User to Re-Drop Images)
Never ask the user to upload Hero Kai or NPC reference images that already exist in Google Drive!

To obtain a valid image_references file_reference from Google Drive, ALWAYS call context_service_agent:get_context with the exact canonical filename (e.g., "00_KAI_NORMAL_4H_TURNAROUND_CLEAN.jpg") or Drive URL.
Pass the returned file_reference verbatim into image_gen:generate_image(image_references=[...]). (Note: drive:download_file_content saves to the VM but does NOT create a file_reference for image_gen.)
ANTI-COLLAGE RULE: NEVER pass multi-character grid/collage boards (like 12_FULL_CAST_AND_SPIRITS_MASTER_QA_BOARD.jpg or the 4K 8-NPC overview board) into image_gen — individual faces are too tiny in a collage and cause immediate face/hair/outfit drift. ALWAYS pull the individual full-res 4-view turnaround for each character appearing in the panel!
### 1. Read Mandatory Vault Standards & Check Sealed Assets First
Read agent.md (10kzyqjcRJ4gXhM9CkGXAW-piq3dXaKw73mXDUgU88hs) and 00_MUST_READ_KAI_WORKFLOW_STYLE_AND_PREFERENCES.md (1at0MoNCxoAL12rbzTcp6NkSilPLOnx1FrfWL_uCn_E8) first.
Check 01_Sealed_Chibi_Assets (1_xqMlKMXQoYXDWhXnlGLCumi3Hg-dY6W) and 05_generated_packs (1nG2O5g9LijALOEC7duNGyxiKbo8jJ7rU) before calling image_gen so sealed assets are reused instead of regenerated.
### 2. Use Code Compositing Before AI Generation
For equipment, eco-tools, or outfit swaps, download sealed mannequins (MOD_B01_04_KAI_CAPYBARA_CHIBI_SOCKET_MANNEQUIN_4x4.png 1jdsu7EuZyFfl1PD_UNRL9LNg5Zy4D6yQ for Chibi, or MOD_B01_01–03 for HD-2D/SRPG) and run kai_paperdoll_compositor.py instead of regenerating Kai's base body.
For new magic/eco-skill casting sheets, generate only the transparent VFX overlay (Z=7) on #FFFFFF and composite it over Kai's sealed casting poses.
### 3. Compile Deterministically with Genome v5.0 & Strict Track Isolation
Download kai_canonical_genome_v5.json (1K17hFaAzVh0ANYefHE_UsIibVcwWMo-t) and kai_prompt_and_rig_compiler.py (1d9BfjMH9CH-Yidls-3S-lCICxvPj_5W4) from 00_KAI_ENGINE_SDK (1l6OYPCS0hk1iDTFpgzyoI1atZA0X8tS3) and pass --weapon none|wooden_sword|iron_sword|eco_tool (default none). Match references strictly to the target track:

Normal-Size Track (4.0H Comic / Storybook / HD-2D — 05_Kai_Comic sepia ink + watercolor/pencil style, cream trousers #EDE8DE, 3 potions):
Hero Kai Anchors (pull via context_service_agent:get_context):
00_KAI_NORMAL_4H_TURNAROUND_CLEAN.jpg (1P31jHSAVtBrmEzf0apbGMGNODu6yIUbR) — PRIMARY 1-file anchor for comic panels
00_KAI_NORMAL_4H_FRONT_ANCHOR.jpg (1brhZPn-068ZBNooSde-w1Ln1CaHiazqw)
00_KAI_TZU_CHI_BELT_BUCKLE_ANCHOR.jpg (1KhF9mkqPS8ZS1gUA61M_V-nZWcZ3fZpN)
Volume 2 & 3 Locked 8-NPC Vault (00_8_NPC_MASTER_REFERENCE_VAULT, 15hOit7DyYHeJq-3vVewYNsM4MVlyMgZg — use individual 4-view sheets, NOT the 4K overview board):
NPC-01 Sir Cedric: NPC01_SIR_CEDRIC_4VIEW.jpg (1p57HFKw7VMfi7hP9vQGUW7XOVi62FZme) — silver armor, NO helmet plume
NPC-02 Mira the Baker: NPC02_MIRA_THE_BAKER_4VIEW.jpg (1n126bdigKGGjnvWIm9dExp67l8UyeJjO)
NPC-03 Old Tomas: NPC03_OLD_TOMAS_4VIEW.jpg (18In9Wfj1FgCgVJFODQSTV8HprgJpKzz4)
NPC-04 Pip the Messenger: NPC04_PIP_THE_MESSENGER_4VIEW.jpg (1f4oSwxxyZsLMIZECb8N1ozResk6GtmY7)
NPC-05 Herbalist Meilin: NPC05_HERBALIST_MEILIN_4VIEW.jpg (1mDCRDAdiNCiAuhAGCqYh-Xh49cqGzVlt)
NPC-06 Captain Simon (renamed from Barnaby): NPC06_CAPTAIN_SIMON_4VIEW.jpg (1Z6kG7C0STECrK_MMloSbwiHNVn6UsY-L)
NPC-07 Scholar Elena: NPC07_SCHOLAR_ELENA_4VIEW.jpg (1a37Zp5WPOQvI7Ll-PXx_XDdWId6z9jOC)
NPC-08 Mayor Aldous: NPC08_MAYOR_ALDOUS_4VIEW.jpg (1K1h-4_VUApeN4gfrfDevDpC1RqOGdDXb)
NEVER pass text-heavy 003. Equipment Callout.png, legacy brown-eyed 001. Turnaround.png, or multi-character collage sheets to image_references.
Chibi Track (2.0H–2.2H Capybara Go! / Love & Earth Studio — thick #2B1B12 outlines, taupe-brown trousers #6E5442, 1 ruby-pink vial):
Pull ONLY 00_KAI_CHIBI_CANONICAL_FACE_HAIR_BODY_ANCHOR.jpg (1_uOl64q6SCPfnuhqkvVOz2HiemRhEG4Z) and 00_KAI_CHIBI_4VIEW_CLEAN.jpg (1QguHmW_wyBzmrqmbImzmmt1FWN6XRlws), cross-checked against 01_Sealed_Chibi_Assets (1_xqMlKMXQoYXDWhXnlGLCumi3Hg-dY6W).
NEVER pass any 4.0H normal-size sheet into Chibi generation.
### 4. Run the 1–2 Panel Pilot Gate Before Scaling
Before generating a full 8–10 panel/sheet batch, generate 1–2 pilot outputs first and visually inspect them side-by-side against the track anchor. Only scale after confirming cobalt-blue eyes, spiky golden-blond hair silhouette, Tzu Chi winged-lotus Dharma ship belt buckle, outline weight, and proportions match with zero drift.
### 5. Post-Process & Verify Before Delivery
Sprites: Run acve_kai_verifier_v3.py --clean-captions --strip-islands --clamp-palette on every output PNG to strip enclosed white islands, preserve #F4EFE6 cream tunic pixels, verify bilateral hip asymmetry (viewer-left plain brown satchel / viewer-right potion holster), and reject brown/grey eyes or drifted hair hue.
Comics (05_Kai_Comic): Auto-crop outer white margins from every generated panel before compositing, use comic_page_compositor_v4.py (Dedicated Top Dialogue Band, 0% face overlap, 18–21pt fonts, speaker-side dipping tails), and run comic_qa_preflight_linter.py before exporting PDFs (<= 6.35 MB).
## Gotchas
Never ask the user to re-upload Hero Kai or NPC reference images — retrieve their Drive file_reference via context_service_agent:get_context.
Never pass multi-character collage boards into image_gen; always pass individual full-res 4-view sheets.
Never cross-contaminate 4.0H Normal anchors and 2.0H–2.2H Chibi anchors.
Always lock bright cobalt-blue irises (#256BC4 / #1D63B8), the Tzu Chi winged-lotus & white Dharma sailing ship emerald shield belt buckle, and sword-free default outfit (--weapon none).
NPC-06 is permanently locked as Captain Simon (never Barnaby).
