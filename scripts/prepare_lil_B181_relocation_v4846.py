"""Prepare reversible linear B181 relocation and final stored native alignment."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B181_relocation_tools_v4846')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B179_relocation_v4729.py','scripts/research_lil_B181_relocation_v4846.py',{
        'B179':'B181','relocation_v4729':'relocation_v4846','combined_v4701':'combined_v4821',
        'all14':'all10','all14speech_and2_nonrelative_leaves_preserved':'all10speech_and3_nonrelative_leaves_preserved',
        'len(source)==old_end==512':'len(source)==old_end==396',
        "len(spec['all_current_native_commands'])==16":"len(spec['all_current_native_commands'])==13",
        "sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==14":"sum(c['word']==0x4000 for c in spec['all_current_native_commands'])==10",
        '==[0xA000,0]':'==[0xA000,0xC200,0]','number==179':'number==181','==[508]':'==[392]',
        "sum(len(r['text_records']) for r in results)==14":"sum(len(r['text_records']) for r in results)==10",
        "sum(len(r['command_map']) for r in results)==16":"sum(len(r['command_map']) for r in results)==13",
        'not in [179]':'not in [181]','no_source_C200_commands=True':'source_one_C200_command_preserved=True',
        "context=read(doc['source_context']);branches=read(doc['branch_proof'])":
        "context=read(doc['source_context']);linear=read(doc['branch_proof']);assert linear['no_source_relative_sites_predicates_pause_resources_presentations_or_typed_objects'];branches={'operands_requiring_adjustment_when_resizing':[],'cases':[]}",
        'Relocate all14 B179 speeches;preserve13 progressive,one impersonal FE,leading A000 and single end; no C200.':
        'Relocate all10 B181 speeches;preserve9 progressive,one impersonal FE,A000,C200 and end.',
        '16structural commands/14speech/13progressive/1impersonalFE,no relative sites,pause orpredicate,one opaque A000/single endword,no C200,inversebytes and335otherblocks exact. Researchonly.':
        '13structural commands/10speech/9progressive/1FE,A000/C200/end,no relative sites or predicates;inversebytes and335otherblocks exact. Researchonly.'})]
    tools.append(derive('scripts/prove_lil_B180_stored_v4799.py','scripts/prove_lil_B181_stored_v4847.py',{
        'B180':'B181','stored_v4799':'stored_v4847','relocation_v4798':'relocation_v4846','voices_v4775':'voices_v4833',
        'in [166,167,254]':'in [166,167,168,254]','len(cases)==11':'len(cases)==10','fresh+reused==44':'fresh+reused==40',
        'all11_final_stored_targets44_macro_cases':'all10_final_stored_targets40_macro_cases',
        'current_final_stored_macro_alignment_cases=44':'current_final_stored_macro_alignment_cases=40',
        'all11_final_targets':'all10_final_targets','Verify all11':'Verify all10',
        'actual_selected_B180_scene_predicates_three_effects_C200_and_end_reachability_unexecuted':
        'actual_selected_B181_scene_A000_C200_and_end_reachability_unexecuted',
        'stored_targets=11,progressive=10':'stored_targets=10,progressive=9','macro_cases=44':'macro_cases=40'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_relocation.json',dict(tools=tools,source_bytes=396,source_commands=13,
        speeches=10,progressive=9,FE=1,A000=1,C200=1,end392=True,source_predicates=0,relative_sites=0,
        final_stored_alignment_cases=40,no_ROM_registry_ledger_or_credit_change=True,full_goal_complete=False))
    print('Prepared linear B181 relocation/inverse and40 stored native alignment cases;all source controls retained.')
