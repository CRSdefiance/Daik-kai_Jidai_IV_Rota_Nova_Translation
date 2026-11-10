"""Save19 contextual prose decisions;leave native formatting/name integration uncredited."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B200_prose_v5839 as prose
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B200_author_v5840')
COMPARISON=Path('work/analysis/lil_B200_comparison_v5838/all19_complete_clean_and_predecessor_exchange.json')
OUTPUT=Path('translations/lil_B200_editorial_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    comparison=read(COMPARISON);source=read(comparison['source_context']);terms=read(comparison['contextual_reconciliation'])
    assert comparison['source19_complete_glosses_before_previous_English'] and terms['source_actual_speeches']==19
    assert comparison['current_registered_catalog_matches']==0
    assert len(prose.REVISIONS)==13 and len(prose.RETAIN_NOTES)==6 and not set(prose.REVISIONS)&set(prose.RETAIN_NOTES)
    assert set(prose.REVISIONS)|set(prose.RETAIN_NOTES)=={r['source_record_index'] for r in source['records']}
    base=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],
        current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_prose_or_completion_credit_added=0,formatting_review_pending=True,
        status='source-context-localization-naturalness-reviewed;native-format-reference-English-actual-name-target-and-release-pending',
        whole_exchange_context=terms['complete_exchange_progression'])
    deps=dict(source_context=comparison['source_context'],whole_exchange_context_notes=source['whole_exchange_context_notes'],
        contextual_reconciliation=comparison['contextual_reconciliation'],actor_terminology_reconciliation=comparison['contextual_reconciliation'],
        effective_current_comparison=str(COMPARISON),
        actor_voice_contract='work/analysis/lil_B200_voices_v5827/current207_catalog_eight_voices_and_two_source_selectors.json',
        control_contract='work/analysis/lil_B200_dispatches_v5828/all19_source_current_dispatches_no_macros_and12_control_leaves.json',
        branch_proof='work/analysis/lil_B200_branches_v5830/original_relative_skip_operand_proof.json',
        source_entry_proof='work/analysis/lil_B200_entry_v5829/source_EV2_B200_action_dependency_and_native_getter_binding.json',
        source_effect_and_predicate_contract='work/analysis/lil_B200_controls_v5833/twelve_exact_leaves_two_resources6003_picture47xx_six_structural_pairs_and_end.json',
        source_nameplate_consumer_proof='work/analysis/lil_B200_names_v5831/four_original_progressive_and_catalogue_name_consumers.json',
        source_name_literal_scope_proof='work/analysis/collapsed_speaker_lead_v5832/all_route_literal_uses_exact_name_fields_and_localization_finding.json',
        actual_original_response_paths=terms['source_actual_paths'])
    for key,path in deps.items():base[key]=path;base[key+'_sha256']=sha(Path(path).read_bytes())
    rows=[]
    for original in comparison['records']:
        r=deepcopy(original);index=r['source_record_index'];old=r['previous_paragraph'];decision='revise' if index in prose.REVISIONS else 'retain-wording'
        body,note=prose.REVISIONS[index] if decision=='revise' else (old,prose.RETAIN_NOTES[index])
        assert body.isascii() and body==' '.join(body.split()) and not any(v in body for v in ['%','{LB','{PAD','{MACRO:'])
        assert (body!=old)==(decision=='revise') and not any(body.count(m) for m in ['FI','FA','FO'])
        assert not body.startswith('(') and not body.endswith(')')
        speaker=('Collapse sound effect' if index==5 else 'Game status notification') if r['source_selector']==254 else terms['approved_prose_names'][str(r['source_selector'])]
        r.update(english='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+body,speaker=speaker,
            source_meaning=r['fresh_source_gloss'],context=terms['complete_exchange_progression'],localization_note=note,
            editorial_decision=decision,effective_predecessor_paragraph=old,full_clean_context_precedes_comparison=True,
            editorial_predecessor_English_comparison_pending=False,current_macro_dispatch_bound=True,current_complete_native_display_pending=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status=base['status'],
            prose_author_module=str(Path(prose.__file__)),source_prose_or_completion_credit_added=0,record_index=r['current_record_index'],
            current_effective_macro_template_hex=r['previous_effective_template_body'].encode('cp932').hex(),
            current_effective_macro_template_English=r['previous_effective_template_body'],current_effective_paragraph=old,
            current_raw_storage_English=r['previous_raw_storage_body'],registered_runtime_catalog_entry=r['previous_registered_catalog_entry'],
            current_native_UI_body_explicit_unexecuted_boundary=True,
            original_native_display_consumer='original_null_actor_24310_then5473C_FE' if r['kind']=='system-FE' else 'original_progressive_54020')
        if r['source_selector']==172:r['speaker_nameplate_target_pending']=True;r['current_nameplate']='Collapsed Person';r['draft_nameplate']='Stranger'
        if decision=='retain-wording':r['fresh_retained_wording_justification']=note
        rows.append(r)
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':13,'retain-wording':6}
    save(OUTPUT,{**base,'records':rows,'revised':13,'retained':6,
        'no_authored_line_break_alignment_spaces_or_fit_driven_prose_shortening':True,
        'rescue_causative_doctor_denial_polite_gift_refusal_insistence_acceptance_and_exact_Charm_increment_preserved':True,
        'no_specific_diagnosis_carrying_method_kinship_rank_occupation_payment_or_spoken_item_title_invented':True,
        'two_distinct_FE_roles_and_no_FI_FA_FO_parentheses_or_choices_preserved':True,
        'all19_source_speeches_observed_no_offline_only_source_lines':True,
        'actor172_Strander_draft_not_applied_no_new_name_localization_completion_credit':True,
        'existing_Carlo_Sinat_retained_with_source_field_rationale':True,'full_goal_complete':False})
    ROOT.mkdir(parents=True);save(ROOT/'all19_clean_first_contextual_decisions.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        objects=19,revised=13,retained=6,all6_retentions_individually_justified=True,
        source_context_localization_naturalness_true_formatting_false=True,
        actor172_Stranger_target_still_pending=True,Carlo_not_a_doctor=True,
        evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,Path(comparison['contextual_reconciliation']),Path(prose.__file__),Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B20019 contextual decisions:13 revisions/six justified retentions. Stranger target pending;native layout,English scene and release pending. Zero credit.')
