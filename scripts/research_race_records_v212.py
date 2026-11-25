"""Execute all RACE record reads; preserve unresolved grid/color semantics."""

import json
import struct
from collections import Counter
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R10,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, machine

ROOT = Path("work/analysis/race_raw_v212")
ROM = Path("out/all_routes_combined_v211_candidate.nds")
BUFFER = 0x02480020
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert sha(ROM.read_bytes()) == "d6cd1ecc3702d75a9f0c9e6e89a84501dbde8eb5fcaa9c6af82154716a8d5ae1"
    rom, clean = NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    arm, old = rom.read_file("/__arm9__.bin"), clean.read_file("/__arm9__.bin")
    assert arm[0xF71B0:0xF72E8] == old[0xF71B0:0xF72E8]
    raw = rom.read_file("/GRP/RACE.DK4")
    assert raw == clean.read_file("/GRP/RACE.DK4")
    u = machine(arm)
    handles, events = {}, []

    def bridge(uc, address, size, _):
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            name = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1), 64)).split(b"\0")[0].decode("ascii").replace("\\", "/")
            assert name == "/GRP/RACE.DK4" and not handles
            handles[obj] = 0
            value = 1
            events.append({"operation": "open", "path": name})
        elif address == SEEK:
            offset = uc.reg_read(UC_ARM_REG_R1)
            assert uc.reg_read(UC_ARM_REG_R2) == 0 and 0 <= offset < len(raw)
            handles[obj] = offset
            value = 1
            events.append({"operation": "seek", "offset": offset})
        elif address == READ:
            offset = handles[obj]
            target, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            assert target == BUFFER and offset + count <= len(raw)
            uc.mem_write(target, raw[offset:offset + count])
            handles[obj] += count
            value = count
            events.append({"operation": "read", "offset": offset, "bytes": count})
        else:
            handles.pop(obj)
            value = 1
            events.append({"operation": "close"})
        uc.reg_write(UC_ARM_REG_R0, value)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, bridge)
    records = []
    try:
        for index in range(7):
            count, offset = struct.unpack_from("<2I", arm, 0x16B4B8 + index * 8)
            start = len(events)
            u.mem_write(BUFFER - 16, b"\xa5" * (count + 32))
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_R10, BUFFER)
            u.mem_write(STACK + 0x10, struct.pack("<I", index))
            u.emu_start(0x020F71B0, 0x020F71F8, count=100000)
            assert u.reg_read(UC_ARM_REG_PC) == 0x020F71F8 and u.reg_read(UC_ARM_REG_SP) == STACK
            assert u.reg_read(UC_ARM_REG_R10) == BUFFER and not handles
            loaded = bytes(u.mem_read(BUFFER, count))
            assert loaded == raw[offset:offset + count]
            assert bytes(u.mem_read(BUFFER - 16, 16)) == b"\xa5" * 16
            assert bytes(u.mem_read(BUFFER + count, 16)) == b"\xa5" * 16
            dimensions = struct.unpack_from("<4H", arm, 0x16B480 + index * 8)
            records.append({"index": index, "offset": offset, "bytes": count, "source_sha256": sha(loaded),
                            "native_metadata": list(dimensions),
                            "metadata_width_height_times2": dimensions[2] * dimensions[3] * 2,
                            "metadata_extent_matches_read": count == dimensions[2] * dimensions[3] * 2,
                            "complete_native_read_close_and_guards_exact": True, "events": events[start:]})
    finally:
        u.hook_del(hook)
    cursor = 0
    for row in sorted(records, key=lambda r: r["offset"]):
        assert row["offset"] == cursor
        cursor += row["bytes"]
    assert cursor == len(raw)
    words = struct.unpack(f"<{len(raw) // 2}H", raw)
    result = {"format": "dk4-native-race-record-read-proof-v1", "ROM_sha256": sha(ROM.read_bytes()),
              "path": "/GRP/RACE.DK4", "source_sha256": sha(raw), "source_bytes": len(raw),
              "records": records, "complete_record_partition_no_gaps_or_overlap": True,
              "native_reader_context": "Original open/indexed offset/size/read/close fragment with preceding stack-index and buffer fixtures. Later border writes/rendering not executed.",
              "source_uint16_values": {"unique": len(set(words)), "maximum": max(words), "most_common": Counter(words).most_common(16)},
              "coherent_geographic_grid_diagnostics_reviewed": 7,
              "RGB555_diagnostic_is_not_color_or_display_classification": True,
              "records_with_native_metadata_size_mismatch": [r["index"] for r in records if not r["metadata_extent_matches_read"]],
              "mismatch_already_present_in_clean_code_and_data": True,
              "grid_value_semantics_palette_and_actual_consumers_pending": True,
              "DSCHR_generated_text_followup": {"native_raw_mode_reader": "020CDE20", "actual_direct_caller": "020CE6D0",
                                                  "preserved_Japanese_sources": ["0215F72C", "0215F870"],
                                                  "text_overlay_entry": "01FFB4B0 -> 01FFB4BC",
                                                  "active_display_or_already_translated_alternative_not_proved": True},
              "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "native_record_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_native_records": len(records), "all_file_bytes_read_exact": len(raw),
                      "native_metadata_size_mismatch_indices": result["records_with_native_metadata_size_mismatch"]}))


if __name__ == "__main__":
    main()
