"""Actual cold-boot stylus navigation and resident Sea View graphics identity."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/equipment_gameplay_v265")
ORIGINAL = Path("work/emulation_v193/equipment_gameplay_v265")
CAPTURE = Path("work/emulation_v193/equipment_touch_v265")
ROM = Path("out/all_routes_combined_v263_candidate.nds")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    report, prior = load(CAPTURE / "capture_report.json"), load(ORIGINAL / "capture_report.json")
    digest = sha(ROM.read_bytes())
    assert report["ROM_sha256"] == prior["ROM_sha256"] == digest
    assert report["frames"] == 34000 and prior["frames"] == 33000
    for data in [report, prior]:
        assert data["cold_boot"] and not data["savestate_loaded"] and not data["callback_errors"]
        for row in data["frames_captured"]:
            assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
    old = {r["frame"]: r for r in prior["frames_captured"] if "cold_boot" in r["path"]}
    unchanged = []
    for row in report["frames_captured"]:
        if "cold_boot" in row["path"] and row["frame"] in old:
            assert row["PNG_sha256"] == old[row["frame"]]["PNG_sha256"]
            unchanged.append(row["frame"])
    assert len(unchanged) == 85
    assert report["scripted_input_schedule"][:len(prior["scripted_input_schedule"])] == prior["scripted_input_schedule"]
    touches = [r for r in report["scripted_input_schedule"] if "touch" in r]
    assert touches[:2] == [{"start": 33041, "duration": 8, "buttons": [], "touch": [102, 100]},
                           {"start": 33081, "duration": 8, "buttons": [], "touch": [88, 64]}]
    assert not any(r["buttons"] for r in report["scripted_input_schedule"] if 33041 <= r["start"] <= 33120)
    assert report["core_options"]["desmume_pointer_type"] == "touch"
    # Complete Deck help verifies that the two ordinary taps reached its actual UI.
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file("/__arm9__.bin"))
    plan = load("work/analysis/deck_filter_v263/runtime_plan.json")
    image = Image.open(CAPTURE / "frame_033120_navigation.png").convert("RGB")
    expected = set()
    for record, y in zip(plan["records"][2:], [32, 48, 80]):
        for n, line in enumerate(record["compiled"].split("\n")):
            line = line[1:] if n else line
            expected |= {(i * 6 + x, y + n * 16 + yy) for i, ch in enumerate(line)
                         for yy in range(11) for x in range(6) if font.decode(ch).getpixel((x, yy))}
    actual = {(x, y) for y in range(32, 128) for x in range(256) if image.getpixel((x, y)) == (230, 230, 230)}
    assert expected == actual and len(expected) == 2299
    state = report["read_only_native_state"]
    assert state["read_only_export"] and not state["state_loaded"]
    assert state["main_RAM_unchanged_by_export"] and state["serialized_RAM_matches_same_frame_direct_export"]
    ram_row = report["read_only_RAM_snapshot"]
    ram = Path(ram_row["path"]).read_bytes()
    assert sha(ram) == ram_row["sha256"]
    rom, clean = NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    resident = []
    for path in ["/_pxl/__frame.pxl", "/_pxl/__marker.pxl", "/_pxl/chara00.pxl", "/_pxl/seaarea.pxl"]:
        blob = rom.read_file(path)
        offset = ram.find(blob)
        assert offset >= 0 and ram.find(blob, offset + 1) == -1
        resident.append({"path": path, "address": 0x02000000 + offset, "complete_bytes": len(blob),
                         "whole_header_palette_and_pixels_sha256": sha(blob), "complete_saved_ROM_file_resident_exact": True})
    sea = rom.read_file("/_pxl/seaarea.pxl")
    assert sea == clean.read_file("/_pxl/seaarea.pxl")
    pxl = PxlImage.from_bytes(sea)
    assert (pxl.width, pxl.height, pxl.bits_per_pixel) == (244, 1280, 4)
    owner = 0x0231336C
    fields = struct.unpack_from("<5I", ram, owner - 0x02000000)
    name = bytes(ram[fields[3] - 0x02000000:fields[3] - 0x02000000 + 64]).split(b"\0")[0]
    assert name == b"_pxl/seaarea.pxl"
    source_frame = Image.open(ORIGINAL / "frame_029200_navigation.png").convert("RGB")
    capture_pixels = [tuple(c // 8 for c in col) for col in source_frame.crop((6, 16, 250, 176)).get_flattened_data()]
    candidates = []
    for bank in range(8):
        palette = [tuple(c // 8 for c in bgr555(v)[:3]) for v, in struct.iter_unpack("<H", sea[20 + bank * 32:52 + bank * 32])]
        for page in range(8):
            pixels = [palette[i] for i in pxl.indices[page * 39040:(page + 1) * 39040]]
            candidates.append({"page": page, "bank": bank, "matching_pixels": sum(a == b for a, b in zip(pixels, capture_pixels))})
    best = max(row["matching_pixels"] for row in candidates)
    leaders = [r for r in candidates if r["matching_pixels"] == best]
    assert best == 37490 and {r["page"] for r in leaders} == {0}
    assert len(leaders) == 8  # Equal palettes do not prove the chosen bank.
    for file in ["translations/graphics_completion_campaign_v1.json", "translations/graphics_visual_audit_v150.json"]:
        audit = load(file)["plaque_style_v247"]
        assert len(audit["ongoing_plaque_inventory"]) == 18 and not audit["full_plaque_audit_complete"]
        assert all(not r["fully_completed"] for r in audit["ongoing_plaque_inventory"])
    proof = {"format": "dk4-sea-view-stylus-v265", "candidate": str(ROM), "candidate_sha256": digest,
             "all85_prior_whole_cold_boot_frames_exact": unchanged,
             "two_standard_stylus_taps_without_buttons_open_Deck_View": touches[:2],
             "all2299_actual_Deck_help_ink_pixels_exact_after_touch": True,
             "native_state_export_is_read_only_no_loaded_state_no_RAM_injection": True,
             "resident_graphics": resident, "actual_seaarea_owner": owner, "actual_owner_fields": list(fields),
             "actual_map_crop": [6, 16, 250, 176], "every_map_pixel_compared": 39040,
             "seaarea_background_matching_pixels": best, "unmatched_map_composite_pixels": 39040 - best,
             "all_page_and_bank_comparisons": candidates,
             "equal_palettes_do_not_establish_selected_bank": True,
             "unmatched_composite_pixels_not_silently_excluded": True,
             "native_parent_draw_palette_dispatch_and_whole_composite_not_proved": True,
             "seamap_is_distinct_not_substituted_for_seaarea": True,
             "equipment_not_acquired_and_occupied_equipment_still_pending": True,
             "all18_plaques_and_variants_incomplete": True, "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "saved_live_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"unchanged_frames": len(unchanged), "touch_Deck_help_pixels": len(expected),
                      "resident_complete_files": len(resident), "map_match": [best, 39040], "occupied_equipment_verified": False}))


if __name__ == "__main__":
    main()
