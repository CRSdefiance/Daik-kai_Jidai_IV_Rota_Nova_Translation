"""Prepare B179 source/current and native-role bindings after complete clean-first glosses."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B179_source_tools_v4708');assert not ROOT.exists()
OLD='lil_B178_source_v4662/all13_clean_current_complete_context'
NEW='lil_B179_source_v4708/all14_clean_current_complete_context'
tools=[derive('scripts/map_lil_B178_source_v4662.py','scripts/map_lil_B179_source_v4708.py',{
    'lil_B178_source_v4662':'lil_B179_source_v4708','editorial_handoff_verification_v4660':'editorial_handoff_verification_v4706',
    'lil_B177_source_v4602/all10_clean_current_complete_context':'lil_B178_source_v4662/all13_clean_current_complete_context',
    'lil_B178_clean_context_v4661/all13_complete_B178':'lil_B179_clean_context_v4707/all14_complete_B179',
    'len(known)==5885':'len(known)==5898','blocks[178]':'blocks[179]','DK4_MES_B178_R':'DK4_MES_B179_R','block=178':'block=179',
    'len(spoken)==13':'len(spoken)==14','selectors=[166,167,168,254]':'selectors=[92,96,152,254]',
    'source_static_actor_selectors=[166,167,168]':'source_static_actor_selectors=[92,96,152]',
    'physical_speeches=13':'physical_speeches=14','total_editorial_objects=13':'total_editorial_objects=14',
    'speech_objects=13':'speech_objects=14','ordinary_source_speeches=12':'ordinary_source_speeches=13',
    'source_A000=1':'source_A000=1,source_C200=0','all13':'all14','Bind13':'Bind14',
    'not_selected_B178':'not_selected_B179',
    'B178 mapped:13 complete preambles,twelve progressive/one FE,16 commands,no macros,A000/C200':
        'B179 mapped:14 complete preambles,thirteen progressive/one FE,16 commands,no macros,A000/no C200',
})]
tools.append(derive('scripts/reconcile_lil_B178_voices_v4663.py','scripts/reconcile_lil_B179_voices_v4709.py',{
    OLD:NEW,'lil_B178_voices_v4663':'lil_B179_voices_v4709','all13_dispatches':'all14_dispatches',
}))
tools.append(derive('scripts/prove_lil_B178_dispatches_v4664.py','scripts/prove_lil_B179_dispatches_v4710.py',{
    OLD:NEW,'lil_B178_dispatches_v4664':'lil_B179_dispatches_v4710','lil_B178_voices_v4663':'lil_B179_voices_v4709',
    'actual_selected_B178_IDs':'actual_selected_B179_IDs','len(cases)==26 and len(leaves)==3':'len(cases)==28 and len(leaves)==2',
    'all13_source_current_dispatches_no_macros_and3_control_leaves':'all14_source_current_dispatches_no_macros_and2_control_leaves',
    'all3_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact':'all2_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact',
    'Bind26 source/current speech calls and3':'Bind28 source/current speech calls and2',
    '26 source/current':'28 source/current','All3 nonrelative':'All2 nonrelative',
}))
tools.append(derive('scripts/prove_lil_B178_branches_v4665.py','scripts/prove_lil_B179_branches_v4711.py',{
    OLD:NEW,'lil_B178_branches_v4665':'lil_B179_branches_v4711',
}))
tools.append(derive('scripts/prove_lil_B178_entry_v4666.py','scripts/prove_lil_B179_entry_v4712.py',{
    OLD:NEW,'lil_B178_entry_v4666':'lil_B179_entry_v4712','lil_B178_voices_v4663':'lil_B179_voices_v4709',
    'B178':'B179','in [178]':'in [179]',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,source_block=179,physical_speeches=14,progressive=13,FE=1,
    source_static_actors=[92,96,152],source_macros=0,commands=16,nonrelative_leaves=2,A000=1,C200=0,end_offsets=[508],
    no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
print('Prepared B179 source/current,three-role,28-dispatch,branch and event-entry bindings;A000 and end only,no C200. No credit.')
