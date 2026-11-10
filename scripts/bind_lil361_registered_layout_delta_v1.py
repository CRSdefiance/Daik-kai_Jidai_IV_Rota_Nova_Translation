"""Add exact registered-counter aliases without recomputing prose or layout."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(Path('scripts/bind_lil269_registered_layout_delta_v1.py').read_text(encoding='utf-8'), {
    'Lil269_B243_B282_clean_20261110': 'Lil361_B283_B298_clean_20261110',
    "len(d['changed_record_IDs']) == 16": "len(d['changed_record_IDs']) == 9",
    '(265, 264, 1)': '(353, 353, 0)',
    "'final_layout_changes': 16, 'pages_reclaimed': 1, 'initial_pages': 265":
        "'final_layout_changes': 9, 'pages_reclaimed': 0, 'initial_pages': 353",
})
if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-original-delta-andexact-dependency-binding', 'exec'), globals())
