"""Qualify B294's actual clean/parent inverses and reject invalid ownership, source and FI."""
from pathlib import Path
from scripts import qualify_lil382_context_rebuild_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path(previous.__file__).read_text(encoding='utf-8'), {
    'Lil382_residual_A_clean_20261110': 'Lil361_B283_B298_clean_20261110',
    'reconstruction_v2/reconstruction.json': 'reconstruction_v1/reconstruction.json',
    "g['block']==115": "g['block']==294",
    "r['block']==115": "r['block']==294",
    "ledgerpath = Path('translations/editorial_review_current_v1.json')":
        "ledgerpath = ROOT/'preintegration_credit_witness_v1.json'",
    'expected_context_objects=9,expected_context_speeches=4': 'expected_context_objects=1,expected_context_speeches=1',
    "r['source_macros'].get('FO')": "r['source_macros'].get('FI')",
    "assert b'FO' in raw": "assert b'FI' in raw",
    "raw.replace(b'FO',b'XX')": "raw.replace(b'FI',b'XX')",
    "len(proof['preserved_credited_context_speeches'])==4": "len(proof['preserved_credited_context_speeches'])==1",
    'positive_B115_target_byte_exact': 'positive_B294_target_byte_exact',
    'preserved_context_objects=9,preserved_context_speeches=4,new_owned_speeches=32':
        'preserved_context_objects=1,preserved_context_speeches=1,new_owned_speeches=15',
    'PASS B115': 'PASS B294',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-block-inverses-andfive-semantic-rejections', 'exec'),
         {'__file__': __file__, '__name__': '__main__'})
