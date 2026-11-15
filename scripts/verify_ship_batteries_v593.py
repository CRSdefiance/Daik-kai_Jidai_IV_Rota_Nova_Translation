"""Verify complete native room headings, ship plaque and registered patch."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ship_battery_labels import ARM, FACE, FILE, SLOTS, apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_portrait_native_pixels_v202 import native5

ROOT = Path("work/analysis/ship_batteries_v593")
ROM = Path("out/all_routes_combined_v593_candidate.nds")
PARENT = Path("out/all_routes_combined_v591_candidate.nds")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193")
DECK_CASES = {5560: ("Gun Deck", "Battery"), 5640: ("Marines", "Quarters"),
              6680: ("Gun Deck", "Battery"), 6720: ("Gun Deck", "Battery"), 6760: ("Gun Deck", "Battery"),
              6840: ("Marines", "Quarters"), 6880: ("Marines", "Quarters"), 6920: ("Marines", "Quarters")}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_report(folder, digest, frames, inputs):
    path = folder / "capture_report.json"
    r = read(path)
    assert r["ROM_sha256"] == digest and r["frames"] == frames
    assert r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"]
    assert not any(value for key, value in r.items() if key.startswith("synthetic_"))
    assert r["scripted_input_schedule"] == inputs
    save = r["battery_save_preloaded"]
    assert save["source_sha256"] == "958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb"
    assert sha(Path(save["source"]).read_bytes()) == save["source_sha256"]
    for s in r["frames_captured"]:
        assert sha(Path(s["path"]).read_bytes()) == s["PNG_sha256"]
    for key in ("read_only_capture_RAM_snapshots", "read_only_pause_RAM_snapshots"):
        for s in r.get(key, []):
            assert sha(Path(s["path"]).read_bytes()) == s["sha256"]
    return r, {"path": str(path), "sha256": sha(path.read_bytes())}


def mask(font, text, x=72, y=24, advance=6):
    return {(x + n * advance + xx, y + yy) for n, ch in enumerate(text)
            for yy in range(11) for xx in range(6) if font.decode(ch).getpixel((xx, yy))}


def composed(blank, points):
    result = bytearray(blank.tobytes())
    for x, y in points:
        offset = (y * 256 + x) * 3
        result[offset:offset + 3] = b"\xE6" * 3
    return bytes(result)


def main():
    current, parent, clean = [NdsImage.open(p) for p in (ROM, PARENT, Path("work/clean.nds"))]
    digest, previous = sha(ROM.read_bytes()), sha(PARENT.read_bytes())
    assert previous == "7f2d10824e18d276adb23b01be48dac2d27adc2c4ec8ec16bb39a93a90dc3d73"
    manifest, prior = read(ROM.with_suffix(".manifest.json")), read(PARENT.with_suffix(".manifest.json"))
    stack = read("translations/release_stack.json")
    assert manifest["profile"] == "all-routes-unified-v593" and manifest["candidate_sha256"] == digest
    assert manifest["base_sha256"] == stack["canonical_baseline"]["sha256"]
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    assert manifest["batches"] == prior["batches"] and len(manifest["batches"]) == 470
    assert manifest["required_batches"] == prior["required_batches"] and len(stack["accepted_layers"]) == 114
    assert all(manifest["checks"].values())
    before = {p: data for _, p, data in parent.iter_files()} | dict(parent.iter_components())
    after = {p: data for _, p, data in current.iter_files()} | dict(current.iter_components())
    assert before.keys() == after.keys()
    assert sorted(p for p in before if before[p] != after[p]) == sorted((ARM, FILE))
    outputs, stages = apply_release(parent, clean, "translations/ship_battery_labels_v1.json")
    assert all(after[path] == data for path, data in outputs.items())
    arm_changes = [n for n, (a, b) in enumerate(zip(before[ARM], after[ARM], strict=True)) if a != b]
    assert set(arm_changes) <= {n for offset, _, _, _ in SLOTS for n in range(offset, offset + 12)}
    font, old_font = [GameAsciiFont.from_arm9(data[ARM]) for data in (after, before)]
    assert font.glyphs == old_font.glyphs
    original, revised = [PxlImage.from_bytes(d[FILE]) for d in (before, after)]
    assert original.source[:original.pixels_offset] == revised.source[:revised.pixels_offset]
    changed = {(n % 256, n // 256) for n, (a, b) in enumerate(zip(original.indices, revised.indices, strict=True)) if a != b}
    assert len(changed) == 139
    preservation_path = Path("work/analysis/ship_quarters_v591/preservation_proof.json")
    preservation = read(preservation_path)
    assert preservation["candidate_sha256"] == previous and len(preservation["entries"]) == 921
    assert all(before[r["path"]] == after[r["path"]] for r in preservation["entries"] if r["path"] != FILE)
    make_xdelta(Path("work/clean.nds"), ROM, ROM.with_suffix(".xdelta"))
    reconstruction = ROOT / "reconstructed_exact.nds"
    apply_xdelta(Path("work/clean.nds"), ROM.with_suffix(".xdelta"), reconstruction)
    assert reconstruction.read_bytes() == ROM.read_bytes()
    deck_inputs = read(ROOT / "deck_replay_inputs.json")
    ship_inputs = read("work/analysis/ship_quarters_v591/replay_inputs.json")
    fixture = read(ROOT / "deck_empty_labels_RESEARCH_ONLY.fixture.json")
    fixture_rom = NdsImage.open(fixture["research_ROM"])
    assert fixture["research_only"] and fixture["not_playable_or_registered_release"]
    assert fixture["parent_sha256"] == previous and sha(fixture_rom.source.read_bytes()) == fixture["research_ROM_sha256"]
    fixture_files = {p: data for _, p, data in fixture_rom.iter_files()} | dict(fixture_rom.iter_components())
    assert [p for p in before if before[p] != fixture_files[p]] == [ARM]
    assert [n for n, (a, b) in enumerate(zip(before[ARM], fixture_files[ARM], strict=True)) if a != b] == [0x12FFFC, 0x130008]
    reports, bindings = {}, {}
    specs = (("deck_control", "ship_batteries_v592", previous, 6920, deck_inputs),
             ("deck_blank", "ship_batteries_v593_deck_blank", fixture["research_ROM_sha256"], 6920, deck_inputs),
             ("deck_actual", "ship_batteries_v593_deck_actual", digest, 6920, deck_inputs),
             ("ship_control", "ship_quarters_v591_actual", previous, 5840, ship_inputs),
             ("ship_actual", "ship_batteries_v593_ships_actual", digest, 5840, ship_inputs))
    for name, folder, version, frames, inputs in specs:
        reports[name], bindings[name] = load_report(CAPTURE / folder, version, frames, inputs)
    assert all(r["core_options"] == reports["deck_actual"]["core_options"] for r in reports.values())
    shots = {name: {s["frame"]: s for s in r["frames_captured"]} for name, r in reports.items()}
    deck_cases, negatives = [], []
    for frame in sorted(shots["deck_actual"]):
        old, blank, new = [Image.open(shots[name][frame]["path"]).convert("RGB")
                           for name in ("deck_control", "deck_blank", "deck_actual")]
        assert old.size == blank.size == new.size == (256, 384)
        old_word, new_word = DECK_CASES.get(frame, ("", ""))
        old_points, new_points = mask(font, old_word), mask(font, new_word)
        assert old.tobytes() == composed(blank, old_points), ("original whole composite", frame)
        assert new.tobytes() == composed(blank, new_points), ("new whole composite", frame)
        if new_word:
            ink, bounds = complete_mask(font, new_word, new, 72, 24, (230, 230, 230))
            assert ink == len(new_points)
            raw = (CAPTURE / f"ship_batteries_v593_deck_actual/frame_{frame:06d}_arm9_ram.bin").read_bytes()
            assert all(raw[offset:offset + 12] == after[ARM][offset:offset + 12] for offset, _, _, _ in SLOTS)
            if frame in (6760, 6920):
                for n in (0, len(new_word) - 1):
                    partial = bytearray(new.tobytes())
                    missing = mask(font, new_word[n], 72 + n * 6, 24)
                    for x, y in missing:
                        at = (y * 256 + x) * 3
                        partial[at:at + 3] = blank.tobytes()[at:at + 3]
                    assert bytes(partial) != composed(blank, new_points)
                    negatives.append({"frame": frame, "word": new_word, "character_index": n,
                                      "letter": new_word[n], "erased_ink_points": len(missing),
                                      "whole_composite_comparator_rejects_missing_end_letter": True})
        else:
            ink, bounds = 0, None
        deck_cases.append({"frame": frame, "old": old_word, "new": new_word, "complete_native_ink": ink,
                           "bounds": bounds, "whole_original_and_new_composites_exact": True,
                           "native_RGB_pixel_positions_checked": 2 * 98304})
    assert len(deck_cases) == 18 and sum(bool(r["new"]) for r in deck_cases) == 8
    ship_cases, resource_views = [], []
    u = machine(after[ARM])
    for frame in sorted(shots["ship_actual"]):
        old, new = [Image.open(shots[name][frame]["path"]).convert("RGB") for name in ("ship_control", "ship_actual")]
        active = frame in (5320, 5340, 5360)
        differences = {(x, y) for y in range(384) for x in range(256)
                       if native5(old.getpixel((x, y))) != native5(new.getpixel((x, y)))}
        assert differences == (changed if active else set()), ("ship composite", frame)
        if active:
            left, top, right, bottom = FACE
            assert all(native5(new.getpixel((x, y))) == native5(revised.palette[revised.indices[y * 256 + x]])
                       for y in range(top, bottom) for x in range(left, right))
            for x, y in changed:
                assert native5(old.getpixel((x, y))) == native5(original.palette[original.indices[y * 256 + x]])
            points = mask(font, "Batteries", 141, 103, 5)
            assert points == {tuple(p) for p in stages[FILE]["new_ink"]}
            assert all(native5(new.getpixel(p)) == native5(revised.palette[1]) for p in points)
            raw = (CAPTURE / f"ship_batteries_v593_ships_actual/frame_{frame:06d}_arm9_ram.bin").read_bytes()
            u.mem_write(BASE, raw)
            views = [(BASE + at, struct.unpack_from("<12I", raw, at)) for at in range(0, len(raw) - 48, 4)
                     if struct.unpack_from("<I", raw, at + 12)[0] == 0x02313C90]
            views = [(at, fields) for at, fields in views if fields[0] == 0x0216017C and fields[7:12] == (0, 0, 0, 256, 192)]
            assert len(views) == 1
            view, fields = views[0]
            executed = call(u, 0xD4170, (view,))
            assert not {0x020DED50, 0x020DEBDC} & executed
            pointer = u.reg_read(UC_ARM_REG_R0)
            assert bytes(u.mem_read(pointer, len(after[FILE]))) == after[FILE]
            resource_views.append({"frame": frame, "view": view, "fields": list(fields), "resident_pointer": pointer,
                                   "complete_named_shipinfo_resident_file_exact_no_bridge": True})
        ship_cases.append({"frame": frame, "whole_native5_pixel_positions_checked": 98304,
                           "only_expected_Batteries_glyph_pixels_change": active,
                           "changed_pixels": len(differences), "full1024_pixel_face_and_complete_word": active})
    assert len(ship_cases) == 12
    result = {"candidate": str(ROM), "candidate_sha256": digest, "parent": str(PARENT), "parent_sha256": previous,
              "profile": manifest["profile"], "canonical_base": manifest["base_rom"], "canonical_base_sha256": manifest["base_sha256"],
              "manifest_sha256": sha(ROM.with_suffix(".manifest.json").read_bytes()),
              "patch_sha256": sha(ROM.with_suffix(".xdelta").read_bytes()), "exact_clean_patch_reconstruction": True,
              "only_ARM9_two_text_slots_and_shipinfo_glyphs_change_from_V591": True,
              "ARM9_changed_byte_count": len(arm_changes), "ARM9_changes_only_in_two12_byte_data_slots": True,
              "all_code_fonts_pointers_and_section_extents_retained": True,
              "all470_batches114_layers921_preservation_entries57_embedded_blocks_retained": True,
              "parent_preservation_proof": str(preservation_path), "parent_preservation_proof_sha256": sha(preservation_path.read_bytes()),
              "image_changed_pixels": len(changed), "label_stage_reports": stages,
              "reports": bindings, "deck_native_frame_cases": deck_cases, "ship_native_frame_cases": ship_cases,
              "first_final_character_negative_controls": negatives, "ship_original_resource_views": resource_views,
              "source_save_unchanged_no_RAM_fixture_in_final_runs": True,
              "blank_control_is_explicit_research_ROM_not_ordinary_candidate": True,
              "other_graphics_contexts_and_full_goal_remain_open": True, "human_acceptance_or_guide_publication": False,
              "script_sha256": sha(Path(__file__).read_bytes()), "full_goal_complete": False}
    (ROOT / "release_proof.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"V593:8 complete native Deck labels/18 whole three-way frames;3 Batteries faces/12 ship pairs;only139 image indices and{len(arm_changes)} text bytes;exact patch passes.")


if __name__ == "__main__":
    main()
