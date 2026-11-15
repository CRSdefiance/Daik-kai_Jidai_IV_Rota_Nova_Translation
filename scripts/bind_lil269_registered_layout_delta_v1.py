"""Add exact dependency bindings and registered-counter aliases to the frozen layout delta."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil269_B243_B282_clean_20261110')

if __name__ == '__main__':
    before = ROOT / 'final_layout_delta_v1.json'
    output = ROOT / 'final_layout_delta_v2.json'
    assert not output.exists()
    d = load(before)
    assert len(d['changed_record_IDs']) == 16 and (d['old_pages'], d['final_pages'], d['reclaimed_pages']) == (265, 264, 1)
    assert digest(d['initial_plan']) == d['initial_plan_sha256'] and digest(d['final_plan']) == d['final_plan_sha256']
    save(output, {**d, 'final_layout_changes': 16, 'pages_reclaimed': 1, 'initial_pages': 265,
        'original_delta': str(before), 'original_delta_sha256': digest(before),
        'exact_metadata_aliases_no_prose_orlayout_recomputed': True,
        'evidence': {str(p): digest(p) for p in [before, Path(d['initial_plan']), Path(d['final_plan']), Path(__file__)]}})
