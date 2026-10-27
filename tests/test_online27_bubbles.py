"""Source-backed bubble meanings, complete lettering and exact screenshot borders."""

import copy
import json
import zlib
from pathlib import Path

import pytest

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.build_integrated_release import apply_pxl_indexed_region_batch
from scripts.online27_bubbles_v177 import (
    BATCH,
    OFFICIAL,
    OFFICIAL_SHA,
    PATH,
    PROFILE,
    SPECS,
    artwork,
    preservation,
    sources,
    target,
)


@pytest.fixture(scope="module")
def case():
    return sources()[0], target()


def test_four_faithful_bubbles_partial_screenshot_and_original_source(case):
    _, raw = case
    proof = preservation(raw)
    assert proof["original_palette_header_extent_bubble_borders_tails_scene_chat_status_exact"]
    assert not proof["entire_screenshot_localized"]
    assert sha(OFFICIAL.read_bytes()) == OFFICIAL_SHA
    b = json.loads(BATCH.read_text(encoding="utf-8"))
    assert [r["english"] for r in b["records"]] == [
        "Thank you!",
        "It's a steal!",
        "Come again!",
        "Welcome!",
    ]
    assert b["records"][1]["source_japanese"] == "もってけ！どろぼー"
    assert "not an accusation of theft" in b["records"][1]["localization_note"]
    assert all(all(r["review"].values()) for r in b["records"])


@pytest.mark.parametrize("index", range(4))
def test_every_visible_character_and_first_last_composited_ink_complete(case, index):
    _, raw = case
    p = PxlImage.from_bytes(raw)
    _, cases = artwork()
    c = cases[index]
    assert [g["character"] for g in c["each_visible_nonspace_character"]] == list(
        c["english"].replace(" ", "")
    )
    x0, y0, x1, y1 = c["full_glyph_box"]
    white = c["background_index"]
    for edge in ("first", "last"):
        for x in range(x0, x1) if edge == "first" else range(x1 - 1, x0 - 1, -1):
            hits = [y * p.width + x for y in range(y0, y1) if p.indices[y * p.width + x] != white]
            if hits:
                break
        assert hits
        for offset in hits:
            damaged = PxlImage.from_bytes(raw)
            damaged.indices[offset] ^= 1
            with pytest.raises(ValueError, match="Complete English bubble"):
                preservation(damaged.to_bytes())


@pytest.mark.parametrize("index", range(4))
def test_original_borders_tails_unowned_chat_and_scene_exact(case, index):
    _, raw = case
    p = PxlImage.from_bytes(raw)
    s = SPECS[index]
    x0, y0, x1, y1 = s["box"]
    for x, y in ((x0 - 1, y0), (x1, y1 - 1), (x0, y0 - 1), (x1 - 1, y1), (10, 160), (180, 120)):
        d = PxlImage.from_bytes(raw)
        d.indices[y * p.width + x] ^= 1
        with pytest.raises(ValueError, match="unowned border/scene/chat"):
            preservation(d.to_bytes())


@pytest.mark.parametrize(
    "change,message",
    [
        ("source", "source SHA-256"),
        ("region", "source region identity"),
        ("bounds", "escapes original"),
        ("payload", "extent or identity"),
        ("overlap", "Overlapping"),
        ("duplicate", "Duplicate"),
    ],
)
def test_locked_source_bounds_payload_and_ownership(case, tmp_path, change, message):
    base, _ = case
    b = json.loads(BATCH.read_text(encoding="utf-8"))
    r = b["records"][0]
    if change == "source":
        b["source_file_sha256"] = "0" * 64
    elif change == "region":
        r["source_region_sha256"] = "0" * 64
    elif change == "bounds":
        r["box"] = [47, 66, 257, 76]
    elif change == "payload":
        r["indices_zlib_hex"] = zlib.compress(b"x").hex()
        r["indices_sha256"] = sha(b"x")
    else:
        b["records"].append(copy.deepcopy(r))
        if change == "overlap":
            b["records"][-1]["id"] = "OTHER"
    file = tmp_path / "bad.json"
    file.write_text(json.dumps(b), encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        apply_pxl_indexed_region_batch(file, base.read_file(PATH))


def test_all_inherited_batches_and_terminal_stages_exact():
    s = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))
    a, b = s["profiles"]["all-routes-unified-v176"], s["profiles"][PROFILE]
    assert b["batches"] == a["batches"] + [BATCH.as_posix()]
    assert len(b["batches"]) == 462
    assert all(v == b[k] for k, v in a.items() if k not in ("batches", "note", "description"))
