"""Pure361-record SC2 successor preserving B294 credited context and every inverse."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

module_source = checked_text(Path('dk4tool/patch/lil382_release_v1.py').read_text(encoding='utf-8'), {
    'lil382': 'lil361',
    'Lil382_residual_A_clean_20261110': 'Lil361_B283_B298_clean_20261110',
    'BLOCKS = list(range(20))+[21,115]+list(range(235,243))': 'BLOCKS = list(range(283,299))',
    'Sealed382 five-gate reviews and34 scoped names:257 revisions/125 retentions.':
        'Sealed361 five-gate reviews and15 scoped names:178 revisions/183 retentions.',
    '(382,378,364,14,4,2,34,386,555,3,82563)': '(361,352,175,177,9,4,15,353,875,15,86324)',
    '30 complete reviewed groups': '16 complete reviewed groups',
    '34 scoped names': '15 scoped names',
    "for r in stored['records'])==3, 'three original FE panels'":
        "for r in stored['records'])==15, '15 original FE panels'",
    'display_run{index}_v1': 'actual_run{index}_v1',
    'number != 115': 'number != 294',
    "len(rows)==32, 'only 32 new B115 speeches'": "len(rows)==15, 'only15 new B294 speeches'",
    "g['block']==115": "g['block']==294",
    'expected_context_objects=9,expected_context_speeches=4': 'expected_context_objects=1,expected_context_speeches=1',
    '"len(styles[\'objects\']) == 2"': '"len(styles[\'objects\']) == 24"',
})
exec(compile(module_source, __file__ + '::same-complete-context-source-current-andcanonical-inverses', 'exec'), globals())
