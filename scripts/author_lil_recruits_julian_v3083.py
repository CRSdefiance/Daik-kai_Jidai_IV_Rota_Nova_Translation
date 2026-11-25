"""Bind197 fresh whole-exchange reviews andtwo typed choices; no ledger credit."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import importlib
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Recruits_Julian_author_v3083')
SOURCE=Path('work/analysis/lil_Recruits_Julian_source_v3072/complete199_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Recruits_Julian_controls_v3074/source_bound197_preambles_FE_and_original_conditional_predicates.json')
BRANCH=Path('work/analysis/lil_Recruits_Julian_branches_v3073/original_relative_skip_operand_proof.json')
CONTEXT=Path('work/analysis/lil_Recruits_Julian_context_v3075/complete_clean_exchange_context_notes.json')
TERMS=Path('work/analysis/lil_Recruits_Julian_terms_v3076/clean_current_crown_Mihwa_alias_and_shipyard_UI_terms.json')
DOC=Path('translations/lil_recruits_julian_editorial_manuscript_v1.json')
MENU=Path('translations/lil_recruits_julian_choice_manuscript_v1.json')
NAMES=['lil_janus_recruitment_prose_v3079','lil_charles_recruitment_prose_v3080','lil_yukihisa_recruitment_prose_v3081','lil_julian_prose_v3082']
FILES=[Path('scripts')/(name+'.py') for name in NAMES]

def previous_paragraph(row):
    paragraph=' '.join(row['current_English'].split())
    for macro in ['FI','FA','FO']:paragraph=paragraph.replace(macro,'{MACRO:'+macro+'}')
    return paragraph

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
    if row.get('original_actor_ID')==109:
        row['preserved_source_packet_speaker_annotation']=row['speaker']
        row['speaker']='Shipwright;original actor109'
        row['speaker_annotation_reconciled_to_exact_native_catalog_without_source_byte_change']=True
    context=contexts[row['block']]
    context+=' Every clean speech and both typed choices in these complete exchanges have been read before comparing the previous English. Storage order is not branch reachability. Approved crown/name/menu terminology is reconciled to exact clean/current sources in the linked proof. Prose review does not claim current native display, selected gameplay, earned recruitment or release completion.'
    row.update(source_meaning=gloss,english=english,localization_note=note,context=context,editorial_decision='retain-wording' if retained else 'revise',
        review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='source-context-prose-approved;current-native-ordinary-FE-choice-format-reference-representative-release-pending')
    return row

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,DOC,MENU])
    assert all(p.is_file() for p in [SOURCE,CONTROL,BRANCH,CONTEXT,TERMS]+FILES)
    source,control,branch,context,terms=map(read,[SOURCE,CONTROL,BRANCH,CONTEXT,TERMS])
    reviews={};choices=None
    for name in NAMES:
        module=importlib.import_module('scripts.'+name)
        for block,rows in module.PROSE.items():
            for index,review in rows.items():
                key=f'DK4_MES_B{block}_R{index:04d}';assert key not in reviews;reviews[key]=review
        if hasattr(module,'CHOICES'):assert choices is None;choices=module.CHOICES
    assert len(reviews)==197 and set(reviews)=={r['id'] for r in source['records']}
    assert set(choices)=={r['id'] for r in source['typed_choice_records']}
    assert source['total_editorial_objects']==199 and source['progressive_speeches']==196 and source['system_FE_panels']==1 and source['typed_choice_labels']==2
    assert len(control['dispatch_cases'])==394 and len(control['current_original_predicate_cases'])==16 and len(control['original_event_queries'])==0
    assert control['all197_complete_preambles_and394_historical_dispatch_contexts_pass']
    assert control['all1_FE_before_fallback208_use5473C_and_original24310_null_macro_actor'] and control['all1_FE_source_unlabeled_ship_rename_guide_preserved_by_original_dispatcher']
    assert len(branch['cases'])==680 and len(branch['operands_requiring_adjustment_when_resizing'])==68
    assert sum(len(b['all_clean_native_commands']) for b in source['blocks'])==372
    assert context['all197_complete_clean_Japanese_speeches_and2_typed_choices_read_before_old_English_comparison']
    assert terms['approved_item_name']=='Silla Gold Crown' and terms['versions'][0]['Mihwa_catalog201']['text']=='美華' and terms['versions'][1]['Mihwa_catalog201']['text']=='Mihwa'
    contexts={r['block']:r['whole_exchange_context'] for r in context['blocks']}
    records=[reviewed(r,reviews[r['id']],contexts) for r in source['records']]
    menu=[reviewed(r,choices[r['id']],contexts) for r in source['typed_choice_records']]
    assert Counter(r['editorial_decision'] for r in records)=={'revise':157,'retain-wording':40}
    assert Counter(r['editorial_decision'] for r in menu)=={'retain-wording':2}
    assert len([r for r in records if r.get('original_actor_ID')==109])==10
    shared=dict(format='dk4-ilnk-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',file_path='/data/SC2.DK4',review_gates=['source','context','localization','naturalness','formatting'],
        source_ROM_sha256=source['source_ROM_sha256'],current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),control_contract=str(CONTROL),control_contract_sha256=sha(CONTROL.read_bytes()),branch_proof=str(BRANCH),branch_proof_sha256=sha(BRANCH.read_bytes()),
        whole_exchange_context_notes=str(CONTEXT),whole_exchange_context_notes_sha256=sha(CONTEXT.read_bytes()),item_terminology_reconciliation=str(TERMS),item_terminology_reconciliation_sha256=sha(TERMS.read_bytes()),
        formatting_review_pending=True,no_authored_line_breaks_or_padding=True,source_prose_credit_added=0,completion_credit_added=0,actual_selected_Recruits_Julian_IDs=[],new_emulator_runs=0,full_goal_complete=False)
    ROOT.mkdir(parents=True)
    save(DOC,dict(**shared,records=records,revised=157,retained=40,typed_choice_companion=str(MENU)))
    save(MENU,dict(**shared,records=menu,revised=0,retained=2,ordinary_FE_companion=str(DOC),typed_menu_command_block=75,typed_menu_command_offset=1058,typed_source_count=2,choice_indices_must_remain=[0,1],not_a_speech_or_speaker_prefix=True))
    save(ROOT/'source_prose_review_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choice_manuscript=str(MENU),choice_manuscript_sha256=sha(MENU.read_bytes()),
        total_editorial_objects=199,speeches=197,ordinary=196,FE=1,typed_choices=2,revised=157,retained=42,all199_clean_source_and_whole_exchange_prose_gates_pass=True,
        source372commands68sites680cases394dispatch16predicates0queries_bound=True,all_source_macros_and_exact_individually_justified_retentions_pass=True,
        original_FE_unlabeled_null_actor_guide_and_visible_Dock_Remodel_terms_bound=True,original_two_choice_count_pointer_ownership_source_mapped=True,
        actor109_reconciled_to_Shipwright_with_original_annotation_preserved=True,
        Janus_practical_inexperience_repairs_debts_character_test_and_excited_self_correction_preserved=True,
        Charles_Academy_letter_conditional_experiment_bomb_science_correction_three_years_and_misunderstanding_preserved=True,
        Yukihisa_personal_moral_judgment_back_of_blade_no_cuts_and_personal_world_resolve_preserved=True,
        Julian_Silla_Gold_Crown_Hangzhou_tavern_Mihwa_Luo_Yuli_and_source_family_history_preserved=True,
        author_files={str(p):sha(p.read_bytes()) for p in FILES+[Path(__file__)]},source_evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROL,BRANCH,CONTEXT,TERMS]},
        current_native_formatting_choice_fonts_pagination_reference_representative_and_registered_release_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print('199fresh source/prose drafts:157revisions/42justified retentions;196ordinary/one FE/two typedchoices. Native/reference/representative/release pending;ledger unchanged.')
