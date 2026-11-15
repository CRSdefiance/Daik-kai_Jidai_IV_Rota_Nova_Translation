"""Save all17 contextual decisions with individual reasons and pending native gates."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B198_prose_v5717 as prose
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B198_author_v5718')
COMPARISON=Path('work/analysis/lil_B198_comparison_v5716/all17_complete_clean_and_predecessor_exchange.json')
OUTPUT=Path('translations/lil_B198_editorial_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    comparison=read(COMPARISON);source=read(comparison['source_context']);terms=read(comparison['terms'])
    assert terms['all_clean_first_glosses_and_original_actual_context_precede_predecessor_speech_comparison']
    assert len(prose.REVISIONS)==12 and len(prose.RETAIN_NOTES)==5 and not set(prose.REVISIONS)&set(prose.RETAIN_NOTES)
    assert set(prose.REVISIONS)|set(prose.RETAIN_NOTES)=={r['source_record_index'] for r in source['records']}
    base=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],
        current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_prose_or_completion_credit_added=0,formatting_review_pending=True,
        status='source-context-localization-naturalness-reviewed;native-format-reference-English-actual-release-pending',
        whole_exchange_context=terms['complete_exchange_progression'])
    deps=dict(source_context=comparison['source_context'],whole_exchange_context_notes=source['whole_exchange_context_notes'],
        contextual_reconciliation=comparison['terms'],actor_terminology_reconciliation=comparison['terms'],effective_current_comparison=str(COMPARISON),
        actor_voice_contract='work/analysis/lil_B198_voices_v5703/current207_catalog_eight_voices_and_two_source_selectors.json',
        control_contract='work/analysis/lil_B198_dispatches_v5704/all17_source_current_dispatches_no_macros_and12_control_leaves.json',
        branch_proof='work/analysis/lil_B198_branches_v5706/original_relative_skip_operand_proof.json',
        source_entry_proof='work/analysis/lil_B198_entry_v5705/source_EV2_B198_action_dependency_and_native_getter_binding.json',
        source_effect_and_predicate_contract='work/analysis/lil_B198_controls_v5710c/twelve_exact_leaves_two_predicates_resource_picture_seven_structural_pairs_and_end.json',
        source_nameplate_consumer_proof='work/analysis/lil_B198_names_v5707/four_original_progressive_and_catalogue_name_consumers.json',
        source_name_literal_scope_proof='work/analysis/lil_B198_source_names_v5711/two_actors_all_clean_fields_and_current_consumers.json',
        actual_original_response_paths=terms['source_actual_paths'])
    for key,path in deps.items():base[key]=path;base[key+'_sha256']=sha(Path(path).read_bytes())
    rows=[]
    for original in comparison['records']:
        r=deepcopy(original);index=r['source_record_index'];old=r['previous_paragraph']
        decision='revise' if index in prose.REVISIONS else 'retain-wording'
        body,note=prose.REVISIONS[index] if index in prose.REVISIONS else (old,prose.RETAIN_NOTES[index])
        assert (body.isascii() or index in [49,76] and body=='……') and body==' '.join(body.split())
        assert not any(v in body for v in ['%','{LB','{PAD','{MACRO:']) and (body!=old)==(decision=='revise')
        speaker='Unattributed Namahage-encounter voice' if r['source_selector']==254 else terms['approved_prose_names'][str(r['source_selector'])]
        r.update(english='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+body,speaker=speaker,
            source_meaning=r['fresh_source_gloss'],context=terms['complete_exchange_progression'],localization_note=note,
            editorial_decision=decision,effective_predecessor_paragraph=old,full_clean_context_precedes_comparison=True,
            editorial_predecessor_English_comparison_pending=False,current_macro_dispatch_bound=True,current_complete_native_display_pending=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status=base['status'],
            prose_author_module=str(Path(prose.__file__)),source_prose_or_completion_credit_added=0,record_index=r['current_record_index'],
            current_native_UI_body_explicit_unexecuted_boundary=True,
            original_native_display_consumer='original_null_actor_24310_then5473C_FE' if r['kind']=='system-FE' else 'original_progressive_54020')
        if decision=='retain-wording':r['fresh_retained_wording_justification']=note
        rows.append(r)
    counts=Counter(r['editorial_decision'] for r in rows);assert counts=={'revise':12,'retain-wording':5}
    save(OUTPUT,{**base,'records':rows,'revised':12,'retained':5,
        'no_authored_line_break_alignment_spaces_or_fit_driven_prose_shortening':True,
        'all_four_chant_calls_three_direct_questions_dream_and_prospective_handover_preserved':True,
        'Namahage_reference_retained_without_new_spoken_item_title_or_folklore_game_facts':True,
        'actual_source_speeches15_offline_only_Angelo_conditional_speeches2':True,
        'existing_names_retained_source_bound_no_new_global_name_review_credit':True,'full_goal_complete':False})
    ROOT.mkdir(parents=True)
    save(ROOT/'all17_clean_first_contextual_decisions.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        objects=17,revised=12,retained=5,all5_retentions_individually_justified=True,
        source_context_localization_naturalness_true_formatting_false=True,
        evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,Path(comparison['terms']),Path(prose.__file__),Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B19817 contextual decisions:12 revisions/five justified retentions. Native format,relocation,English actual and registered release pending;zero credit.')
