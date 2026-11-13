"""Find exact loose-image payloads inside unresolved canonical graphics blocks."""

import hashlib
import json
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
CANDIDATE = Path("out/all_routes_combined_v189_candidate.nds")
OUT = Path("work/analysis/raw_embedded_matches_v190.json")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    assert sha(BASE.read_bytes()) == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    assert sha(CANDIDATE.read_bytes()) == "0361d5ab8d08b2493c1dfd1bb495b1ffbe42126da51b4296771582c0ceae1e74"
    original, candidate = NdsImage.open(BASE), NdsImage.open(CANDIDATE)
    inventory = json.loads(Path("work/analysis/embedded_graphics_v151/inventory.json").read_text())
    blocks = []
    for row in inventory["blocks"]:
        if row["format_status"] != "unclassified-no-preview":
            continue
        path, index = row["path"], row["block_index"]
        raw = IlnkContainer.parse(original.read_file(path)).blocks[index]
        assert sha(raw) == row["block_sha256"]
        saved = IlnkContainer.parse(candidate.read_file(path)).blocks[index]
        blocks.append((path, index, raw, saved))
    images = []
    depth_counts = {}
    for path in rom_files(original):
        if not path.lower().endswith(".pxl"):
            continue
        data = original.read_file(path)
        depth, _width, _height, _palette, offset = struct.unpack_from("<5I", data)
        bits = depth & 255
        depth_counts[bits] = depth_counts.get(bits, 0) + 1
        modes = [("packed-native-pixels", data[offset:])]
        if bits == 4:
            modes.append(("unpacked-4bit-indices", bytes(PxlImage.from_bytes(data).indices)))
        for mode, payload in modes:
            if len(payload) < 1024 or len(set(payload)) < 4:
                continue
            images.append((path, mode, payload, offset, data))
    matches = []
    for path, index, raw, saved in blocks:
        for loose_path, mode, payload, loose_offset, data in images:
            start = raw.find(payload)
            while start >= 0:
                loose_saved = candidate.read_file(loose_path)
                if mode == "unpacked-4bit-indices":
                    current = bytes(PxlImage.from_bytes(loose_saved).indices)
                else:
                    current = loose_saved[loose_offset:]
                matches.append({
                    "archive_path": path,
                    "block_index": index,
                    "source_block_sha256": sha(raw),
                    "offset": start,
                    "bytes": len(payload),
                    "loose_path": loose_path,
                    "mode": mode,
                    "source_loose_sha256": sha(data),
                    "source_payload_sha256": sha(payload),
                    "candidate_loose_changed": current != payload,
                    "candidate_embedded_region_matches_current_loose": saved[start : start + len(payload)] == current,
                    "native_palette_or_usage_proved": False,
                })
                start = raw.find(payload, start + 1)
    result = {
        "status": "complete-bounded-payload-search",
        "canonical_base_sha256": sha(BASE.read_bytes()),
        "candidate_sha256": sha(CANDIDATE.read_bytes()),
        "unclassified_inventory_blocks_searched": len(blocks),
        "loose_PXL_depth_counts": depth_counts,
        "search_payloads": len(images),
        "minimum_payload_bytes": 1024,
        "minimum_distinct_byte_values": 4,
        "matches": matches,
        "limitations": [
            "Exact contiguous payload matching only; absent matches do not classify a block.",
            "Different dimensions, resampling, palette remapping and compressed/tiled copies may not match.",
            "Matching indexed bytes do not prove palette, native usage, alpha or display.",
        ],
        "rom_changed": False,
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
