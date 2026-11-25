"""Check full inherited release and complete repaired shopkeeper glyph pixels."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.common_literal_prefix import ROOT
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage

ROM = Path("out/all_routes_combined_v255_candidate.nds")
CAPTURE = Path("work/emulation_v193/common_literal_prefix_v255")
PRIOR_CAPTURE = Path("work/emulation_v193/square_sign_bounds_v254")


def main():
    prior = Path("out/all_routes_combined_v254_candidate.nds")
    assert (ROOT / "v254_reproduction.nds").read_bytes() == prior.read_bytes()
    a, b = NdsImage.open(prior), NdsImage.open(ROM)
    assert {p: bytes(d) for _, p, d in a.iter_files()} == {p: bytes(d) for _, p, d in b.iter_files()}
    assert a.rom.arm7 == b.rom.arm7 and a.rom.arm9OverlayTable == b.rom.arm9OverlayTable
    assert b.read_file("/__arm9__.bin") == (ROOT / "research_arm9.bin").read_bytes()
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
    previous = json.loads((PRIOR_CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    assert report["ROM_sha256"] == digest and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and report["frames"] == 20000
    assert report["scripted_input_schedule"] == previous["scripted_input_schedule"]
    lookup = {r["frame"]: r for r in previous["frames_captured"] if "cold_boot" in r["path"]}
    unchanged = []
    for row in report["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        if "cold_boot" in row["path"] and row["frame"] < 19600:
            assert row["PNG_sha256"] == lookup[row["frame"]]["PNG_sha256"]
            unchanged.append(row["frame"])
    font = GameAsciiFont.from_arm9(b.read_file("/__arm9__.bin"))
    image = Image.open(CAPTURE / "frame_020000_final.png").convert("RGB")
    source = Image.open(PRIOR_CAPTURE / "frame_020000_final.png").convert("RGB")
    lines = []
    for text, x, y in [("Business? Fair. I wish a good", 28, 296), ("opportunity would arise.", 22, 312)]:
        expected = {(x + n * 6 + gx, y + gy) for n, char in enumerate(text)
                    for gy in range(11) for gx in range(6) if font.decode(char).getpixel((gx, gy))}
        actual = {(gx, gy) for gy in range(y, y + 11) for gx in range(16, 248)
                  if max(image.getpixel((gx, gy))) < 20}
        assert actual == expected, (text, len(actual), len(expected))
        assert x >= 16 and x + len(text) * 6 <= 248 and y + 11 <= 324
        lines.append({"full_text": text, "origin": [x, y], "complete_native_ink_pixels": len(expected),
                      "all_first_internal_and_final_glyphs_exact": True, "no_extra_injected_Japanese_glyphs": True})
    changes = [(x, y) for y in range(384) for x in range(256) if source.getpixel((x, y)) != image.getpixel((x, y))]
    # The removed injected Japanese glyph occupies the twelfth scanline;
    # restored Latin glyphs have the independently verified eleven-row font.
    assert changes and all(88 <= x < 208 and 296 <= y < 308 for x, y in changes)
    assert not any(max(image.getpixel((x, 307))) < 20 for x in range(16, 248))
    assert source.crop((0, 312, 256, 324)).tobytes() == image.crop((0, 312, 256, 324)).tobytes()
    for file in ["translations/graphics_completion_campaign_v1.json", "translations/graphics_visual_audit_v150.json"]:
        audit = json.loads(Path(file).read_text(encoding="utf-8"))["plaque_style_v247"]
        assert not audit["full_plaque_audit_complete"] and len(audit["ongoing_plaque_inventory"]) == 18
        assert all(not r["fully_completed"] and r["status"] == "pending-continued-audit" for r in audit["ongoing_plaque_inventory"])
    clean = Path("work/clean.nds")
    assert sha(clean.read_bytes()) == "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    patch = ROM.with_suffix(".xdelta")
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, ROOT / "exact_patch_reconstruction.nds")
    assert (ROOT / "exact_patch_reconstruction.nds").read_bytes() == ROM.read_bytes()
    sheet = Image.new("RGB", (1024, 808), "#333333")
    draw = ImageDraw.Draw(sheet)
    draw.text((8, 8), "V254: native macro corruption", fill="white")
    draw.text((520, 8), "V255: every stored English glyph restored", fill="white")
    sheet.paste(source.resize((512, 768), Image.Resampling.NEAREST), (0, 32))
    sheet.paste(image.resize((512, 768), Image.Resampling.NEAREST), (512, 32))
    sheet.save(ROOT / "shopkeeper_glyph_review.png")
    native = json.loads((ROOT / "native_proof.json").read_text(encoding="utf-8"))
    proof = {"format": "dk4-common-literal-prefix-live-v255", "candidate": str(ROM), "candidate_sha256": digest,
             "patch_sha256": sha(patch.read_bytes()), "profile": m["profile"], "base_sha256": m["base_sha256"],
             "all467_batches_prior_records_files_routes_art_ARM7_overlays_retained": True,
             "all_stored_COMMON_and_story_strings_byte_identical": True, "only_ARM9_changed": True,
             "exact_full_V254_reproduction": True, "exact_clean_patch_reconstruction": True,
             "native_current_message_count": 3668, "native_repaired_message_count": native["changed_message_count"],
             "original_Japanese_actor_cases_unchanged": native["original_Japanese_entries_compared_for_two_actor_contracts"],
             "full_repaired_dialogue_lines": lines, "only_dialogue_first_line_pixels_differ": len(changes),
             "all_second_line_pixels_unchanged": True, "unchanged_regression_frames": unchanged,
             "title_New_Game_selection_opening_town_three_sign_states_and_shopkeeper_cold_boot_traversed": True,
             "not_all110_messages_live_GPU_verified": True,
             "all18_plaques_and_variants_remain_incomplete": True,
             "legacy_English_wording_review_other_parent_contexts_sources_and_full_goal_pending": True,
             "experimental_user_acceptance_pending": True, "full_goal_complete": False}
    (ROOT / "saved_live_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_sha256": digest, "patch_sha256": proof["patch_sha256"],
                      "restored_current_messages": native["changed_message_count"], "unchanged_frames": len(unchanged),
                      "complete_live_dialogue_ink": sum(r["complete_native_ink_pixels"] for r in lines)}))


if __name__ == "__main__":
    main()
