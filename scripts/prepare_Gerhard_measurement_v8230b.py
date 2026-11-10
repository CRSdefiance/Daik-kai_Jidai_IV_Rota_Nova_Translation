"""Bind the measured post-fixture captain states; do not assume every artificial full-script tail stays Lil."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_measurement_tools_v8230b')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/measure_Gerhard_actual_v8230.py','scripts/measure_Gerhard_actual_v8230b.py',{
        'Gerhard_actual_comparison_v8230':'Gerhard_actual_comparison_v8230b',
        'assert captain==2':"assert captain==(0 if scope=='whole' and number==27 else 2)",
        'no_every_frame_future_sequence_arbitrary_effect_causality_broad_simulation_orfullroute_equivalence_claim=True,':
        "no_every_frame_future_sequence_arbitrary_effect_causality_broad_simulation_orfullroute_equivalence_claim=True,\n        whole_B27_initialized_fullscript_tail_measured_captain0_party0_andfollowing_SC0_B44_both_versions=True,\n        whole_B27_tail_NOT_normal_Lil_route_continuity_ororiginal_optional_event_context_proof=True,\n        Hamburg_andfocused_intro_final_captain2_observed_without_forcing=True,\n        preserved_failure='scripts/measure_Gerhard_actual_v8230.py assumed finalcaptain2 for every fixture;stopped on actual wholeB27 captain0 before any comparison receipt/no replay/no state mutation',",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(derivation=result,
        exact_observed_wholeB27_finalcaptain0_andothers2_bound_instead_ofbroad_allowlist=True,
        whole_B27_tail_is_disclosed_fixture_limit_not_production_continuity_approval=True,
        all_native_addresses_andcomponent_query_guards_preserved=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Prepared measured captain0 wholeB27 tail /captain2 otherfixtures;no continuity orsource-condition claim.')
