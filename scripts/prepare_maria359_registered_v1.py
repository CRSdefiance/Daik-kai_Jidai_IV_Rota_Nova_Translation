"""Freeze359 whole-exchange reviews over the exact registered722-entry predecessor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

_original=Path('scripts/prepare_maria363_registered_v1.py').read_text(encoding='utf-8')
source=checked_text(_original,{
    'dk4tool.patch.maria363_release_v1':'dk4tool.patch.maria359_release_v1',
    'Maria_B216_B252_clean_20261110':'Maria_B253_B274_clean_20261110',
    'maria_B216_B252_':'maria_B253_B274_',
    'maria363_editorial_release_v1':'maria359_editorial_release_v1',
    'maria321_B196_B215_release_v1':'maria363_B216_B252_release_v1',
    '(721,114,56)':'(722,114,57)',
    'dk4tool/patch/maria363_release_v1.py':'dk4tool/patch/maria359_release_v1.py',
    'scripts/finalize_maria363_research_v1.py':'scripts/finalize_maria359_research_v1.py',
    "Path('dk4tool/patch/maria301_release_v1.py')":
        "Path('dk4tool/patch/maria363_release_v1.py'),Path('scripts/prepare_maria363_registered_v1.py'),Path('dk4tool/patch/maria301_release_v1.py')",
    "format='dk4-reviewed-maria363-release-v1',record_count=363,speech_count=351,ordinary_count=266,style_count=85,typed_choice_count=12,menu_count=5":
        "format='dk4-reviewed-maria359-release-v1',record_count=359,speech_count=349,ordinary_count=218,style_count=131,typed_choice_count=10,menu_count=5",
    'scoped_name_count=29,native_pages=353,relative_cases=940,FE_count=38':'scoped_name_count=18,native_pages=350,relative_cases=1015,FE_count=17',
    'actual_frames=97683':'actual_frames=70803',
    "len(proof['changed_records'])==363":"len(proof['changed_records'])==359",
    'source_records=363,physical_body_candidates=351,native_pages=353':'source_records=359,physical_body_candidates=349,native_pages=350',
    'Qualified363 reviews over721-entry Maria321':'Qualified359 reviews over722-entry Maria363',
})
exec(compile(source,__file__+'::same-exact-prefix-source-current-research-andpure-whole-inverse-qualification','exec'),globals())
