"""Verify both notice presentations, sprite bounds, upload and native startup."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R8,
    UC_ARM_REG_R10,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.sailing_no_target import (
    GRAPHIC_POINTER,
    MAIN_OBJ_FIRST_TILE,
    MAIN_OBJ_OFFSET,
    UPLOAD_BYTES,
    prepare,
    transform,
)
from dk4tool.rom.nds import NdsImage
from scripts.execute_scene_caption_raster import execute as raster
from scripts.probe_button_prompt_native import STACK, call
from scripts.probe_common_itcm_arena_reservation import initialize
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels
from scripts.probe_persistent_name_arm7_boot_overlap import execute as boot
from scripts.verify_sailing_panel_packing_v215 import read_pixel
from scripts.verify_sailing_panels_v217 import make_machine

ROOT = Path("work/analysis/no_target_v218")
BUFFER = 0x02460020
RAM = Path("work/emulation_v193/generated_modes_v213/final_arm9_ram.bin")


def main():
    rom = NdsImage.open("out/all_routes_combined_v217_candidate.nds")
    source = rom.read_file("/__arm9__.bin")
    canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/__arm9__.bin")
    manuscript = json.loads(Path("translations/sailing_no_attack_target_manuscript_v1.json").read_text(encoding="utf-8"))
    saved, plan = transform(source, canonical, manuscript)
    assert saved == (ROOT / "English_arm9.bin").read_bytes()
    panel = prepare(source, manuscript)
    u = make_machine(saved, rom)
    u.mem_write(BUFFER - 16, b"\xa5" * (UPLOAD_BYTES + 32))
    call(u, plan["producer_entry"] - BASE, (GRAPHIC_POINTER, 1, BUFFER))
    produced = bytes(u.mem_read(BUFFER, UPLOAD_BYTES))
    assert produced == panel["packed"]
    assert bytes(u.mem_read(BUFFER - 16, 16)) == b"\xa5" * 16
    assert bytes(u.mem_read(BUFFER + UPLOAD_BYTES, 16)) == b"\xa5" * 16
    requests = []
    image = Image.new("L", (256, 176), 0)

    def draw_bridge(uc, address, size, _):
        if address != BASE + 0x89358:
            return
        kind, point, descriptor, tile = [uc.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        x0, y0 = struct.unpack("<2I", uc.mem_read(point, 8))
        assert kind == 0 and descriptor == 0x80004000
        assert 0 <= x0 < x0 + 32 <= 256 and 0 <= y0 < y0 + 16 <= 176
        requests.append({"origin": [x0, y0 + 192], "first_tile": tile, "descriptor": descriptor})
        for y in range(16):
            for x in range(32):
                virtual_x = (tile - MAIN_OBJ_FIRST_TILE) // 8 * 32 + x
                image.putpixel((x0 + x, y0 + y), 255 if read_pixel(produced, virtual_x, y) else 0)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    h = u.hook_add(UC_HOOK_CODE, draw_bridge)
    call(u, plan["draw_entry"] - BASE, (0, STACK, 0x80004000, 0x200))
    u.hook_del(h)
    assert len(requests) == 8
    expected = Image.new("L", image.size, 0)
    font = GameAsciiFont.from_arm9(saved)
    for glyph in panel["glyphs"]:
        x0, y0 = glyph["origin"]
        mask = font.decode(glyph["character"])
        for y in range(11):
            for x in range(6):
                if mask.getpixel((x, y)):
                    expected.putpixel((x0 + x, y0 - 192 + y), 255)
    assert expected.tobytes() == image.tobytes()
    image.save(ROOT / "English_main_sprite_preview.png")
    # Execute the exact original startup producer/cache/upload span. Only the SDK
    # cache and VRAM transfer are bridged; their whole source and offsets are checked.
    upload = make_machine(saved, rom)
    native_buffer = 0x022E1794
    upload.mem_write(native_buffer - 16, b"\xa5" * (UPLOAD_BYTES + 32))
    upload.reg_write(UC_ARM_REG_R8, native_buffer)
    upload.reg_write(UC_ARM_REG_SP, STACK)
    operations = []

    def sdk(uc, address, size, _):
        if address not in (BASE + 0xE4430, BASE + 0xE1E40):
            return
        args = [uc.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)]
        assert args[0] == native_buffer
        if address == BASE + 0xE4430:
            assert args[1] == UPLOAD_BYTES
        else:
            assert args[1:] == [MAIN_OBJ_OFFSET, UPLOAD_BYTES]
            assert bytes(uc.mem_read(native_buffer, UPLOAD_BYTES)) == produced
        operations.append({"function": address, "arguments": args})
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    h = upload.hook_add(UC_HOOK_CODE, sdk)
    upload.emu_start(BASE + 0x7B91C, BASE + 0x7B948, count=100000)
    upload.hook_del(h)
    assert upload.reg_read(UC_ARM_REG_PC) == BASE + 0x7B948 and len(operations) == 2
    assert bytes(upload.mem_read(native_buffer - 16, 16)) == b"\xa5" * 16
    assert bytes(upload.mem_read(native_buffer + UPLOAD_BYTES, 16)) == b"\xa5" * 16
    # The original DSOBJ upload is 0..3E00; DSOBJR is 4000..5520. The original
    # Japanese notice reused 4000..4600. Place the larger English copy at 5600
    # so no additional original prefix bytes are overwritten. The six DSCHR
    # startup uploads use the separate texture upload function E21B8.
    metadata = struct.unpack_from("<I", source, 0x7BB54)[0] - BASE
    assert 0 <= metadata < len(source) - 84
    texture_records = [list(struct.unpack_from("<3I", source, metadata + n * 12)) for n in range(6)]
    prefix_end = 0x4000 + struct.unpack_from("<I", source, 0xF3C)[0]
    assert prefix_end == 0x5520
    assert prefix_end <= MAIN_OBJ_OFFSET and MAIN_OBJ_OFFSET + UPLOAD_BYTES <= 0x8000
    # Execute original constructor/render call with the real captured object binding.
    # Its bitmap is not a CPU paintable surface in this capture; font pixels below
    # use the established explicit generic bitmap/font contract and are scoped as such.
    ctor = make_machine(saved, rom)
    ctor.mem_write(BASE, RAM.read_bytes())
    first = MainCodeFile(saved, BASE).sections[0]
    ctor.mem_write(first.ramAddress, bytes(first.data))
    payload = bytes(MainCodeFile(saved, BASE).sections[3].data[:-48])
    from dk4tool.patch.main_pool_cache_visibility import POOL
    ctor.mem_write(POOL, payload)
    ctor.reg_write(UC_ARM_REG_R10, 0x0218D038)
    ctor.reg_write(UC_ARM_REG_SP, STACK)
    ctor.emu_start(BASE + 0x70004, BASE + 0x70068, count=1000000)
    assert ctor.reg_read(UC_ARM_REG_PC) == BASE + 0x70068
    dimensions = struct.unpack("<2I", ctor.mem_read(0x0218D0B8 + 0x28, 8))
    assert dimensions == (120, 24)
    assert bytes(ctor.mem_read(plan["compiled_pointer"], len(panel["compiled"]) + 1)) == panel["compiled"].encode("ascii") + b"\0"
    font_cases = []
    for mode in (4, 16):
        result = raster(saved, panel["compiled"], tooltip=True, tracking=0, x=0, y=0,
                        mode=mode, kanji_font=rom.read_file("/GRP/KANJI.FNT"))
        glyphs = result["glyph_events"]
        content = [g for g in glyphs if g["code"] != 32]
        assert [g["code"] for g in content] == [ord(c) for c in panel["english"] if c != " "]
        assert all(0 <= g["x"] < g["x"] + 6 <= 120 and 0 <= g["y"] < g["y"] + 11 <= 24 for g in content)
        assert result["pixels"] == expected_pixels(saved, rom.read_file("/GRP/KANJI.FNT"), glyphs, mode, background=0)
        font_cases.append({"mode": mode, "glyph_events": glyphs, "complete_glyphs_and_bounds_exact": True,
                           "pixel_sha256": sha(result["pixels"]),
                           "explicit_generic_surface_binding_larger_than_crop": [256, 192],
                           "every_glyph_within_actual_notice_view": [120, 24]})
    startup = boot(saved, bytes(rom.rom.arm7), rom.rom.arm7RamAddress, True, payload)
    assert startup["arm7_source_changed_bytes_after_arm9_autoload"] == 0
    assert all(row["matches_original"] for row in startup["arm7_native_loaded_sections"])
    assert startup["repaired_pool_matches_complete_payload"]
    arenas = initialize(saved)
    assert arenas["low"][0] == plan["pool_span"][1]
    previous_arenas = initialize(source)
    assert arenas["low"][1:] == previous_arenas["low"][1:] and arenas["high"] == previous_arenas["high"]
    proof = {"format": "dk4-no-target-native-proof-v1", "target_arm9_sha256": sha(saved), "plan": plan,
             "native_producer_and_eight_sprite_requests_exact": True, "sprite_requests": requests,
             "complete_sprite_ink_and_blank_pixels_exact": 256 * 176, "startup_upload_operations": operations,
             "Main_OBJ_upload_span": [MAIN_OBJ_OFFSET, MAIN_OBJ_OFFSET + UPLOAD_BYTES],
             "original_DSOBJ_and_DSOBJR_upload_spans": [[0, 0x3E00], [0x4000, prefix_end]],
             "separate_DSCHR_texture_upload_records": texture_records,
             "original_notice_upload_does_not_overlap_other_startup_regions": True,
             "ownership_scope": "Original DSOBJ prefix and this main-OBJ upload; DSCHR texture uploads use a separate destination. Other gameplay allocation/usage is not inferred unused.",
             "ordinary_native_constructor_dimensions": list(dimensions), "ordinary_font_cases": font_cases,
             "ordinary_font_first_last_glyphs_and_bounds_exact": True,
             "ordinary_pixels_use_explicit_generic_binding_not_captured_unpaintable_bitmap": True,
             "native_sprite_submission_and_SDK_upload_are_explicit_bridges": True,
             "startup": startup, "arenas": arenas,
             "cold_boot_gameplay_pending": True, "full_goal_complete": False}
    (ROOT / "native_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_native_sprite_requests": 8, "whole_sprite_pixels": 256 * 176,
                      "ordinary_font_modes": 2, "ordinary_view": list(dimensions), "startup_ARM7_preserved": True}))


if __name__ == "__main__":
    main()
