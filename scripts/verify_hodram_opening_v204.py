"""Verify complete inheritance, bounded native glyph allocation and reveal pixels."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files, verify_golden_content
from scripts.verify_original_latin_cards_native_v197 import native5

ROOT = Path("work/analysis/hodram_opening_v204")
PRIOR = Path("out/all_routes_combined_v190_candidate.nds")
CANDIDATE = Path("out/all_routes_combined_v204_candidate.nds")
CAPTURE = Path("work/emulation_v193/hodram_opening_v204")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    previous, current = NdsImage.open(PRIOR), NdsImage.open(CANDIDATE)
    before, after = rom_files(previous), rom_files(current)
    assert [path for path in before if before[path] != after[path]] == ["/FLS/M28.fls"]
    old_manifest, manifest = read(PRIOR.with_suffix(".manifest.json")), read(CANDIDATE.with_suffix(".manifest.json"))
    assert manifest["candidate_sha256"] == sha(CANDIDATE.read_bytes())
    assert manifest["profile"] == "all-routes-unified-v204"
    for key in ("batches", "required_batches"):
        expected = [p.replace("opening_m28_title_art_v4.json", "opening_m28_title_and_hodram_art_v5.json")
                    for p in old_manifest[key]]
        assert manifest[key] == expected
    assert len(manifest["batches"]) == 465 and manifest["relocations"] == old_manifest["relocations"]
    for path, records in old_manifest["changed_records"].items():
        expected = records + [f"DK4_OPENING_HODRAM_NAME_{i:02d}_V1" for i in range(27, 47)] if path == "/FLS/M28.fls" else records
        assert manifest["changed_records"][path] == expected
    assert (ROOT / "v190_builder_reproduction.nds").read_bytes() == PRIOR.read_bytes()
    assert (ROOT / "patch_reconstruction.nds").read_bytes() == CANDIDATE.read_bytes()
    old, new = FlsArchive(before["/FLS/M28.fls"]), FlsArchive(after["/FLS/M28.fls"])
    assert old.count == new.count and len(old.source) == len(new.source)
    batch = read("translations/opening_m28_title_and_hodram_art_v5.json")
    new_rows = {row["asset_index"]: row for row in batch["records"] if row["asset_index"] >= 27}
    allowed, allocations = set(), []
    for index in range(old.count):
        a, b = old.texture(index), new.texture(index)
        assert (a.flags, a.width, a.height, a.palette) == (b.flags, b.width, b.height, b.palette)
        if index not in new_rows:
            assert a.indices == b.indices and old.records[index] == new.records[index]
            continue
        row = new_rows[index]
        prefix = row["pixel_slot_prefix_bytes"]
        source_record, target_record = old.records[index], new.records[index]
        assert source_record[:4] == target_record[:4]
        assert target_record[4:] == [source_record[4] - prefix, source_record[5] + prefix]
        assert sum(source_record[4:]) == sum(target_record[4:])
        assert not any(old.source[old.data_offset + target_record[4]:old.data_offset + source_record[4]])
        allowed.update(range(old.table_offset + index * 24 + 16, old.table_offset + index * 24 + 24))
        allowed.update(range(old.data_offset + target_record[4], old.data_offset + sum(target_record[4:])))
        x0, y0, x1, y1 = row["box"]
        assert all(a.indices[y * a.width + x] == b.indices[y * b.width + x]
                   for y in range(a.height) for x in range(a.width) if not x0 <= x < x1 or not y0 <= y < y1)
        allocations.append({"texture": index, "source_record": source_record, "target_record": target_record,
                            "zero_alignment_bytes_reclaimed": prefix, "original_slot_end_and_palette_preserved": True})
    changed = [i for i, (a, b) in enumerate(zip(old.source, new.source, strict=True)) if a != b]
    assert all(i in allowed for i in changed)
    assert all(row["rejected"] for row in read(ROOT / "padding_negative_checks.json"))
    reveals = read(CAPTURE / "fine_reveals/capture_report.json")
    story = read(CAPTURE / "capture_report.json")
    town = read(CAPTURE / "town_regression/capture_report.json")
    for report in (reveals, story, town):
        assert report["ROM_sha256"] == manifest["candidate_sha256"]
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        for frame in report["frames_captured"]:
            assert sha(Path(frame["path"]).read_bytes()) == frame["PNG_sha256"]
    frames = {row["frame"]: row for row in reveals["frames_captured"]}
    cases = []
    for index in range(25, 47):
        frame = 1912 + (index - 25) * 4
        saved = frames[frame]
        with Image.open(saved["path"]) as im:
            image = im.convert("RGB")
        texture = new.texture(index)
        points = {(k % 256, k // 256): native5(texture.palette[color])
                  for k, color in enumerate(texture.indices) if color != 0}
        assert all(0 <= x + 12 < 256 and 0 <= y + 167 < 192 for x, y in points)
        assert all(native5(image.getpixel((x + 12, y + 167))) == color for (x, y), color in points.items()), (index, frame)
        bright = native5(texture.palette[15])
        actual_bright = {(x, y) for y in range(20) for x in range(235)
                         if native5(image.getpixel((x + 12, y + 167))) == bright}
        assert actual_bright == {p for p, color in points.items() if color == bright}, (index, "extra or missing letters")
        cases.append({"texture": index, "frame": frame, "PNG": saved["path"], "PNG_sha256": saved["PNG_sha256"],
                      "exact_native_pixels_including_opaque_black_shadow": len(points),
                      "native_ink_bounds": [min(x for x, y in points) + 12, min(y for x, y in points) + 167,
                                            max(x for x, y in points) + 13, max(y for x, y in points) + 168],
                      "first_last_letters_and_no_extra_bright_strokes": True})
    verify_golden_content(NdsImage.open("out/raphael_natural_v2_accepted_base.nds"), current)
    report = {"format": "dk4-Hodram-opening-integrated-proof-v1", "candidate": CANDIDATE.as_posix(),
              "candidate_sha256": manifest["candidate_sha256"], "profile": manifest["profile"],
              "full_465_batch_and_all_prior_terminal_stages_preserved": True,
              "all_prior_record_ids_retained": True, "full_prior_V190_reproduction_exact": True,
              "changed_paths_vs_V190": ["/FLS/M28.fls"], "all_palettes_dimensions_flags_and_unowned_bytes_exact": True,
              "same_archive_size_and_original_pixel_slot_ends": True, "allocations": allocations,
              "native_reveal_cases": cases, "complete_reveal_cases": len(cases),
              "patch": CANDIDATE.with_suffix(".xdelta").as_posix(),
              "patch_sha256": sha(CANDIDATE.with_suffix(".xdelta").read_bytes()), "patch_reconstruction_exact": True,
              "cold_boot_menu_NewGame_town_story_visual_review": "complete-scoped-saved-frame-review",
              "town_UI_frame": next(row for row in town["frames_captured"] if row["frame"] == 14900),
              "user_acceptance": False, "experimental": True, "full_goal_complete": False}
    (ROOT / "saved_proof.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"all22_native_reveal_cases": len(cases), "final_complete_pixels": cases[-1]["exact_native_pixels_including_opaque_black_shadow"],
                      "full_inheritance_and_exact_patch": True, "only_changed_path_vs_V190": "/FLS/M28.fls"}))


if __name__ == "__main__":
    main()
