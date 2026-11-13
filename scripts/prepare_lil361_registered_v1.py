"""Freeze361 complete reviews over the verified727-entry cumulative predecessor."""
from scripts.prepare_lil382_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'dk4tool.patch.lil382_release_v1': 'dk4tool.patch.lil361_release_v1',
    'Lil382_residual_A_clean_20261110': 'Lil361_B283_B298_clean_20261110',
    'lil_residual_A_382_': 'lil_B283_B298_',
    'lil382_editorial_release_v1': 'lil361_editorial_release_v1',
    'maria315_B286_B302_release_v1': 'lil269_B243_B282_release_v1',
    '(725,114,60)': '(727,114,62)',
    'reconstruction_v2/reconstruction.json': 'reconstruction_v1/reconstruction.json',
    'qualified_credit_ledger_v1.json': 'preintegration_credit_witness_v1.json',
    'display_run': 'actual_run',
    "Path('scripts/finalize_lil382_research_v1.py')":
        "Path('scripts/finalize_lil361_research_v1.py'),Path('scripts/approve_lil361_actual_v1.py'),Path('scripts/approve_lil361_actual_pages_v1.py'),ROOT/'extended_run0_v1/run_plan.json',ROOT/'credited_context_rebuild_qualification_v1.json'",
    "format='dk4-reviewed-lil382-release-v1',record_count=382,speech_count=378,ordinary_count=364,style_count=14,typed_choice_count=4,menu_count=2":
        "format='dk4-reviewed-lil361-release-v1',record_count=361,speech_count=352,ordinary_count=175,style_count=177,typed_choice_count=9,menu_count=4",
    'scoped_name_count=34,native_pages=386,relative_cases=555,FE_count=3,FE_owner_IDs=[],captain=2,actual_frames=82563':
        'scoped_name_count=15,native_pages=353,relative_cases=875,FE_count=15,FE_owner_IDs=[],captain=2,actual_frames=86324',
    "len(proof['changed_records'])==382": "len(proof['changed_records'])==361",
    'source_records=382,physical_body_candidates=378,native_pages=386':
        'source_records=361,physical_body_candidates=352,native_pages=353',
    'Qualified382 reviews over725-entry Maria315': 'Qualified361 reviews over727-entry Lil269',
})
exec(compile(source, __file__ + '::same-exact-prefix-five-gate-andwhole-inverse-qualification', 'exec'), globals())
