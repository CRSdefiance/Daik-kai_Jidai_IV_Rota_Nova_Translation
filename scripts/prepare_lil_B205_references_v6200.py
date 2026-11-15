"""Prepare complete B205 reversible relocation and parity-preserving reference proof."""
from copy import deepcopy
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B205_reference_tools_v6200')
PARENT=Path('out/all_routes_combined_v6160_candidate.nds');ROM=Path('out/lil_B205_reference_v6203_RESEARCH_ONLY.nds');PLAN=Path('work/analysis/lil_B205_relocation_v6201/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists();prior=read('work/analysis/editorial_handoff_verification_v6198/verified_handoff.json');assert prior['B205_source_prose_native_approved_uncredited_objects']==17 and sha(PARENT.read_bytes())==prior['candidate_sha256'] and sha(Path('translations/editorial_review_current_v1.json').read_bytes())==prior['ledger_sha256']
    old=Path('translations/lil_B205_editorial_manuscript_v5.json');new=Path('translations/lil_B205_editorial_manuscript_v6.json');assert not new.exists();doc=deepcopy(read(old))
    for k,p in {'branch_proof':'work/analysis/lil_B205_branches_v6178/original_relative_skip_operand_proof.json','source_entry_proof':'work/analysis/lil_B205_entry_v6177/source_EV2_B205_action_dependency_and_native_getter_binding.json','source_effect_and_predicate_contract':'work/analysis/lil_B205_controls_v6179/eight_exact_leaves_picture147_47xx_two63xx_three_A000_and_guarded_end.json'}.items():doc[k]=p;doc[k+'_sha256']=sha(Path(p).read_bytes())
    assert not read(doc['branch_proof'])['operands_requiring_adjustment_when_resizing'];doc.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),source_native_contract_refs_added_without_words_gates_or_credit_change=True);save(new,doc)
    tools=[derive('scripts/research_lil_B204_relocation_v6136.py','scripts/research_lil_B205_relocation_v6201.py',{
        'B204':'B205','relocation_v6136':'relocation_v6201','manuscript_v7':'manuscript_v6','v6110_candidate':'v6160_candidate','number==204':'number==205',"end_maps[0]['source_offset']==1308":"end_maps[0]['source_offset']==616",
        "sum(len(r['text_records']) for r in results)==20":"sum(len(r['text_records']) for r in results)==17","sum(len(r['command_map']) for r in results)==26":"sum(len(r['command_map']) for r in results)==25",'[204]':'[205]',
        'all20speech':'all17speech','source_FE_system_objects=4':'source_FE_system_objects=7','26commands/20speech':'25commands/17speech','all1312 predecessor':'all620 predecessor',
    })]
    tools.append(derive('scripts/prove_lil_B204_stored_v6137.py','scripts/prove_lil_B205_stored_v6202.py',{
        'B204':'B205','stored_v6137':'stored_v6202','relocation_v6136':'relocation_v6201','manuscript_v7':'manuscript_v6','work/analysis/lil_B204_current_v6118/current_native_input.json':'work/analysis/current_V6160_native_v6168/current_native_input.json',
        '[2,11,124,130,145,254]':'[2,15,254]',"sum(c['consumer']=='FE-paper' for c in cases)==4":"sum(c['consumer']=='FE-paper' for c in cases)==7",'len(cases)==20':'len(cases)==17','fresh+reused==80':'fresh+reused==68','all20':'all17','targets80':'targets68','current_final_stored_macro_alignment_cases=80':'current_final_stored_macro_alignment_cases=68','stored_targets=20,progressive=16,FE=4,macro_cases=80':'stored_targets=17,progressive=10,FE=7,macro_cases=68',
        'actual_English_B204_castle_picture_item_four_letters_and_end_reachability_unexecuted':'actual_English_B205_parrot_echoes_sounds_capture_joke_and_end_reachability_unexecuted',
    }))
    tools.append(derive('scripts/create_lil_B204_reference_v6138.py','scripts/create_lil_B205_reference_v6203.py',{
        'B204':'B205','V6110':'V6160','prepare_lil_B204_references_v6135':'prepare_lil_B205_references_v6200','research_v6138':'research_v6203','stored_v6137':'stored_v6202','verification_v6134':'verification_v6198','all20':'all17','targets80':'targets68',"['current_final_stored_macro_alignment_cases']==80":"['current_final_stored_macro_alignment_cases']==68",'current_final_stored_macro_alignment_cases=80':'current_final_stored_macro_alignment_cases=68','==[204]':'==[205]',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_reference_tools.json',dict(tools=tools,parent=str(PARENT),research=str(ROM),plan=str(PLAN),manuscript=str(new),manuscript_sha256=sha(new.read_bytes()),source_commands=25,source_speeches=17,source_relative_sites=0,source_tailbytes=0,source_FE_panels=7,all_old_producers_and_approved_words_preserved=True,full_goal_complete=False));print('B205 reference tools:25 commands/17 objects/eight leaves/seven FE,end616,zero original tailbytes. No ROM or credit yet.')
