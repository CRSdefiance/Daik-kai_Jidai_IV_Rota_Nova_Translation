"""Saved integrated ROM, exact inherited content, and actual complete help glyphs."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/deck_filter_v263")
ROM = Path("out/all_routes_combined_v263_candidate.nds")
CAPTURE = Path("work/emulation_v193/deck_filter_v263")
PREVIOUS = Path("work/emulation_v193/deck_filter_v262")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def ink(font, text, x, y):
    return {(x + n * 6 + xx, y + yy)
            for n, ch in enumerate(text) for yy in range(11) for xx in range(6)
            if font.decode(ch).getpixel((xx, yy))}


def main():
    prior = Path("out/all_routes_combined_v261_candidate.nds")
    assert Path("work/analysis/deck_filter_v262/v261_reproduction.nds").read_bytes() == prior.read_bytes()
    a, b = NdsImage.open(prior), NdsImage.open(ROM)
    assert {p: bytes(d) for _, p, d in a.iter_files()} == {p: bytes(d) for _, p, d in b.iter_files()}
    assert a.rom.arm7 == b.rom.arm7 and a.rom.arm9OverlayTable == b.rom.arm9OverlayTable
    assert b.read_file("/__arm9__.bin") == (ROOT / "research_arm9.bin").read_bytes()
    manifest, old = load(ROM.with_suffix(".manifest.json")), load(prior.with_suffix(".manifest.json"))
    normalize = lambda rows: [p.replace("\\", "/") for p in rows]
    assert normalize(manifest["batches"]) == normalize(old["batches"]) and len(manifest["batches"]) == 467
    assert manifest["required_batches"] == old["required_batches"]
    for path, ids in old["changed_records"].items():
        assert set(ids) <= set(manifest["changed_records"][path])
    digest = sha(ROM.read_bytes())
    assert manifest["candidate_sha256"] == digest
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    registry = load("translations/release_stack.json")["profiles"]
    assert registry["all-routes-unified-v263"]["common_dialogue_alignment_release"] == registry["all-routes-unified-v261"]["common_dialogue_alignment_release"]
    report, earlier = load(CAPTURE / "capture_report.json"), load(PREVIOUS / "capture_report.json")
    assert report["ROM_sha256"] == digest and report["cold_boot"] and not report["savestate_loaded"]
    assert report["frames"] == 20800 and not report["callback_errors"]
    assert report["scripted_input_schedule"] == earlier["scripted_input_schedule"]
    lookup = {r["frame"]: r for r in earlier["frames_captured"]}
    unchanged, changed = [], []
    for row in report["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        if row["frame"] not in lookup:
            continue
        current = Image.open(row["path"]).convert("RGB")
        previous = Image.open(lookup[row["frame"]]["path"]).convert("RGB")
        delta = [(x, y) for y in range(384) for x in range(256) if current.getpixel((x, y)) != previous.getpixel((x, y))]
        if delta:
            assert all(0 <= x < 256 and 80 <= y < 128 for x, y in delta)
            changed.append(row["frame"])
        else:
            unchanged.append(row["frame"])
    font = GameAsciiFont.from_arm9(b.read_file("/__arm9__.bin"))
    plan = load(ROOT / "runtime_plan.json")
    labels, help_pixels = [], 0
    screen = Image.open(CAPTURE / "frame_020800_cold_boot.png").convert("RGB")
    expected = set()
    for record, y in zip(plan["records"][2:], [32, 48, 80]):
        for number, line in enumerate(record["compiled"].split("\n")):
            # Native protected LF consumes one of its two empty guard spaces.
            text = line[1:] if number else line
            pixels = ink(font, text, 0, y + number * 16)
            expected |= pixels
            labels.append({"text": text.strip(), "origin": [6 if number else 0, y + number * 16], "complete_pixels": len(pixels)})
    actual = {(x, y) for y in range(32, 128) for x in range(256) if screen.getpixel((x, y)) == (230, 230, 230)}
    assert expected == actual, (len(expected), len(actual), sorted(expected-actual)[:5], sorted(actual-expected)[:5])
    help_pixels = len(expected)
    filter_labels = []
    for text in ["Unassigned", "All"]:
        matches = [(x, y) for y in range(268, 303) for x in range(88, 166 - len(text) * 6)
                   if all(screen.getpixel(p) == (8, 8, 8) for p in ink(font, text, x, y))]
        assert len(matches) == 1, (text, matches)
        x, y = matches[0]
        expected_label = ink(font, text, x, y)
        actual_label = {(xx, yy) for yy in range(y, y + 11) for xx in range(90, 165) if screen.getpixel((xx, yy)) == (8, 8, 8)}
        assert expected_label == actual_label
        filter_labels.append({"text": text, "origin": [x, y], "all_native_ink_pixels_exact": len(expected_label)})
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
    proof = {"format": "dk4-deck-filter-live-v263", "candidate": str(ROM), "candidate_sha256": digest,
             "patch_sha256": sha(patch.read_bytes()), "profile": manifest["profile"], "base_sha256": manifest["base_sha256"],
             "all467_prior_batches_records_files_routes_art_ARM7_overlays_retained": True,
             "exact_full_V261_reproduction_and_clean_patch_reconstruction": True,
             "inherited_dialogue_left_alignment_v2_preserved": True,
             "actual_complete_help_lines": labels, "all_help_ink_pixels_exact": help_pixels,
             "actual_complete_filter_labels": filter_labels, "whole_frames_unchanged_from_failed_V262": unchanged,
             "only_help_ability_rows_changed_from_V262": changed,
             "ordinary_cold_boot_no_loaded_state": True, "targeted_test_not_full_playthrough": True,
             "native_parent_coordinate_conversion_remains_supplied_contract": True,
             "all18_plaques_and_variants_incomplete": True, "experimental_user_acceptance_pending": True,
             "full_goal_complete": False}
    (ROOT / "saved_live_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_sha256": digest, "patch_sha256": proof["patch_sha256"], "help_pixels": help_pixels, "filter_labels": filter_labels}))


if __name__ == "__main__":
    main()
