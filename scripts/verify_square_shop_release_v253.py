"""Exact release inheritance and observed ordinary Square caption evidence."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.square_shop_labels import ROOT
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage

ROM = Path("out/all_routes_combined_v253_candidate.nds")
CAPTURE = Path("work/emulation_v193/square_shop_v253")
PRIOR_CAPTURE = Path("work/emulation_v193/occupied_equipment_v253_interactive")


def main():
    prior = Path("out/all_routes_combined_v252_candidate.nds")
    assert (ROOT / "v252_reproduction.nds").read_bytes() == prior.read_bytes()
    a, b = NdsImage.open(prior), NdsImage.open(ROM)
    assert {p: bytes(d) for _, p, d in a.iter_files()} == {p: bytes(d) for _, p, d in b.iter_files()}
    assert a.rom.arm7 == b.rom.arm7 and a.rom.arm9OverlayTable == b.rom.arm9OverlayTable
    assert b.read_file("/__arm9__.bin") == (ROOT / "research_arm9.bin").read_bytes()
    old = json.loads(prior.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    m = json.loads(ROM.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    norm = lambda values: [p.replace("\\", "/") for p in values]
    assert norm(m["batches"]) == norm(old["batches"]) and len(m["batches"]) == 467
    assert m["required_batches"] == old["required_batches"]
    for path, records in old["changed_records"].items():
        assert set(records) <= set(m["changed_records"][path])
    digest = sha(ROM.read_bytes())
    assert m["candidate_sha256"] == digest
    assert m["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    report = json.loads((CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    old_report = json.loads((PRIOR_CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    assert report["ROM_sha256"] == digest and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and report["frames"] == 16400
    assert report["scripted_input_schedule"] == old_report["scripted_input_schedule"]
    exact_frames = 0
    lookup = {r["frame"]: r["PNG_sha256"] for r in old_report["frames_captured"] if "cold_boot" in r["path"]}
    for row in report["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        if row["frame"] <= 15000 and "cold_boot" in row["path"]:
            assert row["PNG_sha256"] == lookup[row["frame"]]
            exact_frames += 1
    image = Image.open(CAPTURE / "frame_016400_final.png").convert("RGB")
    original = Image.open(PRIOR_CAPTURE / "frame_016400_final.png").convert("RGB")
    assert image.crop((0, 0, 256, 200)).tobytes() == original.crop((0, 0, 256, 200)).tobytes()
    font = GameAsciiFont.from_arm9(b.read_file("/__arm9__.bin"))
    captions = []
    for text, y in [("Food Shop", 214), ("Liquor Shop", 246)]:
        expected = set()
        for n, char in enumerate(text):
            glyph = font.decode(char)
            for gy in range(11):
                for gx in range(6):
                    if glyph.getpixel((gx, gy)):
                        expected.add((120 + n * 5 + gx, y + gy))
        colors = {image.getpixel(p) for p in expected}
        assert len(colors) == 1, (text, colors)
        color = next(iter(colors))
        actual = {(x, gy) for gy in range(y, y + 12) for x in range(120, 184) if image.getpixel((x, gy)) == color}
        assert actual == expected, (text, len(actual), len(expected))
        captions.append({"English": text, "origin": [120, y], "advance": 5,
                         "full_glyph_ink_pixels_exact": len(expected), "first_internal_final_glyphs_verified": True})
    # The action button currently covers the third sign. Native backing passes
    # all eighteen raster cases; this is deliberately not third-row GPU proof.
    third_pending = "Trends button overlaps the third sign row; Jewelry Shop GPU visibility remains unverified."
    for f in ["translations/graphics_completion_campaign_v1.json", "translations/graphics_visual_audit_v150.json"]:
        audit = json.loads(Path(f).read_text(encoding="utf-8"))["plaque_style_v247"]
        assert not audit["full_plaque_audit_complete"] and len(audit["ongoing_plaque_inventory"]) == 18
        assert all(not r["fully_completed"] and r["status"] == "pending-continued-audit" for r in audit["ongoing_plaque_inventory"])
    patch = ROM.with_suffix(".xdelta")
    assert sha(Path("work/clean.nds").read_bytes()) == "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    make_xdelta(Path("work/clean.nds"), ROM, patch)
    apply_xdelta(Path("work/clean.nds"), patch, ROOT / "exact_patch_reconstruction.nds")
    assert (ROOT / "exact_patch_reconstruction.nds").read_bytes() == ROM.read_bytes()
    sheet = Image.new("RGB", (1024, 808), "#333333")
    draw = ImageDraw.Draw(sheet)
    draw.text((8, 8), "V252 source", fill="white")
    draw.text((520, 8), "V253 complete first two captions; third row audit OPEN", fill="white")
    sheet.paste(original.resize((512, 768), Image.Resampling.NEAREST), (0, 32))
    sheet.paste(image.resize((512, 768), Image.Resampling.NEAREST), (512, 32))
    sheet.save(ROOT / "square_caption_review.png")
    proof = {"format": "dk4-square-live-v253", "candidate": str(ROM), "candidate_sha256": digest,
             "patch_sha256": sha(patch.read_bytes()), "profile": m["profile"], "base_sha256": m["base_sha256"],
             "all467_batches_and_prior_records_retained": True, "all_files_routes_art_ARM7_overlays_exact_V252": True,
             "full_V252_reproduction_exact": True, "exact_clean_patch_reconstruction": True,
             "cold_boot_no_loaded_state_no_RAM_injection": True, "unaffected_sampled_frames_exact": exact_frames,
             "captions": captions, "third_sign_row_visibility_pending": third_pending,
             "occupied_equipment_not_reached_inventory_empty": True,
             "all18_base_plaque_hint_entries_and_variants_incomplete": True,
             "experimental_user_acceptance_pending": True, "full_goal_complete": False}
    (ROOT / "saved_live_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: proof[k] for k in ("candidate_sha256", "patch_sha256", "unaffected_sampled_frames_exact")}))


if __name__ == "__main__":
    main()
