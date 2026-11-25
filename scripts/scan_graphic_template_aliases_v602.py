"""Find exact decoded control crops across original PXL/FLS image strides and palettes."""

import json
import struct
from collections import Counter
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.compression_probe import decompress_lz10

ROOT = Path("work/analysis/graphics_aliases_v602")
TEMPLATES = (
    ("Confirm_full", "/_pxl/kakutei.pxl", (0, 0, 48, 20)),
    ("Confirm_face", "/_pxl/kakutei.pxl", (4, 3, 43, 17)),
    ("Pick_Cargo", "/_pxl/__frame.pxl", (208, 32, 256, 40)),
    ("Pick_Ship", "/_pxl/__frame.pxl", (208, 40, 240, 48)),
    ("Done", "/_pxl/__frame.pxl", (240, 40, 256, 48)),
    ("Rank", "/_pxl/__frame.pxl", (184, 48, 208, 56)),
    ("Cancel", "/_pxl/__frame.pxl", (208, 48, 256, 56)),
)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def domains(path, source):
    if path.lower().endswith(".pxl"):
        depth, width_words, height, palette_at, pixels_at = struct.unpack_from("<5I", source)
        depth &= 255
        if depth == 16:
            assert len(source) - pixels_at == width_words * height * 2
            yield {"kind": "PXL", "texture": None, "bank": None, "width": width_words, "height": height,
                   "direct_color": source[pixels_at:], "indices": None, "palette": None}
            return
        image = PxlImage.from_bytes(source)
        size = 16 if depth == 4 else 256
        assert (pixels_at - palette_at) % (size * 2) == 0
        for bank in range((pixels_at - palette_at) // (size * 2)):
            palette = struct.unpack_from(f"<{size}H", source, palette_at + bank * size * 2)
            yield {"kind": "PXL", "texture": None, "bank": bank, "width": image.width, "height": height,
                   "direct_color": None, "indices": image.indices, "palette": palette}
    elif path.lower().endswith(".fls"):
        archive = FlsArchive(source)
        for index in range(archive.count):
            image = archive.texture(index)
            offset, extent = archive.records[index][2:4]
            palette_data = (decompress_lz10(source[archive.data_offset + offset:]) if archive.compressed_storage
                            else source[archive.data_offset + offset:archive.data_offset + offset + extent])
            palette = struct.unpack(f"<{len(image.palette)}H", palette_data)
            yield {"kind": "FLS", "texture": index, "bank": 0, "width": image.width, "height": image.height,
                   "direct_color": None, "indices": image.indices, "palette": palette}


def colors(domain):
    if domain["direct_color"] is not None:
        return domain["direct_color"]
    table = [struct.pack("<H", value) for value in domain["palette"]]
    return b"".join(table[index] for index in domain["indices"])


def rows(data, width, box):
    left, top, right, bottom = box
    return [data[((top + y) * width + left) * 2:((top + y) * width + right) * 2] for y in range(bottom - top)]


def find_matches(data, width, height, template):
    offset = 0
    needle = template["rows"][template["anchor"]]
    while (offset := data.find(needle, offset)) >= 0:
        position = offset // 2
        x, y = position % width, position // width - template["anchor"]
        box = [x, y, x + template["width"], y + template["height"]]
        if (offset % 2 == 0 and box[2] <= width and 0 <= y and box[3] <= height
                and rows(data, width, box) == template["rows"]):
            yield box
        offset += 1


def synthetic_controls(original, template):
    source = PxlImage.from_bytes(original.read_file("/_pxl/kakutei.pxl"))
    old_palette = struct.unpack_from("<16H", source.source, 20)
    permutation = list(reversed(range(16)))
    palette = [old_palette[i] for i in permutation]
    mapping = {old: new for new, old in enumerate(permutation)}
    width, height, left, top = 128, 40, 17, 9
    indices = bytearray([mapping[14]]) * (width * height)
    sl, st, sr, sb = template["source_box"]
    for y in range(sb - st):
        for x in range(sr - sl):
            indices[(top + y) * width + left + x] = mapping[source.indices[(st + y) * 48 + sl + x]]

    def encoded(values):
        prefix = struct.pack("<5I", 4, width // 4, height, 20, 84)
        palette_bytes = struct.pack("<16H", *([0xFFFF] * 16)) + struct.pack("<16H", *palette)
        packed = bytes(values[i] | values[i + 1] << 4 for i in range(0, len(values), 2))
        return prefix + palette_bytes + packed

    raw = encoded(indices)
    decoded = list(domains("synthetic.pxl", raw))
    expected_box = [left, top, left + template["width"], top + template["height"]]
    assert list(find_matches(colors(decoded[0]), width, height, template)) == []
    assert list(find_matches(colors(decoded[1]), width, height, template)) == [expected_box]
    # Keep the anchor row intact; a changed Japanese face point on another row
    # must be rejected by complete-row verification, not just by the anchor.
    point = next((x, y) for y in range(template["height"]) if y != template["anchor"]
                 for x in range(template["width"]) if source.indices[(st + y) * 48 + sl + x] == 13)
    changed = bytearray(indices)
    changed[(top + point[1]) * width + left + point[0]] = mapping[0]
    negative = list(domains("synthetic.pxl", encoded(changed)))[1]
    assert rows(colors(decoded[1]), width, expected_box)[template["anchor"]] == rows(colors(negative), width, expected_box)[template["anchor"]]
    assert list(find_matches(colors(negative), width, height, template)) == []
    return {"synthetic_only_not_ROM_artwork": True, "different_source_destination_strides": [48, width],
        "odd_nibble_destination_x": left, "reordered_palette_and_nonzero_bank": 1,
        "complete_crop_found_once": expected_box, "wrong_palette_bank_rejected": True,
        "single_Japanese_ink_point_change_outside_anchor_rejected": list(point),
        "positive_encoded_sha256": sha(raw), "negative_encoded_sha256": sha(encoded(changed))}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    original, current = NdsImage.open("work/clean.nds"), NdsImage.open("out/all_routes_combined_v599_candidate.nds")
    templates = []
    for name, path, box in TEMPLATES:
        domain = next(domains(path, original.read_file(path)))
        sample = rows(colors(domain), domain["width"], box)
        indexed = b"".join(struct.pack("<H", index) for index in domain["indices"])
        indexed_rows = rows(indexed, domain["width"], box)
        anchor = max(range(len(sample)), key=lambda y: len(set(struct.iter_unpack("<H", sample[y]))))
        templates.append({"name": name, "source_path": path, "source_box": list(box), "rows": sample,
            "anchor": anchor, "width": box[2] - box[0], "height": box[3] - box[1],
            "index_rows": indexed_rows,
            "colors": {value for row in sample for value, in struct.iter_unpack("<H", row)}})
    stats, matches, sources = Counter(), [], []
    controls = synthetic_controls(original, next(t for t in templates if t["name"] == "Confirm_face"))
    for _, path, source in original.iter_files():
        if not path.lower().endswith((".pxl", ".fls")):
            continue
        source_domains = list(domains(path, source))
        current_domains = None
        stats["PXL_files" if path.lower().endswith(".pxl") else "FLS_files"] += 1
        stats["FLS_textures"] += len(source_domains) if path.lower().endswith(".fls") else 0
        sources.append({"path": path, "source_file_sha256": sha(source), "decoded_domains": len(source_domains)})
        for number, domain in enumerate(source_domains):
            stats["decoded_domains"] += 1
            needed = [t for t in templates if t["width"] <= domain["width"] and t["height"] <= domain["height"]
                      and (domain["palette"] is None or t["colors"] <= set(domain["palette"]))]
            if not needed:
                stats["domains_rejected_by_dimensions_or_palette_colors"] += 1
                continue
            data = colors(domain)
            stats["domains_with_template_color_coverage"] += 1
            for template in needed:
                stats["anchor_candidates"] += data.count(template["rows"][template["anchor"]])
                for box in find_matches(data, domain["width"], domain["height"], template):
                    if current_domains is None:
                        current_domains = list(domains(path, current.read_file(path)))
                    current_data = colors(current_domains[number])
                    revised = rows(current_data, domain["width"], box)
                    changed = sum(a != b for row, revised_row in zip(template["rows"], revised, strict=True)
                                  for (a,), (b,) in zip(struct.iter_unpack("<H", row), struct.iter_unpack("<H", revised_row), strict=True))
                    matches.append({"template": template["name"], "path": path, "kind": domain["kind"],
                        "texture": domain["texture"], "palette_bank": domain["bank"], "box": box,
                        "exact_source_BGR555_words_including_bit15": True, "current_changed_pixel_words": changed,
                        "same_declared_source_crop": path == template["source_path"] and box == template["source_box"]})
        # A legacy copy can preserve glyph indices while using a different
        # palette. Search the pixel shape once per physical texture as well.
        physical = set()
        for number, domain in enumerate(source_domains):
            if domain["indices"] is None or domain["texture"] in physical:
                continue
            physical.add(domain["texture"])
            stats["distinct_indexed_textures_shape_searched"] += 1
            data = b"".join(struct.pack("<H", index) for index in domain["indices"])
            for template in templates:
                if template["width"] > domain["width"] or template["height"] > domain["height"]:
                    continue
                sample = dict(template, rows=template["index_rows"])
                sample["anchor"] = max(range(len(sample["rows"])), key=lambda y: len(set(struct.iter_unpack("<H", sample["rows"][y]))))
                for box in find_matches(data, domain["width"], domain["height"], sample):
                    if any(m["template"] == template["name"] and m["path"] == path and m["texture"] == domain["texture"]
                           and m["box"] == box for m in matches):
                        continue
                    if current_domains is None:
                        current_domains = list(domains(path, current.read_file(path)))
                    revised = b"".join(struct.pack("<H", index) for index in current_domains[number]["indices"])
                    a, b = rows(data, domain["width"], box), rows(revised, domain["width"], box)
                    changed = sum(x != y for old, new in zip(a, b, strict=True)
                                  for (x,), (y,) in zip(struct.iter_unpack("<H", old), struct.iter_unpack("<H", new), strict=True))
                    matches.append({"template": template["name"], "path": path, "kind": domain["kind"],
                        "texture": domain["texture"], "palette_bank": None, "box": box,
                        "exact_source_BGR555_words_including_bit15": False,
                        "exact_palette_indices_only_not_color_or_alpha_equivalence": True,
                        "current_changed_pixel_words": changed,
                        "same_declared_source_crop": path == template["source_path"] and box == template["source_box"]})
    assert stats["PXL_files"] == 660 and stats["FLS_textures"] == 261
    assert all(any(m["template"] == name and m["same_declared_source_crop"] for m in matches) for name, _, _ in TEMPLATES)
    grouped = {(m["template"], m["path"], m["texture"], tuple(m["box"])) for m in matches}
    foreign = [m for m in matches if not m["same_declared_source_crop"]]
    save(ROOT / "decoded_template_alias_proof.json", {"candidate": str(current.source),
        "candidate_sha256": sha(current.source.read_bytes()), "clean_ROM_sha256": sha(original.source.read_bytes()),
        "stats": dict(stats), "source_files": sources, "templates": [{k: v for k, v in t.items() if k not in ("rows", "colors", "index_rows")}
            for t in templates], "matches": matches, "distinct_rectangles_ignoring_duplicate_palette_banks": len(grouped),
        "matches_outside_declared_crops": foreign, "all7_original_self_controls_found": True,
        "unequal_stride_odd_nibble_palette_reordering_and_negative_controls": controls,
        "packed_file_contiguity_not_assumed_decoded_row_strides_checked": True,
        "limits": "Exact same-size decoded BGR555-plus-flag crops plus unchanged indexed shapes. Palette-permuted recolorings without matching colors, rescaled/partial copies, arbitrary runtime composition and legacy custom archive images are not excluded.",
        "ordinary_parent_or_global_nonuse_inferred": False, "production_ROM_or_patch_changed": False,
        "full_goal_complete": False, "script_sha256": sha(Path(__file__).read_bytes())})
    print({"stats": dict(stats), "matches": len(matches), "distinct_rectangles": len(grouped), "outside_declared_crops": foreign})


if __name__ == "__main__":
    main()
