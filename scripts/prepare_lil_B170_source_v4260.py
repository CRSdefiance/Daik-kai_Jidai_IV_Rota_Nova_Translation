"""Prepare B170 source/current binding and fresh two-actor native contracts."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B170_source_tools_v4260')
if __name__=='__main__':
    assert not ROOT.exists()
    old='lil_B169_source_v4211/all36_clean_current_complete_context'
    new='lil_B170_source_v4260/all33_clean_current_complete_context'
    tools=[derive('scripts/map_lil_B169_source_v4211.py','scripts/map_lil_B170_source_v4260.py',{
        'Bind36 clean/current complete preambles and53 commands':'Bind33 clean/current complete preambles and45 commands',
        'lil_B169_source_v4211':'lil_B170_source_v4260',
        'editorial_handoff_verification_v4209':'editorial_handoff_verification_v4259',
        'lil_B168_source_v4168/all54_clean_current_complete_context':'lil_B169_source_v4211/all36_clean_current_complete_context',
        'lil_B169_clean_context_v4210/all36_complete_B169_exchange':'lil_B170_clean_context_v4257/all33_complete_B170_exchange',
        'len(known) == 5656':'len(known) == 5692','blocks[169]':'blocks[170]',
        'len(old) == 53 and len(spoken) == 36':'len(old) == 45 and len(spoken) == 33',
        'selectors = [], [2,6,9,20,21,76]':'selectors = [], [2,25]',
        'DK4_MES_B169_R':'DK4_MES_B170_R',
        "{'FI':5,'FA':0,'FO':2}":"{'FI':1,'FA':0,'FO':1}",
        "for command in old) == 12":"for command in old) == 0",'block=169':'block=170',
        'physical_speeches=36':'physical_speeches=33','relative_sites=12':'relative_sites=0',
        'all36_clean_current_complete_context':'all33_clean_current_complete_context',
        'historical_snapshot_is_Lil_London_not_selected_B169':'historical_snapshot_is_Lil_London_not_selected_B170',
        'total_editorial_objects=36, speech_objects=36, ordinary_source_speeches=36':'total_editorial_objects=33, speech_objects=33, ordinary_source_speeches=33',
        'source_native_commands=53':'source_native_commands=45','source_predicates=3':'source_predicates=0',
        'all36_clean_first_glosses':'all33_clean_first_glosses',
        'B169 mapped:36 complete preambles/53 commands/12 relative sites,FI5/FO2':'B170 mapped:33 complete preambles/45 commands/no relative sites,FI1/FO1',
    })]
    tools.append(derive('scripts/reconcile_lil_B169_voices_v4213.py','scripts/reconcile_lil_B170_voices_v4262.py',{
        'Bind six source-owned static names/voices':'Bind two source-owned static names/voices',
        'lil_B169_voices_v4213':'lil_B170_voices_v4262',old:new,
        'len(chosen)==6':'len(chosen)==2','::6_source_names':'::2_source_names',
        'current6_static_names_voices':'current2_static_names_voices','fresh6_actor_names':'fresh2_actor_names',
        'all36_dispatches_still_require_separate_proof':'all33_dispatches_still_require_separate_proof',
        '6 static names/voices pass':'2 static names/voices pass',
    }))
    tools.append(derive('scripts/prove_lil_B169_dispatches_v4214.py','scripts/prove_lil_B170_dispatches_v4263.py',{
        'Bind72 source/current speech calls and5 exact non-relative control leaves.':'Bind66 source/current speech calls and12 exact non-relative control leaves.',
        'lil_B169_dispatches_v4214':'lil_B170_dispatches_v4263',old:new,
        'lil_B169_voices_v4213':'lil_B170_voices_v4262',
        'len(cases)==72 and len(leaves)==5':'len(cases)==66 and len(leaves)==12',
        'all36_source_current_dispatches_FI5_FO2_and5_control_leaves':'all33_source_current_dispatches_FI1_FO1_and12_control_leaves',
        'all5_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact':'all12_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact',
        'all6_static_actors_without_role_or_roster_fixture':'all2_static_actors_without_role_or_roster_fixture',
        'actual_selected_B169_IDs':'actual_selected_B170_IDs',
        '72 source/current dispatches pass:six static actors,FI5/FO2,noFE. All5 nonrelative nontext leaves exact.':'66 source/current dispatches pass:two static actors,FI1/FO1,noFE. All12 nonrelative nontext leaves exact.',
    }))
    tools.append(derive('scripts/prove_lil_B169_branches_v4215.py','scripts/prove_lil_B170_branches_v4264.py',{
        'lil_B169_branches_v4215':'lil_B170_branches_v4264',old:new,
    }))
    tools.append(derive('scripts/prove_lil_B169_entry_v4216.py','scripts/prove_lil_B170_entry_v4265.py',{
        'lil_B169_entry_v4216':'lil_B170_entry_v4265',old:new,
        'lil_B169_voices_v4213':'lil_B170_voices_v4262','B169':'B170','in [169]':'in [170]',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_scope=dict(block=170,speeches=33,commands=45,
        selectors=[2,25],FI=1,FA=0,FO=1,relative_sites=0,predicates=0,nonrelative_leaves=12,
        pause_offset=36,A000_offset=1842,C200_offset=1850,end_offsets=[1852,1856]),
        no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
    print('B170 source/current,voice,dispatch,zero-relative-site and entry proof producers prepared;no credit.')
