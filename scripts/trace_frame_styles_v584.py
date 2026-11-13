"""Find literal source styles passed through original shared frame wrappers."""

import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.trace_frame_crop_arguments_v584 import abstract_block, branch, transfer

ROOT = Path("work/analysis/frame_callers_v584")
TARGETS = {0x020D0AC4: "direct_tiled_border", 0x020D0A40: "default_frame",
           0x020D0A64: "frame_style", 0x020D0A84: "strip_style", 0x020D0AA4: "tile_style"}


def main():
    rom = NdsImage.open("out/all_routes_combined_v581_candidate.nds")
    arm = rom.read_file("/__arm9__.bin")
    u = machine(arm)
    sections = [(s.ramAddress, bytes(s.data)) for s in MainCodeFile(arm, 0x02000000).sections]
    sections += [(o.ramAddress, bytes(o.data)) for o in loadOverlayTable(
        rom.rom.arm9OverlayTable, lambda _id, file_id: rom.rom.files[file_id]).values()]
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    decoder.skipdata = True
    cells = [("Pick Cargo", (208, 32, 256, 40)), ("Pick Ship", (208, 40, 240, 48)),
             ("Done", (240, 40, 256, 48)), ("Rank", (184, 48, 208, 56)), ("Cancel", (208, 48, 256, 56))]
    records = []
    for base, data in sections:
        for at in range(0, len(data) - 3, 4):
            word = struct.unpack_from("<I", data, at)[0]
            target = branch(word, base + at)
            if word & 0x0F000000 != 0x0B000000 or target not in TARGETS:
                continue
            start = max(0, at - 200)
            for offset in range(start, at, 4):
                if transfer(struct.unpack_from("<I", data, offset)[0]):
                    start = offset + 4
            registers, _ = abstract_block(decoder, data, base, start, at)
            pointer = (0x0213BEB0 if target == 0x020D0A40 else
                       registers.get("r1") if target == 0x020D0AC4 else registers.get("r2"))
            row = {"call": base + at, "target": target, "kind": TARGETS[target],
                   "style_pointer": pointer, "block_start": base + start,
                   "block_sha256": sha(data[start:at + 4])}
            if pointer is not None and 0x02110000 <= pointer < 0x02180000:
                words = struct.unpack("<4I" if target == 0x020D0AC4 else "<5I",
                                      u.mem_read(pointer, 16 if target == 0x020D0AC4 else 20))
                tile = words if target == 0x020D0AC4 else words[1:]
                x, y, width, height = tile
                row["literal_words"] = words
                row["valid_original_atlas_tile"] = 0 < width <= 256 and 0 < height <= 256 and x + width <= 256 and y + height <= 256
                if row["valid_original_atlas_tile"]:
                    row["first_source_tile_XYWH"] = tile
                    row["first_tile_intersecting_caption_cells"] = [name for name, (l, t, r, b) in cells
                                                                    if x < r and y < b and x + width > l and y + height > t]
            records.append(row)
    result = {"candidate_sha256": sha(rom.source.read_bytes()), "direct_style_call_sites": records,
              "literal_style_sources_not_ordinary_native_parent_credit": True,
              "computed_style_pointers_and_indirect_calls_remain_unresolved": True,
              "source_XYWH_contract": "native_blitter_contract_proof.json", "ROM_changed": False}
    (ROOT / "literal_style_callers.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print({"style_call_sites": len(records), "resolved_literal_tiles": sum(r.get("valid_original_atlas_tile", False) for r in records),
           "unresolved": [hex(r["call"]) for r in records if not r.get("valid_original_atlas_tile")],
           "first_tile_caption_intersections": [r for r in records if r.get("first_tile_intersecting_caption_cells")]})


if __name__ == "__main__":
    main()
