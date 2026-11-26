#!/usr/bin/env python3
"""
San Jie Class (July 2026) — 4-Realm Story & Continuity Alignment Engine (v6.0)
Deterministic linter & cross-chapter validator enforcing:
  1. Strict 17-student roster lock (#01-#17; zero excluded names).
  2. Canonical 4-Realm Squad & Habitat alignment (R1 Frost & Sky, R2 Forge & Tide,
     R3 Verdant, R4 Celestial) from sanjie_4realm_canon_ssot.json.
  3. Companion continuity lock (Hero Kai -> Ember; String -> caring for sick Grandma Looma).
  4. Stage-locked evolution & skill progression (no S2/S3 names or Ultimates in Act I).
  5. Zero-Weapon / 100% Plant-Based World Covenant & Python Spellbook Tray presence.

Usage:
  python3 sanjie_story_realm_aligner.py --chapter CH00A --script CH00A_Seventeen_Pencils_Penang_v6.0_EN.json
  python3 sanjie_story_realm_aligner.py --audit-dir ./scripts/
"""
import argparse
import json
import os
import sys
from pathlib import Path


def load_canon(canon_path: Path) -> dict:
    with open(canon_path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_script_text(script_data: dict) -> str:
    chunks = [
        script_data.get("kicker", ""),
        script_data.get("title", ""),
        script_data.get("subtitle", ""),
    ]
    for sec in script_data.get("sections", []):
        for b in sec.get("balloons", []):
            chunks.append(b.get("text", ""))
        for side in ("left", "right"):
            if side in sec:
                for b in sec[side].get("balloons", []):
                    chunks.append(b.get("text", ""))
        tray = sec.get("code_tray") or {}
        chunks.extend(tray.get("lines", []))
        chunks.append(tray.get("output", ""))
        if sec.get("skill_badge"):
            chunks.append(str(sec["skill_badge"]))
    return "\n".join(chunks)


def audit_chapter(canon: dict, chapter_code: str, script_path: Path) -> dict:
    with open(script_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    full_text = extract_script_text(data)
    lower_text = full_text.lower()
    errors = []
    warnings = []

    # 1. Excluded roster & forbidden world-rule terms
    for term in canon["canon_locks"]["world_rules"]["forbidden_terms"]:
        if term.lower() in lower_text:
            errors.append(f"FORBIDDEN_TERM: '{term}' found in {script_path.name}")

    # 2. Realm & squad alignment check (if chapter declares a primary_realm)
    declared_realm = data.get("primary_realm")
    if declared_realm and declared_realm in canon["realms"]:
        allowed_ids = set(canon["realms"][declared_realm]["members"])
        for g in canon["guardians"]:
            if g["student_en"].lower() in lower_text and g["id"] not in allowed_ids:
                warnings.append(
                    f"REALM_CROSSOVER: #{g['id']} {g['student_en']} (home={g['realm']}) "
                    f"appears in {chapter_code} ({declared_realm}). Verify cameo vs squad lock."
                )

    # 3. Stage-lock check (prevent premature S2/S3 in Act I chapters)
    stage_lock = canon["canon_locks"]["stage_lock_by_act"].get(chapter_code, "")
    if stage_lock in ("S0_Sketch", "S0_Egg_to_S1_Baby", "S1_Baby"):
        for g in canon["guardians"]:
            for forbidden_stage in (g["s2"], g["s3"], g["skills"].get("ultimate", "")):
                if forbidden_stage and forbidden_stage.lower() in lower_text:
                    errors.append(
                        f"PREMATURE_EVOLUTION: '{forbidden_stage}' ({g['student_en']}) "
                        f"referenced during {chapter_code} (locked to {stage_lock})."
                    )

    # 4. Companion continuity check (String must only appear in Grandma Looma cottage context)
    if "string" in lower_text and "looma" not in lower_text and "grandma" not in lower_text:
        warnings.append(
            "COMPANION_CONTINUITY: 'String' mentioned without Grandma Looma cottage context — "
            "confirm String is not accidentally replacing Ember in active adventure scenes."
        )

    # 5. Python Spellbook & Skill Callout coverage
    sections = data.get("sections", [])
    code_trays = sum(1 for s in sections if s.get("code_tray"))
    skill_badges = sum(1 for s in sections if s.get("skill_badge"))
    if code_trays == 0:
        warnings.append(f"MISSING_PYTHON_SPELL: {chapter_code} has 0 inline Python Spellbook trays.")

    return {
        "chapter": chapter_code,
        "file": script_path.name,
        "panels": len(sections),
        "code_trays": code_trays,
        "skill_badges": skill_badges,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
    }


def main():
    ap = argparse.ArgumentParser(description="San Jie 4-Realm Story & Continuity Alignment Engine v6.0")
    ap.add_argument("--canon", type=str, default=str(Path(__file__).parent / "sanjie_4realm_canon_ssot.json"))
    ap.add_argument("--chapter", type=str, help="Chapter code (e.g. CH00A, CH00B, CH01)")
    ap.add_argument("--script", type=str, help="Path to Webtoon JSON script")
    ap.add_argument("--audit-dir", type=str, help="Audit all CH*.json scripts in a directory")
    args = ap.parse_args()

    canon = load_canon(Path(args.canon))
    reports = []
    if args.script and args.chapter:
        reports.append(audit_chapter(canon, args.chapter, Path(args.script)))
    elif args.audit_dir:
        for p in sorted(Path(args.audit_dir).glob("CH*.json")):
            ch = p.name.split("_")[0]
            reports.append(audit_chapter(canon, ch, p))
    else:
        ap.print_help()
        sys.exit(0)

    has_fail = False
    for r in reports:
        print(f"[{r['status']}] {r['chapter']} ({r['file']}): {r['panels']} panels | "
              f"{r['code_trays']} Python trays | {r['skill_badges']} Skill badges")
        for e in r["errors"]:
            has_fail = True
            print(f"   ERROR: {e}")
        for w in r["warnings"]:
            print(f"   WARN : {w}")
    sys.exit(1 if has_fail else 0)


if __name__ == "__main__":
    main()
