#!/usr/bin/env python3
"""
San Jie Class (July 2026) — Zero-Drift Prompt Compiler & Continuity Audit Engine (v1.0)
Deterministic, zero-dependency Python engine enforcing 1:1 visual lock across all
17 photographed students, 17 Pet Guardians (Stages 0–3), and 17 Signature Relics.

Usage:
  python3 sanjie_zero_drift_engine.py --audit
  python3 sanjie_zero_drift_engine.py --compile --students 01,02 --stage 3 --mode comic_panel --scene "crossing the Whispering Bridge"
"""
import argparse, json, os, sys, hashlib

REGISTRY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sanjie_master_registry.json")

FORBIDDEN_TERMS = [
    "Tan Jie Khe Jacob", "Ember", "sword in Kai", "meat", "gun", "modern plastic"
]

def load_registry():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def run_audit(reg):
    roster = reg.get("roster", [])
    errors = []
    if len(roster) != 17:
        errors.append(f"CARDINALITY_FAIL: expected 17 students, found {len(roster)}")
    seen_nums, seen_pids = set(), set()
    for r in roster:
        num, pid = r["num"], r["pet_id"]
        if num in seen_nums: errors.append(f"DUP_NUM: {num}")
        if pid in seen_pids: errors.append(f"DUP_PET_ID: {pid}")
        seen_nums.add(num); seen_pids.add(pid)
        sg = r.get("student_genome", {})
        if not sg.get("hair") or not sg.get("outfit") or len(sg.get("hex", [])) < 3:
            errors.append(f"INCOMPLETE_GENOME: #{num} {r['student_en']}")
        if not r.get("relic", {}).get("en"):
            errors.append(f"MISSING_RELIC: #{num} {r['student_en']}")
        if "Jacob" in r["student_en"]:
            errors.append(f"NEGATIVE_CONTRACT_BREACH: excluded student found ({r['student_en']})")

    raw_bytes = open(REGISTRY_PATH, "rb").read()
    sha = hashlib.sha256(raw_bytes).hexdigest()
    print(f"=== SAN JIE ZERO-DRIFT ENGINE AUDIT (v1.0) ===")
    print(f"Registry SHA-256 : {sha}")
    print(f"Roster Cardinality: {len(roster)}/17")
    print(f"Unique Pet IDs    : {len(seen_pids)}/17")
    print(f"Audit Status      : {'PASS (0 drift errors)' if not errors else 'FAIL'}")
    for e in errors:
        print(f"  [ERROR] {e}")
    return 0 if not errors else 1

def compile_prompt(reg, student_nums, stage, mode, scene):
    by_num = {r["num"]: r for r in reg["roster"]}
    selected = []
    for n in student_nums:
        k = f"{int(n):02d}"
        if k not in by_num:
            raise ValueError(f"Unknown student number: {n} (valid: 01..17)")
        selected.append(by_num[k])

    stage_key = {1: "s1_baby", 2: "s2_site", 3: "s3_grand"}.get(stage, "s2_site")
    relic_key = {1: "s1", 2: "s2", 3: "s3"}.get(stage, "s2")

    char_blocks = []
    for r in selected:
        sg = r["student_genome"]
        char_blocks.append(
            f"[STUDENT #{r['num']} {r['student_en']} ({r['student_zh']}): 11yo Malaysian Chinese, "
            f"hair={sg['hair']}, glasses={sg['glasses']}, outfit={sg['outfit']}, palette={','.join(sg['hex'])} | "
            f"PARTNER PET ({r['pet_id']} {r['pet_name']}, Stage {stage}={r['stages'][stage_key]}) | "
            f"LOCKED RELIC={r['relic']['en']} ({r['relic']['zh']}): {r['relic'][relic_key] or r['relic']['en']}]"
        )

    prompt = (
        f"Studio Ghibli storybook watercolor and crisp sepia ink ({mode}), 100% text-free with zero words, "
        f"zero speech bubbles, zero letters, 100% plant-based eco-friendly world. "
        f"MANDATORY VISUAL LOCKS (anchor 1:1 to MASTER_BOARD_01, MASTER_BOARD_02, MASTER_BOARD_03): "
        + " ; ".join(char_blocks)
        + f". SCENE ACTION: {scene}."
    )
    print(prompt)
    return 0

def main():
    ap = argparse.ArgumentParser(description="San Jie Class Zero-Drift Prompt Compiler & Audit Engine")
    ap.add_argument("--audit", action="store_true", help="Run deterministic cardinality & negative-contract audit")
    ap.add_argument("--compile", action="store_true", help="Compile a drift-locked prompt for specified students")
    ap.add_argument("--students", type=str, default="01", help="Comma-separated student numbers (e.g. 01,02,15)")
    ap.add_argument("--stage", type=int, default=2, choices=[1, 2, 3], help="Pet & Relic evolution stage (1, 2, or 3)")
    ap.add_argument("--mode", type=str, default="comic_panel", help="Target art mode (comic_panel, cinema_poster, editorial_poster)")
    ap.add_argument("--scene", type=str, default="exploring the sunlit valley together", help="Scene description")
    args = ap.parse_args()

    reg = load_registry()
    if args.audit:
        sys.exit(run_audit(reg))
    if args.compile:
        nums = [x.strip() for x in args.students.split(",") if x.strip()]
        sys.exit(compile_prompt(reg, nums, args.stage, args.mode, args.scene))
    ap.print_help()

if __name__ == "__main__":
    main()
