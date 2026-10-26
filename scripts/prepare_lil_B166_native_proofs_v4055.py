"""Derive exact B166 four-actor, dispatch, relative and event-getter proof successors."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B166_native_tools_v4055')
SOURCE='lil_B166_source_v4054/all44_clean_current_complete_context_with_typed_choice'
OLD='lil_B165_source_v4008/all24_clean_current_complete_context'
if __name__=='__main__':
    assert not ROOT.exists();pairs=[]
    pairs.append(derive('scripts/reconcile_lil_B165_voices_v4011.py','scripts/reconcile_lil_B166_voices_v4056.py',{'lil_B165_voices_v4011':'lil_B166_voices_v4056',OLD:SOURCE,'len(chosen)==3':'len(chosen)==4','::3_source_names':'::4_source_names','current3_static_names_voices':'current4_static_names_voices','fresh3_actor_names':'fresh4_actor_names','all24_dispatches_still_require_separate_proof':'all42_dispatches_still_require_separate_proof','no_source_dynamic_selectors_or4100_objects':'no_source_dynamic_selectors_or4100_objects','3 static names/voices pass':'4 static names/voices pass'}))
    pairs.append(derive('scripts/prove_lil_B165_dispatches_v4012.py','scripts/prove_lil_B166_dispatches_v4057.py',{'lil_B165_dispatches_v4012':'lil_B166_dispatches_v4057',OLD:SOURCE,'lil_B165_voices_v4011':'lil_B166_voices_v4056','len(cases)==48 and len(leaves)==12':'len(cases)==84 and len(leaves)==11','all24_source_current_dispatches_FI3_and12_control_leaves':'all42_source_current_dispatches_FI3_and11_control_leaves','all12_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact':'all11_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact','all3_static_actors_without_role_or_roster_fixture':'all4_static_actors_without_role_or_roster_fixture','actual_selected_B165_IDs':'actual_selected_B166_IDs','48 source/current dispatches pass:3static actors,noFE,FI3. All12nonrelative nontext leaves exact.':'84 source/current dispatches pass:4static actors,noFE,FI3. All11nonrelative nontext nonchoice leaves exact.'}))
    pairs.append(derive('scripts/prove_lil_B165_branches_v4013.py','scripts/prove_lil_B166_branches_v4058.py',{'lil_B165_branches_v4013':'lil_B166_branches_v4058',OLD:SOURCE}))
    pairs.append(derive('scripts/prove_lil_B165_entry_v4014.py','scripts/prove_lil_B166_entry_v4059.py',{'lil_B165_entry_v4014':'lil_B166_entry_v4059',OLD:SOURCE,'lil_B165_voices_v4011':'lil_B166_voices_v4056','B165':'B166','in [165]':'in [166]'}))
    ROOT.mkdir(parents=True);save(ROOT/'four_exact_proof_successors.json',dict(tools=pairs,no_ROM_registry_ledger_credit_change=True,full_goal_complete=False));print('Four B166 native proof successors created.')
