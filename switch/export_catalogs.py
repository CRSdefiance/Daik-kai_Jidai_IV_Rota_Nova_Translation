"""Export the English records and their native identities from a verified overlay."""

from __future__ import annotations

import argparse
from bisect import bisect_right
import json
from pathlib import Path
import re
from struct import unpack_from

from .check_layout import ENGINE_SHA256
from .inspect_script import inspect_block, read_bank
from .overlay import verify


MESSAGE_POINTERS = 0x414144
MESSAGE_GROUPS = 0x40DE78
GROUP_COUNT = 53
MESSAGE_COUNT = 4164
JAPANESE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
NATIVE_SECTIONS = (
    "golden_route", "golden_route_guild", "old_maps_and_notices", "native_menus",
    "native_country_wording", "native_ui_labels", "native_ui_literals", "native_data_wording",
    "generated_names", "native_composed_text", "price_report_labels", "protected_stat_names",
)


def apply_literal_ips(image: bytes, patch: bytes) -> bytes:
    if not patch.startswith(b"PATCH") or not patch.endswith(b"EOF"):
        raise ValueError("Expected the Switch release's literal IPS format")
    image = bytearray(image)
    cursor, limit, previous_end = 5, len(patch) - 3, 0
    while cursor < limit:
        if cursor + 5 > limit:
            raise ValueError("Truncated IPS record header")
        offset = int.from_bytes(patch[cursor:cursor + 3], "big")
        length = int.from_bytes(patch[cursor + 3:cursor + 5], "big")
        cursor += 5
        end = offset + length
        if length == 0 or offset < previous_end or end > len(image) or cursor + length > limit:
            raise ValueError("Invalid literal IPS record")
        image[offset:end] = patch[cursor:cursor + length]
        cursor += length
        previous_end = end
    return bytes(image)


def scenario_records(archive: bytes):
    for block in read_bank(archive):
        for record in inspect_block(block, complete_styles=True)["records"]:
            kind = record["kind"]
            base = {"block": block.index, "offset": record["offset"], "kind": kind}
            if kind == "speech":
                yield {**base, "turn": record["turn"], "text": record["text"]}
            elif kind == "choice":
                for slot, label in enumerate(record["labels"]):
                    yield {**base, "slot": slot, "text": label["text"]}
            elif kind == "style_alternatives":
                for alternative in record["alternatives"]:
                    yield {**base, "style_slots": alternative["style_slots"], "text": alternative["text"]}


def shared_records(archive: bytes, engine: bytes):
    blocks = read_bank(archive)
    groups = [unpack_from("<H", engine, MESSAGE_GROUPS + index * 4)[0]
              for index in range(GROUP_COUNT)]
    for index in range(MESSAGE_COUNT):
        group = bisect_right(groups, index) - 1
        pointer, = unpack_from("<H", engine, MESSAGE_POINTERS + index * 2)
        page = blocks[group * 4 + (pointer >> 12)].data
        offset = pointer & 0xfff
        end = page.index(b"\0", offset)
        yield {"id": f"{group:02d}:{index - groups[group]:03d}",
               "text": page[offset:end].decode("cp932")}


def write_catalog(out: Path, records) -> int:
    rows = list(records)
    if not rows or any(JAPANESE.search(row["text"]) for row in rows):
        raise ValueError(f"Expected a nonempty English catalog: {out.name}")
    contents = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    out.write_text(contents, encoding="utf-8", newline="\n")
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--engine", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = json.loads(args.inventory.read_text(encoding="utf-8"))
    verify(args.engine, ENGINE_SHA256, "original v1.0.2 uncompressed main executable")
    engine = args.engine.read_bytes()
    for name, sha in report["mod_files"].items():
        verify(args.overlay / name, sha, f"verified overlay {name}")
    ips_name, = (name for name in report["mod_files"] if name.startswith("exefs/"))
    engine = apply_literal_ips(engine, (args.overlay / ips_name).read_bytes())
    args.output.mkdir(parents=True, exist_ok=True)
    root = args.overlay / "romfs" / "JP"
    count = 0
    for chapter in range(7):
        count += write_catalog(
            args.output / f"sc{chapter}.jsonl",
            scenario_records((root / f"Sc{chapter}.dk4").read_bytes()),
        )
    shared = write_catalog(
        args.output / "shared.jsonl", shared_records((root / "mesfile.dk4").read_bytes(), engine),
    )
    native = [
        {"section": section, "offset": row.get("offset"), "text": row["english"]}
        for section in NATIVE_SECTIONS
        for row in report.get(section, ())
        if "english" in row
    ]
    writ = write_catalog(args.output / "native.jsonl", native)
    print(f"Exported {count} campaign records, {shared} shared messages, and {writ} native labels.")


if __name__ == "__main__":
    main()
