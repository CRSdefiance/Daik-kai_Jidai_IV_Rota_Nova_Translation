"""Bind200 whole-exchange source/prose reviews; no ledger or display credit."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import importlib
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_Crew_Items_author_v3121')
SOURCE=Path('work/analysis/lil_Crew_Items_source_v3112/complete200_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Crew_Items_controls_v3114/source_bound198_preambles_FE_and_original_conditional_predicates.json')
BRANCH=Path('work/analysis/lil_Crew_Items_branches_v3113/original_relative_skip_operand_proof.json')
CONTEXT=Path('work/analysis/lil_Crew_Items_context_v3115/complete_clean_exchange_context_notes.json')
TERMS=Path('work/analysis/lil_Crew_Items_terms_v3116/clean_current_ten_items_stat_UI_and_native_actor_terms.json')
DOC=Path('translations/lil_crew_items_editorial_manuscript_v1.json')
MENU=Path('translations/lil_crew_items_choice_manuscript_v1.json')
NAMES=['lil_islands_miracles_food_prose_v3117','lil_sword_ninja_amber_prose_v3118','lil_julio_samwell_items_prose_v3119','lil_telescope_pot_muramasa_prose_v3120']
FILES=[Path('scripts')/(name+'.py') for name in NAMES]
ANNOTATIONS={108:'Trader;original actor108',114:'Port Worker;original actor114',152:'Former sailor;original native Retainer actor152,source role not noble rank',188:'Margrete;current registered actor188'}

def previous_paragraph(row):
    value=' '.join(row['current_English'].split())
    for macro in ['FI','FA','FO']:value=value.replace(macro,'{MACRO:'+macro+'}')
    return value

def reviewed(original,review,contexts):
    row=deepcopy(original);gloss,english,note=review;choice=row['kind']=='typed-choice-label'
    assert gloss and note and english.isascii() and english==english.strip(),row['id']
    assert not any(tag in english for tag in ['\n','{LB','{ALIGN','{PAD','{SPEAKER:']),row['id']
    raw=bytes.fromhex(row['source_hex']);body=raw if choice else raw[1:]
    for macro in ['FI','FA','FO']:assert body.count(macro.encode())==english.count('{MACRO:'+macro+'}'),row['id']
    retained=english==previous_paragraph(row)
    if retained:row['fresh_retained_wording_justification']=note
    row['normalized_previous_English_for_exact_retention_comparison']=previous_paragraph(row)
    if not choice:english='{SPEAKER:'+row['source_presentation_prefix_hex'].upper()+'}'+english
    if row.get('original_actor_ID') in ANNOTATIONS:
        row['preserved_source_packet_speaker_annotation']=row['speaker'];row['speaker']=ANNOTATIONS[row['original_actor_ID']]
        row['speaker_annotation_reconciled_to_exact_native_catalog_and_clean_source_role_without_byte_change']=True
    context=contexts[row['block']]
    context+=' All198 clean speeches andboth typed choices in14complete exchanges were read before comparing older English. Storage order isnot branch reachability. Exact item/stat/native actor terminology is linked; no rank orfamilyrelationship follows from a familiar address. Prose review claims no currentfont,pagination,selected gameplay,earnedstat/item orregistered-release approval.'
    row.update(source_meaning=gloss,english=english,localization_note=note,context=context,editorial_decision='retain-wording' if retained else 'revise',
        review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='source-context-prose-approved;current-native-ordinary-FE-choice-format-reference-representative-release-pending')
    return row

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,DOC,MENU]) and all(p.is_file() for p in [SOURCE,CONTROL,BRANCH,CONTEXT,TERMS]+FILES)
    source,control,branch,context,terms=map(read,[SOURCE,CONTROL,BRANCH,CONTEXT,TERMS]);reviews={};choices=None
    for name in NAMES:
        module=importlib.import_module('scripts.'+name)
        for block,values in module.PROSE.items():
            for index,review in values.items():
                key=f'DK4_MES_B{block}_R{index:04d}';assert key not in reviews;reviews[key]=review
        if hasattr(module,'CHOICES'):assert choices is None;choices=module.CHOICES
    assert len(reviews)==198 and set(reviews)=={r['id'] for r in source['records']}
    assert set(choices)=={r['id'] for r in source['typed_choice_records']}
    assert (source['total_editorial_objects'],source['progressive_speeches'],source['system_FE_panels'],source['typed_choice_labels'])==(200,191,7,2)
    assert len(control['dispatch_cases'])==396 and control['current_original_predicate_cases']==control['original_event_queries']==[]
    assert control['all198_complete_preambles_and396_historical_dispatch_contexts_pass'] and control['all7_FE_before_fallback208_use5473C_and_original24310_null_macro_actor']
    assert control['all7_FE_source_stat_notices_and_unlabeled_monkey_calls_preserved_by_original_dispatcher']
    assert len(branch['cases'])==40 and len(branch['operands_requiring_adjustment_when_resizing'])==4 and sum(len(b['all_clean_native_commands']) for b in source['blocks'])==268
    assert context['all198_complete_clean_Japanese_speeches_and2_typed_choices_read_before_old_English_comparison']
    assert terms['all10_clean_current_pointer_strings_equal_registered_names'] and {int(k):v for k,v in terms['source_speaker_annotation_reconciliation'].items()}==ANNOTATIONS
    contexts={r['block']:r['whole_exchange_context'] for r in context['blocks']}
    records=[reviewed(r,reviews[r['id']],contexts) for r in source['records']];menu=[reviewed(r,choices[r['id']],contexts) for r in source['typed_choice_records']]
    assert Counter(r['editorial_decision'] for r in records)=={'revise':121,'retain-wording':77} and Counter(r['editorial_decision'] for r in menu)=={'revise':2}
    assert all(r['speaker']==ANNOTATIONS[r['original_actor_ID']] for r in records if r.get('original_actor_ID') in ANNOTATIONS)
    assert len([r for r in records if r['kind']=='system-FE' and '{MACRO:FI}' in r['english']])==2
    shared=dict(format='dk4-ilnk-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',file_path='/data/SC2.DK4',review_gates=['source','context','localization','naturalness','formatting'],
        source_ROM_sha256=source['source_ROM_sha256'],current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),control_contract=str(CONTROL),control_contract_sha256=sha(CONTROL.read_bytes()),branch_proof=str(BRANCH),branch_proof_sha256=sha(BRANCH.read_bytes()),
        whole_exchange_context_notes=str(CONTEXT),whole_exchange_context_notes_sha256=sha(CONTEXT.read_bytes()),item_terminology_reconciliation=str(TERMS),item_terminology_reconciliation_sha256=sha(TERMS.read_bytes()),
        formatting_review_pending=True,no_authored_line_breaks_or_padding=True,source_prose_credit_added=0,completion_credit_added=0,actual_selected_Crew_Items_IDs=[],new_emulator_runs=0,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(DOC,dict(**shared,records=records,revised=121,retained=77,typed_choice_companion=str(MENU)))
    save(MENU,dict(**shared,records=menu,revised=2,retained=0,ordinary_FE_companion=str(DOC),typed_menu_command_block=82,typed_menu_command_offset=114,typed_source_count=2,choice_indices_must_remain=[0,1],not_a_speech_or_speaker_prefix=True))
    save(ROOT/'source_prose_review_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choice_manuscript=str(MENU),choice_manuscript_sha256=sha(MENU.read_bytes()),total_editorial_objects=200,speeches=198,ordinary=191,FE=7,typed_choices=2,revised=123,retained=77,
        all200_clean_source_and_whole_exchange_prose_gates_pass=True,source268commands4sites40cases396dispatch0predicates0queries_bound=True,
        all_source_macros_and_exact_individually_justified_retentions_pass=True,four_stat_FE_two_FI_and_three_unlabeled_monkey_FE_preserved=True,
        full_former_sailor_Japanese_now_translated_and_Fernando_stat_notice_identity_restored=True,
        no_invented_Lil_Uncle_Gerhard_or_Julio_grandfather_relationship=True,ninja_passive_identity_exposure_rule_corrected_without_added_observer_death=True,
        ten_registered_item_names_and_generic_Katzbalger_distinction_preserved=True,Minerva_existence_condition_sea_uncertainty_and_grandfather_self_correction_restored=True,
        source_hearsay_cultural_context_and_personal_character_claims_not_narrator_facts=True,Hestia_had_pot_made_not_personally_crafted_preserved=True,
        author_files={str(p):sha(p.read_bytes()) for p in FILES+[Path(__file__)]},source_evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROL,BRANCH,CONTEXT,TERMS]},current_native_formatting_choice_fonts_pagination_reference_representative_and_registered_release_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print('200fresh source/prose drafts:123revisions/77justified retentions;191ordinary/sevenFE/twochoices. Native/reference/representative/release pending;ledger unchanged.')
