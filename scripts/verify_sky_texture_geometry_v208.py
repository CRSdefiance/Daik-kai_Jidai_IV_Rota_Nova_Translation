"""Confirm sky texture format and reviewable source extents without changing ROM."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R12, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, machine

ROOT = Path("work/analysis/sky_texture_geometry_v208")
CANDIDATE = Path("out/all_routes_combined_v205_candidate.nds")
SOURCE = Path("work/analysis/skywall_native_v207/proof.json")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    previous = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert sha(CANDIDATE.read_bytes()) == previous["ROM_sha256"]
    rom = NdsImage.open(CANDIDATE)
    clean = NdsImage.open("work/clean.nds")
    arm = rom.read_file("/__arm9__.bin")
    original = clean.read_file("/__arm9__.bin")
    assert arm[0x6B0F8:0x6B11C] == original[0x6B0F8:0x6B11C]
    assert arm[0x6B244:0x6B250] == original[0x6B244:0x6B250]
    raw = rom.read_file("/GRP/SKYWALL.DK4")
    assert sha(raw) == previous["source_sha256"] and raw == clean.read_file("/GRP/SKYWALL.DK4")
    u = machine(arm)
    u.mem_map(0x04000000, 0x10000)
    writes = []
    hook = u.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, data:
                     writes.append({"address": address, "bytes": size, "value": value}))
    u.reg_write(UC_ARM_REG_SP, STACK)
    # The preceding native LDR at 6B0E0 supplies the matrix-mode register.
    matrix_register = struct.unpack_from("<I", arm, 0x6B23C)[0]
    assert matrix_register == 0x04000440
    u.reg_write(UC_ARM_REG_R12, matrix_register)
    try:
        u.emu_start(0x0206B0F8, 0x0206B11C, count=10)
    finally:
        u.hook_del(hook)
    assert u.reg_read(UC_ARM_REG_PC) == 0x0206B11C and u.reg_read(UC_ARM_REG_SP) == STACK
    assert writes == [{"address": matrix_register, "bytes": 4, "value": 2},
                      {"address": 0x040004A8, "bytes": 4, "value": 0x71531E00},
                      {"address": 0x040004AC, "bytes": 4, "value": 0x80}]
    fmt = writes[1]["value"]
    width, height, mode = 8 << ((fmt >> 20) & 7), 8 << ((fmt >> 23) & 7), (fmt >> 26) & 7
    texture_offset = (fmt & 65535) * 8
    assert (width, height, mode, texture_offset) == (256, 32, 4, 0xF000)
    assert writes[2]["value"] * 16 == 0x800
    rows = []
    sheet = Image.new("RGB", (4 * 276, 4 * 96), (230, 230, 230))
    draw = ImageDraw.Draw(sheet)
    for record in previous["records"]:
        index, offset, size = record["index"], record["offset"], record["bytes"]
        loaded = raw[offset:offset + size]
        assert sha(loaded) == record["complete_native_read_sha256"]
        pixels, palette_bytes = loaded[:-512], loaded[-512:]
        source_height = len(pixels) // width
        assert len(pixels) == width * source_height
        assert source_height == (64 if index == 13 else height)
        values = struct.unpack("<256H", palette_bytes)
        colors = [tuple((c << 3) | (c >> 2) for c in (v & 31, (v >> 5) & 31, (v >> 10) & 31))
                  for v in values]
        source = Image.new("P", (width, source_height))
        source.putpalette([c for color in colors for c in color])
        source.putdata(pixels)
        assert source.tobytes() == pixels
        path = ROOT / f"sky_{index:02d}_complete_source.png"
        source.save(path)
        with Image.open(path) as saved:
            assert saved.tobytes() == pixels
            assert saved.convert("RGB").tobytes() == source.convert("RGB").tobytes()
        x, y = index % 4 * 276, index // 4 * 96
        sheet.paste(source.convert("RGB"), (x, y + 20))
        draw.text((x, y), f"{index}: 256 x {source_height}", fill=(0, 0, 0))
        rows.append({"index": index, "source_extent": [width, source_height],
                     "complete_source_indices": len(pixels), "indices_sha256": sha(pixels),
                     "palette_sha256": sha(palette_bytes), "PNG": path.as_posix(),
                     "PNG_sha256": sha(path.read_bytes()), "all_source_indices_and_RGB_preserved": True,
                     "regular_texture_extent_matches_loaded_pixel_count": index != 13,
                     "exceptional_second_32_rows_sampling_pending": index == 13,
                     "visual_source_review": "pending"})
    sheet.save(ROOT / "all14_complete_source.png")
    capture_root = Path("work/emulation_v193/raw_graphics_v208/normal_sailing")
    report = json.loads((capture_root / "capture_report.json").read_text(encoding="utf-8"))
    assert report["ROM_sha256"] == previous["ROM_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    ram_row = report["read_only_RAM_snapshot"]
    ram = Path(ram_row["path"]).read_bytes()
    assert len(ram) == 0x400000 and sha(ram) == ram_row["sha256"]
    state_pointer = struct.unpack_from("<I", arm, 0xCB1BC)[0]
    assert state_pointer == 0x022CFD54
    current_selector = ram[state_pointer - 0x02000000 + 12]
    assert current_selector < 14
    final = next(r for r in report["frames_captured"] if Path(r["path"]).name == "frame_019500_final.png")
    assert sha(Path(final["path"]).read_bytes()) == final["PNG_sha256"]
    proof = {"format": "dk4-sky-texture-source-geometry-v1", "ROM_sha256": previous["ROM_sha256"],
             "prior_native_loader_proof": SOURCE.as_posix(), "prior_proof_sha256": sha(SOURCE.read_bytes()),
             "native_format_command_writes": writes, "texture_geometry": [width, height],
             "texture_format": "256-palette-entry indexed texture", "texture_byte_offset": texture_offset,
             "palette_byte_offset": 0x800, "texture_register_fragment_only_no_GPU_emulated": True,
             "hardware_field_reference": [
                 "https://github.com/devkitPro/libnds/blob/master/include/nds/arm9/videoGL.h",
                 "https://github.com/devkitPro/libnds/blob/master/include/nds/arm9/video.h"],
             "all14_complete_source_views": rows, "source_pixels_reviewable": sum(r["complete_source_indices"] for r in rows),
             "unmodified_candidate_cold_boot_sailing": {"capture": final, "read_only_RAM_snapshot": ram_row,
                                                        "current_environment_selector": current_selector,
                                                        "actual_sky_projection_not_proved_by_this_capture": True},
             "exceptional_record13_second_half_sampling_pending": True,
             "native_scene_projection_crop_GPU_and_depth_test_pending": True,
             "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"regular_native_texture_geometry": [width, height], "source_views": len(rows),
                      "complete_source_pixels": proof["source_pixels_reviewable"], "actual_live_environment_selector": current_selector}))


if __name__ == "__main__":
    main()
