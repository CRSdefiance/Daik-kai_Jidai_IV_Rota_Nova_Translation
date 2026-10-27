"""Check current pixel edits against registered ownership and the accepted baseline."""

import json
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/graphics_ownership_v226")


def image(rom, path, index):
    data = rom.read_file(path)
    return PxlImage.from_bytes(data) if index is None else FlsArchive(data).texture(index)


def main():
    stack = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))
    names = list(dict.fromkeys([r["batch"] for r in stack["accepted_layers"]]
                              + stack["profiles"]["all-routes-unified-v218"]["batches"]))
    canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    current = NdsImage.open("out/all_routes_combined_v218_candidate.nds")
    clean = NdsImage.open("work/clean.nds")
    regions = {}
    for name in names:
        batch = json.loads(Path(name).read_text(encoding="utf-8"))
        path = batch.get("file_path", "")
        if not path.lower().endswith((".pxl", ".fls")):
            continue
        for row in batch.get("records", []):
            if not isinstance(row, dict):
                continue
            key = path, row.get("asset_index")
            if "box" in row:
                boxes = [row["box"]]
                if row.get("draw_box"):
                    boxes.append(row["draw_box"])
            elif batch.get("format") == "dk4-fls-label-batch-v1":
                # This registered writer clears/replaces the full subtitle sprite.
                entry = image(canonical, *key)
                boxes = [[0, 0, entry.width, entry.height]]
            else:
                continue
            regions.setdefault(key, []).append({"batch": name, "id": row.get("id"), "boxes": boxes})
    cases = []
    inherited_outside_total = 0
    for (path, index), owners in regions.items():
        original, baseline, saved = [image(r, path, index) for r in (clean, canonical, current)]
        width, height = saved.width, saved.height
        assert (original.width, original.height) == (baseline.width, baseline.height) == (width, height)
        owned = set()
        for owner in owners:
            for x0, y0, x1, y1 in owner["boxes"]:
                assert 0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height
                for y in range(y0, y1):
                    owned.update(range(y * width + x0, y * width + x1))
        new_changes = {i for i, (a, b) in enumerate(zip(baseline.indices, saved.indices)) if a != b}
        assert not new_changes - owned, (path, index, len(new_changes - owned))
        inherited_outside = {i for i, (a, b) in enumerate(zip(original.indices, saved.indices))
                             if a != b and i not in owned}
        assert all(baseline.indices[i] == saved.indices[i] for i in inherited_outside)
        inherited_outside_total += len(inherited_outside)
        cases.append({"file": path, "texture": index, "dimensions": [width, height],
                      "registered_owners": owners, "new_changes_from_canonical": len(new_changes),
                      "new_pixels_outside_registered_regions": 0,
                      "inherited_accepted_pixels_outside_regions_unchanged": len(inherited_outside),
                      "all_pixels_outside_new_owned_regions_match_accepted_baseline": True})
    ROOT.mkdir(parents=True, exist_ok=True)
    report = {"format": "dk4-registered-graphics-pixel-ownership-proof-v1",
              "candidate_sha256": sha(current.source.read_bytes()), "canonical_sha256": sha(canonical.source.read_bytes()),
              "release_stack_sha256": sha(Path("translations/release_stack.json").read_bytes()), "cases": cases,
              "registered_graphic_entries_checked": len(cases), "new_out_of_scope_pixel_changes": 0,
              "inherited_accepted_pixels_preserved_outside_regions": inherited_outside_total,
              "owned_region_is_not_itself_border_or_readability_proof": True,
              "embedded_raw_banks_native_crops_alpha_and_translation_completion_remain_separate": True,
              "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "ownership_proof.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"registered_graphic_entries": len(cases), "new_out_of_scope_pixels": 0,
                      "inherited_accepted_pixels_preserved": inherited_outside_total}))


if __name__ == "__main__":
    main()
