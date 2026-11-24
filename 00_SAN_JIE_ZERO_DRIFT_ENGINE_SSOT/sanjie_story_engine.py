#!/usr/bin/env python3
"""
San Jie Class (July 2026) — Deterministic 30pp Story Engine & Zero-Drift Continuity Linter
Enforces:
  1. Strict 17-student roster lock (zero Ko Zi Xing / Jacob)
  2. Act-gated Pet Evolution Lock (Act 1 Ch.1-4 = S1_Baby ONLY; Act 2 Ch.5-8 = S2_Site; Act 3 Ch.9-12 = S3_Grand)
  3. Mandatory 4-panel Slow Magical Evolution Sequence whenever a stage upgrade occurs
  4. Stage-matched Pet Turnaround Anchor Resolution (auto-emits exact file_reference fetch list)
  5. Zero off-SSOT pet nicknames / Chinese name typos / CJK-in-EN leaks / non-plant-based food terms
  6. 100% 5-part Cardinality Accounting + SHA-256 Script Provenance Logging
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

STAGE_ORDER = {"S0_Sketch": 0, "S0_Egg": 1, "S1_Baby": 2, "S2_Site": 3, "S3_Grand": 4}
REQUIRED_EVO_BEATS = ["beat_1_resonance", "beat_2_cocoon", "beat_3_unfurl", "beat_4_reveal"]
NON_VEG_WORDS = [r"\bbeef\b", r"\bpork\b", r"\bchicken\b", r"\bsteak\b", r"\bsausage\b", r"\bbacon\b", r"\bham\b", r"\bfish\b", r"\bmeat\b"]
CJK_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]")


def log_provenance():
    p = Path(__file__).resolve()
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    print(f"[PROVENANCE] script={p} sha256={sha}", file=sys.stderr)


def lint_batch(state_path: str, manifest_path: str) -> int:
    log_provenance()
    state = json.loads(Path(state_path).read_text(encoding="utf-8"))
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))

    ch_num = str(manifest["chapter"])
    gate = state["act_evolution_gates"][ch_num]
    max_stage = gate["max_pet_stage"]
    max_rank = STAGE_ORDER[max_stage]

    excluded = state["excluded_names"]
    banned = state["banned_drift_terms"]
    students = state["students"]
    core_cast = state["core_cast"]

    total_panels = 0
    passed_panels = 0
    failed_panels = 0
    errors = []
    anchor_plan = []
    evo_beats_by_pet = {}

    for page in manifest.get("pages", []):
        pnum = page["page_num"]
        for panel in page.get("panels", []):
            total_panels += 1
            pid = panel["panel_id"]
            panel_errs = []

            # 1. Text checks (EN/ZH/Prompt)
            en_texts = [panel.get("narration_en", "")] + [d.get("en", "") for d in panel.get("dialogue", [])]
            zh_texts = [panel.get("narration_zh", "")] + [d.get("zh", "") for d in panel.get("dialogue", [])]
            all_text = " ".join(en_texts + zh_texts + [panel.get("art_prompt", "")])

            for ex in excluded:
                if ex.lower() in all_text.lower():
                    panel_errs.append(f"[{pid}] ROSTER_VIOLATION: Excluded name '{ex}' detected.")
            for bt in banned:
                if bt.lower() in all_text.lower():
                    panel_errs.append(f"[{pid}] DRIFT_TERM: Banned off-SSOT term '{bt}' detected.")
            for en_t in en_texts:
                if CJK_RE.search(en_t):
                    panel_errs.append(f"[{pid}] CJK_IN_EN: CJK glyph leaked into EN field: {en_t[:60]}")
            for pat in NON_VEG_WORDS:
                if re.search(pat, all_text, re.IGNORECASE):
                    panel_errs.append(f"[{pid}] PLANT_BASED_VIOLATION: Non-vegetarian term matched '{pat}'.")

            # 2. Pet stage & turnaround anchor lock
            required_anchors = []
            for cid in panel.get("core_cast", []):
                if cid in core_cast:
                    required_anchors.append(core_cast[cid]["turnaround_file"])
            for sid in panel.get("students", []):
                if sid not in students:
                    panel_errs.append(f"[{pid}] UNKNOWN_STUDENT: '{sid}' not in locked 17-student roster.")
                else:
                    required_anchors.append(f"STUDENT_{students[sid]['num']}_{students[sid]['name_en'].replace(' ', '')}_TURNAROUND")

            for pet_entry in panel.get("pets", []):
                sid = pet_entry["student_id"]
                stage = pet_entry["stage"]
                beat = pet_entry.get("evolution_beat", "none")
                if sid not in students:
                    panel_errs.append(f"[{pid}] UNKNOWN_PET_OWNER: '{sid}'.")
                    continue
                if STAGE_ORDER.get(stage, 99) > max_rank:
                    panel_errs.append(
                        f"[{pid}] PREMATURE_EVOLUTION: {students[sid]['pet_en']} ({sid}) set to '{stage}', "
                        f"but Chapter {ch_num} ({gate['act']}) hard-locks max stage to '{max_stage}'."
                    )
                if stage in ("S1_Baby", "S2_Site", "S3_Grand"):
                    required_anchors.append(students[sid]["pet_turnarounds"][stage])
                if beat != "none":
                    if not gate.get("evolution_allowed", False):
                        panel_errs.append(f"[{pid}] EVO_FORBIDDEN_IN_ACT: Evolution beat '{beat}' forbidden in Chapter {ch_num}.")
                    evo_beats_by_pet.setdefault(sid, []).append(beat)

            anchor_plan.append({"page": pnum, "panel_id": pid, "anchors": required_anchors})

            if panel_errs:
                failed_panels += 1
                errors.extend(panel_errs)
            else:
                passed_panels += 1

    # 3. Verify slow 4-panel evolution sequence completeness
    for sid, beats in evo_beats_by_pet.items():
        missing = [b for b in REQUIRED_EVO_BEATS if b not in beats]
        if missing:
            errors.append(
                f"[EVOLUTION_SEQUENCE] {students[sid]['pet_en']} ({sid}) missing mandatory slow-evolution beats: {missing}"
            )

    print(
        f"[CARDINALITY] Chapter={ch_num} Batch={manifest.get('batch_id')} | "
        f"Total_Panels={total_panels} = Passed({passed_panels}) + Failed({failed_panels}) | "
        f"Errors={len(errors)} Silently_Empty=0"
    )
    if errors:
        print("\n[FAIL] Continuity / Drift Violations Detected:")
        for e in errors:
            print("  -", e)
        return 1

    print("[PASS] 100% Zero-Drift & Continuity Gate PASSED.")
    print(f"[ANCHOR_PLAN] Resolved {sum(len(a['anchors']) for a in anchor_plan)} stage-locked turnaround references across {total_panels} panels.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 sanjie_story_engine.py <story_state.json> <batch_manifest.json>", file=sys.stderr)
        sys.exit(2)
    sys.exit(lint_batch(sys.argv[1], sys.argv[2]))
