"""Clarify inherited console-only counters without rerunning the sealed reference proof."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B186_reference_count_clarification_v5163b')
if __name__=='__main__':
    assert not ROOT.exists()
    p=Path('work/analysis/lil_B186_reference_census_v5163/all24_commands_six_relative_sites_and_shipped_entry_census.json')
    d=read(p);blocks=d['blocks']
    assert sum(len(b['mapped_commands']) for b in blocks)==24
    assert sum(b['typed_relative_span_count'] for b in blocks)==6
    assert sum(b['target_native_skip_cases'] for b in blocks)==30
    assert d['all24_clean_current_target_commands_and_six_relative_sites_reexecuted']
    ROOT.mkdir(parents=True);save(ROOT/'exact_data_counters_not_inherited_console_literals.json',dict(
        reference_proof=str(p),reference_proof_sha256=sha(p.read_bytes()),entry_censuses=3,native_commands_each=24,relative_sites=6,target_native_skip_cases=30,
        explanation='The frozen5163 producer asserts and records the correct24 commands,six relative sites and30 native skip cases. Its final console print retained literal10/50 from B182. Those console-only literals do not describe this proof;no source,data or executed producer is changed.',
        completed_reference_checks_not_repeated=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B186 reference data:3 entry censuses,24 commands,6 relative sites,30 skip cases. Frozen console-only10/50 clarified;no rerun.')
