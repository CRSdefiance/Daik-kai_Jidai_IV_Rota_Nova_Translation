from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
OUTPUTS = {
    "/COMMON/HELP.DK4": Path("translations/help_literal_percent_safety_v1.json"),
    "/data/SC0.DK4": Path("translations/raphael_literal_percent_safety_v1.json"),
}
TARGETS = {
    "/COMMON/HELP.DK4": {(7, 0), (8, 0), (22, 0), (36, 0), (37, 0), (38, 0), (39, 0)},
    "/data/SC0.DK4": {(45, 52)},
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replace_literal_percents(raw: bytes) -> bytes:
    text_end = len(raw.rstrip(b" "))
    body = raw[:text_end]
    padding = raw[text_end:]
    rebuilt = body.replace(b"%", b" percent")
    growth = len(rebuilt) - len(body)
    if growth > len(padding):
        raise ValueError(f"literal-percent rewrite needs {growth} padding bytes")
    return rebuilt + padding[growth:]


def materialize(file_path: str, source: bytes) -> dict[str, object]:
    if file_path == "/data/SC0.DK4":
        raise ValueError(
            "Ceuta is an FE system modal, not progressive dialogue. Use "
            "prepare_raphael_system_panel_repair.py with the clean Japanese command; "
            "never decode the canonical translated prefix as CP932 prose."
        )
    container = IlnkContainer.parse(source)
    records: list[dict[str, object]] = []
    for block_index, record_index in sorted(TARGETS[file_path]):
        raw = container.blocks[block_index].split(b"\0")[record_index]
        replacement = replace_literal_percents(raw)
        if replacement == raw or b"%" in replacement:
            raise ValueError(f"B{block_index:02d} R{record_index:04d}: unsafe percent remains")
        translated_start = 0
        records.append(
            {
                "id": f"DK4_MES_B{block_index:02d}_R{record_index:04d}",
                "english": replacement[translated_start:].rstrip(b" ").decode("ascii"),
                "display_entries": [
                    replacement[translated_start:].rstrip(b" ").decode("ascii")
                ],
                "replacement_hex": replacement.hex().upper(),
                "entry_offsets": [0],
                "entry_ends": [len(replacement)],
                "entry_guard_bytes": 0,
                # HELP records contain renderer-owned trailing row markers;
                # the release-wide layout audit validates printable lines.
                "linebreak_guard_bytes": 0,
                "translated_ranges": [[translated_start, len(replacement)]],
                # This limit protects allocation, not stored rows.
                "text_box_max_chars": 255,
                "context": "Literal percent made safe for runtime text formatting.",
                "notes": "Uses the word 'percent' so printf-like render paths cannot consume following text as a conversion.",
            }
        )
    header: dict[str, object] = {
        "format": "dk4-ilnk-translation-batch-v1",
        "content_type": "fixed-text-format-safety-v1",
        "file_path": file_path,
        "source_file_sha256": sha256(source),
        "target_locale": "en-US",
        "scope": "Remove unsafe literal percent tokens from translated fixed text",
        "records": records,
    }
    header.update(
        {
            "ascii_guard_exemption": (
                "Source-locked fixed records preserve their measured entry and "
                "continuation guards; this batch changes only literal percent wording."
            ),
            "fixed_allocation_policy": "screen-entry-layout-v1",
        }
    )
    return header


def main() -> None:
    rom = NdsImage.open(BASE)
    for file_path, output in OUTPUTS.items():
        if file_path == "/data/SC0.DK4":
            print("Legacy Ceuta batch retained for lineage; source-verified system-panel repair supersedes it.")
            continue
        payload = materialize(file_path, rom.read_file(file_path))
        output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"wrote {output}: {len(payload['records'])} records")


if __name__ == "__main__":
    main()
