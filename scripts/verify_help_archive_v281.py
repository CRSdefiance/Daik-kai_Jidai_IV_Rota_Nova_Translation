"""Actual ILNK loading of all HELP topics and original topic-history behavior."""

import json
import struct

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_help_pages_v281 import ROOT
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.research_online_loader_v190 import resource_call

OBJECT, NAME, BUFFER = 0x02460000, 0x02461000, 0x02233040
SDK_OPEN, SDK_READ, SDK_SEEK, SDK_CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def main():
    raw = (ROOT / "help_research_only.bin").read_bytes()
    blocks = IlnkContainer.parse(raw).blocks
    arm = NdsImage.open("out/all_routes_combined_v275_candidate.nds").read_file("/__arm9__.bin")
    cpu = machine(arm)
    handles, events = {}, []

    def bridge(uc, address, size, _):
        if address not in (SDK_OPEN, SDK_READ, SDK_SEEK, SDK_CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == SDK_OPEN:
            pointer = uc.reg_read(UC_ARM_REG_R1)
            filename = bytes(uc.mem_read(pointer, 80)).split(b"\0", 1)[0]
            assert filename == b"\\COMMON\\HELP.DK4"
            handles[obj] = 0
            uc.mem_write(obj + 0x20, struct.pack("<2I", 0, len(raw)))
            result = 1
        elif address == SDK_SEEK:
            offset, origin = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            assert origin == 0 and 0 <= offset <= len(raw)
            handles[obj] = offset
            result = 1
        elif address == SDK_READ:
            destination, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            offset = handles[obj]
            assert offset + count <= len(raw)
            if count:
                uc.mem_write(destination, raw[offset:offset + count])
            handles[obj] += count
            events.append({"file_offset": offset, "count": count, "destination": destination})
            result = count
        else:
            handles.pop(obj)
            result = 1
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
    cpu.hook_add(UC_HOOK_CODE, bridge)
    cpu.mem_write(NAME, b"\\COMMON\\HELP.DK4\0")
    call(cpu, 0xD2100, (OBJECT,))
    call(cpu, 0xD2018, (OBJECT, NAME))
    assert cpu.reg_read(UC_ARM_REG_R0) == 1
    assert struct.unpack("<I", cpu.mem_read(OBJECT + 0x28, 4))[0] == len(blocks)
    cases = []
    for topic, data in enumerate(blocks):
        cpu.mem_write(BUFFER - 16, b"\xA5" * (len(data) + 32))
        # This is the real HELP caller's zero requested-size contract: the
        # native ILNK reader chooses the complete selected block length.
        cpu.mem_write(STACK, bytes(4))
        resource_call(cpu, 0xD1EF0, (OBJECT, BUFFER, topic, 0))
        assert cpu.reg_read(UC_ARM_REG_R0) == len(data)
        assert bytes(cpu.mem_read(BUFFER, len(data))) == data
        assert bytes(cpu.mem_read(BUFFER - 16, 16)) == bytes(cpu.mem_read(BUFFER + len(data), 16)) == b"\xA5" * 16
        cases.append({"topic": topic, "bytes": len(data), "native_full_block_and_guards_exact": True})
    call(cpu, 0xD2004, (OBJECT,))
    assert not handles
    parent = 0x02470000
    cpu.mem_write(parent - 16, b"\xA5" * (0x6B0 + 32))
    cpu.mem_write(parent + 0x668, struct.pack("<16I", *([203] * 16)))
    cpu.mem_write(parent + 0x6A8, bytes(4))
    histories = []
    for topic in (7, 202, 37, 204, 205, 184, 150, 187):
        # The native topic updater receives a slot selected by its UI caller.
        call(cpu, 0x7D070, (parent, topic))
        result = struct.unpack("<16I", cpu.mem_read(parent + 0x668, 64))
        assert result[0] == topic and result[1:] == (203,) * 15
        histories.append({"topic": topic, "native_current_slot": result[0], "sentinel203_next_slots_preserved": True})
    assert bytes(cpu.mem_read(parent - 16, 16)) == bytes(cpu.mem_read(parent + 0x6B0, 16)) == b"\xA5" * 16
    proof = {"format": "dk4-help-native-archive-history-v281", "HELP_sha256": sha(raw),
             "native206_topic_full_load_cases": cases, "SDK_host_file_bridge_reads": events,
             "native_history_cases": histories, "203_not_used_as_a_clickable_topic": blocks[203] == b"\0",
             "exact_native_HELP_buffer_address": BUFFER,
             "native_GUI_link_creation_clicked_navigation_and_physical_display_pending": True,
             "playable_ROM_modified": False, "full_goal_complete": False}
    (ROOT / "native_archive_history_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_topic_loads": len(cases), "history_cases": len(histories), "max_loaded_topic_bytes": max(map(len, blocks))}))


if __name__ == "__main__":
    main()
