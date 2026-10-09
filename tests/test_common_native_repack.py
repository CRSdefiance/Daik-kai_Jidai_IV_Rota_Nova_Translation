from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_repack import repack_native_records


@pytest.fixture
def current_sources():
    path = Path("out/all_routes_combined_v101_candidate.nds")
    if not path.exists():
        pytest.skip("V101 required for verified native repack evidence")
    image = NdsImage.open(path)
    return image.read_file("/COMMON/MESFILE.DK4"), image.read_file("/__arm9__.bin")


def test_repack_funds_full_prose_and_preserves_every_unrelated_selection(current_sources):
    common, arm9 = current_sources
    text = "Ｉ hear they eat shark fins in China and shark eggs around the Black Sea, beyond the Mediterranean.".encode("cp932")
    result = repack_native_records(common, arm9, {3037: text}, {(33, 48): b"  "})
    old_blocks, new_blocks = IlnkContainer.parse(common).blocks, IlnkContainer.parse(result.common).blocks
    assert [len(block) for block in old_blocks] == [len(block) for block in new_blocks]
    assert [block.count(b"\0") for block in old_blocks] == [block.count(b"\0") for block in new_blocks]
    before = common_message_entries(common, arm9, clean=False)
    for old, new in zip(before, result.entries, strict=True):
        assert new.text.rstrip(b" ") == (text if new.message_id == 3037 else old.text.rstrip(b" "))
    assert (33, 48) in result.changed_records
    assert len(result.changed_records) > 1  # An explicitly mapped donor funds expansion.


def test_repack_rejects_partial_packed_translation(current_sources):
    common, arm9 = current_sources
    with pytest.raises(ValueError, match="every native entry"):
        repack_native_records(common, arm9, {889: b"Not enough money."}, {(11, 26): b" "})


def test_native_packed_copy_spans_need_no_artificial_separator(current_sources):
    common, arm9 = current_sources
    paragraphs = {889: b"Admiral, we're short on funds...", 890: b"We'll recruit sailors for %s coins."}
    result = repack_native_records(common, arm9, paragraphs, {(11, 26): b" "})
    for entry in result.entries:
        if entry.message_id in paragraphs:
            assert entry.text == paragraphs[entry.message_id]


def test_repack_never_expands_native_cache_to_fit_prose(current_sources):
    common, arm9 = current_sources
    with pytest.raises(ValueError, match="terminal padding"):
        repack_native_records(common, arm9, {3037: b"x" * 4097}, {(33, 48): b"  "})


def test_padding_donation_preserves_trailing_linebreak_guards(current_sources):
    common, arm9 = current_sources
    entries = common_message_entries(common, arm9, clean=False)
    owners = Counter((entry.block, entry.record_index) for entry in entries)
    container = IlnkContainer.parse(common)
    rows = container.blocks[11].split(b"\0")
    donor = max((entry for entry in entries if entry.block == 11 and entry.record_index != 26
                 and owners[entry.block, entry.record_index] == 1), key=lambda entry: len(rows[entry.record_index]))
    old = (b" " * donor.start + b"Unchanged.\n  ").ljust(len(rows[donor.record_index]), b" ")
    rows[donor.record_index] = old
    container.blocks[11] = b"\0".join(rows)
    common = container.to_bytes()
    result = repack_native_records(common, arm9, {
        889: b"Admiral, we're short on funds...",
        890: b"We'll recruit sailors for %s coins.",
    }, {(11, 26): b" "})
    new = IlnkContainer.parse(result.common).blocks[11].split(b"\0")[donor.record_index]
    assert old.rstrip(b" ").endswith(b"\n")
    assert len(new) < len(old)
    assert new.endswith(b"\n  ") or len(new) - len(new.rstrip(b" ")) >= 2
    assert old.rstrip(b" ") == new.rstrip(b" ")
