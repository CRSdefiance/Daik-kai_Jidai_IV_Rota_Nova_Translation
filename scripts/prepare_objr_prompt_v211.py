"""Source-lock the embedded START prompt to the already accepted English PXL."""

import copy
import json
from pathlib import Path

from PIL import Image

from dk4tool.graphics.obj_banked_sync import apply_banked_sync
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/objr_prompt_v211")
BATCH = Path("translations/objr_start_prompt_embedded_sync_v1.json")


def decode(data):
    assert len(data) == 4096
    indices = bytearray(256 * 32)
    for tile in range(128):
        for p, value in enumerate(data[tile * 32:(tile + 1) * 32]):
            x = tile // 32 * 64 + tile % 8 * 8 + p % 4 * 2
            y = tile % 32 // 8 * 8 + p // 4
            indices[y * 256 + x] = value & 15
            indices[y * 256 + x + 1] = value >> 4
    return bytes(indices)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    base = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    prior = NdsImage.open("out/all_routes_combined_v205_candidate.nds")
    assert sha(prior.source.read_bytes()) == "88444cb34139aada935f81b39b478fa81b5f54a32ef7c88a7e08b2b3dfe1dfa0"
    path = "/GRP/DSOBJR.DK4"
    raw = base.read_file(path)
    assert raw == prior.read_file(path) == NdsImage.open("work/clean.nds").read_file(path)
    assert len(raw) == 10016 and sha(raw) == "516bda02bf8e3dc6a5e4b5c721f5776f005d56ad0b721bc91ad4bcb0894f995d"
    reference_path = "/_pxl/title/title02.pxl"
    reference = base.read_file(reference_path)
    assert reference == prior.read_file(reference_path)
    image = PxlImage.from_bytes(reference)
    assert (image.width, image.height, image.bits_per_pixel) == (256, 29, 4)
    assert set(image.indices) == {0, 15}
    batch = {"format": "dk4-obj-banked-pxl-sync-v1", "file_path": path,
             "source_file_sha256": sha(raw), "source_image_path": reference_path,
             "source_image_sha256": sha(reference), "source_image_extent": [256, 29],
             "target_offset": 0x1720, "target_region_bytes": 4096,
             "source_region_sha256": sha(raw[0x1720:]), "bank_width": 64, "bank_height": 32,
             "bank_count": 4, "blank_index": 0, "allowed_indices": [0, 15],
             "record_id": "DK4_OBJR_EMBEDDED_START_TOUCH_PROMPT_V1", "target_locale": "en-US",
             "source_Japanese": "スタートボタンを押すか、下の画面をタッチしてください",
             "English": "Press START or\ntouch the screen",
             "localization_note": "Reuse the accepted title02 wording/artwork. Both controls remain explicit; screen refers to the DS touch screen. Pad only the three additional native bank rows with transparent index zero.",
             "native_source_extent": [256, 32], "native_layout": "four consecutive 64x32 4bpp banks",
             "preserve_main_sprite_prefix_and_all_palette_bytes": True}
    rebuilt, records = apply_banked_sync(batch, raw, reference)
    assert rebuilt[:0x1720] == raw[:0x1720]
    expected = bytes(image.indices) + bytes(256 * 3)
    assert decode(rebuilt[0x1720:]) == expected
    preview = Image.new("P", (256, 32))
    preview.putpalette([c for color in image.palette for c in color[:3]])
    preview.putdata(expected)
    preview.save(ROOT / "English_embedded_prompt.png")
    original = Image.new("L", (256, 32))
    original.putdata([v * 17 for v in decode(raw[0x1720:])])
    original.save(ROOT / "Japanese_source_indices.png")
    negatives = []
    for key, bad in (("source_file_sha256", "0" * 64), ("source_image_sha256", "0" * 64),
                     ("source_region_sha256", "0" * 64), ("bank_count", 5), ("target_offset", True)):
        test = copy.deepcopy(batch)
        test[key] = bad
        try:
            apply_banked_sync(test, raw, reference)
        except (ValueError, TypeError) as error:
            negatives.append({"field": key, "rejected": True, "reason": str(error)})
        else:
            raise AssertionError(f"Invalid {key} accepted")
    BATCH.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    stack_path = Path("translations/release_stack.json")
    stack = json.loads(stack_path.read_text(encoding="utf-8"))
    profile = copy.deepcopy(stack["profiles"]["all-routes-unified-v205"])
    profile["batches"].append(BATCH.as_posix())
    profile["description"] = "Complete V205 stack plus the source-locked embedded START/touch prompt synchronized from accepted English title02."
    profile["note"] = "Experimental graphics copy synchronization; original loader/main sprite/palette bytes preserved. Native verification pending."
    stack["profiles"]["all-routes-unified-v211"] = profile
    stack_path.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = {"batch": BATCH.as_posix(), "reference_SHA256": sha(reference), "source_SHA256": sha(raw),
              "expected_DSOBJR_SHA256": sha(rebuilt), "records": records,
              "complete_reference_and_padding_indices_exact": True, "protected_prefix_palette_bytes": 5920,
              "native_payload_bytes": 4096, "negative_cases": negatives,
              "profile": "all-routes-unified-v211", "active_batches": len(profile["batches"])}
    (ROOT / "preparation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"active_batches": len(profile["batches"]), "negative_cases_rejected": len(negatives),
                      "copied_source_indices": len(image.indices), "transparent_padding_indices": 768}))


if __name__ == "__main__":
    main()
