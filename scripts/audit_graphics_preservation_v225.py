"""Check original dimensions, formats and palettes across every PXL/FLS entry."""

import json
import struct
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/graphics_preservation_v225")


def main():
    clean = NdsImage.open("work/clean.nds")
    current = NdsImage.open("out/all_routes_combined_v218_candidate.nds")
    current_files = {p: bytes(v) for _, p, v in current.iter_files()}
    entries = []
    for _, path, source in clean.iter_files():
        saved = current_files[path]
        if path.lower().endswith(".pxl"):
            left, right = struct.unpack_from("<5I", source), struct.unpack_from("<5I", saved)
            assert left[:3] == right[:3], path
            depth = left[0] & 255
            palette_bytes = 32 if depth == 4 else 512 if depth == 8 else 0
            assert source[left[3]:left[3] + palette_bytes] == saved[right[3]:right[3] + palette_bytes], path
            assert len(source) - left[4] == len(saved) - right[4], path
            entries.append({"file": path, "kind": "PXL", "flags_pitch_height_preserved": True,
                            "palette_preserved": True, "complete_payload_extent_preserved": True,
                            "changed": source != saved})
        elif path.lower().endswith(".fls"):
            left, right = FlsArchive(source), FlsArchive(saved)
            assert left.count == right.count and left.compressed_storage == right.compressed_storage, path
            for index in range(left.count):
                a, b = left.texture(index), right.texture(index)
                assert (a.flags, a.width, a.height) == (b.flags, b.width, b.height), (path, index)
                assert a.palette == b.palette and len(a.indices) == len(b.indices), (path, index)
                entries.append({"file": path, "texture": index, "kind": "FLS", "flags_dimensions_preserved": True,
                                "palette_preserved": True, "complete_payload_extent_preserved": True,
                                "changed": a.indices != b.indices})
    assert len(entries) == 921
    ROOT.mkdir(parents=True, exist_ok=True)
    report = {"format": "dk4-complete-graphics-preservation-proof-v1",
              "candidate": str(current.source), "candidate_sha256": sha(current.source.read_bytes()),
              "clean_source_sha256": sha(clean.source.read_bytes()), "entries": entries,
              "PXL_entries": sum(x["kind"] == "PXL" for x in entries),
              "FLS_entries": sum(x["kind"] == "FLS" for x in entries),
              "changed_entries": sum(x["changed"] for x in entries),
              "all_original_dimensions_formats_flags_palettes_and_payload_extents_preserved": True,
              "border_text_pixels_native_crops_alpha_and_translation_completion_not_inferred": True,
              "full_goal_complete": False}
    (ROOT / "whole_asset_proof.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"PXL": report["PXL_entries"], "FLS": report["FLS_entries"],
                      "changed_graphics": report["changed_entries"], "all_preservation_invariants_pass": True}))


if __name__ == "__main__":
    main()
