"""Record24 contextual decisions;formatting and integration are still pending."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B197_prose_v5664 as prose
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B197_author_v5665')
COMPARISON=Path('work/analysis/lil_B197_comparison_v5663/all24_complete_clean_and_predecessor_exchange_with_three_choices.json')
OUTPUTS=[Path('translations/lil_B197_editorial_manuscript_v1.json'),Path('translations/lil_B197_choice_manuscript_v1.json')]
if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS)
    comparison=read(COMPARISON);source=read(comparison['source_context']);terms=read(comparison['terms'])
    assert terms['all_clean_first_glosses_and_original_actual_context_precede_predecessor_speech_comparison']
    assert len(prose.REVISIONS)==14 and len(prose.RETAIN_NOTES)==7 and not set(prose.REVISIONS)&set(prose.RETAIN_NOTES)
    assert set(prose.REVISIONS)|set(prose.RETAIN_NOTES)=={r['source_record_index'] for r in source['records']}
    base=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],
        current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_prose_or_completion_credit_added=0,formatting_review_pending=True,
        status='source-context-localization-naturalness-reviewed;native-format-choice-reference-English-actual-release-pending',
        whole_exchange_context=terms['complete_exchange_progression'],complete_contextual_review_includes_all_three_actual_original_paths=True,
        total_editorial_objects_across_speech_and_choice_companions=24)
    deps=dict(source_context=comparison['source_context'],whole_exchange_context_notes=source['whole_exchange_context_notes'],
        contextual_reconciliation=comparison['terms'],actor_terminology_reconciliation=comparison['terms'],effective_current_comparison=str(COMPARISON),
        actor_voice_contract='work/analysis/lil_B197_voices_v5648/current207_catalog_eight_voices_and_two_source_selectors.json',
        control_contract='work/analysis/lil_B197_dispatches_v5649/all21_source_current_dispatches_no_macros_and11_control_leaves.json',
        branch_proof='work/analysis/lil_B197_branches_v5651/original_relative_skip_operand_proof.json',
        source_entry_proof='work/analysis/lil_B197_entry_v5650/source_EV2_B197_action_dependency_and_native_getter_binding.json',
        source_effect_and_predicate_contract='work/analysis/lil_B197_controls_v5654/eleven_exact_leaves_five_effect_two47xx_pairs_picture_resource_6003_and_end_cases.json',
        source_nameplate_consumer_proof='work/analysis/lil_B197_names_v5652/four_original_progressive_and_catalogue_name_consumers.json',
        source_name_literal_scope_proof='work/analysis/lil_B197_source_names_v5653/two_source_name_fields_four_current_consumers_and_literal_scope.json',
        source_financial_context=terms['source_financial_context'],actual_original_response_paths=terms['source_actual_paths'])
    for key,path in deps.items():base[key]=path;base[key+'_sha256']=sha(Path(path).read_bytes())
    groups={'speech':[],'player-choices':[]};all_decisions=[]
    for original in comparison['records']:
        r=deepcopy(original);choice=r['kind']=='typed-choice-label';old=r['previous_paragraph']
        if choice:
            body,decision,note=prose.CHOICE_DECISIONS[r['option_index']]
            speaker='Player decision addressed to Ian';english=body
        else:
            index=r['source_record_index'];decision='revise' if index in prose.REVISIONS else 'retain-wording'
            body,note=prose.REVISIONS[index] if index in prose.REVISIONS else (old,prose.RETAIN_NOTES[index])
            speaker='Impersonal common-tail Ian Charm notice' if r['source_selector']==254 else terms['approved_prose_names'][str(r['source_selector'])]
            english='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+body
        assert body.isascii() and body==' '.join(body.split()) and not any(v in body for v in ['%','{LB','{PAD','{MACRO:'])
        assert (body!=old)==(decision=='revise'),r['id']
        assert all(m not in bytes.fromhex(r['source_hex']) for m in [b'FI',b'FA',b'FO'])
        r.update(english=english,speaker=speaker,source_meaning=r['fresh_source_gloss'],context=terms['complete_exchange_progression'],
            localization_note=note,editorial_decision=decision,effective_predecessor_paragraph=old,
            full_clean_context_precedes_comparison=True,editorial_predecessor_English_comparison_pending=False,
            current_macro_dispatch_bound=not choice,current_complete_native_display_pending=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            status=base['status'],prose_author_module=str(Path(prose.__file__)),source_prose_or_completion_credit_added=0)
        if choice:r['current_native_typed_choice_font_reference_and_outcome_binding_pending']=True
        else:r.update(record_index=r['current_record_index'],current_native_UI_body_explicit_unexecuted_boundary=True,
            original_native_display_consumer='original_null_actor_24310_then5473C_FE' if r['kind']=='system-FE' else 'original_progressive_54020')
        if decision=='retain-wording':r['fresh_retained_wording_justification']=note
        groups['player-choices' if choice else 'speech'].append(r);all_decisions.append(r)
    manifests=[]
    for path,kind in zip(OUTPUTS,['speech','player-choices'],strict=True):
        rows=groups[kind];counts=Counter(r['editorial_decision'] for r in rows)
        assert counts==({'revise':14,'retain-wording':7} if kind=='speech' else {'revise':2,'retain-wording':1})
        save(path,{**deepcopy(base),'manuscript_kind':kind,'prose_companions':[str(p) for p in OUTPUTS if p!=path],
            'records':rows,'revised':counts.get('revise',0),'retained':counts['retain-wording'],
            'no_authored_line_break_alignment_spaces_or_fit_driven_prose_shortening':True,
            'purchase_R53_romance_refusal_delegated_gift_and_common_FE_notice_context_preserved':True,
            'Indian_classic_celestial_maiden_sage_and_tentative_identity_preserved_no_new_spoken_item_title':True,
            'actual_Japanese_source_three_paths_observed_revised_English_fixture_not_yet_run':True,
            'full_goal_complete':False})
        manifests.append(dict(path=str(path),sha256=sha(path.read_bytes()),kind=kind,records=len(rows),counts=dict(counts)))
    assert Counter(r['editorial_decision'] for r in all_decisions)=={'revise':16,'retain-wording':8}
    ROOT.mkdir(parents=True);save(ROOT/'all24_clean_first_contextual_decisions_with_two_companions.json',dict(manuscripts=manifests,
        whole_exchange_objects=24,source_speeches=21,source_choice_labels=3,revised=16,retained=8,retained_speeches=7,retained_choice_labels=1,
        all8_retentions_individually_justified=True,all24_records_reviewed_as_one_exchange_with_three_original_response_paths=True,
        source_context_localization_naturalness_true_formatting_false=True,
        evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,Path(comparison['terms']),Path(prose.__file__),Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B197:21 speeches/3 labels;16 revisions/8 individual retentions. Native formatting,relocation,English actual and release pending;zero completion credit.')
