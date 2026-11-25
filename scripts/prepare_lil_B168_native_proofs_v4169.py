"""Derive B168's eight static-actor, three FE, relative-span and source-entry probes."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B168_native_tools_v4169')
OLD='lil_B167_source_v4118/all29_clean_current_complete_context_with_typed_choice'
SOURCE='lil_B168_source_v4168/all54_clean_current_complete_context'
if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/reconcile_lil_B167_voices_v4120.py','scripts/reconcile_lil_B168_voices_v4170.py',{
        'Bind6 source-owned static names/voices':'Bind eight source-owned static names/voices',
        'lil_B167_voices_v4120':'lil_B168_voices_v4170',OLD:SOURCE,'len(chosen)==5':'len(chosen)==8',
        '::5_source_names':'::8_source_names','current5_static_names_voices':'current8_static_names_voices','fresh5_actor_names':'fresh8_actor_names',
        'no_FE_source_objects_or_static_getter_calls':'three_FE_source_objects_have_no_static_actor_getter_calls',
        'all27_dispatches_still_require_separate_proof':'all54_dispatches_still_require_separate_proof',
        '5 static names/voices pass':'8 static names/voices pass'}))
    tools.append(derive('scripts/prove_lil_B167_dispatches_v4121.py','scripts/prove_lil_B168_dispatches_v4171.py',{
        'Bind90 source/current speech calls and29 exact non-relative control leaves.':'Bind108 source/current speech calls and16 exact non-relative control leaves.',
        'lil_B167_dispatches_v4121':'lil_B168_dispatches_v4171',OLD:SOURCE,'lil_B167_voices_v4120':'lil_B168_voices_v4170',
        'len(cases)==54 and len(leaves)==6':'len(cases)==108 and len(leaves)==16',
        "sum(c['source_selector']==254 for c in cases)==0":"sum(c['source_selector']==254 for c in cases)==6",
        'all27_source_current_dispatches_no_macros_and6_control_leaves':'all54_source_current_dispatches_macros_FE_and16_control_leaves',
        'all6_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact':'all16_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact',
        'all5_static_actors_without_role_or_roster_fixture':'all8_static_actors_without_role_or_roster_fixture',
        'no_FE_system_objects_in_this_source_scope':'three_FE_panels_keep_distinct_original_null_actor_modal_dispatch',
        'actual_selected_B167_IDs':'actual_selected_B168_IDs',
        '54 source/current dispatches pass:5static actors,noFE ormacros. All6nonrelative nontext nonchoice leaves exact.':'108 source/current dispatches pass:eight static actors,three FE panels,FI7/FA1/FO1. All16 nonrelative nontext leaves exact.'}))
    tools.append(derive('scripts/prove_lil_B167_branches_v4122.py','scripts/prove_lil_B168_branches_v4172.py',{
        'lil_B167_branches_v4122':'lil_B168_branches_v4172',OLD:SOURCE}))
    tools.append(derive('scripts/prove_lil_B167_entry_v4123.py','scripts/prove_lil_B168_entry_v4173.py',{
        'lil_B167_entry_v4123':'lil_B168_entry_v4173',OLD:SOURCE,'lil_B167_voices_v4120':'lil_B168_voices_v4170','B167':'B168','in [167]':'in [168]'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,source_scope=dict(block=168,speech_objects=54,progressive=51,FE=3,static_actors=[2,6,9,20,76,87,165,166],source_commands=82,relative_sites=12,FI=7,FA=1,FO=1),no_ROM_registry_ledger_credit_change=True))
    print('Four source-bound B168 native proof successors created;no credit.')
