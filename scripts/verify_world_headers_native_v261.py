"""Complete native fleet-name formatting, glyph bounds and inherited boot checks."""

import json
import struct

from ndspy.code import MainCodeFile

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.world_map_headers import BASE, POOL, ROOT
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_common_itcm_arena_reservation import initialize
from scripts.probe_persistent_name_arm7_boot_overlap import execute


def main():
    arm = (ROOT / "research_arm9.bin").read_bytes()
    plan = json.loads((ROOT / "runtime_plan.json").read_text(encoding="utf-8"))
    u = machine(arm)
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    u.mem_write(POOL, payload)
    font = GameAsciiFont.from_arm9(arm)
    metrics = struct.unpack_from("<I", arm, 0xD5088)[0]
    u.mem_write(metrics + 4, struct.pack("<2I", 6, 16))
    header, view, ctx, name = 0x02450000, 0x02454000, 0x02455000, 0x02456000
    cases = []
    for record in plan["records"]:
        pointer = record["target_pointer"]
        text = bytes(u.mem_read(pointer, 64)).split(b"\0", 1)[0].decode("ascii")
        assert text == record["English"]
        names = ["Lil Fleet", "Fleet", "Indigo", "ABCDEFGHIJKLMNOPQR"] + ["W" * n for n in range(1, 19)] if "%s" in text else [None]
        for fleet in names:
            width, height = 172, 16
            raw_header = struct.pack("<5I", 4, width // 4, height, 0x02453000 - header, 20)
            u.mem_write(header - 16, b"\xA5" * (20 + width * height // 2 + 32))
            u.mem_write(header, raw_header + bytes(width * height // 2))
            u.mem_write(view - 16, b"\xA5" * 80)
            call(u, 0xD3D80, (view,))
            u.mem_write(STACK, struct.pack("<4I", width, height, 0, 0))
            call(u, 0xD3AFC, (view, header, 0, 0))
            call(u, 0xD5160, (ctx, view, 1))
            if fleet is None:
                expected = text
                call(u, 0xD5404, (ctx, pointer))
            else:
                u.mem_write(name, fleet.encode("ascii") + b"\0")
                expected = text.replace("%s", fleet)
                call(u, 0xD5200, (ctx, pointer, name))
            p = bytes(u.mem_read(header + 20, width * height // 2))
            indices = bytes(n for b in p for n in (b & 15, b >> 4))
            mask = bytearray(width * height)
            for n, ch in enumerate(expected):
                g = font.decode(ch)
                for y in range(11):
                    for x in range(6):
                        if g.getpixel((x, y)):
                            assert n * 6 + x < width
                            mask[y * width + n * 6 + x] = 1
            assert indices == mask
            assert bytes(u.mem_read(header - 16, 16)) == bytes(u.mem_read(header + 20 + width * height // 2, 16)) == b"\xA5" * 16
            assert bytes(u.mem_read(view - 16, 16)) == bytes(u.mem_read(view + 48, 16)) == b"\xA5" * 16
            cases.append({"pointer_field": record["field"], "fleet": fleet, "full_English": expected,
                          "complete_native_font_ink_pixels": sum(mask), "first_internal_final_glyphs_and_bounds_exact": True})
    rom = NdsImage.open("out/all_routes_combined_v260_candidate.nds")
    boot = execute(arm, bytes(rom.rom.arm7), rom.rom.arm7RamAddress,
                   repair_entry=plan["cache"]["entry"], expected_pool=payload)
    proof = {"format": "dk4-world-headers-native-v261", "cases": cases,
             "complete_selection_labels_fit172_pixel_contract": True,
             "native_printf_and_complete_font_pixels_guards_stack_saved_registers_pass": True,
             "actual_centered_header_and_instruction_GPU_pending": True,
             "boot": boot, "arena": initialize(arm), "all18_plaques_remain_incomplete": True,
             "actual_GPU_cold_boot_pending": True}
    (ROOT / "native_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(f"{len(cases)} complete native rank/name raster cases and inherited boot/cache/ARM7 checks pass.")


if __name__ == "__main__":
    main()
