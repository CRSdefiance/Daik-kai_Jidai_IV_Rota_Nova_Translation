"""Verify complete village labels, native names/input/development and regressions."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.village_ui_compact import apply_release
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, STOP, call, machine
from scripts.run_village_ui_v610 import relocate
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_village_wrap_v608 import read, report, save

ROOT = Path("work/analysis/village_ui_v610")
ROM = Path("out/all_routes_combined_v610_candidate.nds")
PARENT = Path("out/all_routes_combined_v608_candidate.nds")
DIGEST = "bf3dbc0cf6e27c73f08d2e12c7f91ce0ee9bbe180e0cd01d6248983aa8f67599"
BAD = "8a5d32954b482cfd47e91408964a3d200c0023f5ae57087b9cb1cb72124a68a2"


def snapshot(report_data, frame):
    rows = report_data.get("read_only_pause_RAM_snapshots", []) + report_data.get("read_only_capture_RAM_snapshots", [])
    row = next(r for r in rows if r["frame"] == frame)
    raw = Path(row["path"]).read_bytes()
    assert row["read_only_export"] and len(raw) == 0x400000 and sha(raw) == row["sha256"]
    return raw


def main():
    assert sha(ROM.read_bytes()) == DIGEST
    parent, rom = NdsImage.open(PARENT), NdsImage.open(ROM)
    before = {p: data for _, p, data in parent.iter_files()} | dict(parent.iter_components())
    after = {p: data for _, p, data in rom.iter_files()} | dict(rom.iter_components())
    assert before.keys() == after.keys()
    assert sorted(p for p in before if before[p] != after[p]) == ["/__arm9__.bin", "/data/SC2.DK4"]
    old_arm, arm = before["/__arm9__.bin"], after["/__arm9__.bin"]
    a, s, transform = apply_release(old_arm, before["/data/SC2.DK4"], "translations/village_ui_text_v2.json")
    assert arm == a and s == after["/data/SC2.DK4"]
    assert transform["pool_growth"] == 0 and len(transform["placements"]) == 30
    assert len(transform["same_width_name_corrections"]) == 3
    old_code, code = [MainCodeFile(x, BASE) for x in (old_arm, arm)]
    assert all(bytes(old_code.sections[i].data) == bytes(code.sections[i].data) for i in (1, 2, 3, 4))
    assert all(arm[o:o + 4] == old_arm[o:o + 4] for o in (0x8E4, 0xE45DC, 0xE45E4))
    for lo, hi in transform["interleaved_RTTI_metadata_preserved"]:
        assert arm[lo:hi] == old_arm[lo:hi]
    manifest, previous = read(ROM.with_suffix(".manifest.json")), read(PARENT.with_suffix(".manifest.json"))
    registry = read("translations/release_stack.json")
    assert manifest["profile"] == "all-routes-unified-v610" and manifest["candidate_sha256"] == DIGEST
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    assert manifest["base_sha256"] == registry["canonical_baseline"]["sha256"]
    assert sha(Path(manifest["base_rom"]).read_bytes()) == manifest["base_sha256"]
    assert manifest["batches"] == previous["batches"] and len(manifest["batches"]) == 470
    assert manifest["required_batches"] == previous["required_batches"] and len(registry["accepted_layers"]) == 114
    assert all(manifest["checks"].values())
    assert sha((ROOT / "patch_reconstructed.nds").read_bytes()) == DIGEST
    patch_sha = sha(ROM.with_suffix(".xdelta").read_bytes())
    assert patch_sha == "43b97163853f12cdc62d5f2d26f7471f49dfce753d7364ad1f07df8552146db8"
    preservation = read(ROOT / "preservation_proof.json")
    assert preservation["candidate_sha256"] == DIGEST and preservation["current921_format_palette_extent_checks"]
    assert preservation["all57_embedded_block_extents_exact"]
    village, shots, village_binding = report("village_ui_v610_inuvik", 14200, DIGEST)
    donor = village["battery_save_preloaded"]
    assert donor["source_sha256"] == sha(Path(donor["source"]).read_bytes()) == "958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb"
    raw = snapshot(village, 5200)
    _, fixture = relocate(arm, raw, 0)
    assert village["synthetic_location_fixtures"] == [dict(fixture, frame=5200)]
    assert not any(v for k, v in village.items() if k.startswith("synthetic_") and k != "synthetic_location_fixtures")
    font = GameAsciiFont.from_arm9(arm)
    menu_specs = [("Resupply", 104, 232), ("Stay", 116, 252), ("Repair Ship", 95, 272),
                  ("Recruit Sailors", 83, 292), ("Set Sail", 104, 312), ("Promised Words", 86, 332)]
    masks = []
    for frame in (6900, 7000, 7100, 7200, 7300, 7400):
        image = Image.open(shots[frame]["path"]).convert("RGB")
        expected = set()
        for text, x, y in menu_specs:
            ink, bounds = complete_mask(font, text, image, x, y, (8, 8, 8))
            masks.append({"frame": frame, "English": text, "ink_pixels": ink, "bounds": bounds})
            for n, char in enumerate(text):
                glyph = font.decode(char)
                expected |= {(x + n * 6 + xx, y + yy) for yy in range(11) for xx in range(6)
                             if glyph.getpixel((xx, yy))}
        assert len(expected) == 694
        for y in range(228, 348):
            for x in range(80, 176):
                assert (image.getpixel((x, y)) == (8, 8, 8)) == ((x, y) in expected)
    name_masks = []
    for frame, text in ((6000, "Discovered Inuvik."), (6400, "Dock at Inuvik?")):
        image = Image.open(shots[frame]["path"]).convert("RGB")
        ink, bounds = complete_mask(font, text, image, 16, 296, (0, 8, 0))
        name_masks.append({"frame": frame, "text": text, "ink_pixels": ink, "bounds": bounds})
    # Actual initialized village models; no synthesized object or name getter.
    raw = snapshot(village, 6900)
    old_raw = Path("E:/Rota Nova translations/Generated/work/emulation_v193/village_wrap_v608_inuvik/frame_005200_arm9_ram.bin").read_bytes()
    u = machine(arm)
    u.mem_write(BASE, raw)
    call(u, 0xCB118, ())
    master = u.reg_read(UC_ARM_REG_R0)
    names = []
    for row in (r for r in transform["placements"] if r["kind"] == "name"):
        call(u, 0xCACAC, (master, row["index"]))
        model = u.reg_read(UC_ARM_REG_R0)
        offset = model - BASE
        vt = struct.unpack("<I", u.mem_read(model, 4))[0]
        assert vt == 0x0215AF74
        getter = struct.unpack("<I", u.mem_read(vt + 8, 4))[0]
        call(u, getter - BASE, (model,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        name = bytes(u.mem_read(pointer, 40)).split(b"\0", 1)[0].decode("ascii")
        assert pointer == row["target_pointer"] and name == row["English"]
        assert raw[offset:offset + 8] == old_raw[offset:offset + 8]
        assert raw[offset + 12:offset + 52] == old_raw[offset + 12:offset + 52]
        for reg, value in ((UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, STOP), (UC_ARM_REG_R0, 297),
                           (UC_ARM_REG_R1, pointer), (UC_ARM_REG_R2, 0), (UC_ARM_REG_R3, 0)):
            u.reg_write(reg, value)
        # Execute the real Common297 getter and variadic formatter; stop before
        # the interactive modal drawing/body, rather than bridging its result.
        u.emu_start(BASE + 0x546B8, BASE + 0x5479C, count=1000000)
        assert u.reg_read(UC_ARM_REG_PC) == BASE + 0x5479C
        prepared = "Discovered " + name + "."
        for field in (0x54890, 0x54894):
            buffer = struct.unpack_from("<I", arm, field)[0]
            assert bytes(u.mem_read(buffer, 240)).split(b"\0", 1)[0].decode("ascii") == prepared
        assert len(prepared) * 6 <= 216
        names.append({"index": row["index"], "English": name, "actual_model": model, "actual_pointer": pointer,
                      "original_discovery_preparation_both_buffers_exact": prepared,
                      "first_final_characters_and_all24_model_geometry_unchanged": True})
    assert len(names) == 24
    history = read(ROOT / "keyboard_navigation.json")
    assert len(history) == 18
    marker = read("work/analysis/village_promised_words_plan.json")["keyboard_wrapper"]["provider_vtable"]
    needle = struct.pack("<I", marker)
    entered = snapshot(village, 10400)
    parents = [n - 4 for n in range(0x170000, len(entered) - 4, 4) if entered[n:n + 4] == needle]
    assert len(parents) == 1
    editor = parents[0]
    assert entered[editor + 0xB4:editor + 0xBB] == b"Aurora\0"
    assert struct.unpack_from("<I", entered, editor + 0x78)[0] == 6
    assert struct.unpack_from("<I", entered, editor + 0xD8)[0] == 18
    for step in history:
        b = snapshot(village, step["frame"])
        actual = b[editor + 0xB4:editor + 0xB4 + 19].split(b"\0", 1)[0].decode("ascii")
        assert actual == step["state"]["entry"] and "Aurora".startswith(actual)
    # Confirm the original success branch and village development, not an
    # intended password or a supplied flag. Initial fixture owns only coordinates.
    clean = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    assert arm[0x78AF4:0x78B24] == clean[0x78AF4:0x78B24]
    statuses = []
    for frame, expected in ((6900, 0), (10400, 0), (11300, 2), (14200, 2)):
        b = snapshot(village, frame)
        uc = machine(arm)
        uc.mem_write(BASE, b)
        call(uc, 0xCB178, ())
        town = uc.reg_read(UC_ARM_REG_R0) + 4 + 90 * 108
        call(uc, 0xB50D8, (town,))
        actual = uc.reg_read(UC_ARM_REG_R0)
        assert actual == expected
        statuses.append({"frame": frame, "town90": town, "original_development_check": actual})
    market, market_shots, market_binding = report("village_ui_v610_market", 24100, DIGEST)
    old_market, old_shots, old_binding = report("village_wrap_v608_market", 24100, sha(PARENT.read_bytes()))
    assert market["scripted_input_schedule"] == old_market["scripted_input_schedule"]
    assert not market.get("battery_save_preloaded")
    assert not any(v for k, v in market.items() if k.startswith("synthetic_"))
    assert set(market_shots) == set(old_shots) and len(market_shots) == 19
    assert all(market_shots[f]["PNG_sha256"] == old_shots[f]["PNG_sha256"] for f in market_shots)
    # Preserve and classify the failed predecessor and the storage-only control.
    _, bad_shots, bad_binding = report("village_ui_v609_market", 24100, BAD)
    bad_image = Image.open(bad_shots[24100]["path"]).convert("RGB")
    assert not any(bad_image.crop((0, 0, 256, 192)).tobytes())
    probes = {}
    for kind in ("compact", "growth_only"):
        path = Path(f"work/analysis/village_ui_v609/{kind}_RESEARCH_ONLY.nds")
        r, images, receipt = report(f"village_ui_v609_{kind}_probe", 5200, sha(path.read_bytes()))
        assert r["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
        image = Image.open(images[5200]["path"]).convert("RGB")
        if kind == "growth_only":
            assert not any(image.crop((0, 0, 256, 192)).tobytes())
            probe_rom = NdsImage.open(path)
            assert probe_rom.read_file("/data/SC2.DK4") == before["/data/SC2.DK4"]
            probe_arm = probe_rom.read_file("/__arm9__.bin")
            for row in transform["placements"]:
                field = row["pointer_field"]
                assert probe_arm[field:field + 4] == old_arm[field:field + 4]
        else:
            assert image.tobytes() == Image.open(shots[5200]["path"]).convert("RGB").tobytes()
        probes[kind] = receipt
    save(ROOT / "final_recorded_inputs.json", village["scripted_input_schedule"])
    save(ROOT / "release_proof.json", {"candidate": str(ROM), "candidate_sha256": DIGEST,
        "patch_sha256": patch_sha, "canonical_base": manifest["base_rom"], "canonical_base_sha256": manifest["base_sha256"],
        "script_sha256": sha(Path(__file__).read_bytes()), "transform": transform,
        "all470_batches114_accepted_layers_and_exact_clean_patch": True,
        "all_staged_pool_startup_arena_cache_and_native_code_exact_V608": True,
        "all_art_and_other_routes_exact_V608": True, "only_ARM9_and_three_SC2_same_width_names_changed": True,
        "complete_menu_masks": masks, "menu_complete_ink_pixels_across_six_frames": 4164,
        "all_six_whole_96x120_menu_foreground_regions_exact": True, "actual_Inuvik_name_masks": name_masks,
        "all24_actual_name_getters_and_original_discovery_preparations": names,
        "ordinary_keyboard_Aurora_entry_verified": True, "keyboard_editor_parent": editor + BASE,
        "keyboard_navigation_steps": len(history), "original_password_success_and_development_checks": statuses,
        "developed_Inuvik_port_screen": shots[14200], "typed_password_under_location_fixture_not_user_save_progress": True,
        "village_frames": 14200, "ordinary_market_frames": 24100, "all19_ordinary_whole_frames_exact_V608": True,
        "rejected_V609_and_growth_only_upper_screens_black": True, "exact_growth_failure_mechanism_still_unresolved": True,
        "probes": probes, "reports": {"village": village_binding, "market": market_binding,
                                       "baseline_market": old_binding, "rejected_V609_market": bad_binding},
        "all24_villages_ordinary_GPU_contexts_not_claimed": True,
        "all8_original_village_card_contexts_still_open": True,
        "all18_plaques_incomplete_all22_historical_objects_retained": True,
        "human_accepted": False, "full_goal_complete": False})
    print("V610:36 complete menu masks;24 actual names/preparations;typed Aurora/development/port;19 ordinary screens;V609 growth-only failure isolated;full integration/patch pass.")


if __name__ == "__main__":
    main()
