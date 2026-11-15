"""Verify complete Square caption selection and exact full-stack inheritance."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.square_sign_bounds import ROOT, transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage

ROM = Path("out/all_routes_combined_v254_candidate.nds")
CAPTURE = Path("work/emulation_v193/square_sign_bounds_v254")


def main():
    prior = Path("out/all_routes_combined_v253_candidate.nds")
    assert (ROOT / "v253_reproduction.nds").read_bytes() == prior.read_bytes()
    a, b = NdsImage.open(prior), NdsImage.open(ROM)
    assert {p: bytes(d) for _, p, d in a.iter_files()} == {p: bytes(d) for _, p, d in b.iter_files()}
    assert a.rom.arm7 == b.rom.arm7 and a.rom.arm9OverlayTable == b.rom.arm9OverlayTable
    proposed, _ = transform(a.read_file("/__arm9__.bin"))
    assert proposed == b.read_file("/__arm9__.bin") == (ROOT / "research_arm9.bin").read_bytes()
    old = json.loads(prior.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    m = json.loads(ROM.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    normalize = lambda rows: [r.replace("\\", "/") for r in rows]
    assert normalize(m["batches"]) == normalize(old["batches"]) and len(m["batches"]) == 467
    assert m["required_batches"] == old["required_batches"]
    for path, records in old["changed_records"].items():
        assert set(records) <= set(m["changed_records"][path])
    digest = sha(ROM.read_bytes())
    assert m["candidate_sha256"] == digest
    assert m["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    report = json.loads((CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    assert report["ROM_sha256"] == digest and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and report["frames"] == 20000
    frames = {r["frame"]: r for r in report["frames_captured"] if "cold_boot" in r["path"]}
    for row in report["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
    font = GameAsciiFont.from_arm9(proposed)
    cases = []
    screens = []
    for number, selected in [(18400, 0), (18800, 1), (19200, 2)]:
        row = frames[number]
        im = Image.open(row["path"]).convert("RGB")
        labels = []
        for index, (text, y) in enumerate([("Food Shop", 214), ("Liquor Shop", 246), ("Jewelry Shop", 278)]):
            expected = {(120 + n * 5 + x, y + gy) for n, ch in enumerate(text)
                        for gy in range(11) for x in range(6) if font.decode(ch).getpixel((x, gy))}
            actual = {(x, yy) for yy in range(y, y + 12) for x in range(120, 184)
                      if im.getpixel((x, yy)) == (230, 230, 230)}
            assert actual == expected, (number, text, len(actual), len(expected))
            top = 208 + index * 32
            if index == selected:
                # The original native focus painter adds two pixels around
                # the selectable rectangle. Preserve and verify that padding.
                for yy in range(top - 2, top + 26):
                    for x in range(170, 186):
                        assert im.getpixel((x, yy)) == ((230, 230, 230) if (x, yy) in expected else (0, 165, 172))
                assert im.getpixel((186, top + 4)) == (123, 121, 98)
            else:
                assert im.getpixel((180, top + 4)) == (57, 56, 57)
            labels.append({"English": text, "full_ink_pixels": len(expected), "selected": index == selected,
                           "all_first_internal_and_final_glyphs_exact": True})
        cases.append({"frame": number, "selected_row": selected, "capture": row,
                      "all3_complete_captions": labels, "full96_pixel_selection_background_inside_original_frame": True})
        screens.append((f"Selected: {labels[selected]['English']}", im))
    source = Image.open("work/emulation_v193/square_context_v254/frame_018400_final.png").convert("RGB")
    target = screens[0][1]
    differences = [(x, y) for y in range(384) for x in range(256) if source.getpixel((x, y)) != target.getpixel((x, y))]
    assert differences and all(170 <= x < 186 and 206 <= y < 234 for x, y in differences)
    baseline_report = json.loads(Path("work/emulation_v193/square_shop_v253/capture_report.json").read_text(encoding="utf-8"))
    baseline = {r["frame"]: r["PNG_sha256"] for r in baseline_report["frames_captured"] if "cold_boot" in r["path"]}
    unchanged = [n for n, row in frames.items() if n < 16400 and n in baseline]
    assert all(frames[n]["PNG_sha256"] == baseline[n] for n in unchanged)
    for file in ["translations/graphics_completion_campaign_v1.json", "translations/graphics_visual_audit_v150.json"]:
        audit = json.loads(Path(file).read_text(encoding="utf-8"))["plaque_style_v247"]
        assert len(audit["ongoing_plaque_inventory"]) == 18 and not audit["full_plaque_audit_complete"]
        assert all(not r["fully_completed"] for r in audit["ongoing_plaque_inventory"])
    clean = Path("work/clean.nds")
    assert sha(clean.read_bytes()) == "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    patch = ROM.with_suffix(".xdelta")
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, ROOT / "exact_patch_reconstruction.nds")
    assert (ROOT / "exact_patch_reconstruction.nds").read_bytes() == ROM.read_bytes()
    sheet = Image.new("RGB", (768, 410), "#333333")
    draw = ImageDraw.Draw(sheet)
    for index, (label, im) in enumerate(screens):
        draw.text((index * 256 + 4, 4), label, fill="white")
        sheet.paste(im, (index * 256, 24))
    sheet.save(ROOT / "all_three_selected_review.png")
    proof = {"format": "dk4-square-sign-live-v254", "candidate": str(ROM), "candidate_sha256": digest,
             "patch_sha256": sha(patch.read_bytes()), "profile": m["profile"], "base_sha256": m["base_sha256"],
             "all467_batches_prior_records_files_routes_art_ARM7_overlays_retained": True,
             "only_four_byte_ARM9_row_right_coordinate_changed": True, "exact_full_V253_reproduction": True,
             "exact_clean_patch_reconstruction": True, "three_actual_selection_states": cases,
             "only_selected_row_extension_pixels_differ_in_complete_source_frame": len(differences),
             "unchanged_regression_frame_count": len(unchanged), "cold_boot_ordinary_inputs_no_loaded_state_no_RAM_injection": True,
             "third_sign_activated_at19201_shopkeeper_frame20000_visually_reviewed": True,
             "shopkeeper658_dialogue_fidelity_investigation": "work/analysis/square_sign_bounds_v254/shopkeeper658_followup.json",
             "original_choice_menu_occlusion_retained_as_contextual_behavior": True,
             "all18_plaque_entries_and_variants_remain_incomplete": True,
             "other_cities_categories_and_occupied_equipment_pending": True,
             "experimental_user_acceptance_pending": True, "full_goal_complete": False}
    (ROOT / "saved_live_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: proof[k] for k in ("candidate_sha256", "patch_sha256", "only_selected_row_extension_pixels_differ_in_complete_source_frame")}))


if __name__ == "__main__":
    main()
