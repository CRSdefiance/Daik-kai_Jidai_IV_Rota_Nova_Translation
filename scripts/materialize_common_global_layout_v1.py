from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.sjis_scan import contains_japanese


BASE_ROM = Path("out/lil_guild_shipyard_polish_v4_candidate.nds")
SOURCE_ROM = Path("out/raphael_natural_v2_accepted_base.nds")
CLEAN_ROM = Path("work/clean.nds")
OUTPUT = Path("translations/common_global_layout_v1.json")
FILE_PATH = "/COMMON/MESFILE.DK4"
EXCEPTIONS = {(14, 59), (15, 63)}
ROW_PATTERN = re.compile(r"DK4_MES_B([0-9]+)_R([0-9]+)")

# A handful of legacy strings filled their allocations completely. These
# concise rewrites create room for the guard bytes while preserving meaning,
# printf macros, and every independently addressed segment boundary.
MANUAL_SEGMENTS: dict[tuple[int, int, int], str] = {
    (0, 4, 0): "  Admiral,\nthey're at the Square.",
    (0, 27, 0): "Admiral,\nsupplies will run out\nvery soon.",
    (7, 0, 1): "Admiral! No Marine Captain.\nWe can't control the crew.",
    (7, 10, 0): " Stop!\nYou hit the Admiral.\nIsn't that enough?!",
    (7, 52, 0): "Dizzy...\nI'm starving...\nI can't go on.",
    (7, 52, 2): "%s\ncanceled.",
    (10, 27, 0): "  Use %s?\nNo remodel needed\n%s coins.\nBuy it?",
    (11, 38, 0): " %s crew\njoined.",
    (12, 28, 0): " %s?\nNice name.\nI'm %s.",
    (12, 47, 0): "Some ignore fashion.\nWalking with them\nwould be embarrassing.",
    (13, 9, 0): "  Romance isn't for me.\nCall me childish,\nbut celebrating with\neveryone is more fun.",
    (13, 24, 0): "  Thanks for coming by.\nA drink is free today.\nRelax and enjoy it.",
    (13, 25, 0): " Sailing sounds fun.\nThis job is nice too,\nwith many tales to hear.",
    (14, 36, 0): "%s! You aid the city's defense\nwithout a contract?\nHow generous\nof you.",
    (14, 40, 0): "  Your share reflects the fee.\nHow much will you pay?",
    (18, 80, 0): "Does good food raise\nmorale...?",
    (19, 43, 0): "Measurement, not fighting,\nmatters...",
    (24, 25, 0): "Ah, this feels good. Hot springs\ncure travel fatigue.",
    (31, 10, 0): "A bracelet carved with an angel\nsaid to grant divine aid.",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_entry_offsets() -> dict[tuple[int, int], list[int]]:
    offsets: dict[tuple[int, int], list[int]] = {}
    for path in Path("translations").rglob("*.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        records = payload.get("records") if isinstance(payload, dict) else None
        if not isinstance(records, list):
            continue
        for record in records:
            if not isinstance(record, dict):
                continue
            match = ROW_PATTERN.fullmatch(str(record.get("id", "")))
            starts = record.get("entry_offsets")
            if not starts:
                english = str(record.get("english", ""))
                starts = [0] + [
                    int(value)
                    for value in re.findall(r"\{ALIGN@([0-9]+)\}", english)
                ]
            if not match or not (
                isinstance(starts, list)
                and starts
                and all(isinstance(value, int) for value in starts)
                and starts[0] == 0
                and starts == sorted(set(starts))
            ):
                continue
            key = (int(match.group(1)), int(match.group(2)))
            if len(starts) > len(offsets.get(key, [])):
                offsets[key] = starts
    return offsets


def normalize_segment(segment: bytes) -> tuple[bytes, int]:
    output = bytearray()
    cursor = 0
    added = 0
    removed = 0
    while cursor < len(segment):
        byte = segment[cursor]
        output.append(byte)
        cursor += 1
        if byte != 0x0A:
            continue
        # Spaces immediately before a hard break are invisible and often came
        # from legacy hand-wrapping. Reclaim them before consuming allocation
        # padding or shortening prose.
        while len(output) >= 2 and output[-2] == 0x20:
            del output[-2]
            removed += 1
        guard_start = cursor
        while cursor < len(segment) and segment[cursor] == 0x20:
            cursor += 1
        guard = cursor - guard_start
        if cursor >= len(segment) or not 0x21 <= segment[cursor] <= 0x7E:
            output.extend(segment[guard_start:cursor])
            continue
        wanted = max(guard, 2)
        output.extend(b" " * wanted)
        added += wanted - guard
    output.extend(segment[cursor:])
    delta = added - removed
    if delta <= 0:
        output.extend(b" " * -delta)
        return bytes(output), added
    trailing = len(output) - len(output.rstrip(b" "))
    if trailing < delta:
        raise ValueError(
            f"needs {delta} net guard byte(s), but only {trailing} trailing pad byte(s) remain"
        )
    del output[len(output) - delta :]
    if len(output) != len(segment):
        raise AssertionError("normalization changed segment length")
    return bytes(output), added


def materialize(base_rom: Path, source_rom: Path, clean_rom: Path) -> dict[str, object]:
    candidate_source = NdsImage.open(base_rom).read_file(FILE_PATH)
    release_source = NdsImage.open(source_rom).read_file(FILE_PATH)
    clean_source = NdsImage.open(clean_rom).read_file(FILE_PATH)
    container = IlnkContainer.parse(candidate_source)
    release_container = IlnkContainer.parse(release_source)
    clean_container = IlnkContainer.parse(clean_source)
    known_offsets = load_entry_offsets()
    records: list[dict[str, object]] = []
    failures: list[str] = []
    repaired_lines = 0
    for block_index, block in enumerate(container.blocks):
        clean_records = clean_container.blocks[block_index].split(b"\0")
        for record_index, raw in enumerate(block.split(b"\0")):
            key = (block_index, record_index)
            if (
                not raw
                or key in EXCEPTIONS
                or (
                    record_index < len(clean_records)
                    and raw == clean_records[record_index]
                )
            ):
                continue
            text = raw.decode("cp932", errors="replace")
            if contains_japanese(text) or not any(char.isascii() and char.isalpha() for char in text):
                continue
            starts = known_offsets.get(key, [0])
            if starts[-1] >= len(raw):
                starts = [0]
            rebuilt = bytearray()
            changed = 0
            try:
                for position, start in enumerate(starts):
                    end = starts[position + 1] if position + 1 < len(starts) else len(raw)
                    original_segment = raw[start:end]
                    manual = MANUAL_SEGMENTS.get((block_index, record_index, position))
                    if manual is not None:
                        encoded = manual.encode("ascii")
                        if len(encoded) > len(original_segment):
                            raise ValueError(
                                f"manual rewrite needs {len(encoded)} bytes in a "
                                f"{len(original_segment)}-byte segment"
                            )
                        if re.findall(rb"%[-+0-9.*]*[sd]", encoded) != re.findall(
                            rb"%[-+0-9.*]*[sd]", original_segment
                        ):
                            raise ValueError("manual rewrite changed printf macros")
                        original_segment = encoded.ljust(len(original_segment), b" ")
                    segment, count = normalize_segment(original_segment)
                    rebuilt.extend(segment)
                    changed += count
            except ValueError as error:
                failures.append(
                    f"DK4_MES_B{block_index:02d}_R{record_index:04d}: {error}"
                )
                continue
            if not changed:
                continue
            repaired_lines += changed
            replacement = bytes(rebuilt)
            display_entries = [
                replacement[
                    start : starts[position + 1]
                    if position + 1 < len(starts)
                    else len(replacement)
                ]
                .rstrip(b" \n")
                .decode("ascii")
                for position, start in enumerate(starts)
            ]
            release_records = release_container.blocks[block_index].split(b"\0")
            if (
                record_index >= len(release_records)
                or release_records[record_index] != raw
            ):
                raise ValueError(
                    f"DK4_MES_B{block_index:02d}_R{record_index:04d}: repair "
                    "overlaps an earlier batch in the same release profile"
                )
            records.append(
                {
                    "id": f"DK4_MES_B{block_index:02d}_R{record_index:04d}",
                    "english": replacement.rstrip(b" ").decode("ascii").replace("\n", " / "),
                    "display_entries": display_entries,
                    "replacement_hex": replacement.hex().upper(),
                    "status": "translated",
                    "context": "Existing COMMON translation normalized for the fixed-text renderer.",
                    "notes": "Adds the proven two-byte continuation guard without changing allocation or packed entry offsets.",
                    "structure": "packed-multiple-entry" if len(starts) > 1 else "single-entry",
                    "entry_offsets": starts,
                    "entry_ends": starts[1:] + [len(raw)],
                    "entry_guard_bytes": 0,
                    "linebreak_guard_bytes": 2,
                    "text_box_max_chars": 96,
                    "translated_ranges": [
                        [start, starts[position + 1] if position + 1 < len(starts) else len(raw)]
                        for position, start in enumerate(starts)
                    ],
                }
            )
    if failures:
        raise ValueError("unable to normalize every record:\n" + "\n".join(failures))
    return {
        "format": "dk4-ilnk-translation-batch-v1",
        "content_type": "common-fixed-dialogue-v1",
        "file_path": FILE_PATH,
        "source_file_sha256": sha256(release_source),
        "target_locale": "en-US",
        "scope": "Release-wide repair of legacy COMMON continuation guards",
        "ascii_guard_exemption": "Legacy records use several independently measured entry conventions; screen-entry-layout-v1 enforces the proven two-byte continuation guard while preserving each existing entry start.",
        "fixed_allocation_policy": "screen-entry-layout-v1",
        "records": records,
        "audit": {
            "repaired_record_count": len(records),
            "inserted_guard_byte_count": repaired_lines,
            "renderer_exceptions": [
                "DK4_MES_B14_R0059: Inn renderer preserves one visible indentation byte",
                "DK4_MES_B15_R0063: compact shipyard help renderer consumes no continuation byte",
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=BASE_ROM)
    parser.add_argument("--source", type=Path, default=SOURCE_ROM)
    parser.add_argument("--clean", type=Path, default=CLEAN_ROM)
    parser.add_argument("--out", type=Path, default=OUTPUT)
    args = parser.parse_args()
    batch = materialize(args.base, args.source, args.clean)
    args.out.write_text(
        json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"wrote {args.out}: {batch['audit']['repaired_record_count']} records, "
        f"{batch['audit']['inserted_guard_byte_count']} inserted guard bytes"
    )


if __name__ == "__main__":
    main()
