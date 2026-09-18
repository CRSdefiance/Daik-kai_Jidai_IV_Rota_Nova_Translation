from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from collections import Counter, defaultdict
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.sjis_scan import contains_japanese


STACK = Path("translations/release_stack.json")
TEXT_PATHS = {
    "/COMMON/MESFILE.DK4",
    "/COMMON/HELP.DK4",
    "/data/SC0.DK4",
    "/data/SC1.DK4",
    "/data/SC2.DK4",
    "/data/SC3.DK4",
}
ROW_PATTERN = re.compile(r"DK4_MES_B([0-9]+)_R([0-9]+)")
PRINTF_PATTERN = re.compile(rb"%(?:%|[-+ #0]*[0-9]*(?:\.[0-9]+)?[diouxXeEfFgGcs])")
RUNTIME_F_NAME_POINTERS = {
    0x120D44: "Ｆerog",
    0x120DA8: "Ｆerid",
    0x120E00: "Ｆernando",
    0x120FC8: "Ｆazul",
    0x120FE0: "Ｆernan",
    0x121088: "Ｆong",
    0x121264: "Ｆlahven",
    0x1221C0: "Ｆollower",
    0x1222C0: "Ｆrancisca",
    0x1223C0: "Ｆaticia",
}
RUNTIME_NAME_SEPARATORS = (0x1484DC, 0x1484E0)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def visible(raw: bytes) -> bytes:
    return bytes(value for value in raw if value not in b" \t\r\n\0")


def has_text(raw: bytes) -> bool:
    if not visible(raw):
        return False
    decoded = raw.decode("cp932", errors="replace")
    return any(character.isalnum() for character in decoded) or contains_japanese(decoded)


def invalid_printf_offsets(raw: bytes) -> list[int]:
    invalid: list[int] = []
    cursor = 0
    while cursor < len(raw):
        position = raw.find(b"%", cursor)
        if position < 0:
            break
        match = PRINTF_PATTERN.match(raw, position)
        if match is None:
            invalid.append(position)
            cursor = position + 1
        else:
            cursor = match.end()
    return invalid


def c_string(data: bytes, offset: int, limit: int = 64) -> bytes:
    end = data.find(b"\0", offset, min(len(data), offset + limit))
    if end < 0:
        return b""
    return data[offset:end]


def load_json(path: Path) -> dict[str, object] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def profile_paths(profile: str) -> set[Path]:
    stack = load_json(STACK)
    if stack is None:
        raise ValueError(f"cannot read {STACK}")
    profiles = stack.get("profiles")
    if not isinstance(profiles, dict) or profile not in profiles:
        raise ValueError(f"unknown release profile: {profile}")
    value = profiles[profile]
    if not isinstance(value, dict) or not isinstance(value.get("batches"), list):
        raise ValueError(f"invalid release profile: {profile}")
    return {Path(str(path)) for path in value["batches"]}


def iter_declarations(active: set[Path]):
    for path in sorted(Path("translations").rglob("*.json")):
        payload = load_json(path)
        if payload is None or payload.get("format") != "dk4-ilnk-translation-batch-v1":
            continue
        file_path = str(payload.get("file_path", ""))
        if file_path not in TEXT_PATHS:
            continue
        records = payload.get("records")
        if not isinstance(records, list):
            continue
        for record in records:
            if not isinstance(record, dict):
                continue
            match = ROW_PATTERN.fullmatch(str(record.get("id", "")))
            offsets = record.get("entry_offsets")
            if match is None or not (
                isinstance(offsets, list)
                and offsets
                and all(isinstance(value, int) for value in offsets)
                and offsets == sorted(set(offsets))
            ):
                continue
            ends = record.get("entry_ends")
            if not (
                isinstance(ends, list)
                and len(ends) == len(offsets)
                and all(isinstance(value, int) for value in ends)
            ):
                ends = offsets[1:] + [None]
            yield {
                "batch": path.as_posix(),
                "active": path in active,
                "file_path": file_path,
                "block": int(match.group(1)),
                "record": int(match.group(2)),
                "offsets": offsets,
                "ends": ends,
                "structure": str(record.get("structure", "")),
                "replacement_hex": record.get("replacement_hex"),
                "entry_guard_bytes": record.get("entry_guard_bytes", 0),
                "entry_guards": record.get("entry_guards"),
            }


def build_report(candidate: Path, clean: Path, profile: str) -> dict[str, object]:
    candidate_rom = NdsImage.open(candidate)
    clean_rom = NdsImage.open(clean)
    active = profile_paths(profile)
    declarations = list(iter_declarations(active))
    grouped: dict[tuple[str, int, int], list[dict[str, object]]] = defaultdict(list)
    for declaration in declarations:
        grouped[
            (
                str(declaration["file_path"]),
                int(declaration["block"]),
                int(declaration["record"]),
            )
        ].append(declaration)

    candidate_files = {
        path: IlnkContainer.parse(candidate_rom.read_file(path)) for path in TEXT_PATHS
    }
    clean_files = {
        path: IlnkContainer.parse(clean_rom.read_file(path)) for path in TEXT_PATHS
    }
    issues: list[dict[str, object]] = []
    audited_entries = 0
    active_records = 0
    corpus_records = 0
    printf_records = 0
    runtime_name_count = 0

    for (file_path, block_index, record_index), rows in sorted(grouped.items()):
        candidate_blocks = candidate_files[file_path].blocks
        clean_blocks = clean_files[file_path].blocks
        if block_index >= len(candidate_blocks) or block_index >= len(clean_blocks):
            continue
        candidate_records = candidate_blocks[block_index].split(b"\0")
        clean_records = clean_blocks[block_index].split(b"\0")
        if record_index >= len(candidate_records) or record_index >= len(clean_records):
            continue
        raw = candidate_records[record_index]
        source = clean_records[record_index]
        active_rows = [row for row in rows if bool(row["active"])]
        active_records += int(bool(active_rows))
        corpus_records += 1
        signatures = Counter(
            tuple(int(value) for value in row["offsets"])
            for row in rows
            if all(0 <= int(value) < len(raw) for value in row["offsets"])
        )
        if len(signatures) > 1 and active_rows:
            active_signature = tuple(int(value) for value in active_rows[-1]["offsets"])
            missing = sorted(
                offset
                for signature in signatures
                for offset in signature
                if offset not in active_signature and 0 <= offset < len(raw)
            )
            if missing:
                issues.append(
                    {
                        "severity": "warning",
                        "code": "historical-entry-boundary-not-in-active-batch",
                        "file_path": file_path,
                        "id": f"DK4_MES_B{block_index:02d}_R{record_index:04d}",
                        "active_offsets": list(active_signature),
                        "historical_offsets": sorted({value for sig in signatures for value in sig}),
                        "missing_offsets": missing,
                    }
                )

        # Audit the union of every source-locked entry declaration. Historical
        # boundaries are included specifically to catch a later batch silently
        # replacing an interior message with padding.
        boundaries: dict[tuple[int, int], set[str]] = defaultdict(set)
        for row in rows:
            offsets = [int(value) for value in row["offsets"]]
            ends = row["ends"]
            for position, start in enumerate(offsets):
                end_value = ends[position]
                end = int(end_value) if isinstance(end_value, int) else (
                    offsets[position + 1] if position + 1 < len(offsets) else len(raw)
                )
                if 0 <= start < end <= len(raw):
                    boundaries[(start, end)].add(str(row["batch"]))
        for (start, end), batches in sorted(boundaries.items()):
            audited_entries += 1
            segment = raw[start:end]
            if has_text(segment):
                continue
            source_segment = source[start : min(end, len(source))]
            if has_text(source_segment):
                active_boundary = any(
                    row["active"]
                    and start in row["offsets"]
                    for row in rows
                )
                issues.append(
                    {
                        "severity": "error" if active_boundary else "warning",
                        "code": "translated-entry-overwritten-by-space",
                        "file_path": file_path,
                        "id": f"DK4_MES_B{block_index:02d}_R{record_index:04d}",
                        "offset": start,
                        "end": end,
                        "active_boundary": active_boundary,
                        "declared_by": sorted(batches),
                    }
                )

        if raw != source and any(0x41 <= value <= 0x7A for value in raw):
            bad_percent = [
                offset
                for offset in invalid_printf_offsets(raw.rstrip(b" \0"))
                if not (
                    file_path.startswith("/data/SC")
                    and offset == 0
                    and source.startswith(b"%")
                )
            ]
            if bad_percent:
                printf_records += 1
                for offset in bad_percent:
                    issues.append(
                        {
                            "severity": "error",
                            "code": "unsafe-literal-percent",
                            "file_path": file_path,
                            "id": f"DK4_MES_B{block_index:02d}_R{record_index:04d}",
                            "offset": offset,
                        }
                    )

        for row in active_rows:
            replacement_hex = row.get("replacement_hex")
            if isinstance(replacement_hex, str) and replacement_hex:
                expected = bytes.fromhex(replacement_hex)
                if raw != expected:
                    issues.append(
                        {
                            "severity": "error",
                            "code": "active-batch-candidate-mismatch",
                            "file_path": file_path,
                            "id": f"DK4_MES_B{block_index:02d}_R{record_index:04d}",
                            "batch": row["batch"],
                        }
                    )
            offsets = [int(value) for value in row["offsets"]]
            guards = row.get("entry_guards")
            if not (
                isinstance(guards, list)
                and len(guards) == len(offsets)
                and all(isinstance(value, int) for value in guards)
            ):
                guards = [int(row.get("entry_guard_bytes", 0))] * len(offsets)
            for start, guard in zip(offsets, guards):
                if guard and raw[start : start + guard] != b" " * guard:
                    issues.append(
                        {
                            "severity": "error",
                            "code": "entry-leading-guard-missing",
                            "file_path": file_path,
                            "id": f"DK4_MES_B{block_index:02d}_R{record_index:04d}",
                            "offset": start,
                            "expected_guard_bytes": guard,
                        }
                    )

    # Percent scanning must cover every translated record, including records
    # that have no packed-entry declaration.
    for file_path in sorted(TEXT_PATHS):
        candidate_container = candidate_files[file_path]
        clean_container = clean_files[file_path]
        for block_index, block in enumerate(candidate_container.blocks):
            clean_records = clean_container.blocks[block_index].split(b"\0")
            for record_index, raw in enumerate(block.split(b"\0")):
                if record_index >= len(clean_records) or raw == clean_records[record_index]:
                    continue
                decoded = raw.decode("cp932", errors="replace")
                if contains_japanese(decoded) or not any(character.isascii() and character.isalpha() for character in decoded):
                    continue
                key = (file_path, block_index, record_index)
                if key in grouped:
                    continue
                for offset in invalid_printf_offsets(raw.rstrip(b" \0")):
                    if (
                        file_path.startswith("/data/SC")
                        and offset == 0
                        and clean_records[record_index].startswith(b"%")
                    ):
                        continue
                    printf_records += 1
                    issues.append(
                        {
                            "severity": "error",
                            "code": "unsafe-literal-percent",
                            "file_path": file_path,
                            "id": f"DK4_MES_B{block_index:02d}_R{record_index:04d}",
                            "offset": offset,
                        }
                    )

    # Static %s records cannot reveal bytes supplied later by runtime entity
    # expansion. In this renderer, a raw ASCII F begins the FI/FA/FO/FU macro
    # family, so names such as Fernando and Ferog lose that leading character.
    # Audit the live pointers and the separate full-name separator constants.
    arm9 = candidate_rom.read_file("/__arm9__.bin")
    for pointer_offset, expected in sorted(RUNTIME_F_NAME_POINTERS.items()):
        runtime_name_count += 1
        target = struct.unpack_from("<I", arm9, pointer_offset)[0] - 0x02000000
        raw_name = c_string(arm9, target) if 0 <= target < len(arm9) else b""
        decoded = raw_name.decode("cp932", errors="replace")
        if raw_name.startswith(b"F"):
            issues.append(
                {
                    "severity": "error",
                    "code": "runtime-name-reserved-ascii-f",
                    "pointer_offset": pointer_offset,
                    "target_offset": target,
                    "decoded": decoded,
                }
            )
        if decoded != expected:
            issues.append(
                {
                    "severity": "error",
                    "code": "runtime-name-representation-mismatch",
                    "pointer_offset": pointer_offset,
                    "target_offset": target,
                    "expected": expected,
                    "decoded": decoded,
                }
            )
    for separator_offset in RUNTIME_NAME_SEPARATORS:
        if arm9[separator_offset : separator_offset + 2] != b" \0":
            issues.append(
                {
                    "severity": "error",
                    "code": "runtime-full-name-separator-mismatch",
                    "offset": separator_offset,
                    "actual_hex": arm9[separator_offset : separator_offset + 4].hex(),
                }
            )

    blocking = [issue for issue in issues if issue["severity"] == "error"]
    return {
        "format": "dk4-release-translation-integrity-audit-v1",
        "candidate": str(candidate),
        "candidate_sha256": sha256(candidate.read_bytes()),
        "clean_source": str(clean),
        "profile": profile,
        "declaration_count": len(declarations),
        "corpus_record_count": corpus_records,
        "active_declared_record_count": active_records,
        "audited_entry_count": audited_entries,
        "unsafe_percent_record_count": printf_records,
        "runtime_name_count": runtime_name_count,
        "status": "pass" if not blocking else "fail",
        "blocking_issue_count": len(blocking),
        "warning_count": len(issues) - len(blocking),
        "issue_counts": dict(Counter(str(issue["code"]) for issue in issues)),
        "issues": issues,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit a unified ROM for blank packed entries, missing guards, and unsafe formatting."
    )
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--clean", type=Path, default=Path("work/clean.nds"))
    parser.add_argument("--profile", default="all-routes-unified-v1")
    parser.add_argument(
        "--out", type=Path, default=Path("work/analysis/release_translation_integrity.json")
    )
    parser.add_argument("--allow-fail", action="store_true")
    args = parser.parse_args()
    report = build_report(args.candidate, args.clean, args.profile)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {key: value for key, value in report.items() if key != "issues"}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if report["status"] != "pass" and not args.allow_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
