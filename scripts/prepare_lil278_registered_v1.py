"""Freeze 278 reviewed records over the exact 728-entry registered predecessor."""

from scripts.prepare_lil269_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    'Freeze337 complete reviews over the exact716-entry registered predecessor.':
        'Freeze 278 complete reviews over the exact 728-entry registered predecessor.',
    'Lil269_B243_B282_clean_20261110': 'Lil278_B299_B311_clean_20261110',
    'lil_B243_B282_': 'lil_B299_B311_',
    'lil382_residual_A_release_v1': 'lil361_B283_B298_release_v1',
    '(726,114,61)': '(728,114,63)',
    "ROOT/'display_run0_v1/run_plan.json',ROOT/'display_run1_v1/run_plan.json',ROOT/'display_run2_v1/run_plan.json'":
        "ROOT/'actual_run0_v1/run_plan.json'",
    "Path('scripts/finalize_maria305_research_v1.py')": "Path('scripts/check_editorial_stored_exact_scope_v1.py')",
    'lil269': 'lil278',
    'record_count=269,speech_count=262,ordinary_count=246,style_count=16,typed_choice_count=7,menu_count=3':
        'record_count=278,speech_count=272,ordinary_count=133,style_count=139,typed_choice_count=6,menu_count=3',
    'scoped_name_count=25,native_pages=264,relative_cases=990,FE_count=36,FE_owner_IDs=[],captain=2,actual_frames=64563':
        'scoped_name_count=10,native_pages=280,relative_cases=670,FE_count=8,FE_owner_IDs=[],captain=2,actual_frames=25121',
    "len(proof['changed_records'])==269": "len(proof['changed_records'])==278",
    'source_records=269,physical_body_candidates=262,native_pages=264':
        'source_records=278,physical_body_candidates=272,native_pages=280',
    'Qualified269 reviews over726-entry Lil382': 'Qualified 278 reviews over the 728-entry Lil361 release',
})

exec(compile(source, __file__, 'exec'), globals())
