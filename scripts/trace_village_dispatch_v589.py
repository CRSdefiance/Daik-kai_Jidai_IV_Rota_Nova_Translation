"""Extend village-card source census and exhaust the original operand decoder.

Byte candidates are not decoded instructions. Supplied operands are not normal
event triggers, and negative direct-reference results are not global non-use.
"""

import hashlib
import json
import struct
from collections import Counter
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs
from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, machine
from scripts.trace_frame_crop_arguments_v584 import branch
from scripts.verify_event_still_routing_v426 import CARDS

ROOT = Path("work/analysis/village_dispatch_v589")
ROM = Path("out/all_routes_combined_v581_candidate.nds")
OWNER, STREAM, RESULT, LENGTH = 0x02460000, 0x02461000, 0x02462000, 0x02462020
TARGETS = (0x02028B74, 0x02028AA8, 0x02028BAC)


def census(rom, arm):
    units = [(f"main{i}", s.ramAddress, bytes(s.data))
             for i, s in enumerate(MainCodeFile(arm, BASE).sections)]
    units += [(f"overlay{i}", o.ramAddress, bytes(o.data)) for i, o in loadOverlayTable(
        rom.rom.arm9OverlayTable, lambda _id, file_id: rom.rom.files[file_id]).items()]
    results = {target: {"ARM_B_BL": [], "Thumb_BL_BLX": [], "stored_pointers": []} for target in TARGETS}
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    for name, base, data in units:
        for at in range(0, len(data) - 3, 4):
            word = struct.unpack_from("<I", data, at)[0]
            target = branch(word, base + at)
            if target in results:
                results[target]["ARM_B_BL"].append({"unit": name, "address": base + at,
                                                   "link": bool(word & 0x01000000), "condition": word >> 28})
        for at in range(len(data) - 3):
            value = struct.unpack_from("<I", data, at)[0]
            if value & ~1 in results:
                results[value & ~1]["stored_pointers"].append({"unit": name, "address": base + at, "value": value})
        for at in range(0, len(data) - 3, 2):
            first, second = struct.unpack_from("<2H", data, at)
            if first & 0xF800 != 0xF000 or second & 0xF800 not in (0xE800, 0xF800):
                continue
            for ins in decoder.disasm(data[at:at + 4], base + at, count=1):
                if ins.mnemonic not in ("bl", "blx") or not ins.op_str.startswith("#0x"):
                    continue
                target = int(ins.op_str[1:], 16)
                if target in results:
                    results[target]["Thumb_BL_BLX"].append({"unit": name, "address": ins.address})
    expected = {0x02028B74: [0x02028AF8, 0x02028B0C, 0x02042F6C],
                0x02028AA8: [0x02029FB4], 0x02028BAC: [0x02021BB8, 0x02029FD0]}
    for target, sites in expected.items():
        assert [row["address"] for row in results[target]["ARM_B_BL"]] == sites
        assert all(row["link"] and row["condition"] == 14 for row in results[target]["ARM_B_BL"])
        assert not results[target]["Thumb_BL_BLX"] and not results[target]["stored_pointers"]
    return {"targets": results, "units": [{"name": n, "base": b, "bytes": len(d), "sha256": sha(d)}
                                          for n, b, d in units]}


def decode(arm):
    u = machine(arm)
    u.mem_write(OWNER - 16, b"\xA5" * 80)
    u.mem_write(OWNER, bytes(16))
    u.mem_write(OWNER + 4, struct.pack("<I", STREAM))
    u.mem_write(STREAM - 16, b"\xA5" * 36)
    u.mem_write(RESULT - 16, b"\xA5" * 80)
    digest = hashlib.sha256()
    counts = Counter()
    for operand in range(65536):
        source = struct.pack("<2H", 0x4620, operand)
        u.mem_write(STREAM, source)
        u.mem_write(LENGTH, bytes(4))
        for reg, value in ((UC_ARM_REG_R0, RESULT), (UC_ARM_REG_R1, OWNER),
                           (UC_ARM_REG_R2, LENGTH), (UC_ARM_REG_SP, STACK)):
            u.reg_write(reg, value)
        short = bool(operand & 0x8000)
        stop = 0x02029FB4 if short else 0x02029FD0
        u.emu_start(0x0202A510, stop, count=128)
        assert u.reg_read(UC_ARM_REG_PC) == stop
        assert struct.unpack("<I", u.mem_read(LENGTH, 4))[0] == 4
        assert u.reg_read(UC_ARM_REG_R0) == 0x02276F88
        arg1 = u.reg_read(UC_ARM_REG_R1)
        arg2 = u.reg_read(UC_ARM_REG_R2)
        options = arg2 if short else u.reg_read(UC_ARM_REG_R3)
        assert struct.unpack("<3I", u.mem_read(options, 12)) == (2, 0, 0)
        assert arg1 == (operand & 255 if short else operand >> 8 & 127)
        if not short:
            assert arg2 == operand & 255
        digest.update(struct.pack("<4I", operand, stop, arg1, 0 if short else arg2))
        counts["event_still" if short else "town"] += 1
        assert bytes(u.mem_read(STREAM, 4)) == source
    assert bytes(u.mem_read(OWNER + 4, 4)) == struct.pack("<I", STREAM)
    for address in (OWNER - 16, OWNER + 16, STREAM - 16, STREAM + 4, RESULT - 16, RESULT):
        assert bytes(u.mem_read(address, 16)) == b"\xA5" * 16
    assert bytes(u.mem_read(LENGTH + 4, 28)) == b"\xA5" * 28
    return {"instruction": "4620", "all65536_operands": dict(counts),
            "ordered_native_argument_digest": digest.hexdigest(), "input_and_result_guards_exact": True,
            "stopped_at_original_parent_calls_before_loading_or_GPU": True}


def scans(rom):
    rows = []
    for _, path, data in rom.iter_files():
        if not path.startswith(("/data/", "/testdata/", "/COMMON/")):
            continue
        if data.startswith(b"ILNK"):
            blocks = IlnkContainer.parse(data).blocks
            kind = "ILNK blocks"
        elif data.startswith(b"VE"):
            blocks, kind = [data], "whole VE file including header"
        else:
            continue
        counts, hits, positions = Counter(), [], 0
        for block_id, block in enumerate(blocks):
            for offset in range(len(block) - 3):
                word, operand = struct.unpack_from("<2H", block, offset)
                positions += 1
                if word & 0xFF00 == 0x4600 and operand & 0x8000:
                    counts[operand & 255] += 1
                    if operand & 255 in CARDS:
                        hits.append({"block": block_id, "offset": offset, "word": word, "operand": operand})
        if path != "/data/WORLDMAP.DK4":
            assert not hits, (path, hits)
        rows.append({"path": path, "sha256": sha(data), "container": kind, "blocks": len(blocks),
                     "byte_positions": positions, "pattern_counts_not_decoded_instructions": dict(sorted(counts.items())),
                     "village_card_byte_candidates_not_reachability": hits})
    assert len(rows) == 20
    return rows


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current, clean = NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    assert sha(ROM.read_bytes()) == "542c2faf58bde6f408c873a930e29cdb215ef4940375aeffb650644c26d41e68"
    arm, original = current.read_file("/__arm9__.bin"), clean.read_file("/__arm9__.bin")
    ranges = [(0x2A510, 0x2A5BC), (0x29AA0, 0x29AF8), (0x29F50, 0x29FFC),
              (0x28AA8, 0x28BA8), (0x28BAC, 0x28C80), (0xB7128, 0xB762C)]
    assert all(arm[lo:hi] == original[lo:hi] for lo, hi in ranges)
    # Native alternate path B7128 -> B7294 -> B7260 -> B7158 uses town artwork.
    string_address = struct.unpack_from("<I", arm, 0xB7290)[0]
    town = arm[string_address - BASE:].split(b"\0", 1)[0]
    assert town == b"/towngrp/towngrp%02u.pxl"
    event_format = b"/evstill/evstill%03u.pxl\0"
    assert arm[0x134BC8:0x134BC8 + len(event_format)] == original[0x134BC8:0x134BC8 + len(event_format)] == event_format
    decoded = {"current": decode(arm), "clean": decode(original)}
    assert decoded["current"] == decoded["clean"]
    sources = {"current": scans(current), "clean": scans(clean)}
    census_result = census(current, arm)
    source_census = census(clean, original)
    assert census_result["targets"] == source_census["targets"]
    for rows in sources.values():
        world = next(row for row in rows if row["path"] == "/data/WORLDMAP.DK4")
        assert len(world["village_card_byte_candidates_not_reachability"]) == 16
    assert current.read_file("/data/WORLDMAP.DK4") == clean.read_file("/data/WORLDMAP.DK4")
    assert all(current.read_file(row["path"]) == clean.read_file(row["path"])
               for row in sources["current"] if row["path"].startswith("/testdata/"))
    proof = {"format": "dk4-village-dispatch-v589", "candidate": str(ROM), "candidate_sha256": sha(ROM.read_bytes()),
             "clean_sha256": sha(clean.source.read_bytes()), "source_exact_code_ranges": ranges,
             "village_card_indices": list(CARDS), "native_operand_decoders": decoded,
             "original_town_format": town.decode(), "current_target_census": census_result,
             "clean_target_census": source_census, "container_scans": sources,
             "testdata_containers_and_worldmap_exact_to_clean": True,
             "worldmap_byte_candidates_not_decoded_as_script_or_event_triggers": True,
             "omitted_shared_event_and_testdata_containers_now_checked": True,
             "other_computed_indirect_filename_or_fileID_readers_not_excluded": True,
             "no_new_GPU_ordinary_village_context_or_global_unused_claim": True,
             "production_ROM_or_patch_changed": False, "full_goal_complete": False,
             "script_sha256": sha(Path(__file__).read_bytes())}
    (ROOT / "dispatch_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print("V589: 131072 native operand cases;40 clean/current container scans;3 original caller target censuses. No ordinary village trigger established.")


if __name__ == "__main__":
    main()
