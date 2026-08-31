from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.arm9_profiles import PROFILES


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def has_japanese(text: str) -> bool:
    return any(
        "\u3040" <= char <= "\u30ff" or "\u3400" <= char <= "\u9fff"
        for char in text
    )


def decode_slot(data: bytes) -> str:
    return data.rstrip(b"\0 ").decode("cp932", errors="replace")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit profile-backed ARM9 UI and changed graphics in a candidate ROM."
    )
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--clean", type=Path, default=Path("work/clean.nds"))
    parser.add_argument(
        "--scan", type=Path, default=Path("work/arm9_menu_scan.json")
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("work/analysis/interface_localization_audit.json"),
    )
    args = parser.parse_args()

    clean = NdsImage.open(args.clean)
    candidate = NdsImage.open(args.candidate)
    candidate_arm9 = candidate.read_file("/__arm9__.bin")

    records: list[dict[str, object]] = []
    covered_ranges: list[tuple[int, int]] = []
    for entry in PROFILES["all"]:
        start = entry.offset
        end = start + entry.source_length
        covered_ranges.append((start, end))
        actual = candidate_arm9[start:end]
        english = entry.suggested_english.encode("cp932").ljust(
            entry.source_length, b"\0"
        )
        if actual == english:
            state = "english-exact"
        elif actual == entry.expected_bytes:
            state = "japanese-source"
        else:
            decoded = decode_slot(actual)
            state = "japanese-variant" if has_japanese(decoded) else "english-variant"
        records.append(
            {
                "id": entry.row_id,
                "offset": start,
                "length": entry.source_length,
                "context": entry.context,
                "japanese": entry.japanese,
                "suggested_english": entry.suggested_english,
                "actual_text": decode_slot(actual),
                "state": state,
            }
        )

    uncovered_scan_hits: list[dict[str, object]] = []
    if args.scan.exists():
        scan = json.loads(args.scan.read_text(encoding="utf-8"))
        for hit in scan["files"][0]["sjis_hits"]:
            offset = int(hit["offset"])
            decoded = str(hit["decoded"])
            if (
                offset < 0x110000
                or hit.get("terminator") != "00"
                or float(hit["score"]) < 0.85
                or not has_japanese(decoded)
                or any(start <= offset < end for start, end in covered_ranges)
            ):
                continue
            length = int(hit["length"])
            actual = candidate_arm9[offset : offset + length]
            uncovered_scan_hits.append(
                {
                    "offset": offset,
                    "length": length,
                    "source_text": decoded,
                    "score": hit["score"],
                    "candidate_text": decode_slot(actual),
                    "candidate_has_japanese": has_japanese(decode_slot(actual)),
                }
            )

    clean_files = {path: data for _, path, data in clean.iter_files()}
    candidate_files = {path: data for _, path, data in candidate.iter_files()}
    graphics = []
    for path in sorted(
        path
        for path in clean_files
        if path.lower().endswith((".pxl", ".fls"))
        and clean_files[path] != candidate_files.get(path)
    ):
        graphics.append(
            {
                "path": path,
                "source_sha256": sha256(clean_files[path]),
                "candidate_sha256": sha256(candidate_files[path]),
                "size": len(candidate_files[path]),
            }
        )

    report = {
        "format": "dk4-interface-localization-audit-v1",
        "candidate": str(args.candidate),
        "candidate_sha256": sha256(args.candidate.read_bytes()),
        "profile_record_count": len(records),
        "profile_states": dict(Counter(str(row["state"]) for row in records)),
        "profile_records": records,
        "uncovered_high_confidence_arm9_scan_hits": uncovered_scan_hits,
        "changed_graphics": graphics,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: report[key] for key in report if key != "profile_records"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
