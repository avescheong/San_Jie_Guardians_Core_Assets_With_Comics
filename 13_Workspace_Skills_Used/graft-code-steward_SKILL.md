## name: graft-code-steward description: Pre-build engineering steward, codebase mapper, blast-radius checker, and persistent learnings vault modeled on Trail-Code (formerly Graft). Auto-activates before building or starting any new coding project, web app, HTML5 game, pipeline, script, or automation, whenever editing or refactoring multi-file codebases (Hero Kai, Pythonia, HTML5 games, TGL engineering scripts, Apps Script dashboards), when referencing 000_Graft_Memory (1eWZwE_e93NbHrzjaWlSF6zJWTnCq_GMr), or when the user mentions graft, trail-code, blast radius, callers, code map, lessons learnt, save this as a learning, or always follow. allowed-tools: drive view_file write_to_file execute_bash
# Graft Code Steward
Enforce pre-build orientation, Trail-Code (formerly Graft) codebase mapping, blast-radius checks, and persistent learnings across coding sessions, anchored to the 000_Graft_Memory Google Drive workspace (1eWZwE_e93NbHrzjaWlSF6zJWTnCq_GMr).
## When to Use
Before building anything new in code — starting a new web app, game, studio, script, asset pipeline, or automation so proven always_follow: true principles are applied from line 1.
Working on or refactoring multi-file codebases (e.g., Hero Kai / Pythonia, HTML5 games, TGL engineering scripts, Apps Script dashboards).
Explicit triggers — referencing 000_Graft_Memory, asking to "save this as a learning", setting an "always follow" rule, or requesting a blast-radius, caller, or lessons-learnt check.
## Workflow
### 1. Orient First (Pre-Build & Code Map Gate)
Before scaffolding a new coding project or editing multiple files, check 000_Graft_Memory (1eWZwE_e93NbHrzjaWlSF6zJWTnCq_GMr) for:

Active always_follow: true learnings in learnings/ that apply to the stack, target platform (Canvas, Drive, GitHub, Netlify, Python, FFmpeg, Godot), or project family.
Existing code_maps/ entries matching the target project or filenames.

When inspecting code in the sandbox VM, inspect function signatures and import/caller edges first rather than reading entire files blindly. If a local git repo already has graft/ or .trail/learnings/ (via trail init), read those files directly.
### 2. Blast-Radius Check Before Editing
Before changing any shared function signature, constant, schema, or CSS/DOM contract:

Identify every file or module that imports, calls, or depends on that symbol.
Check if any always_follow: true learning in 000_Graft_Memory/learnings/ governs that file or constant (preferring newer notes if an older note was superseded).
Surface any potential conflict or sibling file that also needs an update before making the edit.
### 3. Capture Learnings
Save a learning note only when a non-obvious decision is made, an approach is tried and ruled out, a subtle bug/gotcha is solved, or the user explicitly says "save this as a learning" or "always follow".

Write a concise Markdown file to 000_Graft_Memory/learnings/ (and .trail/learnings/ if working inside a local git repo) using this structure:

Metadata header with title, project, date, status (active or superseded), always_follow (true or false), and touches: (list of affected files). Wrap Drive IDs in backticks so Google Docs Markdown conversion does not italicize underscores.
## Decided - What was chosen and why.
## Tried and ruled out - What failed or was rejected, so future sessions do not repeat it.
## Watch out - Crucial invariants, constants, or caller dependencies (extract the crux logic, not brittle line numbers).
### 4. Pre-Handoff Verification
Before finishing a build or multi-file change, verify that the output does not violate any active always_follow: true learning and that all downstream callers remain compatible.
## Gotchas
Never store raw transcripts or secrets in learnings/; keep each note short and actionable.
Never rely on raw line numbers in notes, as line numbers drift when files are edited; quote the exact symbol name or crux condition instead.
Do not apply this skill to pure prose deliverables (like EIA/EMP Word or PDF reports or stock memos) that have no code dependencies.
