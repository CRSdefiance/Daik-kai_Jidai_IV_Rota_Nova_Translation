"""Source-lock bounded native-state/scene/RGB comparison to the two actual outcome pairs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_outcome_comparison_tools_v8337');assert not root.exists()
    result=derive('scripts/compare_Hodram_actual_v8283.py','scripts/compare_Hodram_outcomes_actual_v8337.py',{
        'Hodram_actual_comparison_v8283':'Hodram_outcome_actual_comparison_v8337',
        'for number in [137,45,46]:':'for number in [47,48]:',
        "path=Path(f'work/analysis/Hodram_actual_v8282/B{number}/paired_actual_dialogue_headers_flow_returns.json');proof=read(path)":"path=Path('work/analysis/Hodram_outcome_actual_v8335'+('b' if number==48 else ''))/f'B{number}/paired_actual_dialogue_headers_FE_flow_returns.json';proof=read(path)",
        'all_observed_complete_body_name_holds_andnative_flow_pass':'all_observed_complete_body_name_orFE_absent_header_holds_andnative_flow_pass',
        'three_paired_whole_exchanges_controls_scenes_returns_bounded_later_state':'two_paired_whole_outcomes_controls_scenes_returns_bounded_later_state',
        'total_actual_frames=100006':'total_actual_frames=40004',
        'current_registered_V8259':'current_registered_V8300',
    })
    root.mkdir(parents=True);save(root/'bounded_two_outcome_native_andRGB_comparison_derivation.json',dict(derivation=result,all_native_numeric_constants_andmultiplicity_preserved=True,no_input_state_seed_orresult_forcing_no_everyframe_orfuture_outcome_claim=True,new_credit=0,full_goal_complete=False))
