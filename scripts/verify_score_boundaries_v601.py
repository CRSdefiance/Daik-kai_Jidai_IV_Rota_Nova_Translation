"""Live controllers, original blitter and bitmap-plane checks for V600's 29 gaps."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageChops
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.direct_equipment_paper import FRAMEBUFFER, ORIGIN_X, ORIGIN_Y
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_score_parent_v600 import opaque, quantized

ROOT = Path("work/analysis/score_boundaries_v601")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193")
KINDS = ("current", "original_score_control", "blank_label_control")
OBJECTS, CONTEXT, OWNER = (0x02184B2C, 0x02184BF4), 0x023117C4, 0x02313A38


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def controllers(raw):
    result = []
    for n, address in enumerate(OBJECTS):
        at = address - BASE
        data = raw[at:at + 0xC8]
        assert struct.unpack_from("<I", data)[0] == 0x0213038C
        assert struct.unpack_from("<I", data, 0x34)[0] == 1 - n
        view = struct.unpack_from("<12I", data, 0x98)
        # The original constructor does not zero every spare view word.
        # Guard its documented fields and compare the entire live objects below.
        assert tuple(view[i] for i in (0, 3, 5, 6, 7, 8, 10, 11)) == (
            0x0216017C, OWNER, 4, 0, 160 + n * 24, 0, 24, 24)
        result.append(data)
    return result


def image_seed(image):
    pixels = image.load()
    result = bytearray()
    for y0 in (192, 0):
        for y in range(y0, y0 + 192):
            for x in range(256):
                r, g, b = pixels[x, y]
                result.extend(struct.pack("<H", 0x8000 | r | g << 5 | b << 10))
    return bytes(result)


def buffer_image(data):
    rgb = bytes(channel for (word,) in struct.iter_unpack("<H", data)
                for channel in (word & 31, word >> 5 & 31, word >> 10 & 31))
    screens = Image.frombytes("RGB", (256, 384), rgb)
    result = Image.new("RGB", (256, 384))
    result.paste(screens.crop((0, 192, 256, 384)), (0, 0))
    result.paste(screens.crop((0, 0, 256, 192)), (0, 192))
    return result


def native_parent(arm, raw, seed, pair, resource):
    u = machine(arm)
    u.mem_write(BASE, raw)
    assert bytes(u.mem_read(CONTEXT, 4)) == struct.pack("<I", 0x0215FA94)
    assert struct.unpack("<i", u.mem_read(ORIGIN_X, 4))[0] == struct.unpack("<i", u.mem_read(ORIGIN_Y, 4))[0] == 0
    u.mem_write(FRAMEBUFFER - 16, b"\xA5" * 16)
    u.mem_write(FRAMEBUFFER, seed)
    u.mem_write(FRAMEBUFFER + len(seed), b"\xA5" * 16)
    executed = set()
    for obj, rect in zip(OBJECTS, pair, strict=True):
        # Only observed original animation geometry is supplied to this bounded
        # source replay. The independently captured resident view/owner stays real.
        u.mem_write(obj + 0x20, struct.pack("<4i", *rect))
        executed |= call(u, 0xD4170, (obj + 0x98,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        assert bytes(u.mem_read(pointer, len(resource))) == resource
        executed |= call(u, 0xC054, (obj, CONTEXT), instruction_limit=1000000)
    assert {0x0200C054, 0x020CFDE8, 0x020CFD6C, 0x020D4170, 0x01FF92D8} <= executed
    assert not {0x020DED50, 0x020DEBDC} & executed
    assert bytes(u.mem_read(FRAMEBUFFER - 16, 16)) == bytes(u.mem_read(FRAMEBUFFER + len(seed), 16)) == b"\xA5" * 16
    assert bytes(u.mem_read(pointer, len(resource))) == resource
    return bytes(u.mem_read(FRAMEBUFFER, len(seed)))


def main():
    previous_path = Path("work/analysis/material_review_v600/native_score_parent_proof.json")
    previous = read(previous_path)
    assert previous["script_sha256"] == sha(Path("scripts/verify_score_parent_v600.py").read_bytes())
    production = Path(previous["production_ROM"])
    assert sha(production.read_bytes()) == previous["production_ROM_sha256"]
    arm = NdsImage.open(production).read_file("/__arm9__.bin")
    clean_arm = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    assert arm[0xC054:0xC0FC] == clean_arm[0xC054:0xC0FC]
    assert arm[0xCFD6C:0xCFE64] == clean_arm[0xCFD6C:0xCFE64]
    frames = read(ROOT / "frames.json")
    old_results = previous["native_three_way_frame_results"]
    pending = sorted(old_results["no_digit_anchor"] + [r["frame"] for r in old_results["whole_composite_mismatch"]])
    assert len(pending) == 29 and set(pending) <= set(frames)
    fixture = read(previous["research_fixture_manifest"])
    reports, shots, ram, native, bindings, replay = {}, {}, {}, {}, {}, []
    resources = {}
    for kind in KINDS:
        resources[kind] = NdsImage.open(fixture["research_ROMs"][kind]["path"]).read_file("/_pxl/deck04.pxl")
        shots[kind], ram[kind], native[kind] = {}, {}, {}
        old_report = read(previous["reports"][kind]["path"])
        old_shots = {s["frame"]: s for s in old_report["frames_captured"]}
        for prefix in ("score_boundaries_v601", "score_BG3_v601"):
            report_path = CAPTURE / f"{prefix}_{kind}/capture_report.json"
            r = read(report_path)
            assert r["ROM_sha256"] == fixture["research_ROMs"][kind]["sha256"]
            assert r["frames"] == 4650 and r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"]
            assert r["scripted_input_schedule"] == old_report["scripted_input_schedule"]
            source = r["battery_save_preloaded"]
            assert source["source_sha256"] == "958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb"
            assert sha(Path(source["source"]).read_bytes()) == source["source_sha256"]
            for s in r["frames_captured"]:
                assert sha(Path(s["path"]).read_bytes()) == s["PNG_sha256"]
                assert Image.open(s["path"]).tobytes() == Image.open(old_shots[s["frame"]]["path"]).tobytes()
                shots[kind][s["frame"]] = s
            for s in r["read_only_capture_RAM_snapshots"]:
                assert s["read_only_export"] and sha(Path(s["path"]).read_bytes()) == s["sha256"]
                ram[kind][s["frame"]] = Path(s["path"]).read_bytes()
            for n in r["read_only_capture_native_states"]:
                assert n["read_only_export"] and not n["state_loaded"]
                assert n["main_RAM_unchanged_by_export"] and n["serialized_RAM_matches_same_frame_direct_export"]
                assert sha(Path(n["path"]).read_bytes()) == n["sha256"]
                for region in n["regions"].values():
                    assert sha(Path(region["path"]).read_bytes()) == region["sha256"]
                native[kind][n["frame"]] = n
            reports[kind, prefix] = r
            bindings[f"{prefix}_{kind}"] = {"path": str(report_path), "sha256": sha(report_path.read_bytes())}
            replay.append({"kind": kind, "run": prefix, "all_captured_images_exact_V600": True,
                           "unique_image_frames": sorted({s["frame"] for s in r["frames_captured"]})})
    live = []
    for frame in frames:
        objects = [controllers(ram[kind][frame]) for kind in KINDS]
        assert objects[0] == objects[1] == objects[2]
        live.append({"frame": frame, "both_entire200_byte_controller_objects_exact_all3_runs": True,
                     "current_controller_rectangles": [list(struct.unpack_from("<4i", obj, 0x20)) for obj in objects[0]]})
    poses = sorted({tuple(tuple(r) for r in s["rectangles"])
                    for s in read("work/analysis/material_review_v600/original_result_animation_states.json")["states"]})
    atlas = PxlImage.from_bytes(resources["current"])
    anchors = []
    for pair in poses:
        points = []
        for sx, dx, rect in ((16, 0, pair[0]), (0, 16, pair[0]), (32, 16, pair[1])):
            x, y = rect[0] + dx, rect[1] + 192
            if 0 <= x and x + 16 <= 256 and 192 <= y and y + 24 <= 384:
                points += opaque(atlas, sx, 16, x, y)
        anchors.append((pair, points))
    cases, full_pairs, background_frames = [], 0, []
    for frame in pending:
        blank = quantized(shots["blank_label_control"][frame]["path"])
        pixels = blank.load()
        matches = [(pair, points) for pair, points in anchors if points and all(pixels[x, y] == c for x, y, c in points)]
        assert len(matches) == 1
        pair, points = matches[0]
        seed = image_seed(blank)
        variants = []
        for kind in KINDS[:2]:
            result = native_parent(arm, ram[kind][frame], seed, pair, resources[kind])
            expected = buffer_image(result)
            actual = quantized(shots[kind][frame]["path"])
            difference = ImageChops.difference(expected, actual)
            outside = difference.getbbox()
            for rect in pair:
                x, y = rect[0] + 32, rect[1] + 192
                box = max(0, x), max(0, y), min(256, x + 24), min(384, y + 24)
                if box[0] < box[2] and box[1] < box[3]:
                    assert difference.crop(box).getbbox() is None
            if outside:
                assert 128 <= outside[0] < outside[2] <= 168 and 232 <= outside[1] < outside[3] <= 276
            else:
                full_pairs += 1
            variants.append({"kind": kind, "whole_native5_frame_exact": outside is None,
                "all_visible_score_label_cells_exact": True, "non_score_difference_bounds": outside})
        if any(v["non_score_difference_bounds"] for v in variants):
            background_frames.append(frame)
        cases.append({"frame": frame, "pose_from_only_complete_unchanged_digit_cells": pair,
                      "independent_digit_anchor_pixels": len(points), "variants": variants})
    assert full_pairs == 48 and len(background_frames) == 9
    planes = []
    for frame in background_frames:
        pair = next(c["pose_from_only_complete_unchanged_digit_cells"] for c in cases if c["frame"] == frame)
        hardware = {kind: native[kind][frame] for kind in KINDS}
        vram = {kind: Path(n["regions"]["LCDM"]["path"]).read_bytes() for kind, n in hardware.items()}
        assert len({n["regions"]["OAMS"]["sha256"] for n in hardware.values()}) == 1
        for n in hardware.values():
            io = Path(n["regions"]["9REG"]["path"]).read_bytes()
            assert io[0x242:0x244] == b"\x84\x81"  # Captured C=sub BG, D=main BG mappings.
            assert struct.unpack_from("<H", io, 0xE)[0] == struct.unpack_from("<H", io, 0x100E)[0] == 0x4084
            assert struct.unpack_from("<I", io)[0] & 8  # Actual main BG0 is the original 3D layer.
        # Full texture/palette banks are byte-identical; only the bitmap banks vary.
        assert all(vram[kind][:0x40000] == vram["blank_label_control"][:0x40000]
                   and vram[kind][0x80000:] == vram["blank_label_control"][0x80000:] for kind in KINDS[:2])
        blank_vram = vram["blank_label_control"]
        seed = blank_vram[0x60000:0x78000] + blank_vram[0x40000:0x58000]
        for kind in KINDS[:2]:
            expected = native_parent(arm, ram[kind][frame], seed, pair, resources[kind])
            target = vram[kind][0x60000:0x78000] + vram[kind][0x40000:0x58000]
            assert expected == target  # Includes bit15, every pixel, both complete bitmap planes.
            assert vram[kind][0x40000:0x60000] == blank_vram[0x40000:0x60000]
            planes.append({"frame": frame, "kind": kind, "both49152_pixel_bitmap_planes_entire16_bit_words_exact": True,
                           "bytes_checked": len(seed), "source_resource_getter_and_painter_unbridged": True,
                           "OAM_and_non_bitmap_VRAM_assets_exact_all3": True})
    save(ROOT / "boundary_proof.json", {"production_ROM": str(production),
        "production_ROM_sha256": previous["production_ROM_sha256"], "production_ROM_or_patch_changed": False,
        "V600_proof": str(previous_path), "V600_proof_sha256": sha(previous_path.read_bytes()),
        "reports": bindings, "exact_replay_comparisons": replay, "all33_live_controller_comparisons": live,
        "remaining_V600_frames": pending, "all29_visible_score_label_cases_native_exact": True,
        "native_parent_source_and_cache_payloads_not_bridged": True,
        "digit_pose_selection_uses_no_Japanese_or_English_label_pixels": True,
        "original_parent_replays_supply_only_independently_observed_original_animation_geometry": True,
        "cases": cases, "whole_native5_frames_exact": full_pairs,
        "nine_background_only_full_frame_disagreements": background_frames,
        "whole_bitmap_plane_word_cases": planes, "bitmap_plane_bytes_checked": sum(c["bytes_checked"] for c in planes),
        "test_model_corrections": ["Use complete unclipped unchanged digits for pose anchors",
                                   "Run the original parent and blitter rather than assuming a generic host crop"],
        "limits": "Nine final composed frames still differ over the existing foreground/3D crew figure; all their text cells, both bitmap planes, OAM and non-bitmap VRAM assets pass. Exact foreground timing/raster cause is unproved; do not claim full final-frame equality or earned results.",
        "no_source_or_capture_frame_retiming": True, "all18_plaques_incomplete_and22_objects_retained": True,
        "research_only_no_normal_guide_or_earned_result_credit": True, "full_goal_complete": False,
        "headless_script_sha256": sha(Path("scripts/headless_desmume_v193.py").read_bytes()),
        "script_sha256": sha(Path(__file__).read_bytes())})
    print("V601:all29 score cells pass original native parent;48 whole frames exact;18 entire two-plane16-bit bitmap cases exact;9 foreground-only final-frame gaps retained.")


if __name__ == "__main__":
    main()
