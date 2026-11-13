"""Bind real ending-photo effects to actual native selectors and live quads.

Two-pixel bounds account for rasterization around the original FX12 vertices.
This is source usage/crop evidence, not a full photo/alpha GPU compositor.
"""

import json
import math
import struct
from pathlib import Path

from PIL import Image, ImageChops
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ending_fixture_v537 import request_ending
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.research_fls_frames_v312 import quad

ROOT = Path("work/analysis/ending_photo_markers_v594")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def find_live(raw, source):
    movie = FlsArchive(source)
    start, candidates = 0, []
    while (at := raw.find(source[:16], start)) >= 0:
        start = at + 1
        if raw[at:at + movie.data_offset] != source[:movie.data_offset]:
            continue
        needle = struct.pack("<2I", BASE + at, BASE + at + movie.table_offset)
        pos = 0
        while (offset := raw.find(needle, pos)) >= 0:
            pos = offset + 1
            obj = offset - 4
            if not 0 <= obj <= len(raw) - 0x1B18:
                continue
            if struct.unpack_from("<I", raw, obj + 0x1F8)[0] != BASE + at:
                continue
            buffer = struct.unpack_from("<h", raw, obj + 0x1A08)[0]
            if buffer not in (0, 1):
                continue
            pointer = struct.unpack_from("<I", raw, obj + 0x1A04)[0]
            if pointer not in (BASE + obj + 0x204, BASE + obj + 0xE04):
                continue
            candidates.append({"object": BASE + obj, "file_prefix": BASE + at,
                               "prefix_bytes": movie.data_offset, "prefix_sha256": sha(source[:movie.data_offset]),
                               "native_counter": struct.unpack_from("<h", raw, obj + 0x1A0A)[0],
                               "object_bytes_sha256": sha(raw[obj:obj + 0x1B18])})
    assert len(candidates) <= 1
    return candidates[0] if candidates else None


def project(arm, raw, live, case):
    u = machine(arm)
    u.mem_write(BASE, raw)
    obj = live["object"]
    offset = obj - BASE
    previous = struct.unpack_from("<h", raw, offset + 0x1A08)[0] ^ 1
    rows = []
    width, height = case["native_dimensions"]
    for slot in range(1, 32):
        at = offset + 0x204 + previous * 0xC00 + slot * 0x60
        state = raw[at:at + 0x60]
        if struct.unpack_from("<h", state)[0] == 0 or struct.unpack_from("<h", state, 0x34)[0] != 0:
            continue
        texture_input = struct.unpack_from("<h", state, 2)[0]
        call(u, 0x100390, (obj, texture_input & 0xFFFFFFFF))
        if u.reg_read(UC_ARM_REG_R0) != case["texture"]:
            continue
        corners = quad(u, obj, slot)
        if corners is None:
            continue
        assert corners[0][1] == corners[1][1] and corners[2][1] == corners[3][1]
        assert corners[0][0] == corners[2][0] and corners[1][0] == corners[3][0]
        left, top = (v / 4096 for v in corners[0])
        right, bottom = (v / 4096 for v in corners[3])
        assert right > left and bottom > top
        rectangles = []
        for tag in case["tags"]:
            x1, y1, x2, y2 = tag["source_rect"]
            if not tag["within_native_header"]:
                continue
            box = [max(0, math.floor(left + x1 / width * (right - left)) - 2),
                   max(0, math.floor(top + y1 / height * (bottom - top)) - 2),
                   min(256, math.ceil(left + x2 / width * (right - left)) + 2),
                   min(192, math.ceil(top + y2 / height * (bottom - top)) + 2)]
            if box[0] < box[2] and box[1] < box[3]:
                rectangles.append({"tag": tag["id"], "projected_clipped_rect_with2pixel_margin": box})
        rows.append({"slot": slot, "texture_input": texture_input, "original_selector_result": case["texture"],
                     "original_quad_FX12": corners, "projected_valid_tag_rectangles": rectangles})
    return rows


def load_run(case, mode, digest, arm):
    folder = CAPTURE / f"ending_photos_v594_{case['label']}_{mode}"
    path = folder / "capture_report.json"
    r = read(path)
    assert r["ROM_sha256"] == digest and r["frames"] == case["frames"]
    assert r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"]
    assert r["scripted_input_schedule"] == read(case["inputs"])
    assert not r["earned_completion_verified"]
    fixtures = r["synthetic_ending_fixtures"]
    assert len(fixtures) == 1 and fixtures[0]["frame"] == 3000
    before = (folder / "frame_003000_arm9_ram.bin").read_bytes()
    _, replay = request_ending(arm, before, case["captain"])
    assert replay == {k: v for k, v in fixtures[0].items() if k != "frame"}
    assert replay["changes"] == [{"address": 0x022796BC, "before": 1, "after": 4}]
    for bad_arm, bad_captain in ((arm + b"\0", case["captain"]), (arm, (case["captain"] + 1) % 4)):
        try:
            request_ending(bad_arm, before, bad_captain)
        except ValueError:
            pass
        else:
            raise AssertionError("Ending fixture guard failed")
    save = r["battery_save_preloaded"]
    assert save["source_sha256"] == case["source_save_sha256"]
    assert sha(Path(save["source"]).read_bytes()) == case["source_save_sha256"]
    for key in ("read_only_capture_RAM_snapshots", "read_only_pause_RAM_snapshots"):
        for snap in r.get(key, []):
            assert sha(Path(snap["path"]).read_bytes()) == snap["sha256"]
    shots = {}
    for shot in r["frames_captured"]:
        assert sha(Path(shot["path"]).read_bytes()) == shot["PNG_sha256"]
        shots[shot["frame"]] = shot
    return r, shots, {"path": str(path), "sha256": sha(path.read_bytes())}


def main():
    manifest = read(ROOT / "fixture_manifest.json")
    rom = NdsImage.open(manifest["candidate"])
    arm = rom.read_file("/__arm9__.bin")
    assert sha(rom.source.read_bytes()) == manifest["candidate_sha256"]
    assert sha(arm) == manifest["verified_ARM9_sha256"]
    clean = NdsImage.open("work/clean.nds")
    for row in manifest["source_exact_original_code_ranges"]:
        lo, hi = row["offset"]
        assert arm[lo:hi] == clean.read_file("/__arm9__.bin")[lo:hi]
        assert sha(arm[lo:hi]) == row["sha256"]
    cases = []
    for case in manifest["cases"]:
        source = rom.read_file(case["only_internal_file_changed"])
        marked_rom = NdsImage.open(case["research_ROM"])
        assert sha(marked_rom.source.read_bytes()) == case["research_ROM_sha256"]
        assert marked_rom.read_file("/__arm9__.bin") == arm
        original_files = {p: d for _, p, d in rom.iter_files()} | dict(rom.iter_components())
        marked_files = {p: d for _, p, d in marked_rom.iter_files()} | dict(marked_rom.iter_components())
        assert [p for p in original_files if original_files[p] != marked_files[p]] == [case["only_internal_file_changed"]]
        assert source == clean.read_file(case["only_internal_file_changed"])
        a, b = [FlsArchive(data) for data in (source, marked_files[case["only_internal_file_changed"]])]
        assert a.records == b.records and len(a.source) == len(b.source)
        owner = {y * 256 + x for tag in case["tags"] for y in range(tag["source_rect"][1], tag["source_rect"][3])
                 for x in range(tag["source_rect"][0], tag["source_rect"][2])}
        for i in range(a.count):
            x, y = a.texture(i), b.texture(i)
            assert (x.flags, x.width, x.height, x.palette) == (y.flags, y.width, y.height, y.palette)
            if i != case["texture"]:
                assert x.indices == y.indices
            else:
                changes = {n for n, (c, d) in enumerate(zip(x.indices, y.indices, strict=True)) if c != d}
                assert changes <= owner and len(changes) == case["changed_source_indices"]
        old, old_shots, old_binding = load_run(case, "control", manifest["candidate_sha256"], arm)
        marked, marked_shots, marked_binding = load_run(case, "markers", case["research_ROM_sha256"], arm)
        assert old_shots.keys() == marked_shots.keys() and old["core_options"] == marked["core_options"]
        frame_cases = []
        for frame in sorted(old_shots):
            before, after = [Image.open(shots[frame]["path"]).convert("RGB") for shots in (old_shots, marked_shots)]
            assert before.size == after.size == (256, 384)
            assert before.crop((0, 192, 256, 384)).tobytes() == after.crop((0, 192, 256, 384)).tobytes()
            diff = ImageChops.difference(before, after).getbbox()
            frame_cases.append({"frame": frame, "full_two_screen_exact": diff is None,
                                "difference_bounds": list(diff) if diff else None,
                                "whole_lower_screen_exact": True})
        snapshot_rows = []
        old_raw = {s["frame"]: s for s in old["read_only_capture_RAM_snapshots"]}
        marked_raw = {s["frame"]: s for s in marked["read_only_capture_RAM_snapshots"]}
        for frame in sorted(old_raw.keys() & marked_raw.keys()):
            left = Path(old_raw[frame]["path"]).read_bytes()
            right = Path(marked_raw[frame]["path"]).read_bytes()
            live = find_live(left, source)
            if live is None:
                continue
            obj = live["object"] - BASE
            assert left[obj:obj + 0x1B18] == right[obj:obj + 0x1B18], (case["label"], frame, "movie controller differs")
            assert find_live(right, source) == live
            drawing = project(arm, left, live, case)
            rectangles = [r for d in drawing for r in d["projected_valid_tag_rectangles"]]
            images = [Image.open(shots[frame]["path"]).convert("RGB") for shots in (old_shots, marked_shots)]
            differences = [(x, y) for y in range(384) for x in range(256)
                           if images[0].getpixel((x, y)) != images[1].getpixel((x, y))]
            coverage = {r["tag"]: 0 for r in rectangles}
            for x, y in differences:
                hits = [r for r in rectangles if r["projected_clipped_rect_with2pixel_margin"][0] <= x < r["projected_clipped_rect_with2pixel_margin"][2]
                        and r["projected_clipped_rect_with2pixel_margin"][1] <= y < r["projected_clipped_rect_with2pixel_margin"][3]]
                assert hits, (case["label"], frame, "changed pixel outside independent original projection", x, y)
                for hit in hits:
                    coverage[hit["tag"]] += 1
            snapshot_rows.append({"frame": frame, "live_source": live, "all_controller_bytes_exact_between_pair": True,
                                  "original_photo_drawings": drawing, "changed_native_pixels": len(differences),
                                  "every_difference_inside_independent_projected_tags": True,
                                  "tag_changed_pixels": coverage, "both_screen_pixels_checked": 98304})
        positive = [r for r in snapshot_rows if r["changed_native_pixels"]]
        assert len(positive) >= 3, (case["label"], "Need multiple positively identified native photo states")
        assert any(r["full_two_screen_exact"] and r["frame"] < positive[0]["frame"] for r in frame_cases)
        assert any(r["full_two_screen_exact"] and r["frame"] > positive[-1]["frame"] for r in frame_cases)
        visible = sorted({int(tag) for row in positive for tag, count in row["tag_changed_pixels"].items() if count})
        cases.append({"label": case["label"], "captain": case["captain"], "file": case["only_internal_file_changed"],
                      "texture": case["texture"], "native_dimensions": case["native_dimensions"],
                      "source_file_exact_clean": True, "reports": {"control": old_binding, "markers": marked_binding},
                      "all_paired_frame_cases": frame_cases, "native_snapshot_projection_cases": snapshot_rows,
                      "positive_projected_states": len(positive), "visible_source_tags": visible,
                      "observed_changed_native_pixels_in_bound_states": sum(r["changed_native_pixels"] for r in positive),
                      "full_source_alpha_compositor_texel_sampling_or_all_frames_not_proven": True,
                      "source_Japanese_caption_not_found_original_illustration_retained": True})
    assert sha(rom.source.with_suffix(".xdelta").read_bytes()) == "e6e1097e9caa7577a4c51d9bcc175274eb68e4f8041d86acd05d8ba1f4ad52c7"
    result = {"candidate": manifest["candidate"], "candidate_sha256": manifest["candidate_sha256"],
              "cases": cases, "source_fixture_manifest_sha256": sha((ROOT / "fixture_manifest.json").read_bytes()),
              "script_sha256": sha(Path(__file__).read_bytes()),
              "actual_native_photo_usage_and_bounded_zoom_crops_proven": True,
              "source_art_timeline_palettes_dimensions_and_production_ROM_patch_unchanged": True,
              "four_authorized_one_byte_ending_fixtures_not_earned_endings": True,
              "all_screenshots_are_test_evidence_not_guide_approved": True, "full_goal_complete": False}
    (ROOT / "native_photo_usage_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_photo_states": {c["label"]: c["positive_projected_states"] for c in cases},
                      "paired_frames": sum(len(c["all_paired_frame_cases"]) for c in cases),
                      "usage_and_projected_marker_bounds": "PASS", "production_V593_unchanged": True}))


if __name__ == "__main__":
    main()
