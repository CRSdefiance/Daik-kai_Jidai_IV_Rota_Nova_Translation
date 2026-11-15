"""Derive three source actors,48 speech calls,two-menu exclusion,entry and eight relative sites."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B206_contract_tools_v6233')
SOURCE='work/analysis/lil_B206_source_v6232/all28_clean_current_complete_context_with_four_choice_labels.json'
OLD_SOURCE='work/analysis/lil_B205_source_v6172/all17_clean_current_complete_context.json'
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/reconcile_lil_B205_voices_v6173.py','scripts/reconcile_lil_B206_voices_v6233.py',{
        'B205':'B206','voices_v6173':'voices_v6233',OLD_SOURCE:SOURCE,'[2,15]':'[2,7,173]','current_V6160_native_v6168':'current_V6220_native_v6228','len(rows)==2':'len(rows)==3','two_source_selectors':'three_source_selectors','fresh2_actor_names':'fresh3_actor_names','and two B205':'and three B206',
    })]
    tools.append(derive('scripts/prove_lil_B205_names_v6174.py','scripts/prove_lil_B206_names_v6234.py',{
        'B205':'B206','names_v6174':'names_v6234',OLD_SOURCE:SOURCE,'voices_v6173':'voices_v6233','two_source_selectors':'three_source_selectors','[2,15]':'[2,7,173]','source-two-name-consumers':'source-three-name-consumers','current_V6160_native_v6168':'current_V6220_native_v6228',"len(native['rows'])==4":"len(native['rows'])==6",'fresh2_actor_names':'fresh3_actor_names','four_original_progressive':'six_original_progressive','native_four_consumer_cases':'native_six_consumer_cases','Four source-owned':'Six source-owned',
    }))
    tools.append(derive('scripts/bind_lil_B205_source_names_v6175.py','scripts/bind_lil_B206_source_names_v6235.py',{
        'B205':'B206','source_names_v6175':'source_names_v6235',OLD_SOURCE:SOURCE,'names_v6174':'names_v6234','voices_v6173':'voices_v6233','four_original_progressive':'six_original_progressive','two_source_selectors':'three_source_selectors','[2,15]':'[2,7,173]','fresh2_actor_names':'fresh3_actor_names','two_exact_source_name_fields':'three_exact_source_name_fields',
    }))
    tools.append(derive('scripts/prove_lil_B205_dispatches_v6176.py','scripts/prove_lil_B206_dispatches_v6236.py',{
        'B205':'B206','dispatches_v6176':'dispatches_v6236',OLD_SOURCE:SOURCE,'current_V6160_native_v6168':'current_V6220_native_v6228',
        '[0x4000,0x100,0x200,0x300,0x400,0x2200]':'[0x4000,0x100,0x200,0x300,0x400,0x2100,0x2200]',
        'Bind34 source/current speech calls and8 exact nonrelative control leaves.':'Bind48 source/current speech calls and8 exact nonrelative nonchoice control leaves.',
        'len(cases)==34':'len(cases)==48',"sum(c['source_selector']==254 for c in cases)==14":"sum(c['source_selector']==254 for c in cases)==0",'all17_source_current_dispatches_seven_FE_sounds_echoes_no_macros_and8_control_leaves':'all24_source_current_dispatches_three_actors_no_macros_and8_control_leaves',
        'all2_static_actors':'all3_static_actors','seven_FE_sound_echo_objects_use_original_null_actor_path':'no_source_FE_actor_or_system_object_inherited',
        '34 source/current dispatches pass:two static actors,seven FE sound/echo objects,no macros. All8 nonrelative leaves exact. No native display/gameplay/reviewcredit claim.':'48 source/current dispatches pass:three static actors,zero FE,no macros. Eight nonrelative nonchoice leaves exact;two menus/eight relative sites remain separately bound. No display/gameplay/credit claim.',
    }))
    tools.append(derive('scripts/prove_lil_B205_entry_v6177.py','scripts/prove_lil_B206_entry_v6237.py',{'B205':'B206','entry_v6177':'entry_v6237',OLD_SOURCE:SOURCE,'[205]':'[206]','current_V6160_native_v6168':'current_V6220_native_v6228'}))
    tools.append(derive('scripts/prove_lil_B205_branches_v6178.py','scripts/prove_lil_B206_branches_v6238.py',{'B205':'B206','branches_v6178':'branches_v6238',OLD_SOURCE:SOURCE,'len(edges)==0 and len(cases)==0':'len(edges)==8 and len(cases)==80'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_actor_speech_entry_and_branch_tools.json',dict(tools=tools,source_speeches=24,source_static_actors=[2,7,173],source_typed_menus=2,source_relative_sites=8,source_nonrelative_nonchoice_leaves=8,no_inherited_FE_or_parrot_echo_count=True,no_ROM_registry_ledger_or_review_credit_change=True,full_goal_complete=False));print('B206 three-actor/name,48-dispatch,entry and80-case relative proof tools prepared. No inherited FE/echo contracts.')
