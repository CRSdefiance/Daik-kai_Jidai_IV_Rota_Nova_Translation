"""Trace actual portrait fields, loose-resource loading and legacy-buffer reads."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R4,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.research_online_loader_v190 import resource_call

CANDIDATE = Path("out/all_routes_combined_v190_candidate.nds")
BASE = Path("out/raphael_natural_v2_accepted_base.nds")
ROOT = Path("work/analysis/portrait_binding_v202")
OBJECT, VIEW = 0x02460000, 0x02470000
RAW_BUFFER, RAW_BYTES = 0x02233040, 104 * 136
SDK_OPEN, SDK_READ, SDK_SEEK, SDK_CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert sha(CANDIDATE.read_bytes()) == "9ccff57aec0326722b89b85877fb5be23e63dc466022b1f7c2e0a984ccdd9424"
    assert sha(BASE.read_bytes()) == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    rom, original = NdsImage.open(CANDIDATE), NdsImage.open(BASE)
    arm, old_arm = rom.read_file("/__arm9__.bin"), original.read_file("/__arm9__.bin")
    ranges = [(0x9EDD8, 0x9EE94), (0xD3BD4, 0xD3BFC), (0xD3D30, 0xD42AC),
              (0xD6524, 0xD6C90), (0x10E190, 0x11155C), (0x4704C, 0x470B4)]
    assert all(arm[lo:hi] == old_arm[lo:hi] for lo, hi in ranges)
    uc = machine(arm)
    registration = resource_call(uc, 0x10E190, ())
    manager = struct.unpack_from("<I", arm, 0x5D24)[0]
    call(uc, 0xD6C0C, (manager,))
    pool_start, pool_end = struct.unpack("<2I", uc.mem_read(manager, 8))
    handles, events, raw_reads = {}, [], []
    captured = []

    def code_hook(u, address, size, _):
        if address == 0x0209EE18:
            captured.append(bytes(u.mem_read(STACK + 0xDC, 48)))
        if address == 0x020E5650:
            raise ValueError("Native image loader reached a fatal assertion")
        if address not in (SDK_OPEN, SDK_READ, SDK_SEEK, SDK_CLOSE):
            return
        obj = u.reg_read(UC_ARM_REG_R0)
        if address == SDK_OPEN:
            pointer = u.reg_read(UC_ARM_REG_R1)
            name = bytes(u.mem_read(pointer, 128)).split(b"\0", 1)[0].decode("ascii")
            path = "/" + name.replace("\\", "/").lstrip("/")
            raw = rom.read_file(path)
            assert obj not in handles
            handles[obj] = {"path": path, "raw": raw, "position": 0}
            u.mem_write(obj + 0x20, struct.pack("<2I", 0, len(raw)))
            events.append({"operation": "open", "path": path, "bytes": len(raw), "sha256": sha(raw)})
            result = 1
        elif address == SDK_SEEK:
            state = handles[obj]
            offset, origin = u.reg_read(UC_ARM_REG_R1), u.reg_read(UC_ARM_REG_R2)
            assert origin == 0 and 0 <= offset <= len(state["raw"])
            state["position"] = offset
            events.append({"operation": "seek", "path": state["path"], "offset": offset})
            result = 1
        elif address == SDK_READ:
            state = handles[obj]
            destination, count = u.reg_read(UC_ARM_REG_R1), u.reg_read(UC_ARM_REG_R2)
            start, end = state["position"], state["position"] + count
            assert 0 <= start <= end <= len(state["raw"])
            u.mem_write(destination, state["raw"][start:end])
            state["position"] = end
            events.append({"operation": "read", "path": state["path"], "bytes": count,
                           "offset": start, "destination": destination})
            result = count
        else:
            state = handles.pop(obj)
            events.append({"operation": "close", "path": state["path"]})
            result = 1
        u.reg_write(UC_ARM_REG_R0, result)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    def observe_reads(u, access, address, size, value, _):
        if address < RAW_BUFFER + RAW_BYTES and address + size > RAW_BUFFER:
            raw_reads.append({"PC": u.reg_read(UC_ARM_REG_PC), "address": address, "bytes": size})

    code = uc.hook_add(UC_HOOK_CODE, code_hook)
    reads = uc.hook_add(UC_HOOK_MEM_READ, observe_reads)
    slack = IlnkContainer.parse(rom.read_file("/GRP/SLACKIMG.DK4"))
    old_slack = IlnkContainer.parse(original.read_file("/GRP/SLACKIMG.DK4"))
    cases = []
    try:
        for index in range(4):
            embedded = slack.blocks[14 + index]
            assert embedded == old_slack.blocks[14 + index] and len(embedded) == RAW_BYTES
            start_events, start_reads = len(events), len(raw_reads)
            uc.mem_write(RAW_BUFFER - 16, b"\xA5" * (RAW_BYTES + 32))
            uc.mem_write(OBJECT - 16, b"\xA5" * (0x800 + 32))
            uc.mem_write(STACK + 0xCC, b"\xA5" * 80)
            uc.mem_write(STACK + 0x14, struct.pack("<I", 0))
            for reg, value in ((UC_ARM_REG_SP, STACK), (UC_ARM_REG_R4, 104),
                               (UC_ARM_REG_R6, 136), (UC_ARM_REG_R7, OBJECT),
                               (UC_ARM_REG_R9, index), (UC_ARM_REG_R10, OBJECT), (UC_ARM_REG_R11, 0)):
                uc.reg_write(reg, value)
            uc.emu_start(0x0209EDD8, 0x0209EE80, count=100000)
            assert uc.reg_read(UC_ARM_REG_PC) == 0x0209EE80 and uc.reg_read(UC_ARM_REG_SP) == STACK
            constructed = captured[-1]
            persisted = bytes(uc.mem_read(OBJECT + 0x5B0, 44))
            assert persisted == constructed[4:]
            fields = struct.unpack("<12I", constructed)
            owner = struct.unpack_from("<I", arm, 0x119E24 + index * 4)[0]
            assert fields[3] == owner and fields[10:12] == (104, 136)
            assert bytes(uc.mem_read(RAW_BUFFER, RAW_BYTES)) == embedded
            assert bytes(uc.mem_read(RAW_BUFFER - 16, 16)) == b"\xA5" * 16
            assert bytes(uc.mem_read(RAW_BUFFER + RAW_BYTES, 16)) == b"\xA5" * 16
            assert bytes(uc.mem_read(OBJECT - 16, 16)) == b"\xA5" * 16
            assert bytes(uc.mem_read(OBJECT + 0x800, 16)) == b"\xA5" * 16
            expected_object = bytearray(b"\xA5" * 0x800)
            expected_object[0x5B0:0x5DC] = persisted
            assert bytes(uc.mem_read(OBJECT, 0x800)) == expected_object
            path = f"/_pxl/personbustup{index:02d}.pxl"
            name_ptr = struct.unpack("<I", uc.mem_read(owner + 12, 4))[0]
            actual_name = bytes(uc.mem_read(name_ptr, 128)).split(b"\0", 1)[0].decode("ascii")
            assert "/" + actual_name.replace("\\", "/").lstrip("/") == path
            raw = rom.read_file(path)
            assert raw == original.read_file(path)
            image = PxlImage.from_bytes(raw)
            assert (image.width, image.height, image.bits_per_pixel) == (104, 136, 8)
            # The copied persistent fields are proven above. Resolve a separately
            # constructed native view on that exact owner, without forging its
            # header, palette or cache pointer. The whole UI constructor is not run.
            uc.mem_write(VIEW - 16, b"\xA5" * 80)
            uc.mem_write(VIEW, bytes(48))
            uc.mem_write(STACK, struct.pack("<4I", 104, 136, 0, 0))
            call(uc, 0xD3D30, (VIEW, owner, 0, 0))
            before_load = len(events)
            trace = resource_call(uc, 0xD4170, (VIEW,))
            pointer = uc.reg_read(UC_ARM_REG_R0)
            assert pool_start + 16 <= pointer < pointer + len(raw) <= pool_end
            assert bytes(uc.mem_read(pointer, len(raw))) == raw
            assert bytes(uc.mem_read(VIEW - 16, 16)) == b"\xA5" * 16
            assert bytes(uc.mem_read(VIEW + 48, 16)) == b"\xA5" * 16
            assert {0x020D4170, 0x020D6558, 0x020D68F0} <= trace
            assert len(raw_reads) == start_reads
            assert not handles
            cases.append({"block": 14 + index, "embedded_sha256": sha(embedded), "actual_owner": owner,
                          "path": path, "full_PXL_sha256": sha(raw), "native_view_extent": [104, 136],
                          "all44_persistent_field_bytes_exact": True,
                          "constructed_view": list(fields), "resolved_cache_pointer": pointer,
                          "complete_native_loaded_palette_and_pixels_exact": True,
                          "palette_sha256": sha(raw[20:532]), "pixel_indices_sha256": sha(image.indices),
                          "embedded_vs_loose_index_differences": sum(a != b for a, b in zip(embedded, image.indices, strict=True)),
                          "legacy_buffer_native_reads_in_tested_parent_and_loader_path": raw_reads[start_reads:],
                          "parent_archive_IO": events[start_events:before_load], "native_PXL_loader_IO": events[before_load:]})
    finally:
        uc.hook_del(reads)
        uc.hook_del(code)
    report = {"format": "dk4-native-portrait-resource-binding-proof-v1", "ROM": CANDIDATE.as_posix(),
              "ROM_sha256": sha(CANDIDATE.read_bytes()), "ARM9_sha256": sha(arm),
              "native_code_ranges": [{"offset": lo, "end": hi, "sha256": sha(arm[lo:hi])} for lo, hi in ranges],
              "native_registry_instructions": len(registration), "cases": cases,
              "SDK_IO_bridge_only": True, "all_handles_closed": not handles,
              "scope": "Actual native parent 0209EDD8-0209EE80 with supplied preceding register/stack/object context, followed by an actual native view/cache resolution on its proven owner. No entire UI constructor, physical NitroFS or GPU proof is inferred.",
              "legacy_buffers_do_not_supply_pixels_or_palette_in_tested_path": True,
              "legacy_palettes_other_consumers_still_unclassified": True,
              "ROM_changed": False, "goal_complete": False}
    (ROOT / "native_resource_binding.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_parent_field_copies": len(cases), "complete_native_PXL_loads": len(cases),
                      "native_legacy_buffer_reads_in_tested_path": len(raw_reads), "all_handles_closed": not handles}))


if __name__ == "__main__":
    main()
