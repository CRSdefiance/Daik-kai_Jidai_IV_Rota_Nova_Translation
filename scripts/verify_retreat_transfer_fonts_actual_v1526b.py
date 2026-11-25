"""Correct1526's physical-slot/logical-role mismatch; preserve the failed producer."""
from pathlib import Path
from scripts import verify_retreat_transfer_fonts_actual_v1526 as previous

if __name__ == '__main__':
    source = Path(previous.__file__).read_text(encoding='utf-8')
    for old, new in [
        ('work/analysis/retreat_transfer_actual_fonts_v1526', 'work/analysis/retreat_transfer_actual_fonts_v1526b'),
        ('actor = get(0x82428, fleets + 0x2090, 1)', 'actor = actors + 4 + identity * 32'),
        ("'visual_review_still_pending': True,", "'visual_review_still_pending': True, 'physical_slot_accessor_not_used_as_logical_role': True,"),
    ]:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
