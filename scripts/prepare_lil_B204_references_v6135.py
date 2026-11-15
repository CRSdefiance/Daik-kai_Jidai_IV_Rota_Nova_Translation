"""Prepare source-bound B204 relocation and stored-byte/reference checks."""
from copy import deepcopy
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B204_reference_tools_v6135')
PARENT=Path('out/all_routes_combined_v6110_candidate.nds')
ROM=Path('out/lil_B204_reference_v6138_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B204_relocation_v6136/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists();prior=read('work/analysis/editorial_handoff_verification_v6134/verified_handoff.json')
    assert prior['B204_source_prose_native_approved_uncredited_objects']==20 and sha(PARENT.read_bytes())==prior['candidate_sha256'] and sha(Path('translations/editorial_review_current_v1.json').read_bytes())==prior['ledger_sha256']
    old=Path('translations/lil_B204_editorial_manuscript_v6.json');new=Path('translations/lil_B204_editorial_manuscript_v7.json');assert not new.exists();doc=deepcopy(read(old))
    for k,p in {'branch_proof':'work/analysis/lil_B204_branches_v6068/original_relative_skip_operand_proof.json','source_entry_proof':'work/analysis/lil_B204_entry_v6067/source_EV2_B204_action_dependency_and_native_getter_binding.json','source_effect_and_predicate_contract':'work/analysis/lil_B204_controls_v6069/six_exact_leaves_picture47xx_two43xx_one_A000_structural_pairs_and_guarded_end.json'}.items():
        doc[k]=p;doc[k+'_sha256']=sha(Path(p).read_bytes())
    assert not read(doc['branch_proof'])['operands_requiring_adjustment_when_resizing']
    doc.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),source_native_contract_refs_added_without_words_gates_or_credit_change=True,historical_control_and_entry_bodies_not_relabeled_as_new_current_execution=True);save(new,doc)
    tools=[derive('scripts/research_lil_B203_relocation_v6035.py','scripts/research_lil_B204_relocation_v6136.py',{
        'B203':'B204','relocation_v6035':'relocation_v6136','manuscript_v4':'manuscript_v7','v5998_candidate':'v6110_candidate','number==203':'number==204',
        "end_maps[0]['source_offset']==810":"end_maps[0]['source_offset']==1308",'source[old_end:]==bytes(2)':'source[old_end:]==bytes(0)','inverse_plus_original_two_tailzeros_recovers_every_stored_source_byte':'inverse_plus_original_zero_tailbytes_recovers_every_stored_source_byte',
        "sum(len(r['text_records']) for r in results)==22":"sum(len(r['text_records']) for r in results)==20","sum(len(r['command_map']) for r in results)==31":"sum(len(r['command_map']) for r in results)==26",'[203]':'[204]',
        'all22speech':'all20speech','source_FE_system_objects=1':'source_FE_system_objects=4','31commands/22speech':'26commands/20speech','all816 predecessor':'all1312 predecessor',
    })]
    tools.append(derive('scripts/prove_lil_B203_stored_v6036.py','scripts/prove_lil_B204_stored_v6137.py',{
        'B203':'B204','stored_v6036':'stored_v6137','relocation_v6035':'relocation_v6136','manuscript_v4':'manuscript_v7',
        'scripts.current_build_native_context_v4774':'scripts.current_build_native_context_v6097','lil_current_font_oracles_v5918':'lil_current_font_oracles_v6122','work/analysis/lil_B203_voices_v6011/current_native_input.json':'work/analysis/lil_B204_current_v6118/current_native_input.json',
        '[2,76,170,254]':'[2,11,124,130,145,254]',"sum(c['consumer']=='FE-paper' for c in cases)==1":"sum(c['consumer']=='FE-paper' for c in cases)==4",'len(cases)==22':'len(cases)==20','fresh+reused==88':'fresh+reused==80','all22':'all20','targets88':'targets80','current_final_stored_macro_alignment_cases=88':'current_final_stored_macro_alignment_cases=80','stored_targets=22,progressive=21,FE=1,macro_cases=88':'stored_targets=20,progressive=16,FE=4,macro_cases=80',
        'actual_English_B203_book_picture_negotiation_stat_and_end_reachability_unexecuted':'actual_English_B204_castle_picture_item_four_letters_and_end_reachability_unexecuted',
    }))
    tools.append(derive('scripts/create_lil_B203_reference_v6037.py','scripts/create_lil_B204_reference_v6138.py',{
        'B203':'B204','V5998':'V6110','prepare_lil_B203_references_v6034':'prepare_lil_B204_references_v6135','research_v6037':'research_v6138','stored_v6036':'stored_v6137','verification_v6033':'verification_v6134','all22':'all20','targets88':'targets80',"['current_final_stored_macro_alignment_cases']==88":"['current_final_stored_macro_alignment_cases']==80",'current_final_stored_macro_alignment_cases=88':'current_final_stored_macro_alignment_cases=80','==[203]':'==[204]',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_reference_tools.json',dict(tools=tools,parent=str(PARENT),research=str(ROM),plan=str(PLAN),manuscript=str(new),manuscript_sha256=sha(new.read_bytes()),source_commands=26,source_speeches=20,source_relative_sites=0,source_tailbytes=0,source_FE_panels=4,all_old_producers_and_approved_words_preserved=True,full_goal_complete=False));print('B204 relocation/stored/reference tools prepared:26 commands/20 objects/six leaves/four FE letters,end1308,zero source tailbytes.')
