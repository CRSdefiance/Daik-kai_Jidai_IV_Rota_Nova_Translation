"""Derive B167 five-actor dispatch, twelve-span and source-event getter proofs."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT = Path('work/analysis/lil_B167_native_tools_v4119')
OLD = 'lil_B166_source_v4054/all44_clean_current_complete_context_with_typed_choice'
SOURCE = 'lil_B167_source_v4118/all29_clean_current_complete_context_with_typed_choice'
if __name__ == '__main__':
    assert not ROOT.exists()
    pairs = []
    pairs.append(derive('scripts/reconcile_lil_B166_voices_v4056.py','scripts/reconcile_lil_B167_voices_v4120.py',{
        'lil_B166_voices_v4056':'lil_B167_voices_v4120',OLD:SOURCE,'len(chosen)==4':'len(chosen)==5',
        '::4_source_names':'::5_source_names','current4_static_names_voices':'current5_static_names_voices',
        'fresh4_actor_names':'fresh5_actor_names','all42_dispatches_still_require_separate_proof':'all27_dispatches_still_require_separate_proof',
        '4 static names/voices pass':'5 static names/voices pass'}))
    pairs.append(derive('scripts/prove_lil_B166_dispatches_v4057.py','scripts/prove_lil_B167_dispatches_v4121.py',{
        'lil_B166_dispatches_v4057':'lil_B167_dispatches_v4121',OLD:SOURCE,
        'lil_B166_voices_v4056':'lil_B167_voices_v4120','len(cases)==84 and len(leaves)==11':'len(cases)==54 and len(leaves)==6',
        'all42_source_current_dispatches_FI3_and11_control_leaves':'all27_source_current_dispatches_no_macros_and6_control_leaves',
        'all11_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact':'all6_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact',
        'all4_static_actors_without_role_or_roster_fixture':'all5_static_actors_without_role_or_roster_fixture',
        'actual_selected_B166_IDs':'actual_selected_B167_IDs',
        '84 source/current dispatches pass:4static actors,noFE,FI3. All11nonrelative nontext nonchoice leaves exact.':
            '54 source/current dispatches pass:5static actors,noFE ormacros. All6nonrelative nontext nonchoice leaves exact.'}))
    pairs.append(derive('scripts/prove_lil_B166_branches_v4058.py','scripts/prove_lil_B167_branches_v4122.py',{
        'lil_B166_branches_v4058':'lil_B167_branches_v4122',OLD:SOURCE}))
    pairs.append(derive('scripts/prove_lil_B166_entry_v4059.py','scripts/prove_lil_B167_entry_v4123.py',{
        'lil_B166_entry_v4059':'lil_B167_entry_v4123',OLD:SOURCE,
        'lil_B166_voices_v4056':'lil_B167_voices_v4120','B166':'B167','in [166]':'in [167]'}))
    ROOT.mkdir(parents=True)
    save(ROOT/'five_actor_native_proof_successors.json',dict(tools=pairs,no_ROM_registry_ledger_credit_change=True,full_goal_complete=False))
    print('Four B167 source-bound native proof successors created.')
