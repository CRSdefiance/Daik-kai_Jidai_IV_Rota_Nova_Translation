"""Derive five static voice,64 dispatch, no-branch and entry proofs for B175."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B175_source_tools_v4503')
OLD='lil_B174_source_v4453/all33_clean_current_complete_context'
NEW='lil_B175_source_v4503/all32_clean_current_complete_context'
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/reconcile_lil_B174_voices_v4454.py','scripts/reconcile_lil_B175_voices_v4504.py',{
        OLD:NEW,'lil_B174_voices_v4454':'lil_B175_voices_v4504','four source-owned':'five source-owned',
        'len(chosen)==4':'len(chosen)==5','::4_source_names':'::5_source_names',
        'current4_static_names':'current5_static_names','fresh4_actor_names':'fresh5_actor_names',
        'all33_dispatches_still_require_separate_proof':'all32_dispatches_still_require_separate_proof',
        'no_FE_source_objects_or_static_getter_calls=True':'FE_source_objects_present_but_never_static_getter_calls=True',
        '4 static names/voices pass':'5 static names/voices pass',
    }),derive('scripts/prove_lil_B174_dispatches_v4455.py','scripts/prove_lil_B175_dispatches_v4505.py',{
        OLD:NEW,'lil_B174_dispatches_v4455':'lil_B175_dispatches_v4505','lil_B174_voices_v4454':'lil_B175_voices_v4504',
        'Bind66 source/current speech calls and8 exact non-relative control leaves.':'Bind64 source/current speech calls and7 exact non-relative control leaves.',
        'len(cases)==66 and len(leaves)==8':'len(cases)==64 and len(leaves)==7',
        "sum(c['source_selector']==254 for c in cases)==0":"sum(c['source_selector']==254 for c in cases)==18",
        'all33_source_current_dispatches_no_macros_and8_control_leaves':'all32_source_current_dispatches_FI4_FA1_and7_control_leaves',
        'all8_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact':'all7_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact',
        'all4_static_actors':'all5_static_actors','no_FE_system_objects_in_this_source_scope=True':'all9_FE_source_objects_use_original_null_actor_path=True',
        'actual_selected_B174_IDs':'actual_selected_B175_IDs',
        '66 source/current dispatches pass:four static actors,no macros/noFE. All8 nonrelative nontext leaves exact.':
            '64 source/current dispatches pass:five static actors,nine FE/null-actor speeches,FI4/FA1. All7 nonrelative leaves exact.',
    }),derive('scripts/prove_lil_B174_branches_v4456.py','scripts/prove_lil_B175_branches_v4506.py',{
        OLD:NEW,'lil_B174_branches_v4456':'lil_B175_branches_v4506',
    }),derive('scripts/prove_lil_B174_entry_v4457.py','scripts/prove_lil_B175_entry_v4507.py',{
        OLD:NEW,'lil_B174_entry_v4457':'lil_B175_entry_v4507','lil_B174_voices_v4454':'lil_B175_voices_v4504',
        'B174':'B175','in [174]':'in [175]',
    })]
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,source_block=175,
        physical_speeches=32,progressive=23,FE=9,source_static_actors=[2,9,183,184,185],
        FI=4,FA=1,FO=0,structural_commands=39,nonrelative_leaves=7,relative_sites=0,
        no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
    print('Prepared B175 five static voices,64 dispatches with18 FE cases, no-relative-site proof and source event getter binding.')
