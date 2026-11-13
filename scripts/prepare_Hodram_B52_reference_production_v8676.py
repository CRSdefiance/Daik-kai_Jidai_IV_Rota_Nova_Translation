"""Derive independent source/current/final B52 reference and whole-ROM inverse reader."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B52_reference_production_tools_v8676')
    assert not root.exists()
    receipt = derive('dk4tool/patch/hodram_B49_references_v1.py', 'dk4tool/patch/hodram_B52_references_v1.py', {
        'B49': 'B52', 'hodram_B49_reconstruction_v2': 'hodram_B52_reconstruction_v1',
        'hodram_B49_choices_v2': 'hodram_B52_choices_v1',
        '[49]': '[52]', '==49': '==52', 'block=49': 'block=52',
        "len(group['command_map'])==36 and len(cleantexts)==len(oldtexts)==len(texts)==14": "len(group['command_map'])==14 and len(cleantexts)==len(oldtexts)==len(texts)==3",
        'all36 commands and14 speech identities': 'all14 commands and3 speech identities',
        "len(group['relative_fixups'])==8 and sum(len(r['cases']) for r in group['relocated_skip_cases'])==40": "len(group['relative_fixups'])==4 and sum(len(r['cases']) for r in group['relocated_skip_cases'])==20",
        'all eight native relative sites': 'all four native relative sites',
        'len(refs)==14': 'len(refs)==3',
        'sixteen disjoint canonical identities': 'five disjoint canonical identities',
        "len({r['id'] for r in rows})==16": "len({r['id'] for r in rows})==5",
        "if typed:require(row['native_menu_header_reference']==dict(offset=choice['new_offset'],bytes=choice['new_length'],hex=choice['target_hex']),'exact complete native menu header')": "if typed:require(row['stored_hex']==ref['target_hex'] and target[choice['new_offset']:choice['new_offset']+choice['new_length']].hex()==choice['target_hex'],'exact complete native menu header andlabel')",
        'editorial_references=16,speeches=14,typed_choices=2,commands=36,relative_sites=8': 'editorial_references=5,speeches=3,typed_choices=2,commands=14,relative_sites=4',
    })
    root.mkdir(parents=True)
    save(root / 'derivation.json', receipt)
