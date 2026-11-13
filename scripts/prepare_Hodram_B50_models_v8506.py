"""Bind actual B50 comparisons to already verified complete native planes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_model_tools_v8506');assert not root.exists()
    proof=derive('scripts/model_Hodram_B49_actual_v8408.py','scripts/model_Hodram_B50_actual_v8506.py',{
        'Hodram_B49_models_v8408':'Hodram_B50_models_v8506',
        'Hodram_B49_source_display_v8386b':'Hodram_B50_source_display_v8487',
        'Hodram_B49_stored_v8399':'Hodram_B50_stored_v8496',
        'Hodram_B49_fixtures_v8406':'Hodram_B50_fixtures_v8504',
        'Hodram_B49_pages_v8395':'Hodram_B50_pages_v8492b',
        "'block':49":"'block':50",
        'len(v)==14':'len(v)==3',
        "deepcopy(source['reused_original_scoped_style11_planes'])":"[deepcopy(source['reused_original_Lil_style11_plane'])]",
        "{r['actor_ID'] for r in names}=={1,2}":"{r['actor_ID'] for r in names}=={2}",
        'source_original14_andreviewed_stored14_planes_reused_by_exact_hash':'source_original3_andreviewed_stored3_planes_reused_by_exact_hash',
        'two_current_nameplanes_reused_by_exact_code_font_actor_binding':'one_current_Lil_nameplane_reused_by_exact_code_font_actor_binding',
        'actual_selected_path_hold_membership_not_all14_conditional_speeches_pending':'actual_three_speeches_FE_header_portrait_transition_andcomplete_hold_binding_pending',
        'B49 actual models:14clean+14stored complete native body planes/two currentnameplanes':'B50 actual models:3clean+3stored complete native body planes/one currentnameplane',
        'actual B49':'actual B50',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=proof,native_reexecution=False,new_credit=0,full_goal_complete=False))
