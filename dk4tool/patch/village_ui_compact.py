"""Pack the complete English village UI in its exclusively owned source text pool."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.patch.village_ui_text import transform as original_transform
from dk4tool.rom.nds import NdsImage


def transform(arm, route, manuscript):
    _, target_route, inherited = original_transform(arm, route, manuscript)
    code = MainCodeFile(arm, BASE)
    before = [bytes(s.data) for s in code.sections]
    labels = [r for r in manuscript["records"] if r["kind"] in ("name", "menu")]
    names = [r for r in labels if r["kind"] == "name"]
    start = min(r["source_pointer"] - BASE for r in names)
    end = (max(r["source_pointer"] - BASE + len(bytes.fromhex(r["source_hex"])) for r in names) + 3) & ~3
    assert (start, end) == (0x15ADF8, 0x15AF1C)
    owned = set()
    for row in names:
        at = row["source_pointer"] - BASE
        owned.update(range(at, at + len(bytes.fromhex(row["source_hex"]))))
    bins = [(0x15ADF8, 0x15AE84), (0x15AE90, 0x15AECC), (0x15AED8, 0x15AF1C)]
    assert all(at in owned or arm[at] == 0 for lo, hi in bins for at in range(lo, hi))
    original = NdsImage.open("work/clean.nds")
    units = [(s.ramAddress, bytes(s.data)) for s in code.sections]
    units += [(o.ramAddress, bytes(o.data)) for o in loadOverlayTable(
        original.rom.arm9OverlayTable, lambda _, f: original.rom.files[f]).values()]
    pool_references = [(base + at, pointer) for base, data in units for at in range(len(data) - 3)
                       if any(BASE + lo <= (pointer := struct.unpack_from("<I", data, at)[0]) < BASE + hi
                              for lo, hi in bins)]
    assert sorted(pool_references) == sorted((BASE + r["pointer_field"], r["source_pointer"]) for r in names)
    # The source text spans have precisely these 24 name owners. Preserve the
    # two interleaved RTTI records rather than treating them as spare storage.
    for address, pointer in inherited["all_byte_position_pointer_references"]:
        if BASE + start <= pointer < BASE + end:
            assert address in {BASE + r["pointer_field"] for r in names}
    existing_title = struct.unpack_from("<I", arm, 0xAEA3C)[0]
    title_text = b"Promised Words\0"
    assert before[3][existing_title - POOL:existing_title - POOL + len(title_text)] == title_text
    existing_hekla = struct.unpack_from("<I", arm, 0x1192A8 + 8 * 4)[0]
    assert before[3][existing_hekla - POOL:existing_hekla - POOL + 6] == b"Hekla\0"
    packed_rows = [r for r in labels if not (r["kind"] == "name" and r["index"] == 8)
                   and not (r["kind"] == "menu" and r["index"] in (1, 5))]
    available = [hi - lo for lo, hi in bins]
    buffers = [bytearray(hi - lo) for lo, hi in bins]
    pointers = {}
    # Largest-first best fit retains four-byte alignment without touching the
    # interleaved CVillage RTTI name or its three-word type-info record.
    for row in sorted(packed_rows, key=lambda r: (-((len(r["english"]) + 4) // 4), r["id"])):
        text = row["english"].encode("ascii") + b"\0"
        length = (len(text) + 3) & ~3
        fits = [i for i, value in enumerate(available) if value >= length]
        assert fits, (row["id"], available, length)
        index = min(fits, key=lambda i: (available[i], i))
        offset = len(buffers[index]) - available[index]
        pointers[row["id"]] = BASE + bins[index][0] + offset
        buffers[index][offset:offset + length] = text.ljust(length, b"\0")
        available[index] -= length
    assert available == [0, 0, 0]
    placements = []
    for row in labels:
        if row["kind"] == "menu" and row["index"] == 5:
            target = existing_title
        elif row["kind"] == "name" and row["index"] == 8:
            target = existing_hekla
        elif row["kind"] == "menu" and row["index"] == 1:
            target = row["source_pointer"]
            text = b"Stay\0"
            assert len(text) == len(bytes.fromhex(row["source_hex"]))
            code.sections[0].data[target - BASE:target - BASE + len(text)] = text
        else:
            target = pointers[row["id"]]
        struct.pack_into("<I", code.sections[0].data, row["pointer_field"], target)
        placements.append({"id": row["id"], "kind": row["kind"], "index": row["index"],
            "pointer_field": row["pointer_field"], "source_pointer": row["source_pointer"],
            "target_pointer": target, "Japanese": row["Japanese"], "English": row["english"]})
    for (lo, hi), buffer in zip(bins, buffers, strict=True):
        code.sections[0].data[lo:hi] = buffer
    used = sum(len(b) for b in buffers)
    target = bytes(code.save())
    after = MainCodeFile(target, BASE)
    assert len(target) == len(arm)
    assert all(bytes(after.sections[i].data) == before[i] for i in (1, 2, 3, 4))
    restored = bytearray(after.sections[0].data)
    for lo, hi in bins:
        restored[lo:hi] = before[0][lo:hi]
    restored[0x1478E8:0x1478ED] = before[0][0x1478E8:0x1478ED]
    for row in labels:
        field = row["pointer_field"]
        restored[field:field + 4] = before[0][field:field + 4]
    assert bytes(restored) == before[0]
    inherited.update({"target_arm9_sha256": sha(target), "placements": placements,
        "layout": "exclusive-original-village-name-pool", "pool_growth": 0,
        "all_staged_pool_cache_startup_arena_autoload_bytes_exact_V608": True,
        "source_name_pool": [start, end], "source_name_pool_bins": bins, "source_name_pool_bytes": used,
        "whole_bins_including_zero_padding_all_byte_references": pool_references,
        "interleaved_RTTI_metadata_preserved": [[0x15AE84, 0x15AE90], [0x15AECC, 0x15AED8]],
        "new_packed_UI_bytes": used, "existing_Promised_Words_title_reused": existing_title,
        "existing_Hekla_answer_reused": existing_hekla,
        "original_Japanese_name_strings_replaced_only_in_exclusively_owned_pool": True,
        "Stay_only_menu_source_text_changed_in_owned_five_byte_slot": True,
        "source_pool_prefix_bytes_preserved": len(before[3]),
        "all30_descriptor_action_IDs_geometry_callbacks_preserved": True,
        "V609_failure_cause_not_inferred_from_compact_layout_result": True})
    inherited.pop("all30_source_strings_and_descriptor_action_IDs_geometry_callbacks_preserved")
    return target, target_route, inherited


def apply_release(arm, route, path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    assert config["format"] == "dk4-village-ui-text-v2"
    assert config["source_arm9_sha256"] == sha(arm) and config["source_SC2_sha256"] == sha(route)
    manuscript = Path(config["manuscript"])
    assert config["manuscript_sha256"] == sha(manuscript.read_bytes())
    target, target_route, report = transform(arm, route, json.loads(manuscript.read_text(encoding="utf-8")))
    assert config["target_arm9_sha256"] == sha(target) and config["target_SC2_sha256"] == sha(target_route)
    return target, target_route, report
