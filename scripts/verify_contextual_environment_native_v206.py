"""Execute environmental selectors, caption getters and exact native image reads."""

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
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
)

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.research_online_loader_v190 import resource_call
from scripts.verify_ordinary_name_fidelity_research import initialized

ROOT = Path("work/analysis/contextual_environment_v206")
CANDIDATE = Path("out/all_routes_combined_v205_candidate.nds")
TARGET, VIEW = 0x02460020, 0x02470020
SDK_OPEN, SDK_READ, SDK_CLOSE = 0x020DED50, 0x020DEBDC, 0x020DED08
TOWNS = (32, 33, 35, 37)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert sha(CANDIDATE.read_bytes()) == "88444cb34139aada935f81b39b478fa81b5f54a32ef7c88a7e08b2b3dfe1dfa0"
    image = NdsImage.open(CANDIDATE)
    clean = NdsImage.open("work/clean.nds")
    arm, jp = image.read_file("/__arm9__.bin"), clean.read_file("/__arm9__.bin")
    ranges = [(0xB7158, 0xB7294), (0xB7F5C, 0xB8014), (0xB8220, 0xB822C),
              (0xD3D30, 0xD42AC), (0xD6524, 0xD6C90)]
    assert all(arm[lo:hi] == jp[lo:hi] for lo, hi in ranges)
    u = initialized(arm)
    old = machine(jp)
    registry = resource_call(u, 0x10E190, ())
    manager = struct.unpack_from("<I", arm, 0x5D24)[0]
    call(u, 0xD6C0C, (manager,))
    labels = []
    for index in range(12):
        call(old, 0xB8220, (index,))
        p = old.reg_read(UC_ARM_REG_R0)
        japanese = bytes(old.mem_read(p, 64)).split(b"\0")[0].decode("cp932")
        call(u, 0xB8220, (index,))
        p = u.reg_read(UC_ARM_REG_R0)
        english = bytes(u.mem_read(p, 64)).split(b"\0")[0].decode("ascii")
        labels.append({"facility_index": index, "Japanese": japanese, "English": english,
                       "actual_caption_getter_and_complete_return": True})
    assert labels[4]["Japanese"] == "酒場" and labels[4]["English"] == "Tavern"
    assert labels[8]["Japanese"] == "宿屋" and labels[8]["English"] == "Inn"
    handles, events = {}, []

    def bridge(uc, address, size, _):
        if address == 0x020E5650:
            raise ValueError("Native image reader reached its fatal assertion")
        if address not in (SDK_OPEN, SDK_READ, SDK_CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == SDK_OPEN:
            pointer = uc.reg_read(UC_ARM_REG_R1)
            name = bytes(uc.mem_read(pointer, 128)).split(b"\0")[0].decode("ascii")
            path = "/" + name.replace("\\", "/").lstrip("/")
            raw = image.read_file(path)
            assert obj not in handles
            handles[obj] = (path, raw)
            uc.mem_write(obj + 0x20, struct.pack("<2I", 0, len(raw)))
            events.append({"operation": "open", "path": path, "bytes": len(raw), "sha256": sha(raw)})
            result = 1
        elif address == SDK_READ:
            path, raw = handles[obj]
            destination, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            assert count == len(raw)
            uc.mem_write(destination, raw)
            events.append({"operation": "read", "path": path, "bytes": count, "destination": destination})
            result = count
        else:
            path, _ = handles.pop(obj)
            events.append({"operation": "close", "path": path})
            result = 1
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, bridge)
    icons, towns = [], []
    try:
        for index in (4, 8):
            for variant in (0, 1):
                # Execute the actual branch/MLA selector with preceding function
                # arguments supplied. This is not the full town UI constructor.
                for reg, value in ((UC_ARM_REG_R0, TARGET), (UC_ARM_REG_R2, index), (UC_ARM_REG_R3, variant)):
                    u.reg_write(reg, value)
                u.emu_start(0x020B7F68, 0x020B7F84, count=32)
                expected = 0x0211AB90 if variant else 0x0211AA40
                row_pointer = u.reg_read(UC_ARM_REG_R4)
                assert row_pointer == expected + index * 28
                owner, width, height, x, y, anchor_x, anchor_y = struct.unpack("<7I", u.mem_read(row_pointer, 28))
                name_pointer = struct.unpack("<I", u.mem_read(owner + 12, 4))[0]
                filename = bytes(u.mem_read(name_pointer, 96)).split(b"\0")[0].decode("ascii")
                path = "/" + filename.replace("\\", "/").lstrip("/")
                raw = image.read_file(path)
                p = PxlImage.from_bytes(raw)
                assert (width, height) == (p.width, p.height)
                u.mem_write(VIEW - 16, b"\xA5" * 80)
                u.mem_write(VIEW, bytes(48))
                u.mem_write(STACK, struct.pack("<4I", width, height, 0, 0))
                start = len(events)
                call(u, 0xD3D30, (VIEW, owner, 0, 0))
                resource_call(u, 0xD4170, (VIEW,))
                pointer = u.reg_read(UC_ARM_REG_R0)
                assert bytes(u.mem_read(pointer, len(raw))) == raw
                assert bytes(u.mem_read(VIEW - 16, 16)) == bytes(u.mem_read(VIEW + 48, 16)) == b"\xA5" * 16
                assert not handles
                icons.append({"facility_index": index, "variant_nonzero": bool(variant), "path": path,
                              "actual_owner": owner, "source_sha256": sha(raw), "native_extent": [width, height],
                              "parent_local_origin": [x, y], "parent_anchor": [anchor_x, anchor_y],
                              "caption": labels[index], "full_native_loaded_header_palette_and_pixels_exact": True,
                              "SDK_IO": events[start:]})
        for index in TOWNS:
            path = f"/towngrp/towngrp{index:02d}.pxl"
            raw = image.read_file(path)
            assert raw == clean.read_file(path)
            p = PxlImage.from_bytes(raw)
            blank = bytearray(raw)
            palette_offset = struct.unpack_from("<I", raw, 12)[0]
            blank[palette_offset:] = bytes(len(raw) - palette_offset)
            u.mem_write(TARGET - 16, b"\xA5" * (len(raw) + 32))
            u.mem_write(TARGET, bytes(blank))
            scratch = 0x02233040
            u.mem_write(scratch - 16, b"\xA5" * (len(raw) + 32))
            start = len(events)
            trace = resource_call(u, 0xB7260, (TARGET, index))
            assert {0x020B7260, 0x020B7158, 0x020D7720} <= trace
            assert bytes(u.mem_read(TARGET, len(raw))) == raw
            assert bytes(u.mem_read(TARGET - 16, 16)) == bytes(u.mem_read(TARGET + len(raw), 16)) == b"\xA5" * 16
            assert bytes(u.mem_read(scratch, len(raw))) == raw
            assert bytes(u.mem_read(scratch - 16, 16)) == bytes(u.mem_read(scratch + len(raw), 16)) == b"\xA5" * 16
            assert not handles
            towns.append({"index_argument": index, "actual_formatted_filename": path, "source_sha256": sha(raw),
                          "dimensions": [p.width, p.height], "bits_per_pixel": p.bits_per_pixel,
                          "complete_native_palette_and_pixel_copy_exact": True, "all_buffer_and_ABI_guards_pass": True,
                          "SDK_IO": events[start:]})
    finally:
        u.hook_del(hook)
    report = {"format": "dk4-contextual-environment-native-proof-v1", "ROM": CANDIDATE.as_posix(),
              "ROM_sha256": sha(CANDIDATE.read_bytes()), "ARM9_sha256": sha(arm), "caption_getters": labels,
              "native_icon_selector_and_loader_cases": icons, "native_town_filename_reader_cases": towns,
              "native_registry_instructions": len(registry), "SDK_IO_only_bridged": True,
              "all_handles_closed": not handles, "ROM_or_artwork_changed": False,
              "scope": "Actual selector fragments, caption getters, native image/cache loading and dynamic filename/header/palette/pixel copies. Supplied variant/index/target inputs; full city assignment, complete town UI construction, GPU/live cropping/input/gameplay remain outside this proof.",
              "full_goal_complete": False}
    (ROOT / "native_environment_proof.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_caption_getters": len(labels) * 2, "native_paired_icons": len(icons),
                      "native_complete_town_copies": len(towns), "handles_closed": not handles}))


if __name__ == "__main__":
    main()
