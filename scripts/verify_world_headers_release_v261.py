"""Exact inherited release and actual centered World Map header glyphs."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.world_map_headers import ROOT
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage

ROM = Path("out/all_routes_combined_v261_candidate.nds")
CAPTURE = Path("work/emulation_v193/world_headers_v261")
PRIOR_CAPTURE = Path("work/emulation_v193/map_alternate_v261")


def main():
    prior = Path("out/all_routes_combined_v260_candidate.nds")
    assert (ROOT / "v260_reproduction.nds").read_bytes() == prior.read_bytes()
    a, b = NdsImage.open(prior), NdsImage.open(ROM)
    assert {p: bytes(d) for _, p, d in a.iter_files()} == {p: bytes(d) for _, p, d in b.iter_files()}
    assert a.rom.arm7 == b.rom.arm7 and a.rom.arm9OverlayTable == b.rom.arm9OverlayTable
    assert b.read_file("/__arm9__.bin") == (ROOT / "research_arm9.bin").read_bytes()
    m = json.loads(ROM.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    old = json.loads(prior.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    norm = lambda rows: [p.replace("\\", "/") for p in rows]
    assert norm(m["batches"]) == norm(old["batches"]) and len(m["batches"]) == 467
    assert m["required_batches"] == old["required_batches"]
    for p, ids in old["changed_records"].items():
        assert set(ids) <= set(m["changed_records"][p])
    digest = sha(ROM.read_bytes())
    assert m["candidate_sha256"] == digest and m["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    report = json.loads((CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    original = json.loads((PRIOR_CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    assert report["ROM_sha256"] == digest and report["cold_boot"] and not report["savestate_loaded"]
    assert report["frames"] == 36000 and not report["callback_errors"]
    assert report["scripted_input_schedule"] == original["scripted_input_schedule"]
    prior_frames = {r["frame"]: r for r in original["frames_captured"]}
    unchanged = 0
    for row in report["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        if row["frame"] < 35600 and row["frame"] in prior_frames:
            assert row["PNG_sha256"] == prior_frames[row["frame"]]["PNG_sha256"]
            unchanged += 1
    font = GameAsciiFont.from_arm9(b.read_file("/__arm9__.bin"))
    labels = []
    screens = []
    for number, text, x in [(35600, "Sea Areas", 101), (36000, "Fleets/Villages", 83)]:
        image = Image.open(CAPTURE / f"frame_{number:06d}_cold_boot.png").convert("RGB")
        source = Image.open(prior_frames[number]["path"]).convert("RGB")
        expected = {(x + n * 6 + gx, 194 + gy) for n, ch in enumerate(text)
                    for gy in range(11) for gx in range(6) if font.decode(ch).getpixel((gx, gy))}
        actual = {(xx, yy) for yy in range(194, 205) for xx in range(6, 250) if image.getpixel((xx, yy)) == (230, 230, 230)}
        assert expected == actual and x == (256 - len(text) * 6) // 2
        delta = [(xx, yy) for yy in range(384) for xx in range(256) if image.getpixel((xx, yy)) != source.getpixel((xx, yy))]
        assert all(192 <= yy < 208 or number == 36000 and 64 <= yy < 75 for xx, yy in delta)
        assert image.crop((0, 208, 256, 384)).tobytes() == source.crop((0, 208, 256, 384)).tobytes()
        labels.append({"text": text, "origin": [x, 194], "all_complete_centered_native_ink_pixels": len(expected),
                       "actual_map_pixels_controls_and_markers_unchanged": True})
        screens.append((text, image))
        if number == 36000:
            phrase = "Fleet/Village: select one."
            expected = {(64 + n * 6 + gx, 64 + gy): (0, 255, 255) if n < 13 else (230, 230, 230)
                        for n, ch in enumerate(phrase) for gy in range(11) for gx in range(6) if font.decode(ch).getpixel((gx, gy))}
            for point, color in expected.items():
                assert image.getpixel(point) == color, (point, color, image.getpixel(point))
            actual = {p for p in ((xx, yy) for yy in range(64, 75) for xx in range(64, 240))
                      if image.getpixel(p) in ((0, 255, 255), (230, 230, 230))}
            assert actual == set(expected)
            labels.append({"text": phrase, "origin": [64, 64], "all_complete_native_ink_pixels": len(expected),
                           "prefix_and_instruction_colors_preserved": True})
    for file in ["translations/graphics_completion_campaign_v1.json", "translations/graphics_visual_audit_v150.json"]:
        audit = json.loads(Path(file).read_text(encoding="utf-8"))["plaque_style_v247"]
        assert len(audit["ongoing_plaque_inventory"]) == 18 and not audit["full_plaque_audit_complete"]
        assert all(not row["fully_completed"] for row in audit["ongoing_plaque_inventory"])
    clean = Path("work/clean.nds")
    assert sha(clean.read_bytes()) == "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    patch = ROM.with_suffix(".xdelta")
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, ROOT / "exact_patch_reconstruction.nds")
    assert (ROOT / "exact_patch_reconstruction.nds").read_bytes() == ROM.read_bytes()
    sheet = Image.new("RGB", (512, 410), "#333333")
    draw = ImageDraw.Draw(sheet)
    for index, (label, image) in enumerate(screens):
        draw.text((index * 256 + 4, 4), label, fill="white")
        sheet.paste(image, (index * 256, 24))
    sheet.save(ROOT / "both_modes_review.png")
    proof = {"format": "dk4-world-headers-live-v261", "candidate": str(ROM), "candidate_sha256": digest,
             "patch_sha256": sha(patch.read_bytes()), "profile": m["profile"], "base_sha256": m["base_sha256"],
             "all467_prior_batches_stages_records_files_art_routes_ARM7_overlays_retained": True,
             "only_ARM9_changed": True, "exact_V260_reproduction": True, "exact_clean_patch_reconstruction": True,
             "both_actual_selection_modes_and_complete_glyphs": labels, "unchanged_comparable_full_frames": unchanged,
             "ordinary_cold_boot_no_loaded_state_no_RAM_injection": True,
             "Forces_unknown_values_are_observed_fogged_UI_not_untranslated_text": True,
             "alternate_rank_parents_and_map_native_palette_source_still_pending": True,
             "all18_plaques_and_variants_incomplete": True, "experimental_user_acceptance_pending": True,
             "full_goal_complete": False}
    (ROOT / "saved_live_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_sha256": digest, "patch_sha256": proof["patch_sha256"], "actual_labels": labels, "unchanged_frames": unchanged}))


if __name__ == "__main__":
    main()
