from itertools import pairwise

from dk4tool.script.arm9_profiles import PROFILES


def test_profile_entries_are_unique_and_fixed_replacements_fit():
    entries = PROFILES["all"]
    assert len({entry.row_id for entry in entries}) == len(entries)
    assert len({entry.offset for entry in entries}) == len(entries)
    for entry in entries:
        assert len(entry.suggested_english.encode("cp932")) <= len(entry.source_bytes)


def test_profile_offsets_do_not_overlap():
    ranges = sorted(
        (entry.offset, entry.offset + len(entry.source_bytes), entry.row_id)
        for entry in PROFILES["all"]
    )
    for (_, previous_end, previous_id), (start, _, row_id) in pairwise(ranges):
        assert previous_end <= start, f"{previous_id} overlaps {row_id}"
