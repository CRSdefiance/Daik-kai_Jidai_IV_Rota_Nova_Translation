"""Test the new mixed-menu scope guards while retaining earlier stage qualifications."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/qualify_hodram_B171_B190_release.py').read_text(encoding='utf-8'), {
    'Hodram_B171_B190': 'Hodram_B191_B210',
    'reviewed_scene_batch_v8': 'reviewed_scene_batch_v9',
    "len(proof['changed_records']) == 435": "len(proof['changed_records']) == 373",
    "'terminal-nonspace-event'": "'unqualified-FE-exception'",
    "'DK4_MES_B171_R0075'": "'DK4_MES_B201_R0074'",
    "row = next(r for r in doc['records'] if r['id'] == 'DK4_MES_B179_R0047')\n                row['complete_stored_native_display']['planned_native_row_comparison']['qualified_events'][0]['code'] = 65":
        "row = next(r for r in doc['records'] if r['id'] == 'DK4_MES_B208_R0065')\n                row['complete_stored_native_display'].setdefault('planned_native_row_comparison', {})['exact_owned_terminal_alignment_space_andzeroink_flush_row_qualified'] = True",
    'PASS435-record direct/shared production plans; six new invalid cases rejected':
        'PASS373-record direct/shared production plans; six new invalid cases rejected',
})
exec(compile(source, __file__ + '::same-pure-integration-negatives-current-mixed-menu-scope', 'exec'), globals())
