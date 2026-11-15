"""Execute the actual overlay producer on each confirmed Japanese panel."""

import json
import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, STOP, machine

ROOT = Path("work/analysis/sailing_panel_overlay_v214")
BUFFER = 0x02460020
CAPACITY = 0x10000


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open("out/all_routes_combined_v211_candidate.nds")
    assert sha(rom.source.read_bytes()) == "d6cd1ecc3702d75a9f0c9e6e89a84501dbde8eb5fcaa9c6af82154716a8d5ae1"
    arm = rom.read_file("/__arm9__.bin")
    overlay = loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.rom.files[fid])[0]
    font = rom.read_file("/GRP/KANJI.FNT")
    u = machine(arm)
    u.mem_write(overlay.ramAddress, bytes(overlay.data))
    font_pointer = struct.unpack_from("<I", arm, 0xD19B8)[0]
    assert len(font) == 73480 and 0x02000000 <= font_pointer < 0x02400000
    u.mem_write(font_pointer, font)
    calls = []

    def observe(uc, address, size, _):
        if address == 0x020D198C:
            calls.append(uc.reg_read(UC_ARM_REG_R0))

    hook = u.hook_add(UC_HOOK_CODE, observe)
    results = []
    try:
        for name, pointer in (("info", 0x02147778), ("search", 0x02147540), ("war", 0x02147674)):
            raw = bytes(u.mem_read(pointer, 512)).split(b"\0")[0]
            assert len(raw) % 2 == 0
            u.mem_write(BUFFER - 16, b"\xa5" * (CAPACITY + 32))
            u.mem_write(BUFFER, bytes(CAPACITY))
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_LR, STOP)
            u.reg_write(UC_ARM_REG_R0, pointer)
            u.reg_write(UC_ARM_REG_R1, 15)
            u.reg_write(UC_ARM_REG_R2, BUFFER)
            start = len(calls)
            u.emu_start(0x01FFB4BC, STOP, count=4000000)
            assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK
            assert bytes(u.mem_read(BUFFER - 16, 16)) == b"\xa5" * 16
            assert bytes(u.mem_read(BUFFER + CAPACITY, 16)) == b"\xa5" * 16
            produced = bytes(u.mem_read(BUFFER, CAPACITY))
            active = [n for n, v in enumerate(produced) if v]
            assert calls[start:] == [int.from_bytes(raw[i:i + 2], "big") for i in range(0, len(raw), 2)]
            path = ROOT / f"{name}_native_output.bin"
            path.write_bytes(produced)
            results.append({"name": name, "pointer": pointer, "source_bytes": len(raw),
                            "source_sha256": sha(raw), "source_text": raw.decode("cp932"),
                            "complete_pair_lookup_count": len(calls) - start,
                            "lookup_sequence_exact": True, "output": path.as_posix(), "output_sha256": sha(produced),
                            "nonzero_output_bytes": len(active), "last_nonzero_offset": max(active),
                            "native_return_and_outer_guards_exact": True,
                            "caller_uploaded_bytes": 0x3800, "screen_layout_decode_pending": True})
    finally:
        u.hook_del(hook)
    proof = {"format": "dk4-native-sailing-panel-overlay-calibration-v1", "ROM_sha256": sha(rom.source.read_bytes()),
             "overlay_sha256": sha(bytes(overlay.data)), "font_sha256": sha(font), "font_runtime_address": font_pointer,
             "original_overlay_and_font_map_executed": True, "font_disk_load_not_executed_in_fixture": True,
             "zero_target_and_outer_capacity_explicit_fixture": CAPACITY, "cases": results,
             "rendered_layout_and_English_integration_pending": True, "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "calibration.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_native_producer_cases": len(results), "pairs": [r["complete_pair_lookup_count"] for r in results],
                      "last_written_offsets": [r["last_nonzero_offset"] for r in results]}))


if __name__ == "__main__":
    main()
