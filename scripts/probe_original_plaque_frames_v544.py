"""Restore original town/faction frames; reconstruct only dark Japanese strokes."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/town_force_texture_v544")
GROUPS = [
    ("town", "trading_towninfo_graphics_v2", [
        ([7, 19, 51, 36], [11, 22, 46, 34]),
        ([135, 19, 179, 36], [137, 22, 174, 34]),
        ([7, 39, 51, 56], [11, 42, 46, 54]),
        ([135, 39, 179, 56], [137, 42, 174, 54]),
        ([39, 59, 89, 77], [44, 61, 83, 74]),
        ([163, 59, 235, 77], [170, 61, 215, 74]),
    ]),
    ("force", "force_info_graphics_v2", [
        ([83, 72, 125, 94], [87, 79, 121, 90]),
        ([3, 103, 49, 122], [10, 106, 45, 118]),
        ([3, 123, 49, 142], [10, 126, 45, 138]),
        ([3, 143, 49, 162], [10, 146, 45, 158]),
        ([3, 163, 49, 182], [10, 166, 45, 178]),
    ]),
]


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    clean = NdsImage.open("work/clean.nds")
    current = NdsImage.open("out/all_routes_combined_v543_candidate.nds")
    donor = PxlImage.from_bytes(clean.read_file("/_pxl/towninfo.pxl"))
    config = {"format": "dk4-original-plaque-frames-release-v1",
              "donor_file_sha256": sha(donor.source), "files": [],
              "status": "research-only-native-verification-pending"}
    proofs = []
    for name, batch_name, bounds in GROUPS:
        batch = json.loads(Path(f"translations/{batch_name}.json").read_text(encoding="utf-8"))
        path = batch["file_path"]
        original = PxlImage.from_bytes(clean.read_file(path))
        old = PxlImage.from_bytes(current.read_file(path))
        result = PxlImage.from_bytes(old.source)
        assert old.palette == original.palette
        mapping = {rgb: min(range(len(result.palette)), key=lambda i: sum(
            (result.palette[i][k] - rgb[k]) ** 2 for k in range(3)))
            for rgb in donor.palette}
        records, allowed = [], set()
        for record, (box, erase) in zip(batch["records"], bounds, strict=True):
            l, t, r, b = box
            el, et, er, eb = erase
            ink = {y * old.width + x for y in range(t, b) for x in range(l, r)
                   if old.indices[y * old.width + x] == batch["color_index"]}
            replaced, preserved = 0, 0
            for y in range(t, b):
                for x in range(l, r):
                    position = y * old.width + x
                    index = original.indices[position]
                    if position in ink:
                        result.indices[position] = batch["color_index"]
                    elif el <= x < er and et <= y < eb and original.palette[index][0] < 140:
                        # Reconstruct concealed pixels from a clean, unlettered
                        # source strip. Every other visible source pixel survives.
                        dx, dy = 2 + (x - el) % 40, 62 + (y - et) % 12
                        rgb = donor.palette[donor.indices[dy * donor.width + dx]]
                        result.indices[position] = mapping[rgb]
                        replaced += 1
                    else:
                        result.indices[position] = index
                        preserved += 1
                    allowed.add(position)
            # Original blue header pixels can share the English ink index.
            # Compare the actual eleven-row text band, not unrelated wallpaper.
            bl, bt, br, bb = record["box"]
            font_top = bt + (bb - bt - 11) // 2
            actual_ink = {y * old.width + x for y in range(font_top, font_top + 11)
                          for x in range(bl, br)
                          if result.indices[y * old.width + x] == batch["color_index"]}
            expected_ink = {p for p in ink if font_top <= p // old.width < font_top + 11
                            and bl <= p % old.width < br}
            assert expected_ink == actual_ink, (name, record["text"], "text-band ink differs")
            records.append({"id": record["id"], "english": record["text"],
                            "restore_box": box, "japanese_stroke_box": erase,
                            "ink_palette_index": batch["color_index"],
                            "visible_source_pixels_preserved": preserved,
                            "concealed_dark_pixels_reconstructed": replaced})
        assert all(a == b for p, (a, b) in enumerate(zip(old.indices, result.indices)) if p not in allowed)
        data = result.to_bytes()
        assert data[:old.pixels_offset] == old.source[:old.pixels_offset]
        (ROOT / f"{name}_RESEARCH_ONLY.pxl").write_bytes(data)
        config["files"].append({"file_path": path, "source_sha256": sha(old.source),
                                "japanese_source_sha256": sha(original.source),
                                "target_sha256": sha(data), "records": records})
        proofs.extend(records)
        sheet = Image.new("RGB", (1080, len(records) * 140 + 25), (40, 45, 50))
        draw = ImageDraw.Draw(sheet)
        for col, label in enumerate(["Japanese source", "V543", "Restored source frame"]):
            draw.text((col * 360 + 5, 5), label, fill="white")
        for n, row in enumerate(records):
            draw.text((5, n * 140 + 25), row["english"], fill="white")
            for col, asset in enumerate([original, old, result]):
                crop = asset.render().crop(row["restore_box"]).convert("RGB")
                crop = crop.resize((crop.width * 4, crop.height * 4), Image.Resampling.NEAREST)
                sheet.paste(crop, (col * 360 + 5, n * 140 + 45))
        sheet.save(ROOT / f"{name}_source_frame_review.png")
    (ROOT / "prototype_config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "source_frame_proof.json").write_text(json.dumps({
        "original_visible_texture_and_frames_restored": True, "complete_current_english_ink_masks_preserved": True,
        "all_unowned_pixels_and_palette_dimensions_preserved": True, "records": proofs,
        "concealed_texture_reconstruction_not_exact_recovery": True,
        "dark_mask_threshold_and_extent_require_visual_review": True,
        "production_ROM_not_modified": True, "native_verification_pending": True}, indent=2) + "\n", encoding="utf-8")
    print("Prepared 11 original-frame plaque prototypes with preserved English and unowned pixels.")


if __name__ == "__main__":
    main()
