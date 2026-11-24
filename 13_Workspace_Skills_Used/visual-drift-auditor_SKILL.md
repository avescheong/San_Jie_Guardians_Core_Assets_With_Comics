## name: visual-drift-auditor description: Zero-tolerance visual drift auditor and ensemble-panel remediation workflow for multi-chapter comics, graphic novels, webtoons, storybooks, and illustrated series. Use whenever the user asks to audit panels, check for character or pet drifting, verify visual consistency across chapters, inspect raw comic art against canonical turnaround sheets, fix drifted panels, or split crowded group scenes into zero-drift squad panels. allowed-tools: drive context_service_agent image_gen default_api
# Visual Drift Auditor
A reusable, zero-tolerance visual QA and remediation workflow for illustrated series, graphic novels, and comics. It catches subtle character, pet, prop, continuity, and crowd drift by visually inspecting every panel at full resolution against canonical turnaround sheets, then fixes flagged panels without losing earlier versions.
## When to Use
The user asks to audit, double-check, or QA-review generated comic, manga, webtoon, or storybook panels for visual drift.
A multi-chapter production run finishes and needs a pre-compositing or pre-publishing visual consistency gate.
Crowd or group scenes show off-model faces, missing glasses, duplicate characters, or generic background substitutions.
Characters, companions, masks, or props drift across sequential story beats and need targeted regeneration with Archive-Never-Delete custody.
## Steps
### 1. Parallel Chapter Fan-Out (Read-Only Audit First)
Keep the audit strictly read-only until the user reviews the findings or explicitly authorizes replacements.

For multi-chapter audits (24+ panels), spawn one parallel subagent per chapter so each auditor inspects every panel at full resolution without context overload.
Pass every panel's exact Drive file ID and URL, the canonical Core Cast turnaround IDs, the student/character and companion turnaround folder IDs, and the locked visual DNA table (especially glasses presence/absence, hair color/style, outfit palette, and stage-locked creature traits).
Download both the target panels and the relevant canonical turnaround sheets, then inspect EVERY panel with view_file. Never skip panels or judge from filenames or text summaries.
### 2. Six-Point Zero-Tolerance Inspection Matrix
Evaluate every single panel against six explicit checks:

Main Cast Lock: Verify proportions, signature outfit details, belt/pouch/prop placement, weapon-free rules, and exact companion anatomy (such as single-head locks or limb counts).
Supporting Cast & Glasses Lock: Check hair color/style, exact presence or absence of glasses (and frame shape), outfit colors, and absence of duplicate characters or excluded roster members.
Companion / Creature Stage Lock: Match species, fur/scale/feather colors, wings/horns/tails/halos/collars against the exact stage turnaround (S1, S2, S3). Catch premature evolutions, stage regressions, or partner swaps.
Sequential Continuity Lock: Check props, masks, visors, injuries, and backgrounds across adjacent panels so designs do not mutate mid-scene.
Crowd Integrity Check: Flag any group shot where the generator invented generic off-model hair colors, uniforms, missing glasses, extra limbs, or character clones.
Technical & Canon Guardrails: Verify 100% text-free raw art (zero stray letters, digits, gibberish runes, or speech bubbles on signs, stone, lanterns, or chalkboards), full-bleed aspect ratio (zero white/cream borders or accidental multi-panel splits), clean anatomy, and world-canon rules (such as plant-based food or non-lethal magic).
### 3. Structured Drift Report
Classify every panel into one of three verdicts:

PASS: Visually on-model and publication-ready.
MINOR_NOTE: Publication-safe with trivial omissions (such as an obscured hip prop or faint distant detail); list briefly as optional polish.
DRIFT_FLAGGED: Requires regeneration. Group by chapter with Severity (Critical, High, Moderate), clickable Drive link, and the exact visual defect observed.
### 4. Remediation & Ensemble-Split Protocol
When the user approves fixes (or requests full cast representation in climactic scenes):

Zero-Reupload Reference Anchoring: Retrieve verbatim file_reference tokens from canonical individual turnaround sheets via context_service_agent:get_context and pass them into image_gen:generate_image. Never pass multi-character collage boards.
Ensemble-Split Anti-Crowd-Drift Rule: Image generators reliably hold 4 to 5 locked individual turnarounds per frame, not 15+ tiny faces. Whenever a climax, banquet, or farewell requires an entire large cast (10 to 20 characters), split the beat into sequential 4 to 5 person squad panels (PXX_03, PXX_04, PXX_05, PXX_06) so every single character gets a clear, zero-drift spotlight with zero repetition and zero generic crowd drift.
Mandatory Post-Generation Visual Gate: Inspect every regenerated image with view_file before uploading. Re-roll immediately if any residual drift, stray text, border, or duplicate appears.
### 5. Archive-Never-Delete Custody
Move every superseded Drive file into the project's 99_Archive_Superseded folder using drive:update_file (add archive parent, remove live parent). Never permanently delete superseded files.
Upload the QA-passed replacement JPEG to the live raw-panels folder with the exact canonical filename, then return a concise summary table with clickable Drive links for every replacement.
## Gotchas
Never trust an earlier self-check from generation turns: Generation turns suffer from confirmation bias; always run a dedicated, fresh visual audit pass with canonical turnarounds loaded side-by-side.
Watch for subtle text hallucinations: Stone parapets, weapon blades, scrolls, sky-lanterns, and chalkboards frequently accumulate garbled Latin letters or digits; zoom in mentally on every flat surface.
Lock mask and prop shapes across multi-panel beats: If a character wears a visor or carries a relic across 3 to 4 sequential panels, describe the exact same silhouette verbatim in every prompt so the prop does not morph between panels.
Prevent outfit mashups in multi-character prompts: When passing 4 to 5 character turnarounds together, explicitly map left-to-right screen positions (far left, center-left, center-right, far right) so outfits and glasses do not bleed across adjacent characters.
