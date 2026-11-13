"""Distinguish gun batteries from individual cannon counts in ship and Deck UI."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ship_quarters_label import render_label

ARM = "/__arm9__.bin"
FILE = "/_pxl/shipinfo.pxl"
FACE = (132, 104, 196, 120)
SLOTS = ((0x12FFFC, "海兵詰所", "Marines", "Quarters"),
         (0x130008, "武装砲台", "Gun Deck", "Battery"))


def render(candidate, clean):
    image, image_report = render_label(candidate, clean, FACE, "Guns", "Batteries", "武装砲台",
                                       "DK4_SHIPS_GUN_BATTERY_COUNT")
    original, source = clean.read_file(ARM), candidate.read_file(ARM)
    target = bytearray(source)
    rows = []
    for offset, jp, old, new in SLOTS:
        if original[offset:offset + 12] != (jp.encode("cp932") + b"\0").ljust(12, b"\0"):
            raise ValueError("Original Deck room source differs")
        before, after = (text.encode("ascii").ljust(12, b"\0") for text in (old, new))
        if source[offset:offset + 12] != before:
            raise ValueError("Inherited Deck room label differs")
        target[offset:offset + 12] = after
        rows.append({"address": 0x02000000 + offset, "file_offset": offset,
                     "source_Japanese": jp, "old_English": old, "English": new,
                     "before_hex": before.hex(), "after_hex": after.hex(), "slot_bytes": 12})
    allowed = {n for offset, _, _, _ in SLOTS for n in range(offset, offset + 12)}
    if any(a != b for n, (a, b) in enumerate(zip(source, target, strict=True)) if n not in allowed):
        raise ValueError("Unowned ARM9 byte changed")
    return {FILE: image, ARM: bytes(target)}, {"image": image_report, "room_slots": rows,
                                             "source_arm9_sha256": sha(source), "target_arm9_sha256": sha(target),
                                             "all_code_fonts_pointers_and_section_extents_exact": True}


def apply_release(candidate, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-ship-battery-labels-v1":
        raise ValueError("Unknown ship battery labels format")
    for path, digest in config["source_sha256"].items():
        if sha(candidate.read_file(path)) != digest:
            raise ValueError("Battery label inherited file differs: " + path)
    for path, digest in config["clean_sha256"].items():
        if sha(clean.read_file(path)) != digest:
            raise ValueError("Battery label clean file differs: " + path)
    outputs, report = render(candidate, clean)
    if {path: sha(data) for path, data in outputs.items()} != config["target_sha256"]:
        raise ValueError("Reviewed battery label target differs")
    reports = {FILE: report["image"] | {"changed_records": ["DK4_SHIPS_GUN_BATTERY_COUNT"]},
               ARM: {"source_sha256": report["source_arm9_sha256"], "target_sha256": report["target_arm9_sha256"],
                     "room_slots": report["room_slots"], "all_code_fonts_pointers_and_section_extents_exact": True,
                     "changed_records": ["DK4_DECK_MARINE_QUARTERS_TERM", "DK4_DECK_GUN_BATTERY_TERM"]}}
    return outputs, reports
