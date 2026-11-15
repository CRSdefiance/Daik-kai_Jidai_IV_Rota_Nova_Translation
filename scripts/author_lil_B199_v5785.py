"""Save all31 whole-exchange prose decisions with exact effective-current provenance."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B199_prose_v5784 as prose
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B199_author_v5785')
COMPARISON=Path('work/analysis/lil_B199_comparison_v5783b/all31_complete_clean_and_predecessor_exchange.json')
OUTPUT=Path('translations/lil_B199_editorial_manuscript_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    comparison=read(COMPARISON);source=read(comparison['source_context']);terms=read(comparison['contextual_reconciliation'])
    assert comparison['source31_complete_glosses_before_previous_English'] and terms['source_actual_speeches']==31
    assert comparison['current_registered_catalog_matches']==1 and comparison['registered_R58_effective_Camille_question_and_summons_previously_integrated']
    assert len(prose.REVISIONS)==11 and len(prose.RETAIN_NOTES)==20 and not set(prose.REVISIONS)&set(prose.RETAIN_NOTES)
    assert set(prose.REVISIONS)|set(prose.RETAIN_NOTES)=={r['source_record_index'] for r in source['records']}
    base=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],
        current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_prose_or_completion_credit_added=0,formatting_review_pending=True,
        status='source-context-localization-naturalness-reviewed;native-format-reference-English-actual-release-pending',
        whole_exchange_context=terms['complete_exchange_progression'])
    deps=dict(source_context=comparison['source_context'],whole_exchange_context_notes=source['whole_exchange_context_notes'],
        contextual_reconciliation=comparison['contextual_reconciliation'],actor_terminology_reconciliation=comparison['contextual_reconciliation'],
        effective_current_comparison=str(COMPARISON),
        actor_voice_contract='work/analysis/lil_B199_voices_v5768/current207_catalog_eight_voices_and_three_source_selectors.json',
        control_contract='work/analysis/lil_B199_dispatches_v5769/all31_source_current_dispatches_one_FI_and16_control_leaves.json',
        branch_proof='work/analysis/lil_B199_branches_v5771/original_relative_skip_operand_proof.json',
        source_entry_proof='work/analysis/lil_B199_entry_v5770/source_EV2_B199_action_dependency_and_native_getter_binding.json',
        source_effect_and_predicate_contract='work/analysis/lil_B199_controls_v5778/sixteen_exact_leaves_four_resources_two_pictures_two47xx_pause_and_end.json',
        source_nameplate_consumer_proof='work/analysis/lil_B199_names_v5772/six_original_progressive_and_catalogue_name_consumers.json',
        source_name_literal_scope_proof='work/analysis/couple_context_review_v5775/five_whole_source_contexts_paired_label_draft_and_B199_name_fields.json',
        actual_original_response_paths=terms['source_actual_paths'])
    for key,path in deps.items():base[key]=path;base[key+'_sha256']=sha(Path(path).read_bytes())
    rows=[]
    for original in comparison['records']:
        r=deepcopy(original);index=r['source_record_index'];old=r['previous_paragraph']
        decision='revise' if index in prose.REVISIONS else 'retain-wording'
        body,note=prose.REVISIONS[index] if decision=='revise' else (old,prose.RETAIN_NOTES[index])
        assert body.isascii() and body==' '.join(body.split())
        assert not any(v in body for v in ['%','{LB','{PAD','{MACRO:']) and (body!=old)==(decision=='revise')
        assert {m:body.count(m) for m in ['FI','FA','FO']}=={m:bytes.fromhex(r['source_hex'])[1:].count(m.encode()) for m in ['FI','FA','FO']}
        assert body.startswith('(')==(index in [70,115]) and body.endswith(')')==(index in [70,115])
        speaker='Impact and clatter sound effects' if r['source_selector']==254 else terms['approved_prose_names'][str(r['source_selector'])]
        r.update(english='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+body,speaker=speaker,
            source_meaning=r['fresh_source_gloss'],context=terms['complete_exchange_progression'],localization_note=note,
            editorial_decision=decision,effective_predecessor_paragraph=old,full_clean_context_precedes_comparison=True,
            editorial_predecessor_English_comparison_pending=False,current_macro_dispatch_bound=True,current_complete_native_display_pending=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status=base['status'],
            prose_author_module=str(Path(prose.__file__)),source_prose_or_completion_credit_added=0,record_index=r['current_record_index'],
            current_effective_macro_template_hex=r['previous_effective_template_body'].encode('cp932').hex(),
            current_effective_macro_template_English=r['previous_effective_template_body'],
            current_effective_paragraph=old,current_raw_storage_English=r['previous_raw_storage_body'],
            registered_runtime_catalog_entry=r['previous_registered_catalog_entry'],
            current_native_UI_body_explicit_unexecuted_boundary=True,
            original_native_display_consumer='original_null_actor_24310_then5473C_FE' if r['kind']=='system-FE' else 'original_progressive_54020')
        if decision=='retain-wording':r['fresh_retained_wording_justification']=note
        rows.append(r)
    counts=Counter(r['editorial_decision'] for r in rows);assert counts=={'revise':11,'retain-wording':20}
    save(OUTPUT,{**base,'records':rows,'revised':11,'retained':20,
        'no_authored_line_break_alignment_spaces_or_fit_driven_prose_shortening':True,
        'portrait_qualified_reputation_body_taunt_four_impacts_found_book_and_two_gift_corrections_preserved':True,
        'no_intended_gift_purchase_romance_kinship_rank_ownership_or_new_spoken_item_title':True,
        'one_original_FI_runtime_name_and_private_parentheses_retained':True,
        'R58_existing_registered_runtime_Camille_question_summons_retained_not_misreported_as_live_Kamil':True,
        'all31_source_speeches_observed_no_offline_only_source_lines':True,
        'existing_names_source_bound_no_new_global_name_localization_credit':True,
        'full_goal_complete':False})
    ROOT.mkdir(parents=True)
    save(ROOT/'all31_clean_first_contextual_decisions.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        objects=31,revised=11,retained=20,all20_retentions_individually_justified=True,
        source_context_localization_naturalness_true_formatting_false=True,
        existing_R58_catalog_correction_credited_and_retained=True,
        evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,Path(comparison['contextual_reconciliation']),Path(prose.__file__),Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B19931 whole-exchange decisions:11 revisions/20 justified retentions. Existing effective R58 retained;native layout,English scene and release pending. Zero credit.')
