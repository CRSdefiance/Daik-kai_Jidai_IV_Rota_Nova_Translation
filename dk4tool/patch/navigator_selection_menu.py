"""Canonical-source Sort/Filter strings after the complete V218 stack."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

SOURCE = "a4af5e53f570bdfe76c895fb8704ba0db461851b4935c591daa2ea23647652c1"
CANONICAL = "9a79c25d4a7cf03678a8b5444c3f685a9f675be879109817adb01643141768f5"
SPECS = (("DK4_NAVIGATOR_POPUP_SORT", 0x14F34C, "ソート", "Sort", 8),
         ("DK4_NAVIGATOR_POPUP_FILTER", 0x14F36C, "しぼり込み", "Filter", 12))


def apply_release(source, canonical, config_path):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-navigator-selection-menu-release-v1":
        raise ValueError("Unknown navigator popup release format")
    if sha(source) != SOURCE or sha(canonical) != CANONICAL:
        raise ValueError("Exact complete V218 and canonical ARM9 required")
    manuscript_path = Path(config["manuscript"])
    raw = manuscript_path.read_bytes()
    if sha(raw) != config["manuscript_sha256"]:
        raise ValueError("Navigator popup manuscript hash differs")
    manuscript = json.loads(raw)
    if manuscript["source_file_sha256"] != CANONICAL or len(manuscript["records"]) != 2:
        raise ValueError("Canonical two-record source review required")
    rebuilt = bytearray(source)
    changed = []
    for record, (key, offset, japanese, english, size) in zip(manuscript["records"], SPECS, strict=True):
        expected = japanese.encode("cp932").ljust(size, b"\0")
        if (record["id"] != key or record["offset"] != offset
                or record["source_japanese"] != japanese or record["english"] != english
                or bytes.fromhex(record["source_hex"]) != expected
                or canonical[offset:offset + size] != expected
                or source[offset:offset + size] != expected):
            raise ValueError("Navigator popup source/slot/localization lock differs")
        if not all(record["review"][gate] for gate in ("source", "context", "localization", "naturalness", "formatting")):
            raise ValueError("Navigator popup editorial review incomplete")
        replacement = english.encode("ascii") + b"\0"
        if len(replacement) > size:
            raise ValueError("Navigator popup text exceeds its original slot")
        rebuilt[offset:offset + size] = replacement.ljust(size, b"\0")
        changed.append(key)
    result = bytes(rebuilt)
    if sha(result) != config["target_arm9_sha256"]:
        raise ValueError("Navigator popup target hash differs")
    return result, {"changed_records": changed, "source_arm9_sha256": SOURCE,
                    "target_arm9_sha256": sha(result), "canonical_arm9_sha256": CANONICAL,
                    "manuscript": str(manuscript_path), "manuscript_sha256": sha(raw),
                    "original_slots_only": [[o, n] for _, o, _, _, n in SPECS],
                    "all_other_bytes_preserved": True, "runtime_code_and_pointer_tables_unchanged": True}
