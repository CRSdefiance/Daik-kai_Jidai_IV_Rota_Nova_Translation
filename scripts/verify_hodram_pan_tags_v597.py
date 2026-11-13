"""Bind Hodram's pan order and third tile to actual source-tag rendering."""

import json
import struct
from itertools import pairwise
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ending_fixture_v537 import request_ending
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.research_fls_frames_v312 import quad
from scripts.verify_ending_pan_rows_v596 import one_frame
from scripts.verify_ending_photo_markers_v594 import find_live, project

ROOT = Path("work/analysis/hodram_pan_tags_v597")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load(label, digest, manifest, arm):
    folder = CAPTURE / label
    path = folder / "capture_report.json"
    r = read(path)
    assert r["ROM_sha256"] == digest and r["frames"] == manifest["frames"]
    assert r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"]
    assert r["scripted_input_schedule"] == read(manifest["inputs"])
    assert not r["earned_completion_verified"] and len(r["synthetic_ending_fixtures"]) == 1
    fixture = r["synthetic_ending_fixtures"][0]
    assert fixture["frame"] == 3000
    _, check = request_ending(arm, (folder / "frame_003000_arm9_ram.bin").read_bytes(), 1)
    assert check == {k: v for k, v in fixture.items() if k != "frame"}
    save = r["battery_save_preloaded"]
    assert save["source_sha256"] == manifest["source_save_sha256"]
    assert sha(Path(save["source"]).read_bytes()) == manifest["source_save_sha256"]
    snapshots = {x["frame"]: x for key in ("read_only_capture_RAM_snapshots", "read_only_pause_RAM_snapshots")
                 for x in r.get(key, [])}
    for x in snapshots.values():
        assert sha(Path(x["path"]).read_bytes()) == x["sha256"]
    shots = {x["frame"]: x for x in r["frames_captured"]}
    assert set(range(12000, 13461)) <= shots.keys()
    for shot in shots.values():
        assert sha(Path(shot["path"]).read_bytes()) == shot["PNG_sha256"]
    return r, shots, snapshots, {"path": str(path), "sha256": sha(path.read_bytes())}


def geometry(arm, raw, live):
    u = machine(arm)
    u.mem_write(BASE, raw)
    obj = live["object"]
    offset = obj - BASE
    previous = struct.unpack_from("<h", raw, offset + 0x1A08)[0] ^ 1
    drawn = []
    for slot in range(1, 32):
        at = offset + 0x204 + previous * 0xC00 + slot * 0x60
        if not struct.unpack_from("<h", raw, at)[0] or struct.unpack_from("<h", raw, at + 0x34)[0] != 0:
            continue
        texture_input = struct.unpack_from("<h", raw, at + 2)[0]
        call(u, 0x100390, (obj, texture_input & 0xFFFFFFFF))
        selected = u.reg_read(UC_ARM_REG_R0)
        if selected not in (1, 2, 3):
            continue
        corners = quad(u, obj, slot)
        if corners is not None:
            assert corners[0][1] == corners[1][1] and corners[2][1] == corners[3][1]
            assert corners[0][0] == corners[2][0] and corners[1][0] == corners[3][0]
            drawn.append({"slot": slot, "texture_input": texture_input, "selected_texture": selected,
                          "original_quad_FX12": corners})
    if drawn:
        assert len(drawn) == 3
        ordered = sorted(drawn, key=lambda x: x["original_quad_FX12"][0][1])
        assert [x["selected_texture"] for x in ordered] == [3, 2, 1]
        for upper, lower in pairwise(ordered):
            assert abs(upper["original_quad_FX12"][3][1] - lower["original_quad_FX12"][0][1]) < 2 * 4096
    return drawn


def main():
    manifest_path = ROOT / "hodram_pan_tile3_tags_RESEARCH_ONLY.fixture.json"
    m = read(manifest_path)
    original, marked, clean = [NdsImage.open(p) for p in (m["parent"], m["research_ROM"], "work/clean.nds")]
    assert sha(original.source.read_bytes()) == m["parent_sha256"]
    assert sha(marked.source.read_bytes()) == m["research_ROM_sha256"]
    arm = original.read_file("/__arm9__.bin")
    source = original.read_file(m["only_internal_file_changed"])
    assert source == clean.read_file(m["only_internal_file_changed"])
    assert arm == marked.read_file("/__arm9__.bin")
    for r in m["source_exact_code_ranges"]:
        lo, hi = r["offset"]
        assert sha(arm[lo:hi]) == r["sha256"] and arm[lo:hi] == clean.read_file("/__arm9__.bin")[lo:hi]
    baseline = {p: d for _, p, d in original.iter_files()} | dict(original.iter_components())
    counterpart = {p: d for _, p, d in marked.iter_files()} | dict(marked.iter_components())
    assert baseline.keys() == counterpart.keys()
    assert [p for p in baseline if baseline[p] != counterpart[p]] == [m["only_internal_file_changed"]]
    a, b = FlsArchive(source), FlsArchive(marked.read_file(m["only_internal_file_changed"]))
    assert a.records == b.records and len(a.source) == len(b.source)
    owned = {y * 256 + x for tag in m["tags"] for y in range(tag["source_rect"][1], tag["source_rect"][3])
             for x in range(tag["source_rect"][0], tag["source_rect"][2])}
    for index in range(a.count):
        x, y = a.texture(index), b.texture(index)
        assert (x.flags, x.width, x.height, x.palette) == (y.flags, y.width, y.height, y.palette)
        if index == 3:
            changes = {n for n, (p, q) in enumerate(zip(x.indices, y.indices, strict=True)) if p != q}
            assert changes <= owned and len(changes) == m["changed_source_indices"] == 2048
        else:
            assert x.indices == y.indices
    normal, shots, snapshots, binding = load("ending_pan_v597_hodram", m["parent_sha256"], m, arm)
    tags, tagged_shots, tagged_snapshots, tagged_binding = load("ending_pan_v597_hodram_tags", m["research_ROM_sha256"], m, arm)
    assert shots.keys() == tagged_shots.keys() and normal["core_options"] == tags["core_options"]
    cases, phases, total, seen_tags = [], set(), 0, set()
    # Project only from actually captured native states. Whole additional frames
    # remain separate evidence, not invented intermediate geometry snapshots.
    for frame in sorted(set(snapshots) & set(tagged_snapshots)):
        if not 12040 <= frame <= 13440:
            continue
        raw, changed = [Path(table[frame]["path"]).read_bytes() for table in (snapshots, tagged_snapshots)]
        live, live_tags = [find_live(data, source) for data in (raw, changed)]
        assert live and live_tags and live["object"] == live_tags["object"] and live["file_prefix"] == live_tags["file_prefix"]
        obj = live["object"]
        offset = obj - BASE
        phase = live["native_counter"] * 4096 + struct.unpack_from("<I", raw, offset + 12)[0]
        tag_phase = live_tags["native_counter"] * 4096 + struct.unpack_from("<I", changed, offset + 12)[0]
        delta = tag_phase - phase
        assert delta in (0, 1024), (frame, delta)
        phases.add(delta)
        if delta == 0:
            assert raw[offset:offset + 0x1B18] == changed[offset:offset + 0x1B18]
        else:
            assert one_frame(arm, raw, live) == changed[offset:offset + 0x1B18]
        draws = geometry(arm, raw, live)
        rects = project(arm, raw, live, m)
        shift = delta // 1024
        compared_frame = frame - shift
        before, after = [Image.open(table[f]["path"]).convert("RGB") for table, f in ((shots, frame), (tagged_shots, compared_frame))]
        mask = set()
        tag_masks = {}
        for drawing in rects:
            for tag in drawing["projected_valid_tag_rectangles"]:
                left, top, right, bottom = tag["projected_clipped_rect_with2pixel_margin"]
                points = {y * 256 + x for y in range(top, bottom) for x in range(left, right)}
                mask |= points
                tag_masks.setdefault(tag["tag"], set()).update(points)
        different = {n for n, (x, y) in enumerate(zip(before.get_flattened_data(), after.get_flattened_data())) if x != y}
        assert different <= mask, f"Unexpected source-tag pixel outside original projection at {frame}"
        counts = {tag: len(different & points) for tag, points in tag_masks.items() if different & points}
        seen_tags.update(counts)
        total += len(different)
        resident = None
        if different:
            resident = [data.find(bytes(movie.texture(3).indices)) for data, movie in ((raw, a), (changed, b))]
        cases.append({"frame": frame, "control_frame": compared_frame, "native_phase_delta": delta,
                      "actual_live_binding": live, "exact_control_controller_at_declared_phase": True,
                      "all_three_pan_tile_draws": draws, "third_tile_projected_tags": rects,
                      "changed_native_pixels": len(different), "tag_changed_pixels": counts,
                      "every_other_complete_frame_pixel_exact": True,
                      "main_RAM_full_linear_decoded_tile_search_offsets_minus1_means_not_found": resident,
                      "full_linear_CPU_residency_not_required_or_claimed_for_GPU_tag_evidence": True})
    assert len(phases) == 1 and total > 0 and seen_tags
    fixed_shift = phases.pop() // 1024
    # Keep the first same-frame result visible even when a fixed phase offset is
    # needed; the offset is derived above from original native controller state.
    frame_cases = []
    for frame in sorted(shots):
        left = Image.open(shots[frame]["path"]).convert("RGB")
        right = Image.open(tagged_shots[frame]["path"]).convert("RGB")
        assert left.size == right.size == (256, 384)
        same = left.tobytes() == right.tobytes()
        target = frame - fixed_shift if 12040 <= frame <= 13460 else frame
        aligned = Image.open(tagged_shots[target]["path"]).convert("RGB")
        assert left.crop((0, 192, 256, 384)).tobytes() == aligned.crop((0, 192, 256, 384)).tobytes()
        frame_cases.append({"frame": frame, "control_frame": target, "same_frame_full_exact": same,
                            "aligned_full_frame_exact": left.tobytes() == aligned.tobytes(), "whole_lower_exact": True})
    # Original geometry selects3,2,1. During the opaque pan the upper tile is
    # outside the window, so both historical permutation matches were possible.
    canvas = Image.new("RGB", (256, 384))
    for n, index in enumerate((3, 2, 1)):
        canvas.paste(a.texture(index).render().convert("RGB").point(lambda x: x >> 3), (0, n * 128))
    windows = {sha(canvas.crop((0, y, 256, y + 192)).tobytes()): y for y in range(193)}
    composites = []
    for frame, shot in shots.items():
        image = Image.open(shot["path"]).convert("RGB").point(lambda x: x >> 3).crop((0, 0, 256, 192))
        y = windows.get(sha(image.tobytes()))
        if y is not None:
            assert image.tobytes() == canvas.crop((0, y, 256, y + 192)).tobytes()
            composites.append({"frame": frame, "source_y": y, "whole49152_upper_pixels_exact": True})
    assert len(composites) >= 800
    proof = {"format": "dk4-hodram-pan-tags-v597", "candidate": m["parent"], "candidate_sha256": m["parent_sha256"],
             "fixture": m, "reports": [binding, tagged_binding], "native_projection_cases": cases,
             "source_bound_top_to_bottom_tile_order": [3, 2, 1], "observed_source_tags": sorted(seen_tags),
             "changed_native_pixels_in_projected_states": total, "fixed_native_update_offset": fixed_shift,
             "all_paired_frame_cases": frame_cases, "whole_source_pan_composites": composites,
             "third_star_tile_actual_usage_during_transition_verified": True,
             "source_art_caption_free_original_retained": True,
             "all_source_rows_internal_alpha_all_intermediate_GPU_pixels_and_earned_completion_not_claimed": True,
             "production_ROM_or_patch_changed": False, "full_goal_complete": False,
             "script_sha256": sha(Path(__file__).read_bytes())}
    (ROOT / "pan_tags_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(f"V597: {len(cases)} real geometry states;{total} changed pixels inside source tags;tags{sorted(seen_tags)};{len(composites)} whole source composites;fixed offset{fixed_shift};original order3,2,1.")


if __name__ == "__main__":
    main()
