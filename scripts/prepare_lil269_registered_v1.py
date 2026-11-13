"""Freeze269 complete reviews over the exact726-entry registered Lil382 parent."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/prepare_maria363_registered_v1.py').read_text(encoding='utf-8'), {
    'dk4tool.patch.maria363_release_v1': 'dk4tool.patch.lil269_release_v1',
    'Maria_B216_B252_clean_20261110': 'Lil269_B243_B282_clean_20261110',
    'maria_B216_B252_': 'lil_B243_B282_',
    'maria363_editorial_release_v1': 'lil269_editorial_release_v1',
    'maria321_B196_B215_release_v1': 'lil382_residual_A_release_v1',
    '(721,114,56)': '(726,114,61)',
    '/data/SC3.DK4': '/data/SC2.DK4',
    'only_SC3_changes=True': 'only_SC2_changes=True',
    'display_run_menu': 'display_run',
    "Path('dk4tool/patch/maria363_release_v1.py')": "Path('dk4tool/patch/lil269_release_v1.py')",
    "Path('scripts/finalize_maria363_research_v1.py')":
        "Path('scripts/finalize_lil269_research_v1.py'),Path('scripts/finalize_maria305_research_v1.py'),Path('scripts/approve_lil269_actual_v1.py')",
    "format='dk4-reviewed-maria363-release-v1',record_count=363,speech_count=351,ordinary_count=266,style_count=85,typed_choice_count=12,menu_count=5":
        "format='dk4-reviewed-lil269-release-v1',record_count=269,speech_count=262,ordinary_count=246,style_count=16,typed_choice_count=7,menu_count=3",
    'scoped_name_count=29,native_pages=353,relative_cases=940,FE_count=38,FE_owner_IDs=[],captain=3,actual_frames=97683':
        'scoped_name_count=25,native_pages=264,relative_cases=990,FE_count=36,FE_owner_IDs=[],captain=2,actual_frames=64563',
    "len(proof['changed_records'])==363": "len(proof['changed_records'])==269",
    'source_records=363,physical_body_candidates=351,native_pages=353':
        'source_records=269,physical_body_candidates=262,native_pages=264',
    'Qualified363 reviews over721-entry Maria321': 'Qualified269 reviews over726-entry Lil382',
})
exec(compile(source, __file__ + '::same-exact-prefix-five-gate-andpure-transaction-qualification', 'exec'), globals())
