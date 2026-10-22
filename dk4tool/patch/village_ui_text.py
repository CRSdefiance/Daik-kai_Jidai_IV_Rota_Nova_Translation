"""Source-owned village descriptor/menu labels; preserve all action IDs and code."""

import bisect
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

SOURCE = "c99b2a5ab97ef4a973c648d4b5a3f0faf8109d041e03e2ed81c813d0d4c09605"
SC2_SOURCE = "bb5705149b827d0926e6d5e020dbe6d160aad7ef23372e9497c8617a7d86bb30"


def transform(arm, route, manuscript):
    assert sha(arm) == SOURCE and sha(route) == SC2_SOURCE
    validate_natural_dialogue_batch(manuscript)
    clean_rom = NdsImage.open("work/clean.nds")
    canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    clean, baked = [r.read_file("/__arm9__.bin") for r in (clean_rom, canonical)]
    labels = [r for r in manuscript["records"] if r["kind"] in ("name", "menu")]
    assert len(labels) == 30 and len(manuscript["records"]) == 33
    code = MainCodeFile(arm, BASE)
    before = [bytes(s.data) for s in code.sections]
    ranges = sorted((r["source_pointer"], len(bytes.fromhex(r["source_hex"])), r["pointer_field"])
                    for r in labels)
    starts = [r[0] for r in ranges]
    units = [(s.ramAddress, bytes(s.data)) for s in code.sections]
    units += [(o.ramAddress, bytes(o.data)) for o in loadOverlayTable(
        clean_rom.rom.arm9OverlayTable, lambda _, f: clean_rom.rom.files[f]).values()]
    references = []
    for base, data in units:
        for off in range(len(data) - 3):
            pointer = struct.unpack_from("<I", data, off)[0]
            index = bisect.bisect_right(starts, pointer) - 1
            if index >= 0 and pointer < ranges[index][0] + ranges[index][1]:
                references.append((base + off, pointer))
    assert sorted(references) == sorted((BASE + r[2], r[0]) for r in ranges)
    plan = cache_plan(arm)
    assert plan and len(before) == 5 and code.sections[3].ramAddress == STAGE
    payload = bytearray(before[3][:-112])
    preserved = len(payload)
    changed, placements = [], []
    for row in labels:
        field, original = row["pointer_field"], row["source_pointer"]
        assert all(struct.unpack_from("<I", a, field)[0] == original for a in (arm, clean, baked))
        source_text = bytes.fromhex(row["source_hex"])
        start = original - BASE
        assert all(a[start:start + len(source_text)] == source_text for a in (arm, clean, baked))
        assert row["english"].isascii() and 0 < len(row["english"]) <= 15
        payload.extend(bytes((-len(payload)) % 4))
        target = POOL + len(payload)
        payload.extend(row["english"].encode("ascii") + b"\0")
        struct.pack_into("<I", code.sections[0].data, field, target)
        placements.append({"id": row["id"], "kind": row["kind"], "index": row["index"],
                           "pointer_field": field, "source_pointer": original, "target_pointer": target,
                           "Japanese": row["Japanese"], "English": row["english"]})
        changed.append(row["id"])
    payload.extend(bytes((-len(payload)) % 32))
    size = len(payload) + 64
    assert POOL + size < STAGE and STAGE + size + 48 < 0x023F4000
    entry, copy = STAGE + len(payload), STAGE + size
    payload.extend(wrapper(entry, copy, size, arm))
    code.sections[3].data = payload + before[3][-48:-4] + struct.pack("<I", size)
    struct.pack_into("<I", code.sections[0].data, 0x8E4, branch_link(BASE + 0x8E4, entry))
    struct.pack_into("<I", code.sections[0].data, 0xE45DC, POOL + size)
    target_arm = bytes(code.save())
    after = MainCodeFile(target_arm, BASE)
    assert cache_plan(target_arm)["payload_bytes"] == size
    assert all(bytes(after.sections[i].data) == before[i] for i in (1, 2, 4))
    assert bytes(after.sections[3].data[:preserved]) == before[3][:preserved]
    restored = bytearray(after.sections[0].data)
    fields = [r["pointer_field"] for r in labels] + [0x8E4, 0xE45DC]
    for field in fields:
        restored[field:field + 4] = before[0][field:field + 4]
    settings = code.codeSettingsOffs
    restored[settings:settings + 12] = before[0][settings:settings + 12]
    assert bytes(restored) == before[0]
    container = IlnkContainer.parse(route)
    assert container.to_bytes() == route
    clean_blocks, baked_blocks = [IlnkContainer.parse(r.read_file("/data/SC2.DK4")).blocks
                                  for r in (clean_rom, canonical)]
    block_before = list(container.blocks)
    name_corrections = []
    for row in manuscript["records"]:
        if row["kind"] != "route-name":
            continue
        number, index = row["block"], row["record"]
        parts = container.blocks[number].split(b"\0")
        source = clean_blocks[number].split(b"\0")[index]
        assert source.hex() == row["source_hex"]
        assert baked_blocks[number].split(b"\0")[index].hex() == row["canonical_hex"]
        assert parts[index].hex() == row["current_hex"] and parts[index].count(b"Lebaque") == 1
        offset = sum(len(p) + 1 for p in parts[:index]) + parts[index].index(b"Lebaque")
        before_row = parts[index]
        parts[index] = before_row.replace(b"Lebaque", b"Leveque")
        assert len(parts[index]) == len(before_row) and parts[index][0] == source[0] == before_row[0]
        assert len(b"Leveque") == len(b"Lebaque") == 7
        updated = b"\0".join(parts)
        previous = container.blocks[number]
        assert previous[:offset] == updated[:offset] and previous[offset + 7:] == updated[offset + 7:]
        container.blocks[number] = updated
        name_corrections.append({"id": row["id"], "block": number, "record": index,
                                 "name_offset": offset, "name_bytes": 7,
                                 "all_preamble_controls_other_prose_and_byte_parity_preserved": True})
        changed.append(row["id"])
    assert len(name_corrections) == 3
    for index, (old, new) in enumerate(zip(block_before, container.blocks, strict=True)):
        assert len(old) == len(new)
        if index not in (247, 248):
            assert old == new
    target_route = container.to_bytes()
    assert len(target_route) == len(route) and b"Lebaque" not in target_route
    return target_arm, target_route, {"source_arm9_sha256": SOURCE, "target_arm9_sha256": sha(target_arm),
        "source_SC2_sha256": SC2_SOURCE, "target_SC2_sha256": sha(target_route), "changed_records": changed,
        "placements": placements, "all_byte_position_pointer_references": references,
        "all30_source_strings_and_descriptor_action_IDs_geometry_callbacks_preserved": True,
        "all_native_font_rendering_input_and_resource_code_preserved": True,
        "source_pool_prefix_bytes_preserved": preserved, "pool_growth": size - plan["payload_bytes"],
        "same_width_name_corrections": name_corrections, "source_SC2_block_count": len(block_before),
        "no_other_route_bytes_or_record_lengths_changed": True,
        "status": "experimental", "full_goal_complete": False}


def apply_release(arm, route, path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    assert config["format"] == "dk4-village-ui-text-v1"
    assert config["source_arm9_sha256"] == sha(arm) and config["source_SC2_sha256"] == sha(route)
    manuscript = Path(config["manuscript"])
    assert config["manuscript_sha256"] == sha(manuscript.read_bytes())
    target_arm, target_route, report = transform(arm, route, json.loads(manuscript.read_text(encoding="utf-8")))
    assert config["target_arm9_sha256"] == sha(target_arm) and config["target_SC2_sha256"] == sha(target_route)
    return target_arm, target_route, report
