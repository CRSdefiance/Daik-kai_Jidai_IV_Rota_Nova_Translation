"""Freeze315 complete reviews over the exact724-entry registered predecessor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/prepare_maria363_registered_v1.py').read_text(encoding='utf-8'), {
    'dk4tool.patch.maria363_release_v1': 'dk4tool.patch.maria315_release_v1',
    'Maria_B216_B252_clean_20261110': 'Maria_B286_B302_clean_20261110',
    'maria_B216_B252_': 'maria_B286_B302_',
    'maria363_editorial_release_v1': 'maria315_editorial_release_v1',
    'maria321_B196_B215_release_v1': 'maria349_B275_B285_release_v1',
    '(721,114,56)': '(724,114,59)',
    'dk4tool/patch/maria363_release_v1.py': 'dk4tool/patch/maria315_release_v1.py',
    'scripts/finalize_maria363_research_v1.py': 'scripts/finalize_maria315_research_v1.py',
    "ROOT/'display_run_menu2_v1/run_plan.json',":
        "ROOT/'display_run_menu2_v1/run_plan.json',ROOT/'display_run_menu3_v1/run_plan.json',",
    "Path('dk4tool/patch/maria301_release_v1.py')":
        "Path('dk4tool/patch/maria363_release_v1.py'),Path('scripts/prepare_maria363_registered_v1.py'),Path('dk4tool/patch/maria301_release_v1.py')",
    "format='dk4-reviewed-maria363-release-v1',record_count=363,speech_count=351,ordinary_count=266,style_count=85,typed_choice_count=12,menu_count=5":
        "format='dk4-reviewed-maria315-release-v1',record_count=315,speech_count=309,ordinary_count=196,style_count=113,typed_choice_count=6,menu_count=3",
    'scoped_name_count=29,native_pages=353,relative_cases=940,FE_count=38':
        'scoped_name_count=14,native_pages=309,relative_cases=320,FE_count=13',
    'actual_frames=97683': 'actual_frames=91844',
    "len(proof['changed_records'])==363": "len(proof['changed_records'])==315",
    'source_records=363,physical_body_candidates=351,native_pages=353':
        'source_records=315,physical_body_candidates=309,native_pages=309',
    'Qualified363 reviews over721-entry Maria321': 'Qualified315 reviews over724-entry Maria349',
})
exec(compile(source, __file__+'::same-exact-prefix-five-gate-andpure-whole-inverse-qualification', 'exec'), globals())
