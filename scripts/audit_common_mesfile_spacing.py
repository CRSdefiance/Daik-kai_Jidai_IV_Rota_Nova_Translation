from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage


FILE_PATH = "/COMMON/MESFILE.DK4"
ROW_PATTERN = re.compile(r"DK4_MES_B([0-9]+)_R([0-9]+)")
TARGETED = {
    "DK4_MES_B00_R0034": [b"Resupply? %s coins."],
    "DK4_MES_B00_R0053": [b"Dock at %s?", b"Sailors are unassigned. Continue?"],
    "DK4_MES_B04_R0059": [b"%s acquired!", b"%s joined!"],
    "DK4_MES_B10_R0037": [b"Change supply ratio?"],
    "DK4_MES_B10_R0036": [
        b"Your sailors look tired. Rest at the inn?",
        b"You have no cargo.",
        b"Not enough coins to fully resupply. Buy what you can?",
    ],
    "DK4_MES_B11_R0011": [b"Barkeep, drinks for everyone."],
    "DK4_MES_B11_R0020": [
        b"%s's fleet is hunting %s.",
        b"Word is, %s's fleet is heading to %s.",
    ],
    "DK4_MES_B11_R0021": [b"Word is, %s's fleet is heading to %s."],
    "DK4_MES_B14_R0036": [b"%s! You aid the city's defense"],
    "DK4_MES_B14_R0038": [
        b"A Market recommendation? Let me see it.",
        b"%s! Will you aid the city's defense?",
    ],
}
EXPECTED_GUARDS = {
    "DK4_MES_B00_R0034": [(0, b"  ")],
    "DK4_MES_B04_R0059": [(20, b"  ")],
    "DK4_MES_B10_R0036": [(0, b" ")],
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_report(candidate: Path, batch_path: Path) -> dict[str, object]:
    payload = json.loads(batch_path.read_text(encoding="utf-8"))
    common = NdsImage.open(candidate).read_file(FILE_PATH)
    blocks = IlnkContainer.parse(common).blocks
    issues: list[dict[str, object]] = []
    audited_ranges = 0
    audited_entries = 0

    for record in payload["records"]:
        row_id = str(record["id"])
        match = ROW_PATTERN.fullmatch(row_id)
        if match is None:
            issues.append({"id": row_id, "code": "invalid-id"})
            continue
        block_index = int(match.group(1))
        record_index = int(match.group(2))
        raw = blocks[block_index].split(b"\0")[record_index]
        expected = bytes.fromhex(record["replacement_hex"])
        if raw != expected:
            issues.append({"id": row_id, "code": "candidate-batch-mismatch"})
            continue

        for start, end in record["translated_ranges"]:
            audited_ranges += 1
            segment = raw[start:end]
            if b"\n" in segment.rstrip(b" "):
                issues.append({"id": row_id, "code": "stored-prose-break"})

        for start, end in zip(record["entry_offsets"], record["entry_ends"]):
            audited_entries += 1
            entry = raw[start:end].strip(b" ")
            if not entry or entry.startswith(b"\n"):
                issues.append({"id": row_id, "code": "blank-entry", "offset": start})

        expected_entries = TARGETED.get(row_id)
        if expected_entries is not None:
            actual_entries = [
                raw[start:end].strip(b" ")
                for start, end in zip(record["entry_offsets"], record["entry_ends"])
            ]
            for needle, actual in zip(expected_entries, actual_entries):
                if needle not in actual:
                    issues.append(
                        {
                            "id": row_id,
                            "code": "targeted-entry-text-mismatch",
                            "expected": needle.decode("ascii"),
                            "actual": actual.decode("ascii", errors="replace"),
                        }
                    )

        for offset, guard in EXPECTED_GUARDS.get(row_id, []):
            if not raw.startswith(guard, offset):
                issues.append(
                    {
                        "id": row_id,
                        "code": "runtime-entry-guard-mismatch",
                        "offset": offset,
                        "expected_hex": guard.hex().upper(),
                    }
                )

    return {
        "format": "dk4-common-mesfile-spacing-audit-v1",
        "candidate": str(candidate),
        "candidate_sha256": sha256(candidate.read_bytes()),
        "common_sha256": sha256(common),
        "batch": str(batch_path),
        "audited_records": len(payload["records"]),
        "audited_ranges": audited_ranges,
        "audited_entries": audited_entries,
        "targeted_runtime_repairs": sorted(TARGETED),
        "status": "pass" if not issues else "fail",
        "blocking_issue_count": len(issues),
        "issues": issues,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument(
        "--batch",
        type=Path,
        default=Path("translations/common_mesfile_spacing_v4.json"),
    )
    parser.add_argument(
        "--out", type=Path, default=Path("work/analysis/common_mesfile_spacing.json")
    )
    args = parser.parse_args()
    report = build_report(args.candidate, args.batch)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
