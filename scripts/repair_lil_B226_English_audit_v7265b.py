"""Preserve the stopped preparation; scope shared path substitutions to each measurement tool."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B226_English_audit_repair_v7265b')
if __name__=='__main__':
    assert not ROOT.exists() and not any(Path(p).exists() for p in ['scripts/audit_lil_B226_English_v7265.py','scripts/measure_lil_B226_later_v7266.py','scripts/illustrate_lil_B226_later_v7266b.py','work/analysis/lil_B226_English_audit_tools_v7265'])
    r=derive('scripts/prepare_lil_B226_English_audit_v7265.py','scripts/prepare_lil_B226_English_audit_v7265b.py',{"later={**paths,'later_v7222':'later_v7266'}":"later={k:v for k,v in {**paths,'later_v7222':'later_v7266'}.items() if k in Path('scripts/measure_lil_B225_later_v7222.py').read_text('utf8')}","picture={**paths,'later_pairs_v7222b':'later_pairs_v7266b','later_v7222':'later_v7266'}":"picture={k:v for k,v in {**paths,'later_pairs_v7222b':'later_pairs_v7266b','later_v7222':'later_v7266'}.items() if k in Path('scripts/illustrate_lil_B225_later_v7222b.py').read_text('utf8')}","lil_B226_English_audit_tools_v7265'":"lil_B226_English_audit_tools_v7265b'"})
    ROOT.mkdir(parents=True);save(ROOT/'preserved_preflight_failure_andrepair.json',dict(tool=r,failed_producer='scripts/prepare_lil_B226_English_audit_v7265.py',error='Derivation key absent:English_fixture_v7219 in measurement-only template',stopped_before_any_planned_audit_producer_orproof_write=True,actual_audit_specific_semantic_count_andgeometry_replacements_still_mandatory=True,only_shared_path_dictionary_filtered_for_later_measurement_andpicture_tools=True,no_ROM_orcapture_mutation=True,new_credit=0,full_goal_complete=False))
