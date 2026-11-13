"""Bound numeric filesystem clients; supplied SDK I/O is not artwork display."""

import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs
from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.trace_frame_crop_arguments_v584 import branch

ROOT = Path("work/analysis/numeric_file_clients_v595")
ROM = Path("out/all_routes_combined_v593_candidate.nds")
TARGETS = (0x020DEDA0, 0x020DEE1C, 0x020DE5F4, 0x020DF73C,
           0x020DF7DC, 0x020DF8F0, 0x020EA86C, 0x020EC928,
           0x020DE318, 0x020DFA00, 0x020EA2DC, 0x020DF104)
INFO, TABLE, OUT, NITRO = 0x02460000, 0x02461000, 0x02462000, 0x0237576C
RANGES = ((0x1474, 0x14C4), (0x153C, 0x1564), (0xDE318, 0xDE444),
          (0xDED50, 0xDEE74), (0xDF104, 0xDF124), (0xDF73C, 0xDFA28),
          (0xEA2DC, 0xEA2FC), (0xEA86C, 0xEA8F4), (0xEC928, 0xEC9C0))


def word(data, at):
    return struct.unpack_from("<I", data, at)[0]


def census(rom, arm):
    units = [(f"main{i}", s.ramAddress, bytes(s.data)) for i, s in enumerate(MainCodeFile(arm, BASE).sections)]
    units += [(f"overlay{i}", o.ramAddress, bytes(o.data)) for i, o in loadOverlayTable(
        rom.rom.arm9OverlayTable, lambda _, file_id: rom.rom.files[file_id]).items()]
    rows = {target: {"ARM_B_BL": [], "Thumb_BL_BLX": [], "all_byte_pointers": []} for target in TARGETS}
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    for name, base, data in units:
        for at in range(0, len(data) - 3, 4):
            w = word(data, at)
            target = branch(w, base + at)
            if target in rows:
                rows[target]["ARM_B_BL"].append({"unit": name, "address": base + at,
                                                "link": bool(w & 0x01000000), "condition": w >> 28})
        for at in range(len(data) - 3):
            value = word(data, at)
            if value & ~1 in rows:
                rows[value & ~1]["all_byte_pointers"].append({"unit": name, "address": base + at, "value": value})
        for at in range(0, len(data) - 3, 2):
            first, second = struct.unpack_from("<2H", data, at)
            if first & 0xF800 != 0xF000 or second & 0xF800 not in (0xE800, 0xF800):
                continue
            for ins in decoder.disasm(data[at:at + 4], base + at, count=1):
                if ins.mnemonic in ("bl", "blx") and ins.op_str.startswith("#0x"):
                    target = int(ins.op_str[1:], 16)
                    if target in rows:
                        rows[target]["Thumb_BL_BLX"].append({"unit": name, "address": ins.address})
    expected = {
        0x020DEDA0: [0x020DED78, 0x020DF768, 0x020DF850, 0x020DF9B8, 0x020EA8B4, 0x020EC99C],
        0x020DEE1C: [0x020DE374, 0x020DE3D8, 0x020DF94C],
        0x020DE5F4: [0x020DED14, 0x020DEDDC, 0x020DEE3C, 0x020DEF0C, 0x020DF08C],
    }
    for target, addresses in expected.items():
        assert [x["address"] for x in rows[target]["ARM_B_BL"]] == addresses
    for target, row in rows.items():
        assert not row["Thumb_BL_BLX"]
        assert row["all_byte_pointers"] == ([{"unit": "main0", "address": 0x020DF11C, "value": 0x020DE318}]
                                            if target == 0x020DE318 else [])
    return {"targets": rows, "units": [{"unit": n, "base": b, "bytes": len(d), "sha256": sha(d)} for n, b, d in units]}


class FileBoundary:
    """Explicit supplied filesystem outcomes backed by exact source ROM bytes."""

    def __init__(self, u, rom):
        self.u, self.rom = u, rom
        self.raw = rom.source.read_bytes()
        self.handles, self.events = {}, []

    def ret(self, value):
        self.u.reg_write(UC_ARM_REG_R0, value)
        self.u.reg_write(UC_ARM_REG_PC, self.u.reg_read(UC_ARM_REG_LR))

    def hook(self, u, address, size, data):
        args = [u.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        handle = args[0]
        if address == 0x020DE5F4:
            command = args[1]
            if command == 6:
                archive, file_id = struct.unpack("<2I", u.mem_read(handle + 0x2C, 8))
                assert archive == NITRO and file_id < len(self.rom.rom.files)
                fat = word(self.raw, 0x48) + file_id * 8
                start, end = struct.unpack_from("<2I", self.raw, fat)
                assert self.raw[start:end] == self.rom.rom.files[file_id]
                self.events.append({"kind": "supplied_numeric_open", "file_id": file_id, "range": [start, end]})
            elif command == 7:
                start, end, file_id = struct.unpack("<3I", u.mem_read(handle + 0x2C, 12))
                assert file_id == 0xFFFFFFFF and 0 <= start <= end <= len(self.raw)
                self.events.append({"kind": "supplied_direct_open", "range": [start, end]})
            else:
                raise AssertionError(f"Unplanned filesystem command {command}")
            self.events[-1].update({"bytes": end - start, "payload_sha256": sha(self.raw[start:end])})
            self.handles[handle] = [start, end, start]
            u.mem_write(handle + 0x20, struct.pack("<3I", start, end, start))
            self.ret(1)
        elif address == 0x020DEBDC:
            start, end, pos = self.handles[handle]
            amount = min(args[2], end - pos)
            u.mem_write(args[1], self.raw[pos:pos + amount])
            self.handles[handle][2] += amount
            u.mem_write(handle + 0x28, struct.pack("<I", pos + amount))
            self.events.append({"kind": "supplied_exact_read", "range": [pos, pos + amount], "destination": args[1],
                                "bytes": amount, "payload_sha256": sha(self.raw[pos:pos + amount])})
            self.ret(amount)
        elif address == 0x020DED08:
            assert handle in self.handles
            del self.handles[handle]
            self.events.append({"kind": "supplied_close"})
            self.ret(1)
        elif address in (0x020E447C, 0x020E43F8):
            self.events.append({"kind": "cache_maintenance_no_hardware_effect", "address": address, "args": args[:2]})
            self.ret(0)


def overlays(rom, arm):
    results = []
    for cached in (False, True):
        for cpu, index, success in ((0, 0, True), (0, 1, False), (1, 0, False)):
            u = machine(arm)
            boundary = FileBoundary(u, rom)
            h = u.hook_add(UC_HOOK_CODE, boundary.hook)
            u.mem_write(INFO - 16, b"\xA5" * 80)
            u.mem_write(TABLE, bytes(rom.rom.arm9OverlayTable))
            u.mem_write(0x0237575C, struct.pack("<4I", TABLE if cached else 0, len(rom.rom.arm9OverlayTable), 0, 0))
            u.mem_write(0x027FFE50, boundary.raw[0x50:0x60])
            executed = call(u, 0xDF7DC, (INFO, cpu, index))
            assert u.reg_read(UC_ARM_REG_R0) == int(success)
            if success:
                assert bytes(u.mem_read(INFO, 32)) == rom.rom.arm9OverlayTable
                fid = word(rom.rom.arm9OverlayTable, 24)
                assert fid == 0
                expected_range = struct.unpack_from("<2I", boundary.raw, word(boundary.raw, 0x48) + 8 * fid)
                assert struct.unpack("<3I", u.mem_read(INFO + 32, 12)) == (cpu, expected_range[0], expected_range[1] - expected_range[0])
                assert any(e.get("file_id") == fid for e in boundary.events)
                assert len(boundary.handles) == 0
                # This helper only converts the original overlay-info file-ID field.
                call(u, 0xDFA00, (OUT, INFO))
                assert struct.unpack("<2I", u.mem_read(OUT, 8)) == (NITRO, fid)
                # Complete original load function copies this real overlay, not SLACKIMG.
                target, length, bss = struct.unpack_from("<3I", rom.rom.arm9OverlayTable, 4)
                u.mem_write(target, b"\xA5" * (length + bss))
                call(u, 0xDF73C, (INFO,))
                assert u.reg_read(UC_ARM_REG_R0) == 1
                assert bytes(u.mem_read(target, length)) == bytes(rom.rom.files[fid])
                assert bytes(u.mem_read(target + length, bss)) == bytes(bss)
                assert not boundary.handles
                assert {0x020DF7DC, 0x020DEDA0} <= executed
            else:
                assert not any(e["kind"] == "supplied_numeric_open" for e in boundary.events)
            assert bytes(u.mem_read(INFO - 16, 16)) == b"\xA5" * 16
            assert bytes(u.mem_read(INFO + 44, 20)) == b"\xA5" * 20
            u.hook_del(h)
            results.append({"cached_table": cached, "cpu": cpu, "index": index, "success": success,
                            "complete_original_lookup_and_load_on_success": success, "events": boundary.events})
    return results


def sound(rom, arm):
    u = machine(arm)
    sound_file = next((file_id, path, data) for file_id, path, data in rom.iter_files() if path == "/sound_data.sdat")
    file_id, path, payload = sound_file
    assert file_id == 2 and payload.startswith(b"SDAT")
    boundaries, native_opens, parses = [], [], []
    buffers = (0x02470000, 0x02480000, 0x02490000)

    def readz(address):
        return bytes(u.mem_read(address, 128)).split(b"\0", 1)[0].decode("ascii")

    def ret(value):
        u.reg_write(UC_ARM_REG_R0, value)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    def hook(uc, address, size, data):
        args = [uc.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        if address == 0x020DEE74:
            assert readz(args[1]) == path.lstrip("/")
            uc.mem_write(args[0], struct.pack("<2I", NITRO, file_id))
            boundaries.append({"filename": readz(args[1]), "supplied_FNT_file_id": file_id})
            ret(1)
        elif address == 0x020DE5F4:
            assert args[1] == 6
            pair = struct.unpack("<2I", uc.mem_read(args[0] + 0x2C, 8))
            assert pair == (NITRO, file_id)
            native_opens.append({"handle": args[0], "archive": pair[0], "file_id": pair[1]})
            ret(1)
        elif address == 0x020EA650:
            assert args[2:] == [0, 1] and args[1] == buffers[len(parses)]
            parses.append({"object": args[0], "buffer": args[1], "SDAT_parser_outcome_supplied": 1})
            ret(1)

    # Original allocation result globals are supplied; all path/client/open code runs.
    for instruction, buffer in zip((0x1484, 0x149C, 0x14B4), buffers):
        literal = instruction + 8 + (word(arm, instruction) & 4095)
        global_address = word(arm, literal)
        u.mem_write(global_address, struct.pack("<I", buffer))
    h = u.hook_add(UC_HOOK_CODE, hook)
    try:
        # This is the original three-call sequence, stopped before unrelated sound setup.
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_R0, buffers[2])
        u.emu_start(BASE + 0x1474, BASE + 0x14C4, count=10000)
        assert u.reg_read(UC_ARM_REG_PC) == BASE + 0x14C4
        assert u.reg_read(UC_ARM_REG_SP) == STACK
        assert len(boundaries) == len(native_opens) == len(parses) == 3
        for row in parses:
            assert struct.unpack("<2I", u.mem_read(row["object"] + 0x78, 8)) == (NITRO, file_id)
            assert word(bytes(u.mem_read(row["object"], 0x90)), 0x30) == 1
        call(u, 0xEA2DC, (OUT,))
        assert struct.unpack("<2I", u.mem_read(OUT, 8)) == (NITRO, file_id)
    finally:
        u.hook_del(h)
    return {"original_three_client_calls": [0x02001490, 0x020014A8, 0x020014C0],
            "path_resolver_boundaries": boundaries, "native_command6_arguments": native_opens,
            "supplied_parser_boundaries": parses, "original_selected_ID_getter_exact": True,
            "source_file": path, "source_file_id": file_id, "source_file_sha256": sha(payload),
            "actual_filesystem_resolution_SDAT_parsing_playback_not_claimed": True}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom, clean = NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    assert sha(ROM.read_bytes()) == "d4d572f3356aef8e1d03ee61c18a89f57db01761c381d95b867f1acf25032642"
    arm, source = rom.read_file("/__arm9__.bin"), clean.read_file("/__arm9__.bin")
    assert all(arm[lo:hi] == source[lo:hi] for lo, hi in RANGES)
    c = {"current": census(rom, arm), "clean": census(clean, source)}
    assert c["current"]["targets"] == c["clean"]["targets"]
    native = {"current": {"overlays": overlays(rom, arm), "sound": sound(rom, arm)},
              "clean": {"overlays": overlays(clean, source), "sound": sound(clean, source)}}
    assert native["current"]["sound"] == native["clean"]["sound"]
    # Repacked ROMs have different physical FAT/table locations. Keep both exact
    # ranges in the proof, and compare source payloads, sizes and original calls.
    def semantic(rows):
        return [{**row, "events": [{k: v for k, v in event.items() if k != "range"}
                                    for event in row["events"]]} for row in rows]
    assert semantic(native["current"]["overlays"]) == semantic(native["clean"]["overlays"])
    ids = [{"file_id": file_id, "path": path, "bytes": len(data), "sha256": sha(data)}
           for file_id, path, data in rom.iter_files()
           if path in ("/GRP/CMMNIMG.000", "/GRP/CMMNIMG.DK4", "/GRP/SLACKIMG.DK4", "/GRP/WINFRAME.DK4")]
    assert next(x["file_id"] for x in ids if x["path"] == "/GRP/SLACKIMG.DK4") == 619
    proof = {"format": "dk4-numeric-file-clients-v595", "candidate": str(ROM),
             "candidate_sha256": sha(ROM.read_bytes()), "clean_sha256": sha(clean.source.read_bytes()),
             "source_exact_code_ranges": RANGES, "target_census": c,
             "clean_current_native_semantics_exact_with_repacked_physical_ranges_retained": True,
             "native_original_contracts_with_explicit_supplied_boundaries": native,
             "legacy_file_ids_not_client_reachability": ids,
             "direct_ID_open_callers": {"path_based_open_wrapper": [0x020DED78],
                                        "overlay_metadata_and_load": [0x020DF768, 0x020DF850, 0x020DF9B8],
                                        "sound_archive_and_stream": [0x020EA8B4, 0x020EC99C]},
             "direct_range_open_callers": {"archive_table_buffer_load": [0x020DE374, 0x020DE3D8],
                                           "overlay_table_record_read": [0x020DF94C]},
             "sole_stored_pointer": {"literal": 0x020DF11C, "target": 0x020DE318, "wrapper": 0x020DF104},
             "computed_indirect_other_filesystem_or_ARM7_readers_not_excluded": True,
             "raw_comic_consumer_GPU_display_or_global_unused_not_proved": True,
             "next_action": "Follow non-SDK image-conversion/compositing paths or runtime-generated resource references; direct SDK numeric clients supply no raw-comic viewer lead.",
             "production_ROM_or_patch_changed": False, "full_goal_complete": False,
             "script_sha256": sha(Path(__file__).read_bytes())}
    (ROOT / "numeric_clients_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print("V595: clean/current 12-target census;12 original overlay lookup cases and4 complete overlay loads;6 source-bound sound open calls. No raw-comic display claim.")


if __name__ == "__main__":
    main()
