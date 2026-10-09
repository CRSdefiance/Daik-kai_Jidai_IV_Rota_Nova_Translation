"""Compose the chosen opening name from its existing native reveal glyphs."""

import copy
import json
import zlib
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.compression_probe import compress_lz10

ROOT = Path("work/analysis/hodram_opening_v204")
QA = Path("work/qa/hodram_opening_v204")
BASE = Path("out/raphael_natural_v2_accepted_base.nds")
PRIOR_BATCH = Path("translations/opening_m28_title_art_v4.json")
OUTPUT_BATCH = Path("translations/opening_m28_title_and_hodram_art_v5.json")
# The same original cyan serif lettering supplies every required glyph. Source
# entries are successive complete prefixes; retain their changed indexed pixels.
GLYPHS = (("H", 25, 1), ("o", 26, 14), ("d", 28, 23),
          ("r", 40, 34), ("a", 34, 42), ("m", 31, 54))
TAIL_SOURCE_X, TAIL_SHIFT = 76, -6


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    assert sha(BASE.read_bytes()) == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    policy = json.loads(Path("translations/character_name_localization_policy_v1.json").read_text(encoding="utf-8"))
    assert any(row.get("localized_full_name") == "Hodram Joakim Bergstrom" for row in policy["confirmed_decisions"])
    raw = NdsImage.open(BASE).read_file("/FLS/M28.fls")
    clean_raw = NdsImage.open("work/clean.nds").read_file("/FLS/M28.fls")
    source, clean = FlsArchive(raw), FlsArchive(clean_raw)
    original = {i: source.texture(i) for i in range(25, 47)}
    palette = original[46].palette
    for index, texture in original.items():
        other = clean.texture(index)
        assert texture.palette == palette and (texture.width, texture.height) == (256, 32)
        assert (texture.flags, texture.palette, texture.indices) == (other.flags, other.palette, other.indices)
    sprites, glyph_rows = [], []
    for letter, index, destination_x in GLYPHS:
        after = original[index].indices
        before = bytearray(8192) if index == 25 else original[index - 1].indices
        mask = [i for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
        # Index seven is the source's opaque black shadow; index zero is the
        # unused/transparent background. Keep that distinction even though both
        # decode to RGB black in a simple preview.
        assert mask and all(after[i] != 0 for i in mask)
        x0 = min(i % 256 for i in mask)
        sprite = [(i % 256 - x0 + destination_x, i // 256, after[i]) for i in mask]
        sprites.append(sprite)
        glyph_rows.append({"letter": letter, "source_texture": index, "previous_texture": index - 1 if index > 25 else None,
                           "source_bounds": [x0, min(i // 256 for i in mask), max(i % 256 for i in mask) + 1, max(i // 256 for i in mask) + 1],
                           "source_changed_pixels": len(mask), "destination_x": destination_x,
                           "source_overlap_recolored_pixels_included": sum(bool(before[i]) for i in mask)})
    prefix = bytearray(8192)
    prefixes = []
    for sprite in sprites:
        for x, y, color in sprite:
            assert 0 <= x < 72 and 0 <= y < 20
            prefix[y * 256 + x] = color
        prefixes.append(bytes(prefix))
    assert prefixes[0] == bytes(original[25].indices) and prefixes[1] == bytes(original[26].indices)
    prior = json.loads(PRIOR_BATCH.read_text(encoding="utf-8"))
    assert prior["format"] == "dk4-fls-indexed-region-batch-v1" and prior["source_file_sha256"] == sha(raw)
    batch = copy.deepcopy(prior)
    new_rows, previews, capacities = [], [], []
    for index in range(27, 47):
        target = bytearray(prefixes[min(index - 25, 5)])
        if index >= 32:
            for reveal in range(32, index + 1):
                for offset, (before, after) in enumerate(zip(original[reveal - 1].indices, original[reveal].indices, strict=True)):
                    if before != after:
                        assert after != 0
                        target[offset // 256 * 256 + offset % 256 + TAIL_SHIFT] = after
            assert all(target[y * 256 + x + TAIL_SHIFT] == original[index].indices[y * 256 + x]
                       for y in range(32) for x in range(TAIL_SOURCE_X, 256))
        texture = copy.deepcopy(original[index])
        texture.indices[:] = target
        assert all(target[y * 256 + x] == original[index].indices[y * 256 + x]
                   for y in range(32) for x in range(256) if x >= 235 or y >= 20)
        packed = bytes(target[i] | target[i + 1] << 4 for i in range(0, len(target), 2))
        compressed = compress_lz10(packed)
        slot = source.records[index][5]
        prefix_bytes = max(0, (len(compressed) - slot + 15) // 16 * 16)
        record = source.records[index]
        available = record[4] - record[2] - record[3]
        assert 0 <= prefix_bytes <= available
        assert not any(raw[source.data_offset + record[4] - prefix_bytes:source.data_offset + record[4]])
        capacities.append({"texture": index, "compressed_bytes": len(compressed), "source_slot_bytes": slot,
                           "reclaimed_zero_alignment_bytes": prefix_bytes, "available_palette_to_pixel_gap": available,
                           "new_slot_bytes": slot + prefix_bytes, "fits_mapped_slot": len(compressed) <= slot + prefix_bytes})
        region = bytes(target[y * 256 + x] for y in range(20) for x in range(235))
        record_id = f"DK4_OPENING_HODRAM_NAME_{index:02d}_V1"
        new_rows.append({"id": record_id, "asset_index": index,
                         "source_texture_sha256": sha(original[index].indices), "source_record": source.records[index],
                         "box": [0, 0, 235, 20], "indices_zlib_hex": zlib.compress(region, 9).hex(),
                         "indices_sha256": sha(region), "localized_full_name": "Hodram Joakim Bergstrom",
                         "pixel_slot_prefix_bytes": prefix_bytes,
                         "localization_reason": "User-confirmed faithful Hodram adaptation; original Hoodlum has an unwanted English meaning.",
                         "native_source_glyphs_only": True})
        path = QA / f"M28_{index:02d}.png"
        texture.render().save(path)
        previews.append({"texture": index, "path": path.as_posix(), "sha256": sha(path.read_bytes()),
                         "indices_sha256": sha(target), "visually_reviewed": False})
    # Preserve the original full title recipes verbatim, with no new source locks.
    batch["records"].extend(new_rows)
    batch["description"] = "Retains all V188 opening title art; source-native Hodram name lettering in 20 existing reveal textures. Native palettes/dimensions/timing retained."
    batch["name_art_rationale"] = "docs/glossary.md"
    OUTPUT_BATCH.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sheet = Image.new("RGB", (1040, 10 * 88), "#303030")
    draw = ImageDraw.Draw(sheet)
    for k, row in enumerate(previews):
        with Image.open(row["path"]) as im:
            image = im.convert("RGB").resize((512, 64), Image.Resampling.NEAREST)
        x, y = k % 2 * 520, k // 2 * 88
        draw.text((x + 4, y + 2), f"M28 {row['texture']}", fill="white")
        sheet.paste(image, (x + 4, y + 20))
    sheet_path = QA / "all_reveals.png"
    sheet.save(sheet_path)
    report = {"format": "dk4-opening-Hodram-native-glyph-preparation-v1", "source_FLS_sha256": sha(raw),
              "source_font_glyphs": glyph_rows, "original_title_records_retained_verbatim": batch["records"][:len(prior["records"])] == prior["records"],
              "unchanged_first_two_reveal_textures": [25, 26], "first_name_completion_hold_texture": 31,
              "middle_and_surname_source_pixels_shifted_exactly": TAIL_SHIFT,
              "new_records": new_rows, "slot_capacities": capacities, "previews": previews,
              "review_sheet": sheet_path.as_posix(), "review_sheet_sha256": sha(sheet_path.read_bytes()),
              "batch": OUTPUT_BATCH.as_posix(), "all_mapped_slots_fit": all(row["fits_mapped_slot"] for row in capacities),
              "native_visual_reveal_and_release_integration_pending": True, "registered_ROM_modified": False, "goal_complete": False}
    (ROOT / "preparation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_glyphs": len(sprites), "new_textures": len(new_rows),
                      "largest_padding_reclaim": max(r["reclaimed_zero_alignment_bytes"] for r in capacities),
                      "all_mapped_slots_fit": True, "batch_not_registered": OUTPUT_BATCH.as_posix()}))


if __name__ == "__main__":
    main()
