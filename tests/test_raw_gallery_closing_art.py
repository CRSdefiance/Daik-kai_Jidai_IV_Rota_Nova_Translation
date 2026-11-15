"""Storage preservation, mixed-layer composition and actual missing-letter mutations."""

import copy
import json
import struct
import zlib
from pathlib import Path

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.raw_bgr555_art import FRAME_BYTES, apply_raw_bgr555_art, sha
from scripts.build_integrated_release import (
    apply_ilnk_mixed_art_batches,
    load_batch_header,
    load_release_stack,
    order_graphics_sync_groups,
)
from scripts.closing_gallery_v179 import BATCH, OUT, PATH, authored, sources


@pytest.fixture(scope="module")
def case():
    base, prior, source, _ = sources()
    draft = OUT / "reviewed-format-draft.json"
    batch = json.loads(draft.read_text(encoding="utf-8"))
    target, _ = apply_raw_bgr555_art(draft, source)
    return base, prior, source, batch, target


def write(path, batch):
    path.write_text(json.dumps(batch), encoding="utf-8")
    return path


def test_original_archive_other_frames_unowned_art_and_high_bits_exact(case):
    _, _, source, batch, target = case
    a, b = [IlnkContainer.parse(r).blocks for r in (source, target)]
    assert len(source) == len(target)
    assert source[:96] == target[:96]
    assert all(x == y for i, (x, y) in enumerate(zip(a, b, strict=True)) if i != 19)
    assert a[19][:16 * FRAME_BYTES] == b[19][:16 * FRAME_BYTES]
    assert a[19][17 * FRAME_BYTES:] == b[19][17 * FRAME_BYTES:]
    owned = set()
    for row in batch["records"]:
        x0, y0, x1, y1 = row["box"]
        owned.update(16 * FRAME_BYTES + (y * 320 + x) * 2 + c
                     for y in range(y0, y1) for x in range(x0, x1) for c in (0, 1))
    assert all(x == y for i, (x, y) in enumerate(zip(a[19], b[19], strict=True)) if i not in owned)
    assert all(not (x ^ y) & 0x8000 for (x,), (y,) in zip(struct.iter_unpack("<H", a[19]), struct.iter_unpack("<H", b[19]), strict=True))


def test_gray_antialiasing_connected_to_hand_is_original_not_erased_as_text(case):
    _, _, source, _, target = case
    before, after = [IlnkContainer.parse(r).blocks[19] for r in (source, target)]
    for x, y in [(101, 120), (102, 121), (103, 122), (104, 122), (105, 122),
                 (106, 122), (107, 121), (108, 121), (109, 120), (110, 119),
                 (110, 120), (111, 119), (112, 119)]:
        offset = 16 * FRAME_BYTES + (y * 320 + x) * 2
        assert before[offset:offset + 2] == after[offset:offset + 2]


@pytest.mark.parametrize("row_index", [0, 1])
@pytest.mark.parametrize("end", [0, -1])
def test_rehashed_missing_first_or_final_character_fails_complete_english_gate(case, tmp_path, row_index, end):
    _, _, source, batch, _ = case
    mutated = copy.deepcopy(batch)
    _, evidence = authored()
    row = mutated["records"][row_index]
    x0, _, x1, _ = row["box"]
    width = x1 - x0
    bx0, by0, bx1, by1 = evidence[row_index]["visible_characters"][end]["bbox"]
    payload = bytearray(zlib.decompress(bytes.fromhex(row["words_zlib_hex"])))
    for y in range(by0, by1):
        for x in range(bx0, bx1):
            struct.pack_into("<H", payload, (y * width + x) * 2, row["background"])
    row["words_zlib_hex"] = zlib.compress(payload).hex()
    row["words_sha256"] = sha(payload)
    with pytest.raises(ValueError, match="complete English glyph raster"):
        apply_raw_bgr555_art(write(tmp_path / "missing.json", mutated), source)


@pytest.mark.parametrize("change,message", [
    ("source", "source SHA-256"), ("frame", "source frame"),
    ("dimensions", "dimensions/block"), ("outside", "escapes frame"),
    ("overlap", "Overlapping"), ("review", "review incomplete"),
    ("font", "font identity"), ("payload", "payload extent/identity"),
])
def test_source_extent_review_and_payload_guards(case, tmp_path, change, message):
    _, _, source, batch, _ = case
    mutated = copy.deepcopy(batch)
    row = mutated["records"][0]
    if change == "source": mutated["source_file_sha256"] = "0" * 64
    elif change == "frame": row["image_index"] = 15
    elif change == "dimensions": row["dimensions"] = [160, 480]
    elif change == "outside": row["box"][0] = -1
    elif change == "overlap":
        duplicate = copy.deepcopy(row); duplicate["id"] = "ANOTHER_ID"
        mutated["records"].append(duplicate)
    elif change == "review": row["review"]["visual"] = False
    elif change == "font": mutated["font_sha256"] = "0" * 64
    elif change == "payload": row["words_sha256"] = "0" * 64
    with pytest.raises(ValueError, match=message):
        apply_raw_bgr555_art(write(tmp_path / "bad.json", mutated), source)


def test_mixed_archive_merge_preserves_both_old_atlas_translations(case):
    _, prior, source, _, _ = case
    profile = load_release_stack()["profiles"]["all-routes-unified-v178"]
    syncs = [Path(p) for p in profile["batches"] if load_batch_header(Path(p)).get("file_path") == PATH]
    assert len(syncs) == 2
    refs = {load_batch_header(p)["source_image_path"]: prior.read_file(load_batch_header(p)["source_image_path"]) for p in syncs}
    draft = OUT / "reviewed-format-draft.json"
    result, ids = apply_ilnk_mixed_art_batches(syncs + [draft], source, refs)
    before, after = [IlnkContainer.parse(r).blocks for r in (prior.read_file(PATH), result)]
    assert before[12] == after[12] and before[20] == after[20]
    assert all(a == b for i, (a, b) in enumerate(zip(before, after, strict=True)) if i != 19)
    assert len(ids) == 4
    groups = {PATH: syncs + [draft], "/_pxl/slackimg12.pxl": [], "/_pxl/slackimg20.pxl": []}
    assert order_graphics_sync_groups(groups)[-1][0] == PATH


def test_raw_and_sync_cannot_own_same_block(case, tmp_path):
    _, _, source, _, _ = case
    bad = {"format": "dk4-ilnk-pxl-sync-v1", "block_index": 19}
    with pytest.raises(ValueError, match="overlaps sync block"):
        apply_ilnk_mixed_art_batches([write(tmp_path / "sync.json", bad), OUT / "reviewed-format-draft.json"], source, {})


def test_full_prior_profile_inherited_with_single_new_batch():
    profiles = load_release_stack()["profiles"]
    before, after = [profiles[p] for p in ("all-routes-unified-v178", "all-routes-unified-v179")]
    assert after["batches"] == before["batches"] + [BATCH.as_posix()]
    assert len(after["batches"]) == 463
    assert all(after[k] == v for k, v in before.items() if k not in ("batches", "description", "note"))
