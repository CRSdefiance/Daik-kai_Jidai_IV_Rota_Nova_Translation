"""Prepare exact-source B208 consumer successors without altering native constants."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B208_consumer_tools_v6391')
if __name__=='__main__':
    assert not ROOT.exists();rows=[]
    common={'B207':'B208','source_v6338':'source_v6390','all13_clean_current_complete_context.json':'all24_clean_current_complete_context.json','current_V6327_native_v6337':'current_V6380_native_v6389'}
    rows.append(derive('scripts/reconcile_lil_B207_voices_v6339.py','scripts/reconcile_lil_B208_voices_v6391.py',{**common,'voices_v6339':'voices_v6391','[2,14]':'[7,170]'}))
    rows.append(derive('scripts/prove_lil_B207_names_v6340.py','scripts/prove_lil_B208_names_v6392.py',{**common,'names_v6340':'names_v6392','voices_v6339':'voices_v6391','[2,14]':'[7,170]'}))
    rows.append(derive('scripts/bind_lil_B207_source_names_v6341.py','scripts/bind_lil_B208_source_names_v6393.py',{**common,'source_names_v6341':'source_names_v6393','names_v6340':'names_v6392','voices_v6339':'voices_v6391','[2,14]':'[7,170]'}))
    rows.append(derive('scripts/prove_lil_B207_dispatches_v6342.py','scripts/prove_lil_B208_dispatches_v6394.py',{**common,
        'dispatches_v6342':'dispatches_v6394','Bind26 source/current speech calls and2 exact':'Bind48 source/current speech calls and5 exact',
        'len(cases)==26 and len(leaves)==2':'len(cases)==48 and len(leaves)==5',"sum(c['source_selector']==254 for c in cases)==0":"sum(c['source_selector']==254 for c in cases)==2",
        'all13_source_current_dispatches_two_actors_no_macros_and2_control_leaves.json':'all24_source_current_dispatches_two_actors_one_FE_no_macros_and5_control_leaves.json',
        'all2_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact':'all5_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact',
        'no_source_FE_actor_or_system_object_inherited':'one_source_FE_null_actor_preserved_no_static_FE_getter',
        '26 source/current dispatches pass:two static actors,zero FE,no macros. Two exact leaves:one A000 and complete end.':'48 source/current dispatches pass:two static actors,one null-actor FE,no macros. Five exact leaves:6005,632E,two A000 and complete end.'}))
    rows.append(derive('scripts/prove_lil_B207_entry_v6343.py','scripts/prove_lil_B208_entry_v6395.py',{**common,'entry_v6343':'entry_v6395',"r['script_block'] in [207]":"r['script_block'] in [208]"}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,no_B207_actor_item_speech_FE_or_control_shape_assumption_inherited=True,full_goal_complete=False));print('Five source-bound B208 consumer tools prepared;all native constants preserved.')
