"""Prepare B180 conditional source/current,speaker,dispatch,branch and entry proofs."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B180_source_tools_v4758')
assert not ROOT.exists()
OLD='lil_B179_source_v4708/all14_clean_current_complete_context'
NEW='lil_B180_source_v4758/all11_clean_current_complete_context'
tools=[derive('scripts/map_lil_B179_source_v4708.py','scripts/map_lil_B180_source_v4758.py',{
    'lil_B179_source_v4708':'lil_B180_source_v4758','editorial_handoff_verification_v4706':'editorial_handoff_verification_v4757',
    'lil_B178_source_v4662/all13_clean_current_complete_context':'lil_B179_source_v4708/all14_clean_current_complete_context',
    'lil_B179_clean_context_v4707/all14_complete_B179':'lil_B180_clean_context_v4755/all11_complete_B180',
    "    current,clean=NdsImage.open(prior['candidate']),NdsImage.open('work/clean.nds')":
        "    candidate=ledger['current_integrated_candidate'];prior={**prior,'candidate':candidate['path'],'candidate_sha256':candidate['sha256']}\n    current,clean=NdsImage.open(prior['candidate']),NdsImage.open('work/clean.nds')",
    'len(known)==5898':'len(known)==5912','blocks[179]':'blocks[180]','DK4_MES_B179_R':'DK4_MES_B180_R','block=179':'block=180',
    'len(old)==16 and len(spoken)==14':'len(old)==28 and len(spoken)==11',
    'selectors=[92,96,152,254]':'selectors=[166,167,254]',
    'source_static_actor_selectors=[92,96,152]':'source_static_actor_selectors=[166,167]',
    "assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x2100,0x4100,0x8000,0x8100,0x2000] for c in old)":
        "assert sum(c['word'] in [0x100,0x200,0x300,0x400] for c in old)==10\n    assert sum(c['word']==0x8000 for c in old)==2 and sum(c['word']==0xA000 for c in old)==3\n    assert sum(c['word']==0xC200 for c in old)==1\n    assert not any(c['word'] in [0x2100,0x4100,0x8100,0x2000] for c in old)",
    'physical_speeches=14':'physical_speeches=11','total_editorial_objects=14':'total_editorial_objects=11',
    'speech_objects=14':'speech_objects=11','ordinary_source_speeches=13':'ordinary_source_speeches=10',
    'FE_panels=1,relative_sites=0':'FE_panels=1,relative_sites=10',
    'source_native_commands=16,source_A000=1,source_C200=0,source_relative_sites=0,source_predicates=0':
        'source_native_commands=28,source_A000=3,source_C200=1,source_relative_sites=10,source_predicates=2',
    'all14':'all11','Bind14':'Bind11','not_selected_B179':'not_selected_B180',
    'B179 mapped:14 complete preambles,thirteen progressive/one FE,16 commands,no macros,A000/no C200':
        'B180 mapped:11 complete preambles,ten progressive/one FE,28 commands,10 relative sites,2 predicates,3 A000/C200',
})]
tools.append(derive('scripts/reconcile_lil_B179_voices_v4709.py','scripts/reconcile_lil_B180_voices_v4759.py',{
    OLD:NEW,'lil_B179_voices_v4709':'lil_B180_voices_v4759','len(chosen)==3':'len(chosen)==2',
    'current3_static_names':'current2_static_names','fresh3_actor_names':'fresh2_actor_names',
    'all14_dispatches':'all11_dispatches','::3_source_names':'::2_source_names',
    'Bind three':'Bind two','3 static names/voices':'2 static names/voices',
}))
tools.append(derive('scripts/prove_lil_B179_dispatches_v4710.py','scripts/prove_lil_B180_dispatches_v4760.py',{
    OLD:NEW,'lil_B179_dispatches_v4710':'lil_B180_dispatches_v4760','lil_B179_voices_v4709':'lil_B180_voices_v4759',
    'actual_selected_B179_IDs':'actual_selected_B180_IDs','len(cases)==28 and len(leaves)==2':'len(cases)==22 and len(leaves)==7',
    'all14_source_current_dispatches_no_macros_and2_control_leaves':'all11_source_current_dispatches_no_macros_and7_control_leaves',
    'all2_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact':'all7_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact',
    'all3_static_actors':'all2_static_actors','Bind28 source/current speech calls and2':'Bind22 source/current speech calls and7',
    '28 source/current dispatches pass:three static actors':'22 source/current dispatches pass:two static actors',
    'All2 nonrelative leaves':'All7 nonrelative leaves',
}))
tools.append(derive('scripts/prove_lil_B179_branches_v4711.py','scripts/prove_lil_B180_branches_v4761.py',{
    OLD:NEW,'lil_B179_branches_v4711':'lil_B180_branches_v4761',
}))
tools.append(derive('scripts/prove_lil_B179_entry_v4712.py','scripts/prove_lil_B180_entry_v4762.py',{
    OLD:NEW,'lil_B179_entry_v4712':'lil_B180_entry_v4762','lil_B179_voices_v4709':'lil_B180_voices_v4759',
    'B179':'B180','in [179]':'in [180]',
}))
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,source_block=180,physical_speeches=11,progressive=10,FE=1,
    source_static_actors=[166,167],source_macros=0,commands=28,nonrelative_leaves=7,A000=3,C200=1,predicates=2,
    relative_sites=10,expected_native_clean_current_skip_cases=100,end_offsets=[572],
    candidate_bound_from_current_verified_ledger=True,no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
print('Prepared B180 conditional source/current,two roles,22 dispatches,10 branches and event-entry proofs. No credit.')
