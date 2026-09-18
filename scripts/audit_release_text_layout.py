from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.sjis_scan import contains_japanese


TEXT_FILES = {
    "/COMMON/MESFILE.DK4": ("common-fixed", 2),
    "/COMMON/HELP.DK4": ("help", 1),
    "/data/SC0.DK4": ("story", 1),
    "/data/SC1.DK4": ("story", 1),
    "/data/SC2.DK4": ("story", 1),
    "/data/SC3.DK4": ("story", 1),
}

# These are measured renderer exceptions, not waivers for broken content.
# B14/R59 visibly preserves its one-space Inn indentation. B15/R63 is the
# compact shipyard help panel, whose first continuation byte is not consumed.
COMMON_LINE_GUARD_EXCEPTIONS = {
    (14, 59): 1,
    (15, 63): 0,
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_visible_ascii(byte: int) -> bool:
    return 0x21 <= byte <= 0x7E


def line_guard_issues(
    raw: bytes,
    *,
    expected_guard: int,
    file_path: str,
    renderer: str,
    block_index: int,
    record_index: int,
) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    for offset, byte in enumerate(raw):
        if byte != 0x0A:
            continue
        cursor = offset + 1
        actual_guard = 0
        while cursor < len(raw) and raw[cursor] == 0x20:
            actual_guard += 1
            cursor += 1
        # Empty lines, terminators/padding, control bytes, and Japanese lead
        # bytes are not English continuation glyphs and are checked elsewhere.
        if cursor >= len(raw) or not is_visible_ascii(raw[cursor]):
            continue
        if actual_guard < expected_guard:
            issues.append(
                {
                    "severity": "error",
                    "code": "short-linebreak-guard",
                    "file_path": file_path,
                    "renderer": renderer,
                    "id": f"DK4_MES_B{block_index:02d}_R{record_index:04d}",
                    "linebreak_offset": offset,
                    "expected_guard_bytes": expected_guard,
                    "actual_guard_bytes": actual_guard,
                    "next_byte": raw[cursor],
                }
            )
    return issues


def audit_ilnk(file_path: str, data: bytes, source_data: bytes) -> dict[str, object]:
    renderer, default_guard = TEXT_FILES[file_path]
    container = IlnkContainer.parse(data)
    source_container = IlnkContainer.parse(source_data)
    if len(container.blocks) != len(source_container.blocks):
        raise ValueError(f"{file_path}: source/candidate block counts differ")
    issues: list[dict[str, object]] = []
    english_records = 0
    japanese_records = 0
    mixed_records = 0
    linebreaks_checked = 0
    for block_index, block in enumerate(container.blocks):
        source_records = source_container.blocks[block_index].split(b"\0")
        records = block.split(b"\0")
        for record_index, raw in enumerate(records):
            if not raw:
                continue
            decoded = raw.decode("cp932", errors="replace")
            has_english = any(
                ("A" <= character <= "Z") or ("a" <= character <= "z")
                for character in decoded
            )
            has_japanese = contains_japanese(decoded)
            english_records += int(has_english and not has_japanese)
            japanese_records += int(has_japanese and not has_english)
            mixed_records += int(has_english and has_japanese)
            # Existing translations are records that differ from the clean
            # Japanese ROM. Original ASCII resources are outside this audit.
            source_same = (
                record_index < len(source_records)
                and raw == source_records[record_index]
            )
            if not has_english or has_japanese or source_same:
                continue
            expected_guard = (
                COMMON_LINE_GUARD_EXCEPTIONS.get(
                    (block_index, record_index), default_guard
                )
                if renderer == "common-fixed"
                else default_guard
            )
            current = line_guard_issues(
                raw,
                expected_guard=expected_guard,
                file_path=file_path,
                renderer=renderer,
                block_index=block_index,
                record_index=record_index,
            )
            linebreaks_checked += sum(
                1
                for offset, byte in enumerate(raw)
                if byte == 0x0A
                and any(
                    is_visible_ascii(value)
                    for value in raw[offset + 1 : offset + 4]
                )
            )
            issues.extend(current)
    return {
        "file_path": file_path,
        "renderer": renderer,
        "sha256": sha256(data),
        "english_records": english_records,
        "japanese_records": japanese_records,
        "mixed_records": mixed_records,
        "linebreaks_checked": linebreaks_checked,
        "issues": issues,
    }


def build_report(rom_path: Path, clean_path: Path) -> dict[str, object]:
    rom_bytes = rom_path.read_bytes()
    rom = NdsImage.open(rom_path)
    clean = NdsImage.open(clean_path)
    files = [
        audit_ilnk(path, rom.read_file(path), clean.read_file(path))
        for path in TEXT_FILES
    ]
    issues = [issue for row in files for issue in row["issues"]]
    return {
        "format": "dk4-release-text-layout-audit-v1",
        "candidate": str(rom_path),
        "candidate_sha256": sha256(rom_bytes),
        "clean_source": str(clean_path),
        "status": "pass" if not issues else "fail",
        "blocking_issue_count": len(issues),
        "issue_counts": dict(Counter(str(issue["code"]) for issue in issues)),
        "files": files,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit built ROM text against renderer-specific line guards."
    )
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--clean", type=Path, default=Path("work/clean.nds"))
    parser.add_argument(
        "--out", type=Path, default=Path("work/analysis/release_text_layout.json")
    )
    parser.add_argument(
        "--allow-fail",
        action="store_true",
        help="Write the report without returning a failing exit status.",
    )
    args = parser.parse_args()
    report = build_report(args.candidate, args.clean)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    summary = {
        "candidate": report["candidate"],
        "status": report["status"],
        "blocking_issue_count": report["blocking_issue_count"],
        "issue_counts": report["issue_counts"],
        "files": [
            {
                key: row[key]
                for key in (
                    "file_path",
                    "renderer",
                    "english_records",
                    "japanese_records",
                    "mixed_records",
                    "linebreaks_checked",
                )
            }
            | {"issue_count": len(row["issues"])}
            for row in report["files"]
        ],
        "report": str(args.out),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if report["status"] != "pass" and not args.allow_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
