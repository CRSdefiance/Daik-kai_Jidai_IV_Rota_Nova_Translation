from itertools import pairwise

from dk4tool.script.arm9_profiles import PROFILES, SHIP_MODEL_ENTRIES


def test_profile_entries_are_unique_and_fixed_replacements_fit():
    entries = PROFILES["all"]
    assert len({entry.row_id for entry in entries}) == len(entries)
    assert len({entry.offset for entry in entries}) == len(entries)
    for entry in entries:
        assert len(entry.source_bytes) <= entry.source_length
        assert len(entry.suggested_english.encode("cp932")) <= entry.source_length
        assert len(entry.expected_bytes) == entry.source_length


def test_profile_offsets_do_not_overlap():
    ranges = sorted(
        (entry.offset, entry.offset + entry.source_length, entry.row_id)
        for entry in PROFILES["all"]
    )
    for (_, previous_end, previous_id), (start, _, row_id) in pairwise(ranges):
        assert previous_end <= start, f"{previous_id} overlaps {row_id}"


def test_ship_model_profile_covers_full_catalog_and_visible_galley_family():
    assert len(SHIP_MODEL_ENTRIES) == 119
    translations = {
        (entry.offset, entry.japanese): entry.suggested_english
        for entry in SHIP_MODEL_ENTRIES
    }
    assert translations[(0x15BE18, "ブリグ")] == "Brig"
    assert translations[(0x15CA58, "小型ガレー")] == "Sm Galley"
    assert translations[(0x15CA94, "大型ガレー")] == "Lg Galley"
    assert translations[(0x15E994, "武装ブリガンティン")] == "Armed Brigantine"
