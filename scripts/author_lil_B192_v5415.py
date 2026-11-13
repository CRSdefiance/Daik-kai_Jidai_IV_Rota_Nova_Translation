"""Record all8 clean-first contextual decisions; native formatting remains pending."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B192_prose_v5414 as prose
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B192_author_v5415')
COMPARISON=Path('work/analysis/lil_B192_comparison_v5413/all8_complete_clean_and_predecessor_exchange.json')
OUTPUT=Path('translations/lil_B192_editorial_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();comparison=read(COMPARISON);source=read(comparison['source_context'])
    gp=Path(source['whole_exchange_context_notes']);gloss=read(gp);terms=read(comparison['terms'])
    assert gloss['read_no_predecessor_English'] and len(gloss['records'])==8
    assert set(prose.REVISIONS)|set(prose.RETAIN_NOTES)=={r['source_record_index'] for r in source['records']}
    assert not set(prose.REVISIONS)&set(prose.RETAIN_NOTES)
    doc=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],
        current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_prose_or_completion_credit_added=0,formatting_review_pending=True,status='source-context-localization-naturalness-reviewed;native-layout-relocation-actual-release-pending',
        whole_exchange_context=gloss['complete_exchange_progression'],manuscript_kind='speech',prose_companions=[])
    deps=dict(source_context=comparison['source_context'],whole_exchange_context_notes=str(gp),
        actor_voice_contract='work/analysis/lil_B192_voices_v5407/current207_catalog_eight_voices_and_two_source_selectors.json',
        control_contract='work/analysis/lil_B192_dispatches_v5408/all8_source_current_dispatches_no_macros_and3_control_leaves.json',
        branch_proof='work/analysis/lil_B192_controls_v5410/A000_C200_single_end_and_no_relative_or_predicate_contract.json',
        source_entry_proof='work/analysis/lil_B192_entry_v5409/source_EV2_B192_action_dependency_and_native_getter_binding.json',
        source_effect_and_predicate_contract='work/analysis/lil_B192_controls_v5410/A000_C200_single_end_and_no_relative_or_predicate_contract.json',
        current_C200_source_ownership_proof='work/analysis/lil_B192_controls_v5410/A000_C200_single_end_and_no_relative_or_predicate_contract.json',
        source_nameplate_consumer_proof='work/analysis/lil_B192_names_v5411/four_original_progressive_and_catalogue_name_consumers.json',
        actor_terminology_reconciliation=comparison['terms'],effective_current_comparison=str(COMPARISON))
    for key,path in deps.items():doc[key]=path;doc[key+'_sha256']=sha(Path(path).read_bytes())
    rows=[]
    for original in comparison['records']:
        row=deepcopy(original);index=row['source_record_index'];old=row['previous_paragraph']
        body,note=prose.REVISIONS[index] if index in prose.REVISIONS else (old,prose.RETAIN_NOTES[index])
        decision='revise' if index in prose.REVISIONS else 'retain-wording'
        assert body.isascii() and body==' '.join(body.split()) and not any(v in body for v in ['%','{LB','{PAD','{MACRO:'])
        assert (body!=old)==(decision=='revise')
        speaker='Impersonal fashion notice' if row['kind']=='system-FE' else terms['approved_prose_names'][str(row['source_selector'])]
        row.update(source_meaning=row['fresh_source_gloss'],english='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body,
            speaker=speaker,context=gloss['complete_exchange_progression'],localization_note=note,editorial_decision=decision,
            effective_predecessor_paragraph=old,record_index=row['current_record_index'],full_clean_context_precedes_comparison=True,
            editorial_predecessor_English_comparison_pending=False,current_macro_dispatch_bound=True,current_complete_native_display_pending=True,
            current_native_UI_body_explicit_unexecuted_boundary=True,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            status=doc['status'],prose_author_module=str(Path(prose.__file__)),
            original_native_display_consumer='original_null_actor_24310_then5473C_FE' if row['kind']=='system-FE' else 'original_progressive_54020')
        if decision=='retain-wording':row['fresh_retained_wording_justification']=note
        rows.append(row)
    counts=Counter(r['editorial_decision'] for r in rows);assert counts=={'revise':5,'retain-wording':3}
    doc.update(records=rows,revised=5,retained=3,
        source_Port_Worker115_and_Sailor153_catalogue_Retainer_voices0_4_preserved=True,
        opening_question_reversal_lack_of_chance_and_candid_admission_distinct=True,
        popularity_and_probable_only_person_hyperbole_are_character_claims=True,
        nervous_question_personal_wish_offer_follow_me_and_hesitant_assent_preserved=True,
        source_tobacco_smoking_not_sanitized_or_changed_to_equipment_brand_or_instruction=True,
        no_age_rank_kinship_employment_dependence_health_claim_or_completed_smoking_invented=True,
        source_Tobacco33_and_one_Istanbul_alias_preserved=True,
        source11_linear_commands_one_A000_C200_end_two_tailzeros_no_predicates_or_relatives_preserved=True,
        tentative_Tobacco_Istanbul_FE_not_earlier_location_or_earned_fashion=True,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(OUTPUT,doc)
    save(ROOT/'all8_clean_first_contextual_decisions.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),decision_counts=dict(counts),
        all3_retentions_individually_justified=True,all8_records_reviewed_as_one_exchange=True,
        source_context_localization_naturalness_true_formatting_false=True,new_emulator_runs=0,new_review_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,gp,Path(prose.__file__),Path(__file__)]},full_goal_complete=False))
    print('B192:8 whole-exchange decisions,5 revisions/3 justified retentions. Native formatting pending;zero credit.')
