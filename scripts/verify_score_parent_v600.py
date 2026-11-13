"""Correct score ownership and verify the original result parent with explicit limits."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageChops
from unicorn import UC_HOOK_CODE
from unicorn import arm_const as registers
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_name_treasure_graphics_v161 import mask_for
from scripts.verify_portrait_native_pixels_v202 import native5

ROOT = Path("work/analysis/material_review_v600")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193")
ROM = Path("out/all_routes_combined_v599_candidate.nds")
BASE, OWNER = 0x02000000, 0x02313A38
LUT = [(n * 31 + 127) // 255 for n in range(256)] * 3


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def quantized(path):
    return Image.open(path).convert("RGB").point(LUT)


def opaque(atlas, sx, width, x, y):
    palette = struct.unpack_from("<16H", atlas.source, 20)
    return [(x + xx, y + yy, native5(atlas.palette[index]))
            for yy in range(24) for xx in range(width)
            if palette[index := atlas.indices[yy * atlas.width + sx + xx]] & 0x8000
            and 0 <= x + xx < 256 and 0 <= y + yy < 384]


def composed(blank, atlas, pair):
    result = blank.copy()
    for rect, sx in zip(pair, (160, 184), strict=True):
        for x, y, color in opaque(atlas, sx, 24, rect[0] + 32, rect[1] + 192):
            result.putpixel((x, y), color)
    return result


def animation(arm, raw):
    u = machine(arm)
    u.mem_write(BASE, raw)
    model = 0x02462000
    u.mem_write(model, bytes(0x900))
    u.mem_write(model + 0x8E4, struct.pack("<3I", 10, 2, 12))
    states = []

    def pump(uc, address, size, data):
        if address != 0x020CF7A4:
            return
        sp = uc.reg_read(UC_ARM_REG_SP)
        objects = [bytes(uc.mem_read(sp + at, 0xC8)) for at in (0xA4, 0x16C)]
        for n, obj in enumerate(objects):
            assert struct.unpack_from("<I", obj)[0] == 0x0213038C
            assert struct.unpack_from("<I", obj, 0x34)[0] == 1 - n
            assert struct.unpack_from("<12I", obj, 0x98)[3:12] == (OWNER, 0, 4, 0, 160 + n * 24, 0, 0, 24, 24)
        states.append({"objects_hex": [o.hex() for o in objects],
                       "rectangles": [list(struct.unpack_from("<4i", obj, 0x20)) for obj in objects]})
        uc.reg_write(UC_ARM_REG_R0, 0)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    handle = u.hook_add(UC_HOOK_CODE, pump)
    try:
        executed = call(u, 0xA964, (model,), instruction_limit=1000000)
    finally:
        u.hook_del(handle)
    assert len(states) == 93 and {0x0200A6BC, 0x0200C354, 0x0200C14C} <= executed
    assert not {0x020DED50, 0x020DEBDC} & executed
    return states


def helper_abi(arm, raw):
    cases = []
    for gate, flags in ((True, 0), (True, 0xA0000000), (False, 0x50000000)):
        u = machine(arm)
        u.mem_write(BASE, raw)
        u.mem_write(0x01FFD100, struct.pack("<I", int(gate)))
        expected = {getattr(registers, f"UC_ARM_REG_R{n}"): 0xA5A50000 + n for n in range(13)}
        for reg, value in expected.items():
            u.reg_write(reg, value)
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, 0x027E0000)
        cpsr = (u.reg_read(registers.UC_ARM_REG_CPSR) & 0x0FFFFFFF) | flags
        u.reg_write(registers.UC_ARM_REG_CPSR, cpsr)
        calls = []

        def result(uc, address, size, data, calls=calls):
            if address == 0x0200A964:
                calls.append(uc.reg_read(UC_ARM_REG_R0))
                uc.reg_write(UC_ARM_REG_R0, 0xDEADBEEF)
                uc.reg_write(registers.UC_ARM_REG_CPSR,
                             (uc.reg_read(registers.UC_ARM_REG_CPSR) & 0x0FFFFFFF) | 0xF0000000)
                uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

        handle = u.hook_add(UC_HOOK_CODE, result)
        try:
            u.emu_start(0x020CF7A4, 0x020CF7A8, count=10000)
        finally:
            u.hook_del(handle)
        assert u.reg_read(UC_ARM_REG_PC) == 0x020CF7A8 and u.reg_read(UC_ARM_REG_SP) == STACK - 12
        assert all(u.reg_read(reg) == value for reg, value in expected.items())
        assert u.reg_read(UC_ARM_REG_LR) == 0x027E0000 and u.reg_read(registers.UC_ARM_REG_CPSR) == cpsr
        assert bytes(u.mem_read(STACK - 12, 12)) == struct.pack("<3I", expected[registers.UC_ARM_REG_R4],
            expected[registers.UC_ARM_REG_R5], 0x027E0000)
        assert calls == ([0x01FFD200] if gate else [])
        assert struct.unpack("<I", u.mem_read(0x01FFD100, 4))[0] == 0
        cases.append({"gate": gate, "original_CPSR": cpsr, "all13_registers_LR_flags_and_displaced_push_exact": True,
                      "result_selector_only_bridged_in_this_wrapper_ABI_probe": True})
    return cases


def main():
    fixture = read(ROOT / "native_score_fixture_manifest.json")
    assert fixture["script_sha256"] == sha(Path("scripts/prepare_score_parent_v600.py").read_bytes())
    assert sha(ROM.read_bytes()) == fixture["production_ROM_sha256"]
    current, clean = NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    arm = current.read_file("/__arm9__.bin")
    init = machine(arm)
    call(init, 0x10E190, (), instruction_limit=1000000)
    bindings = []
    for owner, name in ((0x023139FC, b"_pxl/deckchip15.pxl"), (OWNER, b"_pxl/deck04.pxl")):
        pointer = struct.unpack("<I", init.mem_read(owner + 12, 4))[0]
        actual = bytes(init.mem_read(pointer, 64)).split(b"\0")[0]
        assert actual == name
        bindings.append({"owner": owner, "actual_initialized_filename_pointer": pointer,
                         "actual_initialized_filename": actual.decode("ascii")})
    assert struct.unpack_from("<I", arm, 0x10F3A8)[0] == 0x023139FC
    assert struct.unpack_from("<I", arm, 0x10F3AC)[0] == 0x02160A20
    assert arm[0x160A20:0x160A20 + 16] == b"_pxl/deck04.pxl\0"
    reports, shots, bindings_reports = {}, {}, {}
    for kind, item in fixture["research_ROMs"].items():
        assert sha(Path(item["path"]).read_bytes()) == item["sha256"]
        report_path = CAPTURE / f"native_score_v600_{kind}/capture_report.json"
        r = read(report_path)
        assert r["ROM_sha256"] == item["sha256"] and r["frames"] == 7100
        assert r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"]
        save_source = r["battery_save_preloaded"]
        assert save_source["source_sha256"] == "958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb"
        assert sha(Path(save_source["source"]).read_bytes()) == save_source["source_sha256"]
        assert r["scripted_input_schedule"] == read("work/analysis/ship_batteries_v593/deck_replay_inputs.json")
        s = r["read_only_native_state"]
        assert s["read_only_export"] and not s["state_loaded"]
        itcm = Path(s["regions"]["ITCM"]["path"]).read_bytes()
        assert sha(itcm) == s["regions"]["ITCM"]["sha256"]
        assert struct.unpack_from("<I", itcm, 0x5100)[0] == 0
        assert struct.unpack_from("<3I", itcm, 0x5200 + 0x8E4) == (10, 2, 12)
        for row in r["frames_captured"]:
            assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        shots[kind] = {row["frame"]: row for row in r["frames_captured"]}
        reports[kind] = r
        bindings_reports[kind] = {"path": str(report_path), "sha256": sha(report_path.read_bytes())}
    final_raw = Path(reports["current"]["read_only_RAM_snapshot"]["path"]).read_bytes()
    abi_cases = helper_abi(NdsImage.open(fixture["research_ROMs"]["current"]["path"]).read_file("/__arm9__.bin"), final_raw)
    resident = []
    for kind in reports:
        raw_path = Path(reports[kind]["read_only_RAM_snapshot"]["path"])
        raw = raw_path.read_bytes()
        uc = machine(arm)
        uc.mem_write(BASE, raw)
        filename = struct.unpack_from("<I", raw, OWNER + 12 - BASE)[0]
        assert raw[filename - BASE:filename - BASE + 16] == b"_pxl/deck04.pxl\0"
        vt = struct.unpack_from("<I", raw, OWNER - BASE)[0]
        getter = struct.unpack_from("<I", raw, vt - BASE)[0]
        executed = call(uc, getter - BASE, (OWNER,))
        pointer = uc.reg_read(UC_ARM_REG_R0)
        expected = NdsImage.open(fixture["research_ROMs"][kind]["path"]).read_file("/_pxl/deck04.pxl")
        assert bytes(uc.mem_read(pointer, len(expected))) == expected
        assert not {0x020DED50, 0x020DEBDC} & executed
        resident.append({"kind": kind, "owner": OWNER, "getter": getter, "resident_header": pointer,
                         "whole_named_file_exact": True, "no_resource_or_SDK_bridge": True})
    states = animation(arm, final_raw)
    save(ROOT / "original_result_animation_states.json", {"states": states, "frame_pump_only_bridged": True,
        "source_geometry_not_93_new_gameplay_screens": True})
    poses = sorted({tuple(tuple(r) for r in s["rectangles"]) for s in states})
    atlases = {"current": PxlImage.from_bytes(current.read_file("/_pxl/deck04.pxl")),
               "original_score_control": PxlImage.from_bytes(clean.read_file("/_pxl/deck04.pxl"))}
    batch = read("translations/score_won_lost_graphics_v1.json")
    glyphs = []
    for row in batch["records"]:
        expected, _ = mask_for(arm, batch, row)
        box = row["box"]
        points = {(x, y) for y in range(box[1], box[3]) for x in range(box[0], box[2])
                  if expected.getpixel((x, y + 2))}
        actual = {(x, y) for y in range(box[1], box[3]) for x in range(box[0], box[2])
                  if atlases["current"].indices[y * 208 + x] == 15}
        assert actual == points
        glyphs.append({"word": row["text"], "all_first_final_and_inner_ink_pixels": len(points)})
    digit_poses = []
    for pair in poses:
        points = []
        for sx, dx, rect in ((16, 0, pair[0]), (0, 16, pair[0]), (32, 16, pair[1])):
            points.extend(opaque(atlases["current"], sx, 16, rect[0] + dx, rect[1] + 192))
        digit_poses.append((pair, points))
    results = {"unchanged": [], "whole_composites_exact": [], "no_digit_anchor": [],
               "multiple_digit_poses": [], "whole_composite_mismatch": []}
    for frame in range(4200, 4651):
        blank = quantized(shots["blank_label_control"][frame]["path"])
        new, old = [quantized(shots[kind][frame]["path"]) for kind in ("current", "original_score_control")]
        if blank.tobytes() == new.tobytes() == old.tobytes():
            results["unchanged"].append(frame)
            continue
        pixels = blank.load()
        candidates = [(pair, points) for pair, points in digit_poses
                      if points and all(pixels[x, y] == color for x, y, color in points)]
        if not candidates:
            results["no_digit_anchor"].append(frame)
            continue
        if len(candidates) != 1:
            results["multiple_digit_poses"].append(frame)
            continue
        pair, points = candidates[0]
        expected = [composed(blank, atlases[kind], pair) for kind in ("current", "original_score_control")]
        differences = [ImageChops.difference(a, b).getbbox() for a, b in zip(expected, (new, old), strict=True)]
        if any(differences):
            results["whole_composite_mismatch"].append({"frame": frame, "difference_bounds": differences,
                "independent_digit_anchored_rectangles": pair, "digit_anchor_points": len(points)})
        else:
            results["whole_composites_exact"].append({"frame": frame, "independent_digit_anchored_rectangles": pair,
                                                      "unchanged_digit_anchor_points": len(points)})
    assert len(results["whole_composites_exact"]) == 323 and len(results["unchanged"]) == 99
    assert len(results["no_digit_anchor"]) == 12 and len(results["whole_composite_mismatch"]) == 17
    assert not results["multiple_digit_poses"]
    # Independent live blank-run controller snapshot: no geometry selected from lettering.
    raw = (CAPTURE / "native_score_v600_blank_label_control/frame_004500_arm9_ram.bin").read_bytes()
    live = []
    for at in range(0, len(raw) - 0xC8, 4):
        if (struct.unpack_from("<I", raw, at)[0] == 0x0213038C
                and struct.unpack_from("<I", raw, at + 0x98 + 12)[0] == OWNER):
            live.append({"address": BASE + at, "won": struct.unpack_from("<I", raw, at + 0x34)[0],
                         "rectangle": list(struct.unpack_from("<4i", raw, at + 0x20))})
    assert [(v["won"], v["rectangle"]) for v in live] == [(1, [56, 84, 128, 108]), (0, [128, 84, 200, 108])]
    assert any(row["frame"] == 4500 for row in results["whole_composites_exact"])
    all_frames = sorted(shots["current"].keys() & shots["original_score_control"].keys())
    unchanged, different = [], []
    for frame in all_frames:
        new, old = [quantized(shots[kind][frame]["path"]) for kind in ("current", "original_score_control")]
        bounds = ImageChops.difference(new, old).getbbox()
        (different if bounds else unchanged).append({"frame": frame, "difference_bounds": bounds} if bounds else frame)
    save(ROOT / "native_score_parent_proof.json", {"production_ROM": str(ROM),
        "production_ROM_sha256": sha(ROM.read_bytes()), "production_ROM_or_patch_changed": False,
        "corrected_original_initialized_owners": bindings,
        "old_V164_adjacent_owner_filename_pairing_superseded": True,
        "real_score_setup": 0x0200C14C, "real_label_painter": 0x0200C054,
        "ordinary_parent_entry_lead": 0x02073DE0, "source_call_chain": [0x0200A54C, 0x0200A5A8, 0x0200A994, 0x0200A964],
        "all_original_rendering_and_source_selection_code_preserved": True,
        "research_fixture_manifest": str(ROOT / "native_score_fixture_manifest.json"),
        "fixture_manifest_sha256": sha((ROOT / "native_score_fixture_manifest.json").read_bytes()),
        "reports": bindings_reports, "actual_native_resident_files": resident,
        "native_final_ITCM_one_shot_guards_zero_and_counters10_2_12": True,
        "research_wrapper_ABI_cases": abi_cases,
        "complete_independent_English_masks": glyphs, "original_animation_updates": len(states),
        "independent_live_blank_controller_4500": live, "native_three_way_frame_results": results,
        "whole_native5_composites_checked": 323 * 2, "whole_native5_composite_positions": 323 * 2 * 98304,
        "all_same_frame_original_current_comparisons": len(all_frames), "whole_identical_pairs": unchanged,
        "different_pairs": different,
        "failed_and_unanchored_frames_retained_not_silently_retimed_or_excluded": True,
        "remaining": "Resolve 12 unanchored and 17 failed whole triples; source/current phase and early clipping not proven for every frame. Earned result context remains unverified.",
        "research_only_not_normal_battle_or_guide_evidence": True, "full_goal_complete": False,
        "script_sha256": sha(Path(__file__).read_bytes())})
    print(f"V600:corrected score owner;native original result parent and resident files;94 English ink points;646 whole composites exact;12 unanchored/17 mismatches retained;{len(unchanged)} whole pairs identical.")


if __name__ == "__main__":
    main()
