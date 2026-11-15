"""Three complete observed holds include8750; every other sampled frame is unchanged."""
from pathlib import Path
from scripts import verify_retreat_transfer_fonts_actual_v1526 as previous

if __name__ == '__main__':
    source = Path(previous.__file__).read_text(encoding='utf-8')
    for old, new, count in [
        ('work/analysis/retreat_transfer_actual_fonts_v1526', 'work/analysis/retreat_transfer_actual_fonts_v1526c', 1),
        ('actor = get(0x82428, fleets + 0x2090, 1)', 'actor = actors + 4 + identity * 32', 1),
        ('[8800, 8850]', '[8750, 8800, 8850]', 2),
        ("'visual_review_still_pending': True,", "'visual_review_still_pending': True, 'physical_slot_accessor_not_used_as_logical_role': True, '8750_is_already_a_complete_revised_retreat_hold_not_an_unchanged_control': True,", 1),
        ('Actual2684 two full native/reference/RGB holds', 'Actual2684 three full native/reference/RGB holds', 1),
    ]:
        assert source.count(old) == count, old
        source = source.replace(old, new)
    exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
