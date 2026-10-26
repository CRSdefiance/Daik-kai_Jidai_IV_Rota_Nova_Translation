"""Rest advances the original simulation; compare models to matching source frames."""
from pathlib import Path
source=Path('scripts/verify_inn_actual_v2258.py').read_text().replace('inn_actual_verification_v2258','inn_actual_verification_v2258b')
old="    assert all({k:v for k,v in r['models'].items()if k!='company'}=={k:v for k,v in paired[0]['models'].items()if k!='company'}for r in paired)"
new="    within_run_model_changes=[dict(frame=r['frame'],changed_model_keys=[k for k in r['models']if r['models'][k]!=paired[0]['models'][k]])for r in paired]\n    assert all(r['source_state_company_fleet_ship_and_clock_equal']for r in paired)"
assert source.count(old)==1;source=source.replace(old,new)
old='paired_native_state_model_clock_controls=paired,';assert source.count(old)==1
source=source.replace(old,old+'original_rest_model_changes_compared_to_matching_source_frames=within_run_model_changes,no_false_within_run_unchanged_fleet_ship_assertion=True,')
exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
