"""Execute all TITLEMAP parent reads, palette preparation and bitmap construction."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine

ROOT = Path("work/analysis/titlemap_v221")
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom, clean = NdsImage.open("out/all_routes_combined_v218_candidate.nds"), NdsImage.open("work/clean.nds")
    arm = rom.read_file("/__arm9__.bin")
    raw = rom.read_file("/GRP/TITLEMAP.DK4")
    assert raw == clean.read_file("/GRP/TITLEMAP.DK4")
    assert arm[0x4BAB8:0x4BC88] == clean.read_file("/__arm9__.bin")[0x4BAB8:0x4BC88]
    size, buffer, palette = struct.unpack_from("<3I", arm, 0x4BC74)
    assert (size, buffer, palette) == (0x4940, 0x02233040, 0x02237780)
    assert palette - buffer == 152 * 120 and len(raw) == 56 * size
    u = machine(arm)
    handles, events = {}, []

    def sdk(uc, address, width, _):
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            name = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1), 64)).split(b"\0")[0].decode("ascii").replace("\\", "/")
            assert name == "/GRP/TITLEMAP.DK4" and not handles
            handles[obj] = 0
            uc.mem_write(obj + 0x20, struct.pack("<2I", 0, len(raw)))
            value = 1
            events.append({"operation": "open", "path": name})
        elif address == SEEK:
            position = uc.reg_read(UC_ARM_REG_R1)
            assert uc.reg_read(UC_ARM_REG_R2) == 0 and 0 <= position <= len(raw)
            handles[obj] = position
            value = 1
            events.append({"operation": "seek", "offset": position})
        elif address == READ:
            target, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            position = handles[obj]
            assert target == buffer and count == size and position + count <= len(raw)
            uc.mem_write(target, raw[position:position + count])
            handles[obj] += count
            value = count
            events.append({"operation": "read", "offset": position, "bytes": count})
        else:
            handles.pop(obj)
            value = 1
            events.append({"operation": "close"})
        uc.reg_write(UC_ARM_REG_R0, value)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    h = u.hook_add(UC_HOOK_CODE, sdk)
    records = []
    sheet = Image.new("RGB", (8 * 160, 7 * 144), (230, 230, 230))
    draw = ImageDraw.Draw(sheet)
    try:
        for region in range(7):
            for variant in range(8):
                index = region * 8 + variant
                start = len(events)
                file_object = STACK + 0x10
                call(u, 0xD05D0, (file_object,))
                call(u, 0xD0398, (file_object, 0x0213E2CC, 0))
                assert u.reg_read(UC_ARM_REG_R0) == 1
                u.mem_write(buffer - 16, b"\xa5" * (size + 32))
                u.reg_write(UC_ARM_REG_SP, STACK)
                u.reg_write(UC_ARM_REG_R4, variant)
                u.reg_write(UC_ARM_REG_R5, region)
                u.emu_start(0x0204BB0C, 0x0204BBC0, count=100000)
                assert u.reg_read(UC_ARM_REG_PC) == 0x0204BBC0 and u.reg_read(UC_ARM_REG_SP) == STACK
                assert not handles
                source = raw[index * size:(index + 1) * size]
                expected_palette = struct.pack("<256H", *(v | 0x8000 for v in struct.unpack("<256H", source[-512:])))
                assert bytes(u.mem_read(buffer, size)) == source[:-512] + expected_palette
                assert bytes(u.mem_read(buffer - 16, 16)) == b"\xa5" * 16
                assert bytes(u.mem_read(buffer + size, 16)) == b"\xa5" * 16
                header = bytes(u.mem_read(STACK + 0x38, 20))
                flags, pitch, height, pal_delta, pixels_delta = struct.unpack("<5I", header)
                assert (flags, pitch, height) == (0x108, 76, 120)
                assert (STACK + 0x38 + pal_delta) & 0xFFFFFFFF == palette
                assert (STACK + 0x38 + pixels_delta) & 0xFFFFFFFF == buffer
                dimensions = struct.unpack("<2I", u.mem_read(STACK + 0x4C + 0x28, 8))
                assert dimensions == (152, 120)
                colors = [c for v in struct.unpack("<256H", source[-512:])
                          for c in ((v & 31) * 255 // 31, (v >> 5 & 31) * 255 // 31, (v >> 10 & 31) * 255 // 31)]
                im = Image.new("P", dimensions)
                im.putpalette(colors)
                im.putdata(source[:-512])
                path = ROOT / f"native_frame_{index:02d}.png"
                im.save(path)
                assert im.tobytes() == source[:-512]
                x, y = variant * 160, region * 144
                sheet.paste(im.convert("RGB"), (x, y + 20))
                draw.text((x, y), str(index), fill="black")
                records.append({"index": index, "region_fixture": region, "variant_fixture": variant,
                                "offset": index * size, "bytes": size, "source_sha256": sha(source),
                                "source_indices_sha256": sha(source[:-512]), "source_palette_sha256": sha(source[-512:]),
                                "native_palette_alpha_bit_only_added": True, "complete_native_read_and_buffer_guards_exact": True,
                                "native_bitmap_dimensions": list(dimensions), "native_bitmap_header_hex": header.hex(),
                                "native_header_pitch_words": pitch, "actual_pixel_bytes": 152 * 120,
                                "original_parent_read_palette_and_bitmap_constructor_executed": True,
                                "preview": path.as_posix(), "preview_sha256": sha(path.read_bytes()), "events": events[start:]})
    finally:
        u.hook_del(h)
    sheet.save(ROOT / "all56_native_source.png")
    proof = {"format": "dk4-titlemap-native-source-proof-v1", "ROM_sha256": sha(rom.source.read_bytes()),
             "source_file": "/GRP/TITLEMAP.DK4", "source_file_sha256": sha(raw), "file_bytes": len(raw),
             "record_bytes": size, "native_pixel_buffer": buffer, "native_palette_buffer": palette,
             "native_record_partition_complete": True, "records": records,
             "complete_source_indices": 56 * 152 * 120, "complete_source_palettes": 56 * 512,
             "all_handles_closed": not handles, "region_and_variant_are_explicit_preceding_getter_fixtures": True,
             "SDK_file_operations_are_bridges_to_exact_current_ROM": True,
             "native_final_bitmap_blend_crop_GPU_input_and_scene_selection_pending": True,
             "source_visual_review_complete": False, "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "native_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_map_records": len(records), "complete_source_indices": proof["complete_source_indices"],
                      "source_bytes": len(raw), "dimensions": [152, 120], "all_reads_headers_palettes_and_guards_pass": True}))


if __name__ == "__main__":
    main()
