"""Repair all six incomplete inherited bitmap captions from reviewed sources."""

import copy
import json
import zlib
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import REFERENCE_ASCII_FONT_SHA256
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_pxl_native_label_batch

ROOT = Path("work/analysis/radial_marker_v245")
BATCH = Path("translations/radial_marker_caption_repair_v1.json")
MERGED = Path("translations/marker_gender_and_radial_graphics_v2.json")
SYNC = Path("translations/marker_cmmnimg_sync_v3.json")
PATH = "/_pxl/__marker.pxl"
LABELS = (("機能", "Functions"), ("水夫編成", "Crew Setup"), ("甲板画面", "Deck View"),
          ("情報", "Info"), ("航路図", "Route Map"), ("アイテム", "Items"))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    canonical_path = Path("out/raphael_natural_v2_accepted_base.nds")
    prior_path = Path("out/all_routes_combined_v241_candidate.nds")
    clean_path = Path("work/clean.nds")
    assert sha(canonical_path.read_bytes()) == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    assert sha(prior_path.read_bytes()) == "d863f74ba3e5466f5a221ba93e00d53fd1588a32cecdd349006b7eb0698e8027"
    assert sha(clean_path.read_bytes()) == "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    canonical, prior, clean = NdsImage.open(canonical_path), NdsImage.open(prior_path), NdsImage.open(clean_path)
    old = PxlImage.from_bytes(clean.read_file(PATH))
    base = PxlImage.from_bytes(canonical.read_file(PATH))
    current = PxlImage.from_bytes(prior.read_file(PATH))
    backgrounds, evidence = {}, []
    for y in range(2, 18):
        for x in range(3, 61):
            values = [old.indices[(24 * n + y) * 256 + x] for n in range(6)]
            visible = set(values) - {15}
            if visible:
                assert len(visible) == 1
                backgrounds[x, y] = next(iter(visible))
            else:
                assert (x, y) == (23, 11)
                # This is the only concealed pixel. Its continuous stripe is
                # visible at thirteen neighboring diagonal coordinates.
                samples = [(23 + d, 11 - d) for d in range(-6, 8) if d]
                assert all(2 <= sy < 18 and 3 <= sx < 61 for sx, sy in samples)
                assert all(({old.indices[(24 * n + sy) * 256 + sx] for n in range(6)} - {15}) == {6}
                           for sx, sy in samples)
                backgrounds[x, y] = 6
                evidence.append({"coordinate": [23, 11], "all_six_originals_conceal_this_pixel": True,
                                 "inferred_index": 6, "visible_same_stripe_samples": samples,
                                 "not_claimed_recovered_original_pixel": True})
    batch = {"format": "dk4-pxl-native-label-batch-v1", "file_path": PATH,
             "source_file_sha256": sha(base.source), "font_file_path": "/__arm9__.bin",
             "font_sha256": REFERENCE_ASCII_FONT_SHA256, "target_locale": "en-US",
             "editorial_policy": "natural-dialogue-v2", "glyph_width": 5, "advance": 5,
             "color_index": 15, "erase_palette_indices": [15], "records": []}
    for n, (japanese, english) in enumerate(LABELS):
        box = [3, 24 * n + 2, 61, 24 * n + 18]
        for y in range(box[1], box[3]):
            assert current.indices[y * 256 + 3:y * 256 + 61] == base.indices[y * 256 + 3:y * 256 + 61]
        background = bytes(backgrounds[x, y] for y in range(2, 18) for x in range(3, 61))
        batch["records"].append({"id": f"DK4_RADIAL_MARKER_CAPTION_{n}_REPAIR_V1",
                                 "source_japanese": japanese, "text": english, "box": box,
                                 "source_meaning": english, "context": "Shared Functions/crew/deck/information/map/items menu plate.",
                                 "localization_note": "Retain the established natural English term; replace the complete lettering area, including inherited Japanese lower strokes, with full native glyphs. Preserve all plate borders.",
                                 "original_clean_caption_cell_sha256": sha(bytes(old.indices[(24*n+y)*256+x] for y in range(24) for x in range(64))),
                                 "background_indices_zlib_hex": zlib.compress(background).hex(),
                                 "review": {g: True for g in ("source", "context", "localization", "naturalness", "formatting")},
                                 "visual_review": False})
    BATCH.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    merged = copy.deepcopy(json.loads(Path("translations/marker_gender_graphics_v1.json").read_text(encoding="utf-8")))
    assert merged["source_file_sha256"] == batch["source_file_sha256"]
    merged["trim_blank_top_rows"] = 0  # Compact gender glyphs do not use native-font trimming.
    merged["records"].extend(copy.deepcopy(batch["records"]))
    merged["supersedes"] = "translations/marker_gender_graphics_v1.json"
    merged["scope"] = "Preserve both exact compact gender cells and fully repair all six inherited menu captions."
    MERGED.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    repaired, ids = apply_pxl_native_label_batch(BATCH, base.source, prior.read_file("/__arm9__.bin"))
    repaired = PxlImage.from_bytes(repaired)
    for record in batch["records"]:
        x0, y0, x1, y1 = record["box"]
        for y in range(y0, y1):
            current.indices[y * 256 + x0:y * 256 + x1] = repaired.indices[y * 256 + x0:y * 256 + x1]
    target = current.to_bytes()
    sync = copy.deepcopy(json.loads(Path("translations/marker_cmmnimg_sync_v2.json").read_text(encoding="utf-8")))
    sync.update(source_image_sha256=sha(target), supersedes="translations/marker_cmmnimg_sync_v2.json",
                scope="Preserve all prior marker/frame captions and gender symbols; synchronize six complete repaired menu captions. Original palettes, banks, borders, headers and other blocks remain exact.")
    SYNC.write_text(json.dumps(sync, indent=2) + "\n", encoding="utf-8")
    sheet = Image.new("RGB", (512, 576), "#303030")
    for i, p in enumerate((base, current)):
        sheet.paste(p.render().crop((0, 0, 64, 144)).resize((256, 576), Image.Resampling.NEAREST), (i * 256, 0))
    sheet.save(ROOT / "six_caption_repair_preview.png")
    (ROOT / "target_marker.pxl").write_bytes(target)
    plan = {"format": "dk4-radial-marker-repair-plan-v245", "canonical_marker_sha256": sha(base.source),
            "original_clean_marker_sha256": sha(old.source), "prior_marker_sha256": sha(prior.read_file(PATH)),
            "target_marker_sha256": sha(target), "changed_records": ids,
            "original_background_reference_coordinates_per_cell": 927,
            "one_inferred_background_pixel_per_cell": evidence,
            "original_caption_lower_strokes_inherited_in_canonical": True,
            "complete_original_Japanese_ink_extent_per_cell": [9, 6, 56, 17],
            "complete_erase_box_per_cell": [3, 2, 61, 18],
            "preview_visual_review_pending": True, "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "repair_plan.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"repaired_captions": len(ids), "target_marker_sha256": sha(target),
                      "background_inferred_pixels_per_cell": 1, "not_registered_or_compiled_yet": True}))


if __name__ == "__main__":
    main()
