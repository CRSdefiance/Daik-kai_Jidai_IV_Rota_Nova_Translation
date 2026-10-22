"""Verify all103 real equipment hint displays and37 empty-slot cases in V581."""

import json
import shutil
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.native_equipment_fixture_v586 import equip
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_equipment_join_v581 import hint, source_tile
from scripts.verify_portrait_native_pixels_v202 import native5

ROOT = Path("work/analysis/equipment_catalogue_v586")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193/equipment_catalogue_v586_live")
ARCHIVE = Path("E:/Rota Nova translations/Screenshots/Test fixtures/V586 All equipment hints")
ROM = Path("out/all_routes_combined_v581_candidate.nds")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    rom, clean = NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    digest = sha(ROM.read_bytes())
    assert digest == "542c2faf58bde6f408c873a930e29cdb215ef4940375aeffb650644c26d41e68"
    arm = rom.read_file("/__arm9__.bin")
    run_path = CAPTURE / "capture_report.json"
    run = read(run_path)
    assert run["ROM_sha256"] == digest and run["cold_boot"] and not run["savestate_loaded"]
    assert not run["callback_errors"] and run["frames"] == 14360
    sets, catalog = read(ROOT / "equipment_sets.json"), read("work/analysis/equipment_material_v580/current_equipment_name_widths.json")
    names = {r["id"]: {**r, "category": int(category)} for category, rows in catalog.items() for r in rows}
    assert len(names) == 103 and [len(catalog[str(n)]) for n in (2, 3, 4)] == [28, 26, 49]
    assert len(sets) == 28 and {i for row in sets for i in row if i is not None} == set(names)
    assert len([i for row in sets for i in row if i is not None]) == 103
    fixtures = run["synthetic_equipment_display_fixtures"]
    assert [r["items"] for r in fixtures] == sets
    assert [r["frame"] for r in fixtures] == [5480 + n * 320 for n in range(28)]
    assert not run["normal_acquisition_or_eligibility_verified"]
    assert not run.get("synthetic_inventory_fixtures")
    schedule = read(ROOT / "navigation_to_info.json")
    schedule.append({"start": 5401, "duration": 8, "buttons": ["B"]})
    for n in range(28):
        first = 5560 + n * 320
        schedule.append({"start": first - 79, "duration": 8, "buttons": ["A"]})
        schedule.extend({"start": first + offset + 1, "duration": 8, "buttons": ["LEFT"]}
                        for offset in (0, 40, 80, 120))
        if n < 27:
            schedule.append({"start": first + 161, "duration": 8, "buttons": ["B"]})
    assert run["scripted_input_schedule"] == schedule
    copy = read("work/analysis/equipment_material_v580/save_copy_provenance.json")
    for key in ("original", "historical_test_source", "new_test_copy"):
        assert sha(Path(copy[key]).read_bytes()) == copy[key + "_sha256"]
    assert run["battery_save_preloaded"]["source_sha256"] == copy["original_sha256"]
    frames = {}
    for row in run["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        if row["path"].endswith("_navigation.png"):
            assert row["frame"] not in frames
            frames[row["frame"]] = row
    snapshots = {r["frame"]: r for r in run["read_only_pause_RAM_snapshots"]}
    for snapshot in snapshots.values():
        assert sha(Path(snapshot["path"]).read_bytes()) == snapshot["sha256"]
        assert snapshot["bytes"] == 0x400000
    # Replay every fixture on its exported before-state, not a final shared RAM
    # image. This validates exact permitted writes and captured item metadata.
    for record in fixtures:
        raw = Path(snapshots[record["frame"]]["path"]).read_bytes()
        _, replay = equip(arm, raw, record["items"])
        assert record == dict(replay, frame=record["frame"])
    font = GameAsciiFont.from_arm9(arm)
    tile = source_tile(PxlImage.from_bytes(clean.read_file("/_pxl/towninfo.pxl")), True)
    plan = read("work/analysis/direct_equipment_v270/runtime_plan.json")
    at = plan["tile_pointer"] - POOL
    assert bytes(MainCodeFile(arm, BASE).sections[3].data[at:at + 1408]) == tile
    assert rom.read_file("/_pxl/item.pxl") == clean.read_file("/_pxl/item.pxl")
    atlas = PxlImage.from_bytes(rom.read_file("/_pxl/item.pxl")).render().convert("RGB")
    occupied, empty, archives = [], [], []
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for n, items in enumerate(sets):
        for slot in range(5):
            frame = 5560 + n * 320 + (4 - slot) * 40
            shot = frames[frame]
            image = Image.open(shot["path"]).convert("RGB")
            raw = Path(snapshots[frame]["path"]).read_bytes()
            u = machine(arm)
            u.mem_write(BASE, raw)
            call(u, 0x7F244, ())
            assert u.reg_read(UC_ARM_REG_R0) == 3
            call(u, 0xCB184, ())
            captain_record = u.reg_read(UC_ARM_REG_R0) + 0x19E4
            assert list(u.mem_read(captain_record + 0x1B, 5)) == [0xDB if i is None else i for i in items]
            item_id = items[slot]
            name = names[item_id]["name"] if item_id is not None else "Weapon" if slot == 0 else "Armor" if slot == 1 else "Equipped Items"
            display = hint(font, tile, image, name, 16 + slot * 48)
            record = {"set": n, "slot": slot, "item_id": item_id, "frame": frame,
                      "full_screenshot": shot, "RAM_snapshot": snapshots[frame], "display": display}
            if item_id is not None:
                call(u, 0xCB190, ())
                item = u.reg_read(UC_ARM_REG_R0) + 4 + item_id * 20
                call(u, 0x4A448, (item,))
                assert u.reg_read(UC_ARM_REG_R0) == names[item_id]["category"]
                call(u, 0x4A53C, (item,))
                assert bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 128)).split(b"\0")[0].decode("cp932") == name
                call(u, 0x49DE8, (0x02470020, item))
                assert struct.unpack("<2I", u.mem_read(0x02470024, 8)) == (2, 3)
                x = 16 + slot * 48
                assert [native5(c) for c in image.crop((x, 224, x + 32, 256)).get_flattened_data()] == [
                    native5(c) for c in atlas.crop((0, item_id * 32, 32, item_id * 32 + 32)).get_flattened_data()]
                record["complete_original_icon_pixels"] = 1024
                occupied.append(record)
            else:
                empty.append(record)
            assert bytes(u.mem_read(BASE, len(raw))) == raw
            target = ARCHIVE / f"{'item_' + str(item_id) if item_id is not None else 'empty'}_slot{slot}_frame{frame}.png"
            shutil.copyfile(shot["path"], target)
            assert sha(target.read_bytes()) == shot["PNG_sha256"]
            archives.append({"path": str(target), "sha256": sha(target.read_bytes()), "frame": frame,
                             "synthetic_equipment_display_fixture": True})
    assert len(occupied) == 103 and len(empty) == 37
    assert {r["item_id"] for r in occupied} == set(names)
    assert {r["slot"] for r in empty} == {1, 2, 3, 4}
    # Weapon-empty was already verified in V581; this catalogue always keeps a
    # real weapon in slot0. Do not invent a new empty-weapon appearance here.
    assert sha(ROM.read_bytes()) == digest
    assert sha(ROM.with_suffix(".xdelta").read_bytes()) == "e411c4f24e4669309f262493320b08708c9f376da2b9bd80631a002d2f34e415"
    result = {"candidate": str(ROM), "candidate_sha256": digest,
              "report": str(run_path), "report_sha256": sha(run_path.read_bytes()),
              "scripts": {p: sha(Path(p).read_bytes()) for p in (
                  "scripts/verify_equipment_catalogue_v586.py", "scripts/native_equipment_fixture_v586.py",
                  "scripts/headless_desmume_v193.py", "scripts/verify_equipment_join_v581.py")},
              "original_and_test_source_saves_unchanged": copy,
              "all103_native_equipment_items": occupied, "empty_slot_cases": empty,
              "whole_paper_pixels": sum(r["display"]["whole_paper_pixels"] for r in occupied + empty),
              "complete_original_icon_pixels": 103 * 1024,
              "fixture_replays": len(fixtures), "actual_native_hint_appearances": 140,
              "complete_leading_trailing_letters_spaces_and_source_wood_exact": True,
              "captured_category_owner_and_slot_bindings_exact": True,
              "original_transfer_writes_bounded_item_history_and_owner_slot_bytes_only": True,
              "explicit_slots_not_normal_acquisition_eligibility_or_other_owner_condition_proof": True,
              "ROM_and_patch_changed": False, "full_goal_complete": False,
              "hardware_device_verification": False,
              "archive": str(ARCHIVE), "full_screenshots": archives}
    proof = ROOT / "native_catalogue_proof.json"
    proof.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for path in (proof, run_path, ROOT / "equipment_sets.json", ROOT / "navigation_to_info.json"):
        target = ARCHIVE / path.name
        shutil.copyfile(path, target)
        assert sha(target.read_bytes()) == sha(path.read_bytes())
    print(f"V586: all103 equipment names/icons and37 empty hints,140 actual native displays,{result['whole_paper_pixels']} whole-paper pixels pass;V581 unchanged.")


if __name__ == "__main__":
    main()
