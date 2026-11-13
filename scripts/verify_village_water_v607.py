"""Verify source terrain, native discovery and real village UI; retain failures."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_village_water_v607 import relocate
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

ROOT = Path("work/analysis/village_water_v607")
CAP = Path("E:/Rota Nova translations/Generated/work/emulation_v193")
ROM = Path("out/all_routes_combined_v604_candidate.nds")
DIGEST = "fb8de61d20e94e742574bded2d8e4251305f2b56265ff8624dd766eaa6cf9158"
DONOR = "958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    assert sha(ROM.read_bytes()) == DIGEST
    arm = NdsImage.open(ROM).read_file("/__arm9__.bin")
    clean = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    folder = CAP / "village_water_v607_inuvik"
    report_path = folder / "capture_report.json"
    report = read(report_path)
    assert report["ROM_sha256"] == DIGEST and report["frames"] == 17800
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    donor = report["battery_save_preloaded"]
    assert donor["source_sha256"] == DONOR == sha(Path(donor["source"]).read_bytes())
    for key, value in report.items():
        if key.startswith("synthetic_") and key != "synthetic_location_fixtures":
            assert not value, key
    shots = {}
    for shot in report["frames_captured"]:
        assert sha(Path(shot["path"]).read_bytes()) == shot["PNG_sha256"]
        shots[shot["frame"]] = shot
    snapshots = {}
    for row in report["read_only_pause_RAM_snapshots"]:
        raw = Path(row["path"]).read_bytes()
        assert row["read_only_export"] and len(raw) == 0x400000 and sha(raw) == row["sha256"]
        snapshots[row["frame"]] = raw
    before = snapshots[5200]
    after, fixture = relocate(arm, before, 0)
    assert report["synthetic_location_fixtures"] == [dict(fixture, frame=5200)]
    offset = fixture["active_ship"] - 0x02000000 + 16
    assert before[:offset] == after[:offset] and before[offset + 8:] == after[offset + 8:]
    mask_address = 0x022E1174
    mask_offset = mask_address - 0x02000000
    # Verify the source setter owns this manager field; the fixture leaves it exact.
    assert arm[0xCABBC:0xCAC54] == clean[0xCABBC:0xCAC54]
    assert before[mask_offset:mask_offset + 4] == after[mask_offset:mask_offset + 4]
    assert struct.unpack_from("<I", before, mask_offset)[0] == 0
    timeline = []
    for frame in (5200, 5600, 6000, 6400, 6900, 7800, 8200, 8600, 9000, 17800):
        raw = snapshots[frame]
        mask = struct.unpack_from("<I", raw, mask_offset)[0]
        assert mask == (0 if frame == 5200 else 1)
        point = list(struct.unpack_from("<2i", raw, fixture["active_fleet"] - 0x02000000 + 0x34))
        timeline.append({"frame": frame, "discovered_village_mask": mask,
                         "original_cached_fleet_point": point,
                         "active_ship_fixed_point": list(struct.unpack_from("<2i", raw, offset))})
    assert timeline[1]["original_cached_fleet_point"] == [4874, 2323]
    font = GameAsciiFont.from_arm9(arm)
    masks = []
    for frame, text, x, y, disposition in (
        (5600, "Village in sight!", 16, 296, "complete-native-message"),
        (8200, "Enter the promised words.", 16, 296, "complete-native-message"),
        (17800, "The village chief has left.", 16, 296, "complete-native-failure-response"),
        (7800, "Captain, the village chief asks to h", 16, 296, "defect-first-line-splits-hear"),
        (7800, "ear", 16, 312, "defect-second-line-fragment"),
        (7800, "the promised words.", 22, 328, "defect-third-line-after-compiled-break"),
    ):
        image = Image.open(shots[frame]["path"]).convert("RGB")
        ink, bounds = complete_mask(font, text, image, x, y, (0, 8, 0))
        masks.append({"frame": frame, "text": text, "ink_pixels": ink, "bounds": bounds,
                      "disposition": disposition, "screenshot": shots[frame]})
    manuscript = read("translations/village_promised_words_manuscript_v1.json")
    message = next(r for r in manuscript["records"] if r["id"] == "VILLAGE_MESSAGE_0")
    compiled = bytes.fromhex(message["compiled_hex"])
    assert "".join(m["text"] for m in masks[3:5]) == compiled.split(b"\n")[0].decode("ascii")
    assert bytes(snapshots[7800][message["target_pointer"] - 0x02000000:
                                 message["target_pointer"] - 0x02000000 + len(compiled)]) == compiled
    menu_sources = []
    for text, source_offset in (("補給", 0x1478F0), ("宿泊", 0x1478E8), ("船修理", 0x147918),
                                ("水夫募集", 0x147940), ("出港", 0x1478F8), ("約束の言葉", 0x147A24)):
        encoded = text.encode("cp932") + b"\0"
        assert arm[source_offset:source_offset + len(encoded)] == encoded
        assert clean[source_offset:source_offset + len(encoded)] == encoded
        menu_sources.append({"Japanese": text, "source_offset": source_offset,
                             "original_string_retained_in_candidate": True})
    model = fixture["village_model"] - 0x02000000
    name = struct.unpack_from("<I", before, model + 8)[0] - 0x02000000
    name_bytes = arm[name:arm.index(b"\0", name)]
    assert name_bytes.decode("cp932") == "イヌビク"
    assert clean[name:name + len(name_bytes) + 1] == name_bytes + b"\0"
    # The real marked editor is discovered by its provider; never supply a fake parent.
    plan = read("work/analysis/village_promised_words_plan.json")
    provider = plan["keyboard_wrapper"]["provider_vtable"]
    needle = struct.pack("<I", provider)
    owners = [o for o in range(0x170000, len(before) - 4, 4)
              if snapshots[8600][o:o + 4] == needle]
    assert len(owners) == 1
    parent = owners[0] - 4
    assert struct.unpack_from("<I", snapshots[8600], parent + 0xD8)[0] == 18
    assert snapshots[9200][parent + 0xB4:parent + 0xB6] == b"A\0"
    assert snapshots[15400][parent + 0xB4:parent + 0xBB] == b"auaaaa\0"
    assert struct.unpack_from("<I", snapshots[15400], parent + 0x78)[0] == 6
    # Reject the intended password expectation: navigation did not enter Aurora.
    entered = snapshots[16900][parent + 0xB4:parent + 0xBB].split(b"\0", 1)[0]
    assert entered == b"auaaaA" and entered != b"Aurora"
    card_matches = []
    from dk4tool.graphics.pxl import PxlImage
    from scripts.verify_movie_gpu_fixtures_v336 import quantized

    rom = NdsImage.open(ROM)
    for index in (168, 169, 170, 171, 206, 207, 208, 209):
        expected = quantized(PxlImage.from_bytes(rom.read_file(f"/evstill/evstill{index:03d}.pxl")).render()).convert("RGB")
        for frame in (5600, 6000, 6400, 6900, 7800, 8200, 8600, 9000, 17800):
            top = quantized(Image.open(shots[frame]["path"]).crop((0, 0, 256, 192))).convert("RGB")
            if top.tobytes() == expected.tobytes():
                card_matches.append([index, frame])
    assert not card_matches
    negatives = []
    for label, directory, frame in (("Maria-departure-context", "village_location_v606_inuvik", 14400),
                                     ("Syracuse-land-center", "village_location_v606_rafael", 5600)):
        path = CAP / directory / "capture_report.json"
        r = read(path)
        assert r["ROM_sha256"] == DIGEST and r["frames"] == frame
        assert r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"]
        raw = (CAP / directory / "final_arm9_ram.bin").read_bytes()
        assert struct.unpack_from("<I", raw, mask_offset)[0] == 0
        negatives.append({"label": label, "report": str(path), "sha256": sha(path.read_bytes()),
                          "frames": frame, "discovery_mask": 0, "no_village_display_credit": True})
    proof = {"candidate": str(ROM), "candidate_sha256": DIGEST,
             "report": str(report_path), "report_sha256": sha(report_path.read_bytes()),
             "frames": 17800, "all_reported_captures_hash_checked": True,
             "capture_receipts": len(report["frames_captured"]), "unique_capture_frames": len(shots),
             "user_authorized_isolated_location_fixture": fixture,
             "ordinary_travel_or_earned_unlock_not_claimed": True,
             "native_discovery_timeline": timeline, "complete_native_text_masks": masks,
             "source_locked_formatting_defect": message,
             "Japanese_menu_visual_evidence_frame": 6900, "Japanese_menu_source_strings": menu_sources,
             "Japanese_village_name_source": {"offset": name, "Japanese": name_bytes.decode("cp932")},
             "actual_editor_parent": parent + 0x02000000, "actual_editor_capacity": 18,
             "actual_single_byte_input_and_cursor_observed": True,
             "intended_Aurora_navigation_failed_not_keyboard_bug_proof": True,
             "actual_entered_password": "auaaaA", "password_success_not_verified": True,
             "no_eight_village_card_matches_in_nine_selected_whole_top_screens": True,
             "global_unused_card_claim": False, "rejected_v606_setups": negatives,
             "production_ROM_patch_registry_art_or_donor_changed": False,
             "all18_plaques_incomplete_all22_requirements_retained": True,
             "normal_village_logic_after_fixture_not_substituted_scene_operand": True,
             "full_goal_complete": False, "script_sha256": sha(Path(__file__).read_bytes()),
             "implementation_hashes": {str(p): sha(p.read_bytes()) for p in (
                 Path("scripts/native_village_water_v607.py"), Path("scripts/run_village_water_v607.py"),
                 Path("scripts/native_village_location_v606.py"), Path("scripts/headless_desmume_v193.py"))}}
    save(ROOT / "final_recorded_inputs.json", report["scripted_input_schedule"])
    save(ROOT / "native_village_proof.json", proof)
    print("V607: original discovery/menu/editor/failure after eight-coordinate-byte fixture; native wrap defect confirmed; village cards and successful password remain open.")


if __name__ == "__main__":
    main()
