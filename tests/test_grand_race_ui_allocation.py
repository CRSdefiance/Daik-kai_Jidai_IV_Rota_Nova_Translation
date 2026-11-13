import pytest

from scripts.plan_grand_race_ui_allocation import allocate, merge_ranges, subtract_ranges


def test_fragmented_pool_is_packed_when_greedy_best_fit_would_fail():
    entries = [(str(index), bytes(size)) for index, size in enumerate((4, 3, 3, 2, 2, 2))]
    selected, unused = allocate(entries, [[100, 108], [200, 208]])
    assert not unused
    occupied = set()
    for key, raw in entries:
        span = set(range(selected[key], selected[key] + len(raw)))
        assert not occupied & span
        assert span <= set(range(100, 108)) or span <= set(range(200, 208))
        occupied.update(span)


def test_table_reservation_and_neighbor_gaps_cannot_be_allocated():
    owned = merge_ranges([(100, 108), (108, 120), (140, 160)])
    assert owned == [[100, 120], [140, 160]]
    free = subtract_ranges(owned, [(104, 116), (148, 152)])
    assert free == [[100, 104], [116, 120], [140, 148], [152, 160]]
    selected, _ = allocate([('full', b'Complete')], free)
    assert selected['full'] in (140, 152)
    with pytest.raises(ValueError, match='relocation must expand'):
        allocate([('too-long', b'Complete paragraph')], free)


def test_overlapping_source_owners_are_rejected():
    with pytest.raises(ValueError, match='Overlapping'):
        merge_ranges([(100, 120), (110, 130)])
