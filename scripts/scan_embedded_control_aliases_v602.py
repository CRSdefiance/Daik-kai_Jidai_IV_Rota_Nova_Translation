"""Decode bounded legacy packets before searching for copied control artwork."""

import json
import struct
from collections import Counter
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_embedded_graphics_v151 import decode
from scripts.inventory_external_palette_graphics_v151 import PAIRS
from scripts.scan_graphic_template_aliases_v602 import (
    ROOT,
    TEMPLATES,
    colors,
    domains,
    find_matches,
    rows,
)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def packets(raw):
    offset = 0
    while offset + 12 <= len(raw):
        item = decode(raw[offset:])
        if item is None:
            break
        size = 16 if item["depth"] == 4 else 256
        for bank in range(item["palette_banks"]):
            palette = struct.unpack_from(f"<{size}H", item["palette"], bank * size * 2)
            yield {"offset": offset, "bank": bank, "width": item["width"], "height": item["height"],
                   "indices": item["indices"], "palette": palette,
                   "packet_end": offset + item["pixels_offset"] + item["pixels_bytes"]}
        offset += item["pixels_offset"] + item["pixels_bytes"]


def search_domain(d, revised, path, block_number, templates, seen, *, palette_block=None):
    matches = []
    for bits in (16, 15, 0):
        if bits == 0 and d["bank"] != 0:
            continue
        mask = (1 << bits) - 1
        palette = tuple(word & mask for word in d["palette"]) if bits else tuple(range(len(d["palette"])))
        candidates = [t for t in templates if t["bits"] == bits and t["width"] <= d["width"]
                      and t["height"] <= d["height"] and t["colors"] <= set(palette)]
        if not candidates:
            continue
        table = [struct.pack("<H", word) for word in palette]
        data = b"".join(table[i] for i in d["indices"])
        target = b"".join(table[i] for i in revised["indices"])
        for template in candidates:
            for box in find_matches(data, d["width"], d["height"], template):
                key = (template["name"], path, block_number, d["offset"], d["bank"], tuple(box))
                if key in seen:
                    continue
                seen.add(key)
                before, after = rows(data, d["width"], box), rows(target, d["width"], box)
                changed = sum(a != b for x, y in zip(before, after, strict=True)
                              for (a,), (b,) in zip(struct.iter_unpack("<H", x), struct.iter_unpack("<H", y), strict=True))
                matches.append({"template": template["name"], "path": path, "block": block_number,
                    "packet_offset": d["offset"], "palette_bank": d["bank"], "box": box,
                    "compared_bits": bits, "full16_bit_storage_words_exact": bits == 16,
                    "exact_palette_indices_only_not_color_or_alpha_equivalence": bits == 0,
                    "external_palette_block_storage_pair": palette_block,
                    "current_changed_pixel_words_under_same_mask": changed,
                    "native_loading_alpha_or_shared_consumer_not_inferred": True})
    return matches


def external_pair(archive, palette_block, pixels_block):
    palette, pixels = archive.blocks[palette_block], archive.blocks[pixels_block]
    pk, pm, extent, _, colors_per_bank, banks = struct.unpack_from("<IIIIHH", palette)
    ik, im, size, _, words, height = struct.unpack_from("<IIIIHH", pixels)
    assert (pk, pm, colors_per_bank) == (19, 2, 16) and len(palette) == extent + 8 == 20 + banks * 32
    assert (ik, im) == (18, 0) and len(pixels) == size + 8 == 20 + words * 2 * height
    indices = bytes(n for value in pixels[20:] for n in (value & 15, value >> 4))
    assert bytes(indices[i] | indices[i + 1] << 4 for i in range(0, len(indices), 2)) == pixels[20:]
    for bank in range(banks):
        yield {"offset": 20, "bank": bank, "width": words * 4, "height": height, "indices": indices,
               "palette": struct.unpack_from("<16H", palette, 20 + bank * 32)}


def main():
    loose_proof_path = ROOT / "decoded_template_alias_proof.json"
    loose = read(loose_proof_path)
    assert loose["script_sha256"] == sha(Path("scripts/scan_graphic_template_aliases_v602.py").read_bytes())
    source, current = NdsImage.open("work/clean.nds"), NdsImage.open(loose["candidate"])
    assert sha(current.source.read_bytes()) == loose["candidate_sha256"]
    templates = []
    for name, path, box in TEMPLATES:
        domain = next(domains(path, source.read_file(path)))
        original_rows = rows(colors(domain), domain["width"], box)
        for bits in (16, 15):
            mask = (1 << bits) - 1
            sample = [b"".join(struct.pack("<H", word & mask) for word, in struct.iter_unpack("<H", row))
                      for row in original_rows]
            templates.append({"name": name, "bits": bits, "rows": sample,
                "width": box[2] - box[0], "height": box[3] - box[1],
                "anchor": max(range(len(sample)), key=lambda y: len(set(struct.iter_unpack("<H", sample[y])))),
                "colors": {word for row in sample for word, in struct.iter_unpack("<H", row)}})
        sample = rows(b"".join(struct.pack("<H", index) for index in domain["indices"]), domain["width"], box)
        templates.append({"name": name, "bits": 0, "rows": sample,
            "width": box[2] - box[0], "height": box[3] - box[1],
            "anchor": max(range(len(sample)), key=lambda y: len(set(struct.iter_unpack("<H", sample[y])))),
            "colors": {word for row in sample for word, in struct.iter_unpack("<H", row)}})
    census = read("work/analysis/embedded_storage_census_v192.json")
    stats, blocks, matches, seen = Counter(), [], [], set()
    for path in sorted({r["path"] for r in census["blocks"]}):
        original_archive, revised_archive = [IlnkContainer.parse(rom.read_file(path)) for rom in (source, current)]
        for block_number, raw in enumerate(original_archive.blocks):
            stats["embedded_blocks_visited"] += 1
            decoded = list(packets(raw))
            revised_packets = list(packets(revised_archive.blocks[block_number]))
            assert [(d["offset"], d["bank"], d["width"], d["height"], d["palette"])
                    for d in decoded] == [(d["offset"], d["bank"], d["width"], d["height"], d["palette"])
                    for d in revised_packets]
            covered_end = max((d["packet_end"] for d in decoded), default=0)
            blocks.append({"path": path, "block": block_number, "source_sha256": sha(raw),
                "source_bytes": len(raw), "decoded_palette_domains": len(decoded),
                "decoded_packet_offsets": sorted({d["offset"] for d in decoded}),
                "bytes_not_interpreted_after_last_packet": len(raw) - covered_end,
                "not_classified_as_unused_when_no_packet_decoder_applies": True})
            stats["bounded_legacy_packets"] += len({d["offset"] for d in decoded})
            stats["decoded_palette_domains"] += len(decoded)
            for d, revised in zip(decoded, revised_packets, strict=True):
                matches += search_domain(d, revised, path, block_number, templates, seen)
    pair_reports = []
    for path, palette_block, pixels_block in PAIRS:
        a, b = [IlnkContainer.parse(rom.read_file(path)) for rom in (source, current)]
        old, new = list(external_pair(a, palette_block, pixels_block)), list(external_pair(b, palette_block, pixels_block))
        assert len(old) == len(new)
        for d, revised in zip(old, new, strict=True):
            assert d["palette"] == revised["palette"]
            matches += search_domain(d, revised, path, pixels_block, templates, seen, palette_block=palette_block)
        stats["bounded_external_palette_storage_pairs"] += 1
        stats["external_palette_domains"] += len(old)
        pair_reports.append({"path": path, "palette_block": palette_block, "pixels_block": pixels_block,
            "width": old[0]["width"], "height": old[0]["height"], "palette_domains": len(old),
            "original_header_extents_and_index_repacking_exact": True,
            "storage_pairing_not_native_loading_or_alpha_evidence": True})
    assert stats["embedded_blocks_visited"] == 57
    save(ROOT / "embedded_control_alias_proof.json", {"candidate": str(current.source),
        "candidate_sha256": sha(current.source.read_bytes()), "loose_template_proof": str(loose_proof_path),
        "loose_template_proof_sha256": sha(loose_proof_path.read_bytes()), "stats": dict(stats),
        "blocks": blocks, "matches": matches,
        "bounded_external_palette_storage_pairs": pair_reports,
        "full_word_pass_before_lower15_storage_color_pass": True,
        "lower15_matching_does_not_prove_alpha_flags_or_shared_native_users": True,
        "unparsed_custom_headerless_blocks_or_tail_bytes_remain_outside_this_decoder": True,
        "production_ROM_or_patch_changed": False, "full_goal_complete": False,
        "decoder_script_sha256": sha(Path("scripts/inventory_embedded_graphics_v151.py").read_bytes()),
        "script_sha256": sha(Path(__file__).read_bytes())})
    print(json.dumps({"stats": dict(stats), "matches": matches}, indent=2))


if __name__ == "__main__":
    main()
