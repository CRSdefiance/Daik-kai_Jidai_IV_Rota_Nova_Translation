"""Verify the source-faithful sail caption and complete inherited playable ROM."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sail_angle_caption import OFFSET, transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/sail_angle_v267")
ROM = Path("out/all_routes_combined_v267_candidate.nds")
CAPTURE = Path("work/emulation_v193/sail_angle_v267")
PRIOR = Path("work/emulation_v193/equipment_gameplay_v266")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def mask(font, text):
    return {(47 + i * 6 + x, 370 + y) for i, c in enumerate(text)
            for y in range(11) for x in range(6) if font.decode(c).getpixel((x, y))}


def main():
    prior_path = Path("out/all_routes_combined_v263_candidate.nds")
    assert (ROOT / "v263_reproduction.nds").read_bytes() == prior_path.read_bytes()
    a, b = NdsImage.open(prior_path), NdsImage.open(ROM)
    assert {p: bytes(d) for _, p, d in a.iter_files()} == {p: bytes(d) for _, p, d in b.iter_files()}
    assert a.rom.arm7 == b.rom.arm7 and a.rom.arm9OverlayTable == b.rom.arm9OverlayTable
    old_arm, arm = a.read_file("/__arm9__.bin"), b.read_file("/__arm9__.bin")
    clean_arm = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    expected_arm, plan = transform(old_arm, clean_arm)
    assert arm == expected_arm == (ROOT / "research_arm9.bin").read_bytes()
    assert arm[:OFFSET] == old_arm[:OFFSET] and arm[OFFSET + 8:] == old_arm[OFFSET + 8:]
    m, old_m = load(ROM.with_suffix(".manifest.json")), load(prior_path.with_suffix(".manifest.json"))
    norm = lambda rows: [p.replace("\\", "/") for p in rows]
    assert norm(m["batches"]) == norm(old_m["batches"]) and len(m["batches"]) == 467
    assert m["required_batches"] == old_m["required_batches"]
    for path, rows in old_m["changed_records"].items():
        assert set(rows) <= set(m["changed_records"][path])
    digest = sha(ROM.read_bytes())
    assert m["candidate_sha256"] == digest and m["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    report, prior = load(CAPTURE / "capture_report.json"), load(PRIOR / "capture_report.json")
    assert report["ROM_sha256"] == digest and report["cold_boot"] and not report["savestate_loaded"]
    assert report["frames"] == prior["frames"] == 32720 and not report["callback_errors"]
    assert report["scripted_input_schedule"] == prior["scripted_input_schedule"]
    lookup = {row["frame"]: row for row in prior["frames_captured"] if "cold_boot" in row["path"]}
    font = GameAsciiFont.from_arm9(arm)
    expected = mask(font, "Sails ")
    original_ink = mask(font, "Rotate")
    unchanged, changed, labels = [], [], []
    for row in report["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        if "cold_boot" not in row["path"] or row["frame"] not in lookup:
            continue
        image = Image.open(row["path"]).convert("RGB")
        before = Image.open(lookup[row["frame"]]["path"]).convert("RGB")
        delta = [(x, y) for y in range(384) for x in range(256) if image.getpixel((x, y)) != before.getpixel((x, y))]
        if not delta:
            unchanged.append(row["frame"])
            continue
        assert all(46 <= x < 85 and 369 <= y < 383 for x, y in delta)
        actual = {(x, y) for y in range(370, 381) for x in range(47, 83) if image.getpixel((x, y)) == (230, 230, 230)}
        old_actual = {(x, y) for y in range(370, 381) for x in range(47, 83) if before.getpixel((x, y)) == (230, 230, 230)}
        assert actual == expected and old_actual == original_ink
        changed.append(row["frame"])
        labels.append({"frame": row["frame"], "caption": "Sails", "origin": [47, 370],
                       "all_native_ink_pixels": len(expected), "complete_first_and_last_S_and_blank_padding": True,
                       "all_other_footer_controls_whole_screens_and_UI_unchanged": True})
    assert changed and unchanged
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
    proof = {"format": "dk4-sail-angle-live-v267", "candidate": str(ROM), "candidate_sha256": digest,
             "patch_sha256": sha(patch.read_bytes()), "profile": m["profile"], "base_sha256": m["base_sha256"],
             "source_review_and_exact_byte_change": plan,
             "exact_full_V263_reproduction_and_clean_patch_reconstruction": True,
             "all467_prior_batches_records_files_routes_art_ARM7_overlays_and_native_code_retained": True,
             "only_eight_byte_caption_allocation_changed_in_ARM9": True,
             "unchanged_whole_frames": unchanged, "complete_footer_label_cases": labels,
             "ordinary_cold_boot_with_recorded_buttons_and_stylus_no_loaded_state": True,
             "equipment_voyage_unfinished_not_presented_as_acquisition": True,
             "all18_plaques_and_variants_incomplete": True, "experimental_user_acceptance_pending": True,
             "full_goal_complete": False}
    (ROOT / "saved_live_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ROM_sha256": digest, "patch_sha256": proof["patch_sha256"],
                      "verified_label_frames": len(labels), "unchanged_whole_frames": len(unchanged)}))


if __name__ == "__main__":
    main()
