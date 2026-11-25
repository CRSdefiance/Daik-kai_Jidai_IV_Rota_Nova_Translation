"""Prepare complete English masks and honest post-scene comparisons without assumed equality."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B230_English_audit_tools_v7455')
if __name__=='__main__':
    assert not ROOT.exists();common={'B229':'B230','English_actual_v7407':'English_actual_v7455','English_fixture_v7405':'English_fixture_v7453','English_run_v7406':'English_run_v7454','source_actual_v7390':'source_actual_v7438','stored_v7400':'stored_v7448','name_planes_v7386':'name_planes_v7433','consumers_v7382':'consumers_v7429','later_v7408':'later_v7456','later_pairs_v7408b':'later_pairs_v7456b','event229':'event230','original_A000_source932_target908':'original_A000_source976_target966',"p['source_offset']==932":"p['source_offset']==976"};jobs=[]
    for a,b in [('audit_lil_B229_English_v7407','audit_lil_B230_English_v7455'),('measure_lil_B229_later_v7408','measure_lil_B230_later_v7456'),('illustrate_lil_B229_later_v7408b','illustrate_lil_B230_later_v7456b')]:
        src=Path('scripts/'+a+'.py').read_text('utf8');changes={k:v for k,v in common.items() if k in src};assert not Path('scripts/'+b+'.py').exists();checked_text(src,changes);jobs.append(('scripts/'+a+'.py','scripts/'+b+'.py',changes))
    rows=[derive(*j) for j in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_English_andlater_audits.json',dict(tools=rows,all17_actual_complete_body_andname_masks_and28_commands_required=True,all_following_resident_SC0_SC3_payloads_bound=True,no_assumption_of_later_RGB_RNG_calendar_actors_component_orfuture_sequence_equality=True,no_input_retiming_state_forcing_orfull_route_claim=True,new_credit=0,full_goal_complete=False))
