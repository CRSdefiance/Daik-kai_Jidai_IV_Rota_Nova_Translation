"""Bind Lil's actual pan, original controller replay and hidden-row control."""

import hashlib
import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R10

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ending_fixture_v537 import request_ending
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.research_fls_frames_v312 import quad
from scripts.verify_ending_photo_markers_v594 import find_live

ROOT = Path("work/analysis/ending_pan_rows_v596")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193")
ROM = Path("out/all_routes_combined_v593_candidate.nds")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load(label, digest, arm):
    folder = CAPTURE / label
    path = folder / "capture_report.json"
    report = read(path)
    assert report["ROM_sha256"] == digest and report["frames"] == 26600
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["scripted_input_schedule"] == read("work/analysis/endings_current_v583/lil_inputs.json")
    assert report.get("battery_save_preloaded") is None and not report["earned_completion_verified"]
    assert len(report["synthetic_ending_fixtures"]) == 1
    fixture = report["synthetic_ending_fixtures"][0]
    assert fixture["frame"] == 18000
    _, check = request_ending(arm, (folder / "frame_018000_arm9_ram.bin").read_bytes(), 2)
    assert check == {k: v for k, v in fixture.items() if k != "frame"}
    snapshots = {r["frame"]: r for key in ("read_only_capture_RAM_snapshots", "read_only_pause_RAM_snapshots")
                 for r in report.get(key, [])}
    for row in snapshots.values():
        assert sha(Path(row["path"]).read_bytes()) == row["sha256"]
    shots = {r["frame"]: r for r in report["frames_captured"]}
    assert set(range(18000, 21001)) <= shots.keys()
    return report, shots, snapshots, {"path": str(path), "sha256": sha(path.read_bytes())}


def polygon_id(u, obj):
    context = u.context_save()
    u.reg_write(UC_ARM_REG_R10, obj)
    u.emu_start(BASE + 0xFF778, BASE + 0xFF790, count=6)
    u.context_restore(context)


def one_frame(arm, raw, live):
    u = machine(arm)
    u.mem_write(BASE, raw)
    obj = live["object"]
    call(u, 0xFD4F8, (obj,), instruction_limit=500000)
    current = bytes(u.mem_read(obj, 0x1B18))
    previous = struct.unpack_from("<h", current, 0x1A08)[0] ^ 1
    for slot in range(1, 32):
        at = 0x204 + previous * 0xC00 + slot * 0x60
        if (struct.unpack_from("<h", current, at)[0]
                and struct.unpack_from("<h", current, at + 0x34)[0] == 0
                and quad(u, obj, slot) is not None):
            polygon_id(u, obj)
    return bytes(u.mem_read(obj, 0x1B18))


def replay(arm, source, snapshots):
    first, last = 18096, 20548
    raw = Path(snapshots[first]["path"]).read_bytes()
    live = find_live(raw, source)
    assert live and live["native_counter"] == 17
    obj, offset = live["object"], live["object"] - BASE
    u = machine(arm)
    u.mem_write(BASE, raw)
    observed = {i: set() for i in (1, 2, 3)}
    geometry, anchors, digest = [], [], hashlib.sha256()
    last_geometry = None
    min_top, max_bottom, native_calls = {}, {}, 0
    for frame in range(first, last + 1):
        if frame != first:
            call(u, 0xFD4F8, (obj,), instruction_limit=500000)
            native_calls += 1
        object_bytes = bytes(u.mem_read(obj, 0x1B18))
        previous = struct.unpack_from("<h", object_bytes, 0x1A08)[0] ^ 1
        drawn = []
        for slot in range(1, 32):
            state = object_bytes[0x204 + previous * 0xC00 + slot * 0x60:0x204 + previous * 0xC00 + (slot + 1) * 0x60]
            if not struct.unpack_from("<h", state)[0] or struct.unpack_from("<h", state, 0x34)[0] != 0:
                continue
            texture_input = struct.unpack_from("<h", state, 2)[0]
            call(u, 0x100390, (obj, texture_input & 0xFFFFFFFF))
            index = u.reg_read(UC_ARM_REG_R0)
            corners = quad(u, obj, slot)
            if corners is None:
                continue
            if frame != first:
                # The actual renderer increments the controller's polygon-ID
                # byte per drawn quad. Execute its original six instructions;
                # no GPU command or texture-memory operation is simulated.
                polygon_id(u, obj)
            if index not in observed:
                continue
            assert corners[0][0] == corners[2][0] == 0
            assert corners[1][0] == corners[3][0] == 256 * 4096
            assert corners[0][1] == corners[1][1] and corners[2][1] == corners[3][1]
            top, bottom = corners[0][1], corners[3][1]
            assert bottom - top == 128 * 4096
            # This is a geometric viewport test. The paired actual GPU frames
            # separately test the exact row64 raster edge and all lower rows.
            visible = [y for y in range(128) if top + y * 4096 < 192 * 4096 and top + (y + 1) * 4096 > 0]
            observed[index].update(visible)
            min_top[index] = min(min_top.get(index, top), top)
            max_bottom[index] = max(max_bottom.get(index, bottom), bottom)
            drawn.append({"slot": slot, "texture_input": texture_input, "selected_texture": index,
                          "original_quad_FX12": corners, "geometrically_visible_source_rows": visible})
        object_bytes = bytes(u.mem_read(obj, 0x1B18))
        digest.update(object_bytes)
        if frame in snapshots:
            actual = Path(snapshots[frame]["path"]).read_bytes()
            bound = find_live(actual, source)
            assert bound and bound["object"] == obj and bound["file_prefix"] == live["file_prefix"]
            different = [i for i, (x, y) in enumerate(zip(actual[offset:offset + 0x1B18], object_bytes, strict=True)) if x != y]
            assert not different, f"Full controller mismatch at {frame}: {[hex(i) for i in different[:32]]}"
            anchors.append({"frame": frame, "whole_0x1B18_controller_exact": True,
                            "native_counter": bound["native_counter"], "snapshot_sha256": snapshots[frame]["sha256"]})
        if drawn != last_geometry:
            geometry.append({"frame": frame, "geometry": drawn})
            last_geometry = drawn
    assert observed[1] == set(range(64))
    assert observed[2] == observed[3] == set(range(128))
    assert min_top[1] == 128 * 4096
    assert geometry[-1]["geometry"] == []
    last_drawn = max(row["frame"] for row in geometry if row["geometry"])
    assert geometry[-1]["frame"] > last_drawn
    return {"source_snapshot": snapshots[first], "live_binding": live,
            "first_frame": first, "last_frame": last, "original_update_calls": native_calls,
            "all_per_frame_controller_bytes_digest": digest.hexdigest(), "actual_complete_controller_anchors": anchors,
            "all_geometry_changes": geometry, "source_row_envelopes": {i: sorted(rows) for i, rows in observed.items()},
            "texture1_min_top_FX12": min_top[1], "SDK_IO_texture_selection_or_quad_not_bridged": True,
            "pan_exit_to_inactive_geometry_observed": geometry[-1]["frame"],
            "later_scenes_and_full_controller_replay_after_this_pan_not_claimed": True,
            "original_six_instruction_polygon_ID_update_executed_per_drawn_quad": True,
            "before_first_anchor_and_GPU_raster_edges_checked_by_paired_real_frames": True}


def main():
    manifest = read(ROOT / "lil_lower_rows_RESEARCH_ONLY.fixture.json")
    rom, marked, clean = [NdsImage.open(p) for p in (ROM, Path(manifest["research_ROM"]), Path("work/clean.nds"))]
    assert sha(ROM.read_bytes()) == manifest["parent_sha256"]
    assert sha(marked.source.read_bytes()) == manifest["research_ROM_sha256"]
    arm = rom.read_file("/__arm9__.bin")
    assert arm == marked.read_file("/__arm9__.bin")
    source = rom.read_file("/FLS/M31.fls")
    assert source == clean.read_file("/FLS/M31.fls")
    a, b = FlsArchive(source), FlsArchive(marked.read_file("/FLS/M31.fls"))
    assert a.records == b.records and len(a.source) == len(b.source)
    original_files = {p: d for _, p, d in rom.iter_files()} | dict(rom.iter_components())
    research_files = {p: d for _, p, d in marked.iter_files()} | dict(marked.iter_components())
    assert original_files.keys() == research_files.keys()
    assert [p for p in original_files if original_files[p] != research_files[p]] == ["/FLS/M31.fls"]
    for i in range(a.count):
        x, y = a.texture(i), b.texture(i)
        assert (x.flags, x.width, x.height, x.palette) == (y.flags, y.width, y.height, y.palette)
        if i == 1:
            changed = [n for n, (v, w) in enumerate(zip(x.indices, y.indices, strict=True)) if v != w]
            assert len(changed) == manifest["changed_indices"] and all(64 <= n // 256 < 128 for n in changed)
        else:
            assert x.indices == y.indices
    code_ranges = []
    for lo, hi in ((0xFD4F8, 0xFDC60), (0xFEB28, 0xFF9C8), (0x100390, 0x1003CC)):
        assert arm[lo:hi] == clean.read_file("/__arm9__.bin")[lo:hi]
        code_ranges.append({"offset": [lo, hi], "sha256": sha(arm[lo:hi])})
    normal, normal_shots, snaps, normal_report = load("ending_pan_v596_lil", manifest["parent_sha256"], arm)
    control, control_shots, control_snaps, control_report = load("ending_pan_v596_lil_lower", manifest["research_ROM_sha256"], arm)
    assert normal_shots.keys() == control_shots.keys() and normal["core_options"] == control["core_options"]
    pairs = []
    for frame in sorted(normal_shots):
        left, right = [Image.open(shots[frame]["path"]).convert("RGB") for shots in (normal_shots, control_shots)]
        assert left.size == right.size == (256, 384)
        same_frame = left.tobytes() == right.tobytes()
        # Use one fixed offset throughout the movie interval, never a
        # per-image best match. Earlier teardown remains same-frame compared.
        aligned_frame = frame - 1 if 18028 <= frame <= 21000 else frame
        aligned = Image.open(control_shots[aligned_frame]["path"]).convert("RGB")
        assert left.tobytes() == aligned.tobytes(), f"Fixed-alignment lower-row control differs at {frame}"
        for shot in (normal_shots[frame], control_shots[frame]):
            assert sha(Path(shot["path"]).read_bytes()) == shot["PNG_sha256"]
        pairs.append({"frame": frame, "control_frame": aligned_frame, "same_frame_exact": same_frame,
                      "full_two_screen_pixels_exact_at_recorded_alignment": True})
    decoded = []
    for frame in (18120, 19400, 20400):
        raw, tagged = [Path(table[frame]["path"]).read_bytes() for table in (snaps, control_snaps)]
        bindings = [find_live(data, source) for data in (raw, tagged)]
        assert all(bindings)
        assert {k: v for k, v in bindings[0].items() if k != "object_bytes_sha256"} == {
            k: v for k, v in bindings[1].items() if k != "object_bytes_sha256"}
        offset = bindings[1]["object"] - BASE
        assert one_frame(arm, raw, bindings[0]) == tagged[offset:offset + 0x1B18]
        offsets = [data.find(bytes(movie.texture(1).indices)) for data, movie in ((raw, a), (tagged, b))]
        assert all(offset >= 0 for offset in offsets)
        assert bytes(a.texture(1).indices) not in tagged
        decoded.append({"frame": frame, "original_and_marked_whole32768_decoded_indices_resident": True,
                        "resident_addresses": [BASE + offset for offset in offsets],
                        "same_prefix_and_binding_with_exact_one_native_update_phase_offset": bindings,
                        "whole_control_controller_equals_one_original_update_and_draw_ID_from_production": True})
    native = replay(arm, source, snaps)
    # Native selectors and quad geometry establish top-to-bottom order3,2,1.
    # Compare complete opaque upper screens to independently assembled source.
    canvas = Image.new("RGB", (256, 384))
    for n, index in enumerate((3, 2, 1)):
        canvas.paste(a.texture(index).render().convert("RGB").point(lambda x: x >> 3), (0, n * 128))
    windows = {sha(canvas.crop((0, top, 256, top + 192)).tobytes()): top for top in range(129)}
    composites = []
    for frame in range(18000, 21001):
        now = Image.open(normal_shots[frame]["path"]).convert("RGB").point(lambda x: x >> 3).crop((0, 0, 256, 192)).tobytes()
        top = windows.get(sha(now))
        if top is not None:
            assert now == canvas.crop((0, top, 256, top + 192)).tobytes()
            composites.append({"frame": frame, "source_y": top, "entire49152_upper_pixels_exact": True})
    assert len(composites) >= 2300 and min(x["source_y"] for x in composites) == 0
    assert max(x["source_y"] for x in composites) == 128
    proof = {"format": "dk4-ending-pan-rows-v596", "candidate": str(ROM), "candidate_sha256": manifest["parent_sha256"],
             "research_fixture": manifest, "reports": [normal_report, control_report],
             "source_exact_original_code_ranges": code_ranges, "whole_two_screen_control_pairs": pairs,
             "actual_decoded_original_and_marked_texture_bindings": decoded, "original_per_frame_replay": native,
             "actual_whole_upper_source_pan_composites": composites,
             "same_frame_exact_pair_count": sum(x["same_frame_exact"] for x in pairs),
             "same_frame_different_pair_count": sum(not x["same_frame_exact"] for x in pairs),
             "one_update_aligned_pair_count": sum(x["control_frame"] != x["frame"] for x in pairs),
             "fixed_one_update_alignment_interval": [18028, 21000],
             "research_movie_one_original_update_ahead_cause_not_established": True,
             "specific_M31_texture1_rows64_through127_are_outside_this_pan": True,
             "all_16358_marker_changes_including_row64_loaded_without_changing_captured_output": True,
             "other_ending_effects_movies_hardware_and_earned_completion_remain_open": True,
             "no_normal_gameplay_or_guide_credit_for_ending_fixture": True,
             "production_ROM_or_patch_changed": False, "full_goal_complete": False,
             "script_sha256": sha(Path(__file__).read_bytes())}
    (ROOT / "pan_rows_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(f"V596: {len(pairs)} entire framebuffer pairs with explicit0/-1 alignment;{native['original_update_calls']} original updates;{len(native['actual_complete_controller_anchors'])} whole-controller anchors;{len(composites)} whole source composites. Lil tile1 lower64 rows excluded in this pan.")


if __name__ == "__main__":
    main()
