"""Complete PC titles, native-sized embedded pixels and exact source ownership."""

import copy
import json
import struct
import zlib
from pathlib import Path

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.build_integrated_release import (
    apply_ilnk_indexed_region_batch,
    apply_pxl_indexed_region_batch,
)
from scripts.porto_title_copies_v176 import (
    PROFILE,
    SPECS,
    apply,
    asset,
    batch_path,
    preservation,
    regions,
    sources,
)


@pytest.fixture(scope="module")
def case():
    base, _ = sources()
    return base, {s["path"]: apply(s, base.read_file(s["path"]))[0] for s in SPECS}


def damage(spec, raw, offset):
    if "block" in spec:
        a = IlnkContainer.parse(raw)
        b = bytearray(a.blocks[0])
        b[544 + offset] ^= 1
        a.blocks[0] = bytes(b)
        return a.to_bytes()
    p = PxlImage.from_bytes(raw)
    p.indices[offset] ^= 1
    return p.to_bytes()


@pytest.mark.parametrize("index", range(3))
def test_full_artwork_source_gold_palette_metadata_and_native_dimensions(case, index):
    _, targets = case
    s = SPECS[index]
    proof = preservation(s, targets[s["path"]])
    w, h, _, _ = asset(s)
    assert (w, h) == ((320, 240) if "block" in s else (256, 192))
    assert proof["original_gold_pixels_exact"] > 100
    assert proof["unowned_scene_header_palette_border_copyright_exact"]
    assert [l["text"] for c in proof["cases"] for l in c["lines"]] == [
        "UNCHARTED",
        "WATERS IV",
        "Porto Estado",
    ]
    assert all(
        c["gold_and_adjacent_bevel_shadow_pixels_preserved"] > 0 or c["kind"] == "caption"
        for c in proof["cases"]
    )


@pytest.mark.parametrize("index", range(3))
@pytest.mark.parametrize("kind", ["main", "caption"])
def test_first_and_last_actual_blue_letter_ink_cannot_drop(case, index, kind):
    _, targets = case
    s = SPECS[index]
    raw = targets[s["path"]]
    w, _, pixels, palette = asset(s, raw)
    _, cases, _ = regions(s["name"])
    proof = next(c for c in cases if c["kind"] == kind)
    for edge in ("first", "last"):
        line = proof["lines"][0 if edge == "first" else -1]
        x0, y0, x1, y1 = line["full_glyph_box"]
        hits = []
        for x in range(x0, x1) if edge == "first" else range(x1 - 1, x0 - 1, -1):
            hits = [
                y * w + x
                for y in range(y0, y1)
                if palette[pixels[y * w + x]][2] > palette[pixels[y * w + x]][0] + 8
                and palette[pixels[y * w + x]][2] > palette[pixels[y * w + x]][1] + 8
            ]
            if hits:
                break
        assert hits
        for offset in hits:
            with pytest.raises(ValueError, match="Complete English artwork"):
                preservation(s, damage(s, raw, offset))


@pytest.mark.parametrize("index", range(3))
def test_unowned_latin_copyright_and_scenery_exact(case, index):
    _, t = case
    s = SPECS[index]
    w, h, _, _ = asset(s)
    for x, y in ((80, 115 if s.get("water") else 87), (10, h - 20), (80, 10)):
        with pytest.raises(ValueError, match="English artwork or original scene"):
            preservation(s, damage(s, t[s["path"]], y * w + x))


def altered(tmp_path, b):
    p = tmp_path / "wrong.json"
    p.write_text(json.dumps(b), encoding="utf-8")
    return p


@pytest.mark.parametrize(
    "change,message",
    [
        ("file", "source SHA-256"),
        ("block", "source block identity"),
        ("region", "source region identity"),
        ("box", "escapes original"),
        ("payload", "extent or identity"),
        ("overlap", "Overlapping"),
        ("duplicate", "Duplicate"),
        ("index", "invalid"),
    ],
)
def test_embedded_source_block_bounds_payload_and_overlap_guards(case, tmp_path, change, message):
    base, _ = case
    s = SPECS[2]
    b = json.loads(batch_path(s).read_text(encoding="utf-8"))
    r = b["records"][0]
    if change == "file":
        b["source_file_sha256"] = "0" * 64
    elif change == "block":
        r["source_block_sha256"] = "0" * 64
    elif change == "region":
        r["source_region_sha256"] = "0" * 64
    elif change == "box":
        r["box"] = [5, 31, 321, 95]
    elif change == "payload":
        r["indices_zlib_hex"] = zlib.compress(b"x").hex()
        r["indices_sha256"] = sha(b"x")
    elif change == "index":
        r["block_index"] = 9999
    else:
        b["records"].append(copy.deepcopy(r))
        if change == "overlap":
            b["records"][-1]["id"] = "OTHER"
    with pytest.raises(ValueError, match=message):
        apply_ilnk_indexed_region_batch(altered(tmp_path, b), base.read_file(s["path"]))


@pytest.mark.parametrize(
    "change,message",
    [("type", "Exact type-16"), ("extent", "extent differs"), ("height", "escapes original")],
)
def test_native_storage_type_and_extent_reject_malformed_source(case, tmp_path, change, message):
    base, _ = case
    s = SPECS[2]
    a = IlnkContainer.parse(base.read_file(s["path"]))
    raw = bytearray(a.blocks[0])
    if change == "type":
        struct.pack_into("<I", raw, 4, 8)
    elif change == "extent":
        struct.pack_into("<I", raw, 532, 123)
    else:
        struct.pack_into("<I", raw, 532, 320 * 20 + 12)
        struct.pack_into("<H", raw, 542, 20)
    a.blocks[0] = bytes(raw)
    source = a.to_bytes()
    b = json.loads(batch_path(s).read_text(encoding="utf-8"))
    b["source_file_sha256"] = sha(source)
    for r in b["records"]:
        r["source_block_sha256"] = sha(bytes(raw))
    with pytest.raises(ValueError, match=message):
        apply_ilnk_indexed_region_batch(altered(tmp_path, b), source)


@pytest.mark.parametrize("index", [0, 1])
def test_loose_source_region_and_bounds_guards(case, tmp_path, index):
    base, _ = case
    s = SPECS[index]
    b = json.loads(batch_path(s).read_text(encoding="utf-8"))
    b["records"][0]["source_region_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="source region identity"):
        apply_pxl_indexed_region_batch(altered(tmp_path, b), base.read_file(s["path"]))


def test_water_donor_identity_and_complete_bounds(case):
    base, _ = case
    for s in SPECS:
        _, cases, _ = regions(s["name"])
        for c in cases:
            if s.get("water"):
                assert c["background_source_sha256"] == sha(
                    base.read_file("/_pxl/title/title04.pxl")
                )
            x0, y0, x1, y1 = c["box"]
            assert all(
                x0 < x < xend < x1 and y0 < y < yend < y1
                for x, y, xend, yend in (l["full_glyph_box"] for l in c["lines"])
            )


@pytest.mark.parametrize("index,y", [(1, 93), (2, 116)])
def test_original_top_caption_ink_and_adjacent_gold_leave_no_japanese_fleck(case, index, y):
    _, targets = case
    spec = SPECS[index]
    w, _, old, palette = asset(spec)
    _, _, new, _ = asset(spec, targets[spec["path"]])
    x0, _, x1, _ = spec["caption"]
    offsets = [
        y * w + x
        for x in range(x0, x1)
        if palette[old[y * w + x]][2] > palette[old[y * w + x]][0] + 8
        and palette[old[y * w + x]][2] > palette[old[y * w + x]][1] + 8
    ]
    assert offsets
    assert all(
        not (
            palette[new[i]][2] > palette[new[i]][0] + 8
            and palette[new[i]][2] > palette[new[i]][1] + 8
        )
        for i in offsets
    )


def test_all_prior_batches_and_terminal_stages_retained():
    s = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))
    a, b = s["profiles"]["all-routes-unified-v175"], s["profiles"][PROFILE]
    assert b["batches"] == a["batches"] + [batch_path(x).as_posix() for x in SPECS]
    assert len(b["batches"]) == 461
    assert all(v == b[k] for k, v in a.items() if k not in ("batches", "note", "description"))
