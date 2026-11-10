"""Correct the proposed particle-field index afterthe v1 guard rejected the surname slot."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

ORIGINAL = Path('scripts/qualify_rafael351_scoped_identity_v1.py')
source = checked_text(ORIGINAL.read_text(encoding='utf-8'), {
    "ROOT = Path('work/analysis/Rafael351_identity_qualification_v1_20261105')":
        "ROOT = Path('work/analysis/Rafael351_identity_qualification_v2_20261105')",
    "['actor_ID'] == 31)['source_andcurrent_fields'][1]['current']":
        "['actor_ID'] == 31)['source_andcurrent_fields'][2]['current']",
    "field = binding['source_andcurrent_fields'][1]":
        "field = binding['source_andcurrent_fields'][2]\n        assert field['column'] == 8",
    "[CURRENT,FRESH,DYNAMIC,*PRIORS,name_path,Path(__file__)]":
        "[CURRENT,FRESH,DYNAMIC,*PRIORS,name_path,ORIGINAL,Path(__file__)]",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-identity-checks-particle-is-column8-not-surname-column4', 'exec'), globals())
