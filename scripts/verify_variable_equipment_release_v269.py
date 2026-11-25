"""Real purchased/equipped book, complete variable tooltip and inherited ROM."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.variable_equipment_paper import ROOT
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_plaque_style_v247 import paper

ROM = Path("out/all_routes_combined_v269_candidate.nds")
CAPTURE = Path("work/emulation_v193/variable_equipment_v269")
PRIOR = Path("work/emulation_v193/equipment_start_town_v268")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    old_path = Path("out/all_routes_combined_v267_candidate.nds")
    assert (ROOT / "v267_reproduction.nds").read_bytes() == old_path.read_bytes()
    old, rom = NdsImage.open(old_path), NdsImage.open(ROM)
    assert {p: bytes(d) for _, p, d in old.iter_files()} == {p: bytes(d) for _, p, d in rom.iter_files()}
    assert old.rom.arm7 == rom.rom.arm7 and old.rom.arm9OverlayTable == rom.rom.arm9OverlayTable
    arm = rom.read_file("/__arm9__.bin")
    assert arm == (ROOT / "research_arm9.bin").read_bytes()
    m, prior_m = load(ROM.with_suffix(".manifest.json")), load(old_path.with_suffix(".manifest.json"))
    norm = lambda rows: [p.replace("\\", "/") for p in rows]
    assert norm(m["batches"]) == norm(prior_m["batches"]) and len(m["batches"]) == 467
    assert m["required_batches"] == prior_m["required_batches"]
    for path, ids in prior_m["changed_records"].items():
        assert set(ids) <= set(m["changed_records"][path])
    digest = sha(ROM.read_bytes())
    assert m["candidate_sha256"] == digest and m["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    report, earlier = load(CAPTURE / "capture_report.json"), load(PRIOR / "capture_report.json")
    assert report["ROM_sha256"] == digest and report["cold_boot"] and not report["savestate_loaded"]
    assert report["frames"] == earlier["frames"] == 28400 and not report["callback_errors"]
    assert report["scripted_input_schedule"] == earlier["scripted_input_schedule"]
    lookup = {r["frame"]: r for r in earlier["frames_captured"] if "cold_boot" in r["path"]}
    unchanged, changed = [], []
    for row in report["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        if "cold_boot" not in row["path"] or row["frame"] not in lookup:
            continue
        now = Image.open(row["path"]).convert("RGB")
        before = Image.open(lookup[row["frame"]]["path"]).convert("RGB")
        delta = [(x, y) for y in range(384) for x in range(256) if now.getpixel((x, y)) != before.getpixel((x, y))]
        if delta:
            assert row["frame"] == 28400 and all(94 <= x < 224 and 208 <= y < 224 for x, y in delta)
            changed.append(row["frame"])
        else:
            unchanged.append(row["frame"])
    assert changed == [28400]
    image = Image.open(CAPTURE / "frame_028400_cold_boot.png").convert("RGB")
    font = GameAsciiFont.from_arm9(arm)
    label = "Travels of Marco Polo"
    expected_ink = {(96 + n * 6 + x, 210 + y) for n, c in enumerate(label)
                    for y in range(11) for x in range(6) if font.decode(c).getpixel((x, y))}
    actual_ink = {(x, y) for y in range(208, 224) for x in range(94, 224) if image.getpixel((x, y)) == (0, 8, 0)}
    assert expected_ink == actual_ink and len(expected_ink) == 223
    palette = PxlImage.from_bytes(NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/_pxl/towninfo.pxl")).palette
    tile = paper(130, 16, palette)
    for y in range(16):
        for x in range(130):
            point = (94 + x, 208 + y)
            rgb = (0, 8, 0) if point in expected_ink else palette[tile[y * 130 + x]][:3]
            assert tuple(c // 8 for c in image.getpixel(point)) == tuple(c // 8 for c in rgb), point
    # Complete original32x32 book artwork in the normal owned inventory.
    inventory = Image.open(PRIOR / "frame_027400_navigation.png").convert("RGB")
    atlas = PxlImage.from_bytes(rom.read_file("/_pxl/item.pxl")).render().convert("RGB")
    assert [tuple(c // 8 for c in col) for col in inventory.crop((16, 24, 48, 56)).get_flattened_data()] == [
        tuple(c // 8 for c in col) for col in atlas.crop((0, 88 * 32, 32, 89 * 32)).get_flattened_data()]
    for file in ["translations/graphics_completion_campaign_v1.json", "translations/graphics_visual_audit_v150.json"]:
        audit = load(file)["plaque_style_v247"]
        assert len(audit["ongoing_plaque_inventory"]) == 18 and not audit["full_plaque_audit_complete"]
        assert all(not row["fully_completed"] for row in audit["ongoing_plaque_inventory"])
    clean = Path("work/clean.nds")
    assert sha(clean.read_bytes()) == "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    patch = ROM.with_suffix(".xdelta")
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, ROOT / "exact_patch_reconstruction.nds")
    assert (ROOT / "exact_patch_reconstruction.nds").read_bytes() == ROM.read_bytes()
    proof = {"format": "dk4-variable-equipment-live-v269", "candidate": str(ROM), "candidate_sha256": digest,
             "patch_sha256": sha(patch.read_bytes()), "profile": m["profile"], "base_sha256": m["base_sha256"],
             "ordinary_Lisbon_purchase_and_Y_Equip_no_loaded_state_no_inventory_fixture": True,
             "occupied_book": label, "original_source_item_index": 88,
             "all1024_original_inventory_icon_pixels_exact": True,
             "all223_complete_tooltip_glyph_pixels_exact": True,
             "all2080_paper_glyph_and_corner_pixels_exact_native_precision": True,
             "unchanged_comparable_whole_frames": unchanged, "only_occupied_tooltip_changed": changed,
             "all467_prior_batches_records_files_art_routes_ARM7_overlays_retained": True,
             "exact_full_V267_reproduction_and_clean_patch_reconstruction": True,
             "all235_widths_native_paper_proof": "work/analysis/variable_equipment_v269/native_proof.json",
             "weapon_armor_other_health_states_and_all18_plaques_still_incomplete": True,
             "observed_FE_missing_D_and325_record_runtime_guard_repair_pending": True,
             "experimental_user_acceptance_pending": True, "full_goal_complete": False}
    (ROOT / "saved_live_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_sha256": digest, "patch_sha256": proof["patch_sha256"],
                      "whole_frames_unchanged": len(unchanged), "complete_tooltip_ink": len(expected_ink), "exact_composite_pixels": 2080}))


if __name__ == "__main__":
    main()
