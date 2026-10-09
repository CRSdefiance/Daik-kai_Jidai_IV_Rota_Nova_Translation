"""Verify OCINIT's native texture reads and the shared startup palette uploads."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R8,
    UC_ARM_REG_R10,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, machine

ROOT = Path("work/analysis/raw_banks_v223")
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08
PIXELS, PALETTE = 0x020E21B8, 0x020E208C


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom, clean = NdsImage.open("out/all_routes_combined_v218_candidate.nds"), NdsImage.open("work/clean.nds")
    arm = rom.read_file("/__arm9__.bin")
    raw = rom.read_file("/GRP/OCINIT.DK4")
    assert raw == clean.read_file("/GRP/OCINIT.DK4")
    table = struct.unpack_from("<I", arm, 0x7BB54)[0]
    entries = [struct.unpack_from("<3I", arm, table - 0x02000000 + n * 12) for n in range(7)]
    scratch = 0x022E1794
    u = machine(arm)
    handles, events, uploads = {}, [], []

    def bridge(uc, address, size, _):
        if address in (OPEN, READ, SEEK, CLOSE):
            obj = uc.reg_read(UC_ARM_REG_R0)
            if address == OPEN:
                name = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1), 64)).split(b"\0")[0].decode("ascii").replace("\\", "/")
                assert name == "/GRP/OCINIT.DK4" and not handles
                handles[obj] = 0
                value = 1
                events.append({"operation": "open", "name": name})
            elif address == SEEK:
                position = uc.reg_read(UC_ARM_REG_R1)
                assert uc.reg_read(UC_ARM_REG_R2) == 0 and position <= len(raw)
                handles[obj] = position
                value = 1
                events.append({"operation": "seek", "position": position})
            elif address == READ:
                pointer, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
                position = handles[obj]
                assert pointer == scratch and position + count <= len(raw)
                uc.mem_write(pointer, raw[position:position + count])
                handles[obj] += count
                value = count
                events.append({"operation": "read", "offset": position, "bytes": count})
            else:
                handles.pop(obj)
                value = 1
                events.append({"operation": "close"})
            uc.reg_write(UC_ARM_REG_R0, value)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address in (0x020E231C, 0x020E2148, 0x020E2100, 0x020E2034, PIXELS, PALETTE):
            if address in (PIXELS, PALETTE):
                pointer, destination, count = [uc.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)]
                uploads.append({"kind": "texture" if address == PIXELS else "palette", "source": pointer,
                                "destination": destination, "bytes": count,
                                "source_sha256": sha(bytes(uc.mem_read(pointer, count)))})
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    h = u.hook_add(UC_HOOK_CODE, bridge)
    cases = []
    try:
        # Exact open fragment from the normal sailing initializer.
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.emu_start(0x0207B910, 0x0207B91C, count=1000)
        for index, (units, offset_units, destination) in enumerate(entries):
            count, offset = units * 1024, offset_units * 1024
            u.mem_write(scratch - 16, b"\xa5" * (count + 32))
            u.mem_write(STACK + 0x10, struct.pack("<3I", units, offset_units, destination))
            for reg, value in ((UC_ARM_REG_R4, 0x021703B0), (UC_ARM_REG_R5, STACK + 0x10),
                               (UC_ARM_REG_R8, scratch), (UC_ARM_REG_R10, 0)):
                u.reg_write(reg, value)
            start = len(events)
            old_uploads = len(uploads)
            u.emu_start(0x0207B958, 0x0207B998, count=10000)
            assert u.reg_read(UC_ARM_REG_PC) == 0x0207B998
            assert bytes(u.mem_read(scratch, count)) == raw[offset:offset + count]
            assert bytes(u.mem_read(scratch - 16, 16)) == b"\xa5" * 16
            assert bytes(u.mem_read(scratch + count, 16)) == b"\xa5" * 16
            transfer = uploads[old_uploads:]
            assert len(transfer) == 1 and transfer[0]["destination"] == destination and transfer[0]["bytes"] == count
            cases.append({"index": index, "offset": offset, "bytes": count, "destination": destination,
                          "source_sha256": sha(raw[offset:offset + count]), "events": events[start:],
                          "upload": transfer[0], "complete_native_read_and_upload_span_guards_pass": True,
                          "normal_sailing_loop_uses_this_entry": index < 6,
                          "seventh_entry_is_explicit_table_input_not_claimed_normal_loop": index == 6})
        u.emu_start(0x0207B9AC, 0x0207B9B4, count=1000)
        assert not handles
        # Run the unchanged shared startup palette argument sequence; its inputs
        # are immutable ARM9 data, not palettes guessed from a raw file tail.
        old = len(uploads)
        u.emu_start(0x02000E10, 0x02000EE0, count=10000)
        palette_cases = uploads[old:]
        assert len(palette_cases) == 13 and all(p["kind"] == "palette" for p in palette_cases)
        for item in palette_cases:
            offset = item["source"] - 0x02000000
            assert bytes(u.mem_read(item["source"], item["bytes"])) == arm[offset:offset + item["bytes"]]
    finally:
        u.hook_del(h)
    covered_end = max(r["offset"] + r["bytes"] for r in cases)
    assert covered_end == 0x2B000 and len(raw) - covered_end == 0x4800
    proof = {"format": "dk4-ocinit-native-transfer-proof-v1", "ROM_sha256": sha(rom.source.read_bytes()),
             "file_sha256": sha(raw), "file_bytes": len(raw), "texture_cases": cases,
             "normal_initializer_actual_loop_count": 6, "native_table_entries_verified": 7,
             "texture_table_bytes_covered": covered_end, "remaining_unclassified_tail": [covered_end, len(raw)],
             "shared_startup_palette_transfers": palette_cases, "native_file_and_transfer_code_executed": True,
             "SDK_filesystem_and_hardware_transfers_are_explicit_bridges": True,
             "all_file_handles_closed": not handles,
             "source_texture_format_palette_parent_relationship_and_full_art_review_pending": True,
             "direct_RGB555_and_file_tail_palette_diagnostics_not_adopted": True,
             "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "native_ocinit_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_table_texture_cases": len(cases), "covered_source_bytes": covered_end,
                      "unclassified_tail_bytes": len(raw) - covered_end, "native_palette_argument_cases": len(palette_cases)}))


if __name__ == "__main__":
    main()
