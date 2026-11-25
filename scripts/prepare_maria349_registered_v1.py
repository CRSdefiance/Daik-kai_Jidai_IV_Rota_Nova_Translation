"""Freeze349 complete source reviews over the exact723-entry registered predecessor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/prepare_maria363_registered_v1.py').read_text(encoding='utf-8'),{
    'dk4tool.patch.maria363_release_v1':'dk4tool.patch.maria349_release_v1',
    'Maria_B216_B252_clean_20261110':'Maria_B275_B285_clean_20261110',
    'maria_B216_B252_':'maria_B275_B285_',
    'maria363_editorial_release_v1':'maria349_editorial_release_v1',
    'maria321_B196_B215_release_v1':'maria359_B253_B274_release_v1',
    '(721,114,56)':'(723,114,58)',
    'dk4tool/patch/maria363_release_v1.py':'dk4tool/patch/maria349_release_v1.py',
    'scripts/finalize_maria363_research_v1.py':'scripts/finalize_maria349_research_v1.py',
    "Path('dk4tool/patch/maria301_release_v1.py')":"Path('dk4tool/patch/maria363_release_v1.py'),Path('scripts/prepare_maria363_registered_v1.py'),Path('dk4tool/patch/maria301_release_v1.py')",
    "format='dk4-reviewed-maria363-release-v1',record_count=363,speech_count=351,ordinary_count=266,style_count=85,typed_choice_count=12,menu_count=5":
        "format='dk4-reviewed-maria349-release-v1',record_count=349,speech_count=341,ordinary_count=179,style_count=162,typed_choice_count=8,menu_count=3",
    'scoped_name_count=29,native_pages=353,relative_cases=940,FE_count=38':'scoped_name_count=19,native_pages=347,relative_cases=330,FE_count=7',
    'actual_frames=97683':'actual_frames=77043',
    "len(proof['changed_records'])==363":"len(proof['changed_records'])==349",
    'source_records=363,physical_body_candidates=351,native_pages=353':'source_records=349,physical_body_candidates=341,native_pages=347',
    'Qualified363 reviews over721-entry Maria321':'Qualified349 reviews over723-entry Maria359',
})
exec(compile(source,__file__+'::same-exact-prefix-five-gate-andpure-whole-inverse-qualification','exec'),globals())
