"""Audit exact raw/PXL payload copies and complete FLS decoding, including raw storage."""

import json
import struct
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/raw_pxl_matches_v224")


def main():
    clean = NdsImage.open("work/clean.nds")
    current = NdsImage.open("out/all_routes_combined_v218_candidate.nds")
    banks = {name: clean.read_file(f"/GRP/{name}.DK4") for name in ("OCINIT", "DSCHR")}
    matches, fls_rows, raw_rows, direct_color_rows = [], [], [], []
    pxl_count = 0
    for _, path, data in clean.iter_files():
        if path.lower().endswith(".pxl"):
            pxl_count += 1
            depth, pitch, height, _, pixels_offset = struct.unpack_from("<5I", data)
            if depth & 255 == 16:
                packed = data[pixels_offset:]
                assert len(packed) == pitch * height * 2
                dimensions, bits_per_pixel = [pitch, height], 16
                direct_color_rows.append({"file": path, "dimensions": dimensions,
                                          "complete_direct_color_pixels_sha256": sha(packed),
                                          "source_unchanged": data == current.read_file(path)})
            else:
                image = PxlImage.from_bytes(data)
                packed = data[image.pixels_offset:]
                dimensions, bits_per_pixel = [image.width, image.height], image.bits_per_pixel
            if len(packed) < 32 or len(set(packed)) < 3:
                continue
            for family, source in banks.items():
                offset = source.find(packed)
                if offset < 0:
                    continue
                matches.append({"raw_file": f"/GRP/{family}.DK4", "offset": offset,
                                "bytes": len(packed), "pixel_sha256": sha(packed),
                                "loose_file": path, "dimensions": dimensions,
                                "bits_per_pixel": bits_per_pixel,
                                "clean_and_current_loose_and_raw_identical": data == current.read_file(path)
                                and source == current.read_file(f"/GRP/{family}.DK4"),
                                "palette_identity_not_inferred_from_pixel_match": True})
        elif path.lower().endswith(".fls"):
            archive = FlsArchive(data)
            for index in range(archive.count):
                texture = archive.texture(index)
                row = {"file": path, "texture": index, "compressed_storage": archive.compressed_storage,
                       "dimensions": [texture.width, texture.height], "complete_indices_sha256": sha(texture.indices)}
                fls_rows.append(row)
                if not archive.compressed_storage:
                    assert archive.to_bytes() == data
                    assert data == current.read_file(path)
                    preview = ROOT / "raw_harbor_full_reader.png"
                    texture.render().save(preview)
                    raw_rows.append({**row, "header_compression_bit_clear": True,
                                     "source_file_sha256": sha(data), "raw_roundtrip_exact": True,
                                     "visible_height_field": archive.records[index][1] & 65535,
                                     "preview": preview.as_posix(), "preview_sha256": sha(preview.read_bytes()),
                                     "source_art_review": "harbor/coastal buildings, sea and birds; no readable Japanese caption",
                                     "native_final_loading_crop_and_projection_not_proved": True})
    reproduction = ROOT / "v218_reader_reproduction.nds"
    expected = "be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f"
    assert sha(reproduction.read_bytes()) == expected == sha(current.source.read_bytes())
    assert len(matches) == 4 and len(fls_rows) == 261 and len(raw_rows) == 1
    report = {"format": "dk4-raw-copy-and-full-fls-decode-audit-v1", "ROM_sha256": expected,
              "loose_PXL_pixel_payloads_checked": pxl_count, "direct_color_PXL_rows": direct_color_rows,
              "indexed_PXL_decoded": pxl_count - len(direct_color_rows), "exact_payload_matches": matches,
              "FLS_textures_decoded": len(fls_rows), "FLS_decode_errors": 0,
              "FLS_texture_rows": fls_rows, "raw_FLS_records": raw_rows,
              "full_prior_ROM_reproduction_after_reader_change_exact": True,
              "OCINIT_ship_anchors_and_row_repack_are_partial_not_full_copy_proof": True,
              "native_raw_palette_consumer_and_display_mapping_pending": True,
              "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "saved_audit.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"PXL_images": pxl_count, "exact_raw_copies": len(matches), "FLS_textures": len(fls_rows),
                      "decode_errors": 0, "raw_roundtrip": True, "V218_reproduction_exact": True}))


if __name__ == "__main__":
    main()
