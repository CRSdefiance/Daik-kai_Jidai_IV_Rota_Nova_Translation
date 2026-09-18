from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from dk4tool.dialogue.codec import tokenize_raw
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import export_mesfile_rows


ROOT = Path(__file__).resolve().parents[1]
STACK = ROOT / "translations" / "release_stack.json"
PROFILE = "raphael-deep-route-v93"
ROUTE_FILE = "/data/SC0.DK4"
JAPANESE_RANGES = (("ぁ", "ヿ"), ("一", "龯"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path}: JSON root must be an object")
    return value


def _has_japanese(text: str) -> bool:
    return any(low <= character <= high for character in text for low, high in JAPANESE_RANGES)


def audit(
    candidate_path: Path,
    base_path: Path,
    manifest_path: Path,
    layout_path: Path,
    interface_path: Path,
) -> dict[str, object]:
    stack = _load(STACK)
    profile = stack["profiles"][PROFILE]
    batch_paths = [ROOT / path for path in profile["batches"]]
    raphael_paths = [path for path in batch_paths if "raphael_deep_route_" in path.name]

    translated: dict[str, str] = {}
    excluded: dict[str, dict[str, str]] = {}
    speaker_states: set[int] = set()
    duplicate_records: list[str] = []
    for path in raphael_paths:
        batch = _load(path)
        for record in batch.get("records", []):
            row_id = str(record["id"])
            if row_id in translated:
                duplicate_records.append(row_id)
            translated[row_id] = path.name
            english = str(record.get("english", ""))
            if english.startswith("{SPEAKER:"):
                speaker_states.add(int(english[9:11], 16))
        for row_id, reason in batch.get("excluded_records", {}).items():
            excluded[str(row_id)] = {"batch": path.name, "reason": str(reason)}
    # A split batch may deliberately list a record as excluded before a later
    # companion batch translates it under a disambiguated speaker profile.
    excluded = {row_id: details for row_id, details in excluded.items() if row_id not in translated}

    candidate_image = NdsImage.open(candidate_path)
    base_image = NdsImage.open(base_path)
    candidate_records = {
        str(row["id"]): bytes.fromhex(str(row["source_hex"]))
        for row in export_mesfile_rows(
            candidate_image.read_file(ROUTE_FILE),
            ROUTE_FILE,
            include_non_japanese=True,
        )
    }
    base_records = {
        str(row["id"]): bytes.fromhex(str(row["source_hex"]))
        for row in export_mesfile_rows(
            base_image.read_file(ROUTE_FILE),
            ROUTE_FILE,
            include_non_japanese=True,
        )
    }

    manifest = _load(manifest_path)
    manifest_changed = set(manifest.get("changed_records", {}).get(ROUTE_FILE, []))
    missing_translated = sorted(set(translated) - set(candidate_records) - manifest_changed)
    missing_manifest_changes = sorted(set(translated) - manifest_changed)
    unchanged_translated = sorted(
        row_id for row_id in translated
        if row_id in candidate_records and candidate_records[row_id] == base_records[row_id]
    )
    allocation_mismatches = sorted(
        row_id for row_id in translated
        if row_id in candidate_records and len(candidate_records[row_id]) != len(base_records[row_id])
    )
    mutated_exclusions = sorted(
        row_id for row_id in excluded
        if row_id in candidate_records and candidate_records[row_id] != base_records[row_id]
    )

    residuals: list[dict[str, object]] = []
    for row_id, raw in candidate_records.items():
        tokens = tokenize_raw(raw, leading_speaker_bytes=frozenset(speaker_states))
        visible = "".join(token.value for token in tokens if token.kind == "text")
        if not _has_japanese(visible):
            continue
        residuals.append({
            "id": row_id,
            "block": int(row_id.split("_B", 1)[1].split("_", 1)[0]),
            "length": len(raw),
            "source_hex": raw.hex().upper(),
            "decoded_text": visible,
            "excluded": row_id in excluded,
            **excluded.get(row_id, {}),
        })
    unresolved_residuals = [record["id"] for record in residuals if not record["excluded"]]

    layout = _load(layout_path)
    interface = _load(interface_path)
    manifest_hash_matches = manifest.get("candidate_sha256") == _sha256(candidate_path)
    manifest_checks_pass = all(bool(value) for value in manifest.get("checks", {}).values())
    layout_pass = layout.get("status") == "pass" and layout.get("blocking_issue_count") == 0
    interface_states = interface.get("profile_states", {})
    interface_pass = (
        interface.get("candidate_sha256") == _sha256(candidate_path)
        and not interface.get("uncovered_high_confidence_arm9_scan_hits")
        and sum(int(value) for value in interface_states.values()) == int(interface.get("profile_record_count", -1))
        and set(interface_states) <= {"english-exact", "english-variant"}
    )

    blocking = {
        "duplicate_records": duplicate_records,
        "missing_translated_records": missing_translated,
        "translated_records_missing_from_manifest": missing_manifest_changes,
        "unchanged_translated_records": unchanged_translated,
        "allocation_mismatches": allocation_mismatches,
        "mutated_excluded_controls": mutated_exclusions,
        "unresolved_japanese_records": unresolved_residuals,
        "manifest_hash_mismatch": [] if manifest_hash_matches else [str(candidate_path)],
        "manifest_failed_checks": [] if manifest_checks_pass else [str(manifest_path)],
        "layout_audit_failure": [] if layout_pass else [str(layout_path)],
        "interface_audit_failure": [] if interface_pass else [str(interface_path)],
    }
    blocking_count = sum(len(values) for values in blocking.values())
    return {
        "format": "dk4-raphael-route-completion-audit-v1",
        "status": "pass" if blocking_count == 0 else "fail",
        "profile": PROFILE,
        "candidate": str(candidate_path),
        "candidate_sha256": _sha256(candidate_path),
        "base": str(base_path),
        "batch_count": len(raphael_paths),
        "translated_record_count": len(translated),
        "speaker_state_count": len(speaker_states),
        "explicit_exclusion_count": len(excluded),
        "residual_japanese_decode_count": len(residuals),
        "all_residuals_explicitly_excluded": not unresolved_residuals,
        "all_excluded_controls_unchanged": not mutated_exclusions,
        "all_translations_exact_allocation": not allocation_mismatches,
        "manifest_checks_pass": manifest_hash_matches and manifest_checks_pass,
        "layout_audit_pass": layout_pass,
        "interface_audit_pass": interface_pass,
        "interface_profile_record_count": interface.get("profile_record_count"),
        "blocking_issue_count": blocking_count,
        "blocking": blocking,
        "residual_controls": residuals,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Prove cumulative Raphael route translation completion.")
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--layout", type=Path, required=True)
    parser.add_argument("--interface", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = audit(args.candidate, args.base, args.manifest, args.layout, args.interface)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key not in {"blocking", "residual_controls"}}, indent=2))
    if report["status"] != "pass":
        raise SystemExit(f"Raphael completion audit failed with {report['blocking_issue_count']} blocking issue(s)")


if __name__ == "__main__":
    main()
