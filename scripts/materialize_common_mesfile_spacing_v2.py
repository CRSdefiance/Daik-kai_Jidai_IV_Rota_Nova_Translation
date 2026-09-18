from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage


BASE_ROM = Path("out/raphael_deep_route_v93_candidate.nds")
SOURCE_ROM = Path("out/raphael_natural_v2_accepted_base.nds")
COMPONENT_BATCHES = (
    Path("translations/common_shipyard_layout_v2.json"),
    Path("translations/guild_item_descriptions_layout_v3.json"),
    Path("translations/common_mystery_items_v1.json"),
    Path("translations/common_runtime_layout_v4.json"),
    Path("translations/common_global_layout_v1.json"),
)
OUTPUT = Path("translations/common_mesfile_spacing_v2.json")
FILE_PATH = "/COMMON/MESFILE.DK4"
ROW_PATTERN = re.compile(r"DK4_MES_B([0-9]+)_R([0-9]+)")

# Translated COMMON prose is rendered by a native wrapping text box. Stored
# line breaks caused both the visible staircase indentation and the progressive
# ASCII-pair overwrite seen in cold-boot screenshots. Let the native wrapper
# choose rows in every audited COMMON block; independently addressed entries
# remain separated by their fixed byte boundaries, not by stored newlines.
AUTO_WRAP_BLOCKS = set(range(41))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def collapse_stored_breaks(segment: bytes) -> bytes:
    """Replace stored prose breaks and their visible guards with one space."""

    visible = segment.rstrip(b" ")
    padding = len(segment) - len(visible)
    visible = re.sub(rb"[ ]*\n[ ]*", b" ", visible)
    visible = re.sub(rb" {2,}", b" ", visible)
    if len(visible) > len(segment):
        raise ValueError("auto-wrap normalization overflowed a fixed segment")
    return visible.ljust(len(segment), b" ")


def pair_safe_breaks(segment: bytes) -> bytes:
    """Reduce continuation indentation to one cell and preserve ASCII phase."""

    source = segment.rstrip(b" ")
    lines = source.split(b"\n")
    if len(lines) == 1:
        return segment
    output = bytearray()
    ascii_phase = 0
    for index, raw_line in enumerate(lines):
        line = raw_line if index == 0 else raw_line.lstrip(b" ")
        if index:
            # A blank stored row is retained, but it has no printable guard.
            if line:
                if not ascii_phase:
                    output.append(0x20)
                    ascii_phase ^= 1
                output.append(0x0A)
                output.append(0x20)
                ascii_phase ^= 1
            elif index < len(lines) - 1:
                output.append(0x0A)
                output.append(0x20)
                ascii_phase ^= 1
        output.extend(line)
        ascii_phase ^= sum(0x20 <= byte < 0x80 for byte in line) & 1
    if len(output) > len(segment):
        raise ValueError("pair-safe normalization overflowed a fixed segment")
    return bytes(output).ljust(len(segment), b" ")


def fit(text: str, size: int, *, leading: int = 0) -> bytes:
    encoded = (b" " * leading) + text.encode("ascii")
    if len(encoded) > size:
        raise ValueError(f"{text!r} needs {len(encoded)} bytes in {size}")
    return encoded.ljust(size, b" ")


def targeted_replacements(
    source: IlnkContainer,
) -> dict[tuple[int, int], tuple[bytes, list[int], list[int]]]:
    """Cold-boot-derived packed-entry repairs for reported town failures."""

    result: dict[tuple[int, int], tuple[bytes, list[int], list[int]]] = {}

    # The port-resupply formatter consumes two leading bytes before drawing.
    # Preserve the two-byte native entry guard instead of treating it as
    # visible indentation; one guard byte produced the observed "esupply".
    result[(0, 34)] = (
        fit("Resupply? %s coins.", 27, leading=2),
        [0],
        [27],
    )

    # The departure warning's second native entry begins at byte 21.  The old
    # English moved it to byte 16, so the caller landed on "ilors".
    result[(0, 53)] = (
        fit("Dock at %s?", 21, leading=1)
        + fit("Sailors are unassigned. Continue?", 41),
        [0, 21],
        [21, 62],
    )

    # Acquisition and recruitment are separate entries at 0 and 20. Keep the
    # verified two-byte renderer guard, but use a short suffix so even the
    # longest composed crew name remains on one line. Reserved leading F bytes
    # in the expanded names are repaired in the ARM9 entity-name pool.
    result[(4, 59)] = (
        fit("%s acquired!", 20)
        + fit("%s joined!", 23, leading=2),
        [0, 20],
        [20, 43],
    )

    # This ordinary dialogue box displays leading spaces literally.  Remove
    # the old generic two-byte guard and fit the complete prompt on one line.
    result[(10, 37)] = (
        fit("Change supply ratio?", 37),
        [0],
        [37],
    )

    # Cargo Setup R36 is three independent messages.  The early placeholder
    # pass filled only the first 65-byte entry and blanked the native entries
    # at 65 and 93, producing an empty Port Worker box when no cargo existed.
    result[(10, 36)] = (
        fit("Your sailors look tired. Rest at the inn?", 65, leading=1)
        + fit("You have no cargo.", 28)
        + fit("Not enough coins to fully resupply. Buy what you can?", 59),
        [0, 65, 93],
        [65, 93, 152],
    )

    # Tavern rumor R20 contains two independently addressed messages.  The
    # legacy placeholder erased the second one, producing the empty Patron box.
    result[(11, 20)] = (
        fit("%s's fleet is hunting %s.", 44)
        + fit("Word is, %s's fleet is heading to %s.", 53),
        [0, 44],
        [44, 97],
    )
    result[(11, 11)] = (fit("Barkeep, drinks for everyone.", 33), [0], [33])
    result[(11, 21)] = (
        fit("Word is, %s's fleet is heading to %s.", 61, leading=2),
        [0],
        [61],
    )

    result[(14, 36)] = (
        fit("%s! You aid the city's defense without a contract? How generous of you.", 79),
        [0],
        [79],
    )
    result[(14, 38)] = (
        fit("A Market recommendation? Let me see it.", 56)
        + fit("%s! Will you aid the city's defense?", 45),
        [0, 56],
        [56, 101],
    )

    # Restore the proven unwrapped item text.  The native wrapper displayed
    # these cleanly; the later explicit breaks caused rafted/nown/ap fragments.
    item_v2 = json.loads(
        Path("translations/guild_amsterdam_item_descriptions_v2.json").read_text(
            encoding="utf-8"
        )
    )
    for record in item_v2["records"]:
        match = ROW_PATTERN.fullmatch(record["id"])
        assert match is not None
        key = (int(match.group(1)), int(match.group(2)))
        replacement = bytes.fromhex(record["replacement_hex"])
        current = source.blocks[key[0]].split(b"\0")[key[1]]
        if len(replacement) != len(current):
            raise ValueError(f"{record['id']}: item repair changed allocation")
        if key == (32, 12):
            starts = [89]
            ends = [181]
        elif key == (32, 13):
            starts = [77]
            ends = [177]
        else:
            starts = [0]
            ends = [79]
        result[key] = (replacement, starts, ends)
    return result


def materialize(base_rom: Path, source_rom: Path) -> dict[str, object]:
    common = NdsImage.open(base_rom).read_file(FILE_PATH)
    source_common = NdsImage.open(source_rom).read_file(FILE_PATH)
    container = IlnkContainer.parse(common)
    source_container = IlnkContainer.parse(source_common)
    layout_records: dict[str, dict[str, object]] = {}
    for path in COMPONENT_BATCHES:
        component = json.loads(path.read_text(encoding="utf-8"))
        for record in component["records"]:
            row_id = str(record["id"])
            if row_id in layout_records:
                raise ValueError(f"component batches overlap at {row_id}")
            layout_records[row_id] = record
    replacements: dict[tuple[int, int], tuple[bytes, list[int], list[int]]] = {}

    for row_id, record in layout_records.items():
        match = ROW_PATTERN.fullmatch(row_id)
        if match is None:
            continue
        block_index = int(match.group(1))
        record_index = int(match.group(2))
        current = container.blocks[block_index].split(b"\0")[record_index]
        ranges = [tuple(pair) for pair in record.get("translated_ranges", [])]
        if not ranges:
            continue
        rebuilt = bytearray(current)
        for start, end in ranges:
            segment = current[start:end]
            normalizer = (
                collapse_stored_breaks
                if block_index in AUTO_WRAP_BLOCKS
                else pair_safe_breaks
            )
            rebuilt[start:end] = normalizer(segment)
        replacement = bytes(rebuilt)
        replacements[(block_index, record_index)] = (
            replacement,
            list(record.get("entry_offsets", [0])),
            list(record.get("entry_ends", [len(current)])),
        )

    for key, (replacement, starts, ends) in targeted_replacements(container).items():
        current = container.blocks[key[0]].split(b"\0")[key[1]]
        if len(replacement) != len(current):
            raise ValueError(f"B{key[0]:02d} R{key[1]:04d}: allocation changed")
        replacements[key] = (replacement, starts, ends)

    records: list[dict[str, object]] = []
    for (block_index, record_index), (replacement, starts, ends) in sorted(
        replacements.items()
    ):
        current = container.blocks[block_index].split(b"\0")[record_index]
        accepted = source_container.blocks[block_index].split(b"\0")[record_index]
        if replacement == accepted:
            continue
        if current.count(b"%s") != replacement.count(b"%s"):
            # Targeted packed repairs intentionally restore macros lost by an
            # older placeholder layer; every other spacing-only edit must be
            # macro-neutral.
            if (block_index, record_index) not in {(0, 53), (11, 20)}:
                raise ValueError(
                    f"B{block_index:02d} R{record_index:04d}: macro count changed"
                )
        records.append(
            {
                "id": f"DK4_MES_B{block_index:02d}_R{record_index:04d}",
                "english": replacement.rstrip(b" ").decode("cp932", errors="replace"),
                "display_entries": [
                    replacement[start:end]
                    .rstrip(b" ")
                    .decode("cp932", errors="replace")
                    for start, end in zip(starts, ends)
                ],
                "replacement_hex": replacement.hex().upper(),
                "entry_offsets": starts,
                "entry_ends": ends,
                "entry_guard_bytes": 0,
                "linebreak_guard_bytes": 1,
                "translated_ranges": [[start, end] for start, end in zip(starts, ends)],
                "text_box_max_chars": 255 if block_index in AUTO_WRAP_BLOCKS else 40,
                "context": "Global COMMON spacing and packed-entry repair.",
                "notes": (
                    "Prose uses native automatic wrapping; retained structured breaks "
                    "use one continuation guard with progressive ASCII pair phase."
                ),
            }
        )

    return {
        "format": "dk4-ilnk-translation-batch-v1",
        "content_type": "common-fixed-dialogue-v2",
        "file_path": FILE_PATH,
        "source_file_sha256": sha256(source_common),
        "target_locale": "en-US",
        "scope": "Whole-MESFILE spacing normalization and runtime-proven town entry repairs",
        "ascii_guard_exemption": (
            "This source-locked repair preserves every fixed allocation and declared "
            "entry boundary while replacing unsafe stored prose breaks with native wrapping."
        ),
        "fixed_allocation_policy": "screen-entry-layout-v1",
        "records": records,
        "audit": {
            "record_count": len(records),
            "auto_wrap_blocks": sorted(AUTO_WRAP_BLOCKS),
            "targeted_runtime_repairs": [
                "DK4_MES_B00_R0053",
                "DK4_MES_B00_R0034",
                "DK4_MES_B04_R0059",
                "DK4_MES_B10_R0037",
                "DK4_MES_B10_R0036",
                "DK4_MES_B11_R0011",
                "DK4_MES_B11_R0020",
                "DK4_MES_B11_R0021",
                "DK4_MES_B14_R0036",
                "DK4_MES_B14_R0038",
                "DK4_MES_B32_R0012",
                "DK4_MES_B32_R0013",
                "DK4_MES_B32_R0019",
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=BASE_ROM)
    parser.add_argument("--source", type=Path, default=SOURCE_ROM)
    parser.add_argument("--out", type=Path, default=OUTPUT)
    args = parser.parse_args()
    payload = materialize(args.base, args.source)
    args.out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {args.out}: {len(payload['records'])} records")


if __name__ == "__main__":
    main()
