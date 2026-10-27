"""Execute original gender crop branches; keep prior person state and GPU unproved."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R4,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R10,
    UC_ARM_REG_SP,
)

from dk4tool.graphics.compact_font import GENDER_GLYPHS
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, machine
from scripts.research_online_loader_v190 import resource_call
from scripts.verify_title_display_v229 import ROM, ROM_SHA, native_views

OUT = Path("work/analysis/gender_consumers_v240")
MARKER = "/_pxl/__marker.pxl"
OWNER = 0x02313F74
PARENT = 0x02460000


def main():
    assert sha(ROM.read_bytes()) == ROM_SHA
    rom = NdsImage.open(ROM)
    arm = rom.read_file("/__arm9__.bin")
    clean = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    for lo, hi in [(0x15870, 0x158DC), (0x80470, 0x804E4), (0xD3B34, 0xD42AC)]:
        assert arm[lo:hi] == clean[lo:hi]
    loading = native_views(rom, expected_paths={MARKER}, owner_range=(OWNER, OWNER + 20))
    loading.pop("physical_title05_and_standalone_logo_display_not_inferred_from_fixture")
    image = PxlImage.from_bytes(rom.read_file(MARKER))
    assert (image.width, image.height) == (256, 256)
    u = machine(arm)
    resource_call(u, 0x10E190, ())
    object_offset = struct.unpack_from("<I", arm, 0x80A40)[0]
    assert object_offset < 0x10000
    cases = []
    sheet = Image.new("RGB", (320, 200), "#e4e4e4")
    draw = ImageDraw.Draw(sheet)
    for parent_index, (start, end, selector, base_reg, offset) in enumerate((
        (0x02015870, 0x020158DC, UC_ARM_REG_R8, UC_ARM_REG_R7, 0xA0),
        (0x02080470, 0x020804E4, UC_ARM_REG_R4, UC_ARM_REG_R10, object_offset),
    )):
        for value, symbol, origin, ink_origin in ((0, "♂", (232, 96), (237, 100)),
                                                  (1, "♀", (240, 112), (246, 115))):
            dest = PARENT + offset
            u.mem_write(dest - 16, b"\xa5" * 80)
            u.mem_write(dest, bytes(48))
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(base_reg, PARENT)
            u.reg_write(selector, value)
            u.emu_start(start, end, count=100000)
            assert u.reg_read(UC_ARM_REG_PC) == end
            assert u.reg_read(UC_ARM_REG_SP) == STACK
            fields = struct.unpack("<12I", u.mem_read(dest, 48))
            assert fields[3] == OWNER and fields[7:9] == origin
            assert fields[10:12] == (16, 16)
            assert bytes(u.mem_read(dest - 16, 16)) == b"\xa5" * 16
            assert bytes(u.mem_read(dest + 48, 16)) == b"\xa5" * 16
            rows = GENDER_GLYPHS[symbol]
            ink = [(ink_origin[0] + x, ink_origin[1] + y)
                   for y, row in enumerate(rows) for x, bit in enumerate(row) if bit == "1"]
            assert all(origin[0] <= x < origin[0] + 16 and origin[1] <= y < origin[1] + 16
                       and image.indices[y * 256 + x] == 15 for x, y in ink)
            crop = image.render().crop((*origin, origin[0] + 16, origin[1] + 16)).convert("RGB")
            OUT.mkdir(parents=True, exist_ok=True)
            preview = OUT / f"consumer{parent_index}_{value}.png"
            crop.save(preview)
            sx, sy = value * 160, parent_index * 100
            draw.text((sx + 4, sy + 4), f"consumer {parent_index}: {symbol}", fill="black")
            sheet.paste(crop.resize((64, 64), Image.Resampling.NEAREST), (sx + 4, sy + 24))
            cases.append({"branch_start": start, "branch_end": end, "supplied_prior_selector_value": value,
                          "symbol": symbol, "native_owner": OWNER, "native_crop_origin": list(origin),
                          "native_crop_extent": [16, 16], "native_view_fields": list(fields),
                          "complete_symbol_ink_pixels_inside_actual_crop": len(ink),
                          "actual_native_branch_and_crop_setup_executed": True,
                          "stack_and_view_guards_pass": True, "preview": str(preview),
                          "preview_sha256": sha(preview.read_bytes())})
    sheet.save(OUT / "four_actual_crop_previews.png")
    report = {"format": "dk4-native-gender-crops-v240", "ROM_sha256": ROM_SHA,
              "loading": loading, "actual_crop_cases": cases,
              "second_parent_object_view_offset": object_offset,
              "preceding_person_getters_and_surrounding_parent_not_executed": True,
              "supplied_prior_selector_and_object_stack_context": True,
              "GPU_palette_alpha_and_physical_display_pending": True,
              "embedded_CMMNIMG_consumer_not_inferred": True,
              "ROM_modified": False, "full_goal_complete": False}
    (OUT / "native_proof.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"original_parent_crop_cases": len(cases),
                      "complete_symbol_ink_comparisons": sum(c["complete_symbol_ink_pixels_inside_actual_crop"] for c in cases),
                      "actual_marker_loading_verified": True, "physical_display_pending": True}))


if __name__ == "__main__":
    main()
