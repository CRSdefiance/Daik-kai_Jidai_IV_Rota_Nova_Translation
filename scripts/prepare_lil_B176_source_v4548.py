"""Prepare B176 current-source binding and two-actor/native dispatch/entry probes."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B176_source_tools_v4548')
OLD='lil_B175_source_v4503/all32_clean_current_complete_context'
NEW='lil_B176_source_v4548/all10_clean_current_complete_context'
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/map_lil_B175_source_v4503.py','scripts/map_lil_B176_source_v4548.py',{
        'Bind32 complete clean/current preambles, including nine genuine FE objects.':'Bind10 complete clean/current preambles,including one impersonal FE notice.',
        'lil_B175_source_v4503':'lil_B176_source_v4548','editorial_handoff_verification_v4501b':'editorial_handoff_verification_v4546',
        'lil_B174_source_v4453/all33_clean_current_complete_context':'lil_B175_source_v4503/all32_clean_current_complete_context',
        'lil_B175_clean_context_v4502/all32_complete_B175_exchange':'lil_B176_clean_context_v4547/all10_complete_B176_exchange',
        'len(known)==5833':'len(known)==5865','blocks[175]':'blocks[176]',
        'len(old)==39 and len(spoken)==32':'len(old)==13 and len(spoken)==10',
        'selectors=[2,9,183,184,185,254]':'selectors=[174,175,254]',
        "macros=={'FI':4,'FA':1,'FO':0}":"macros=={'FI':0,'FA':0,'FO':0}",
        "sum(r['kind']=='system-FE' for r in rows)==9":"sum(r['kind']=='system-FE' for r in rows)==1",
        '0x8000,0x8100,0xA000,0x2000':'0x8000,0x8100,0x2000',
        'block=175':'block=176','physical_speeches=32':'physical_speeches=10','FE_panels=9':'FE_panels=1',
        'all32_clean_current_complete_context':'all10_clean_current_complete_context',
        'total_editorial_objects=32,speech_objects=32,ordinary_source_speeches=23,system_FE_panels=9':
            'total_editorial_objects=10,speech_objects=10,ordinary_source_speeches=9,system_FE_panels=1',
        'source_static_actor_selectors=[2,9,183,184,185],source_native_commands=39':
            'source_static_actor_selectors=[174,175],source_native_commands=13,source_A000=1',
        'all32_clean_first_glosses':'all10_clean_first_glosses',
        'B175 mapped:32 complete preambles,23 progressive/nine FE,39 commands,FI4/FA1;clean glosses precede current English comparison. No credit.':
            'B176 mapped:10 complete preambles,nine progressive/one FE,13 commands,no macros,A000/C200;clean glosses precede comparison. No credit.',
        'DK4_MES_B175_R':'DK4_MES_B176_R','not_selected_B175':'not_selected_B176',
    })]
    tools.append(derive('scripts/reconcile_lil_B175_voices_v4504.py','scripts/reconcile_lil_B176_voices_v4549.py',{
        OLD:NEW,'lil_B175_voices_v4504':'lil_B176_voices_v4549','five source-owned':'two source-owned',
        'len(chosen)==5':'len(chosen)==2','::5_source_names':'::2_source_names',
        'current5_static_names':'current2_static_names','fresh5_actor_names':'fresh2_actor_names',
        'all32_dispatches_still_require_separate_proof':'all10_dispatches_still_require_separate_proof',
        '5 static names/voices pass':'2 static names/voices pass',
    }))
    tools.append(derive('scripts/prove_lil_B175_dispatches_v4505.py','scripts/prove_lil_B176_dispatches_v4550.py',{
        OLD:NEW,'lil_B175_dispatches_v4505':'lil_B176_dispatches_v4550','lil_B175_voices_v4504':'lil_B176_voices_v4549',
        'Bind64 source/current speech calls and7 exact non-relative control leaves.':'Bind20 source/current speech calls and3 exact nonrelative control leaves.',
        'len(cases)==64 and len(leaves)==7':'len(cases)==20 and len(leaves)==3',
        "sum(c['source_selector']==254 for c in cases)==18":"sum(c['source_selector']==254 for c in cases)==2",
        'all32_source_current_dispatches_FI4_FA1_and7_control_leaves':'all10_source_current_dispatches_no_macros_and3_control_leaves',
        'all7_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact':'all3_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact',
        'all5_static_actors':'all2_static_actors','all9_FE_source_objects_use_original_null_actor_path':'one_FE_source_object_uses_original_null_actor_path',
        'actual_selected_B175_IDs':'actual_selected_B176_IDs',
        '64 source/current dispatches pass:five static actors,nine FE/null-actor speeches,FI4/FA1. All7 nonrelative leaves exact.':
            '20 source/current dispatches pass:two static actors,one FE/null-actor notice,no macros. All3 nonrelative leaves exact.',
    }))
    tools.append(derive('scripts/prove_lil_B175_branches_v4506.py','scripts/prove_lil_B176_branches_v4551.py',{
        OLD:NEW,'lil_B175_branches_v4506':'lil_B176_branches_v4551',
    }))
    tools.append(derive('scripts/prove_lil_B175_entry_v4507.py','scripts/prove_lil_B176_entry_v4552.py',{
        OLD:NEW,'lil_B175_entry_v4507':'lil_B176_entry_v4552','lil_B175_voices_v4504':'lil_B176_voices_v4549',
        'B175':'B176','in [175]':'in [176]',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,source_block=176,physical_speeches=10,
        progressive=9,FE=1,source_static_actors=[174,175],source_macros=0,commands=13,nonrelative_leaves=3,A000=1,C200=1,end_offsets=[386],
        no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
    print('Prepared B176 source mapper,two static voices,20 dispatches,no-relative proof and source entry getter.')
