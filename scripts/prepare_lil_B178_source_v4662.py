"""Bind B178 to the completed V4655 cumulative state after all clean-first glosses."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B178_source_tools_v4662')
assert not ROOT.exists()
OLD='lil_B177_source_v4602/all10_clean_current_complete_context'
NEW='lil_B178_source_v4662/all13_clean_current_complete_context'
tools=[derive('scripts/map_lil_B177_source_v4602.py','scripts/map_lil_B178_source_v4662.py',{
    'lil_B177_source_v4602':'lil_B178_source_v4662',
    'editorial_handoff_verification_v4600':'editorial_handoff_verification_v4660',
    'lil_B176_source_v4548/all10_clean_current_complete_context':'lil_B177_source_v4602/all10_clean_current_complete_context',
    'lil_B177_clean_context_v4601/all10_complete_B177_exchange':'lil_B178_clean_context_v4661/all13_complete_B178_exchange',
    'len(known)==5875':'len(known)==5885','blocks[177]':'blocks[178]',
    'DK4_MES_B177_R':'DK4_MES_B178_R','block=177':'block=178',
    'len(old)==13 and len(spoken)==10':'len(old)==16 and len(spoken)==13',
    'selectors=[174,175,254]':'selectors=[166,167,168,254]',
    'source_static_actor_selectors=[174,175]':'source_static_actor_selectors=[166,167,168]',
    'physical_speeches=10':'physical_speeches=13','total_editorial_objects=10':'total_editorial_objects=13',
    'speech_objects=10':'speech_objects=13','ordinary_source_speeches=9':'ordinary_source_speeches=12',
    'source_native_commands=13':'source_native_commands=16','all10':'all13',
    'Bind10':'Bind13','not_selected_B177':'not_selected_B178',
    'B177 mapped:10 complete preambles,nine progressive/one FE,13 commands':'B178 mapped:13 complete preambles,twelve progressive/one FE,16 commands',
})]
tools.append(derive('scripts/reconcile_lil_B177_voices_v4603.py','scripts/reconcile_lil_B178_voices_v4663.py',{
    OLD:NEW,'lil_B177_voices_v4603':'lil_B178_voices_v4663',
    'two source-owned':'three source-owned','len(chosen)==2':'len(chosen)==3',
    '::2_source_names':'::3_source_names','current2_static_names':'current3_static_names',
    'fresh2_actor_names':'fresh3_actor_names','all10_dispatches':'all13_dispatches','2 static names/voices':'3 static names/voices',
}))
tools.append(derive('scripts/prove_lil_B177_dispatches_v4604.py','scripts/prove_lil_B178_dispatches_v4664.py',{
    OLD:NEW,'lil_B177_dispatches_v4604':'lil_B178_dispatches_v4664',
    'lil_B177_voices_v4603':'lil_B178_voices_v4663','actual_selected_B177_IDs':'actual_selected_B178_IDs',
    'len(cases)==20':'len(cases)==26','all10_source_current_dispatches':'all13_source_current_dispatches',
    'all2_static_actors':'all3_static_actors','Bind20':'Bind26','20 source/current':'26 source/current','two static actors':'three static actors',
}))
tools.append(derive('scripts/prove_lil_B177_branches_v4605.py','scripts/prove_lil_B178_branches_v4665.py',{
    OLD:NEW,'lil_B177_branches_v4605':'lil_B178_branches_v4665',
}))
tools.append(derive('scripts/prove_lil_B177_entry_v4606.py','scripts/prove_lil_B178_entry_v4666.py',{
    OLD:NEW,'lil_B177_entry_v4606':'lil_B178_entry_v4666','lil_B177_voices_v4603':'lil_B178_voices_v4663',
    'B177':'B178','in [177]':'in [178]',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,source_block=178,physical_speeches=13,progressive=12,FE=1,
    source_static_actors=[166,167,168],source_macros=0,commands=16,nonrelative_leaves=3,
    A000=1,C200=1,end_offsets=[490],no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
print('Prepared B178 source/current,three-voice,26-dispatch,branch and event-entry bindings;no credit.')
