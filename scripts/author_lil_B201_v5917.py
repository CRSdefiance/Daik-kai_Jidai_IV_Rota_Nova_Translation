"""Save26 contextual decisions after both clean source paths;native layout remains pending."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B201_prose_v5916 as prose
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_author_v5917')
COMPARISON=Path('work/analysis/lil_B201_comparison_v5915/all26_complete_clean_and_predecessor_exchange_including_two_choices.json')
OUTPUT=Path('translations/lil_B201_editorial_manuscript_v1.json')
MENU=Path('translations/lil_B201_choice_manuscript_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists() and not MENU.exists()
    comparison=read(COMPARISON);source=read(comparison['source_context']);terms=read(comparison['contextual_reconciliation'])
    assert comparison['all24_clean_glosses_and_two_label_glosses_precede_previous_English'] and terms['source_actual_speeches']==24 and not terms['offline_only_speeches']
    assert len(prose.REVISIONS)==len(prose.RETAIN_NOTES)==12 and not set(prose.REVISIONS)&set(prose.RETAIN_NOTES)
    assert set(prose.REVISIONS)|set(prose.RETAIN_NOTES)=={r['source_record_index'] for r in source['records']}
    base=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],
        source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],source_prose_or_completion_credit_added=0,
        formatting_review_pending=True,status='source-context-localization-naturalness-reviewed;native-format-reference-English-actual-and-registered-release-pending',
        whole_exchange_context=terms['complete_exchange_progression'])
    deps=dict(source_context=comparison['source_context'],whole_exchange_context_notes=source['whole_exchange_context_notes'],
        contextual_reconciliation=comparison['contextual_reconciliation'],actor_terminology_reconciliation=comparison['contextual_reconciliation'],effective_current_comparison=str(COMPARISON),
        actor_voice_contract='work/analysis/lil_B201_voices_v5903/current207_catalog_eight_voices_and_three_source_selectors.json',
        control_contract='work/analysis/lil_B201_dispatches_v5904/all24_source_current_dispatches_two_FI_and15_control_leaves.json',
        branch_proof='work/analysis/lil_B201_branches_v5906/original_relative_skip_operand_proof.json',
        source_entry_proof='work/analysis/lil_B201_entry_v5905/source_EV2_B201_action_dependency_and_native_getter_binding.json',
        source_effect_and_predicate_contract='work/analysis/lil_B201_controls_v5908/fifteen_exact_leaves_three_resources_two6003_picture_eight_structural_pairs_and_complete_end.json',
        source_nameplate_consumer_proof='work/analysis/lil_B201_names_v5907/six_original_progressive_and_catalogue_name_consumers.json',
        source_payment_proof='work/analysis/lil_B201_funds_v5912/one_exact100000_source_price_one_unforced_and_five_offline_payment_boundaries.json',
        actual_original_response_paths='work/analysis/lil_B201_source_paths_v5914/two_actual_source_choice_paths_all24_speeches_all53_commands_and_returns.json')
    for key,path in deps.items():base[key]=path;base[key+'_sha256']=sha(Path(path).read_bytes())
    rows=[]
    for original in comparison['records']:
        r=deepcopy(original);index=r['source_record_index'];old=r['previous_paragraph'];decision='revise' if index in prose.REVISIONS else 'retain-wording'
        body,note=prose.REVISIONS[index] if decision=='revise' else (old,prose.RETAIN_NOTES[index])
        assert body.isascii() and body==' '.join(body.split()) and not any(s in body for s in ['%','{LB','{PAD','{MACRO:'])
        assert (body!=old)==(decision=='revise')
        expected=bytes.fromhex(r['source_hex'])[1:].count(b'FI');assert body.count('FI')==expected and not any(m in body for m in ['FA','FO'])
        marked=body.replace('FI','{MACRO:FI}')
        speaker='Game status notification' if r['source_selector']==254 else terms['approved_prose_names'][str(r['source_selector'])]
        r.update(english='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+marked,speaker=speaker,source_meaning=r['fresh_source_gloss'],
            context=terms['complete_exchange_progression'],localization_note=note,editorial_decision=decision,effective_predecessor_paragraph=old,
            full_clean_context_precedes_comparison=True,editorial_predecessor_English_comparison_pending=False,current_macro_dispatch_bound=True,current_complete_native_display_pending=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status=base['status'],prose_author_module=str(Path(prose.__file__)),
            source_prose_or_completion_credit_added=0,record_index=r['current_record_index'],
            current_effective_macro_template_hex=r['previous_effective_template_body'].encode('cp932').hex(),current_effective_macro_template_English=r['previous_effective_template_body'],
            current_effective_paragraph=old,current_raw_storage_English=r['previous_raw_storage_body'],registered_runtime_catalog_entry=r['previous_registered_catalog_entry'],
            current_native_UI_body_explicit_unexecuted_boundary=True,original_native_display_consumer='original_null_actor_24310_then5473C_FE' if r['kind']=='system-FE' else 'original_progressive_54020')
        if decision=='retain-wording':r['fresh_retained_wording_justification']=note
        rows.append(r)
    assert Counter(r['editorial_decision'] for r in rows)=={'revise':12,'retain-wording':12}
    choices=[]
    for original in comparison['typed_choice_records']:
        r=deepcopy(original);body,note=prose.CHOICES[r['option_index']];assert body==r['previous_paragraph'].strip()
        r.update(english=body,speaker='Player decision at the final100000 price',source_meaning=r['fresh_source_gloss'],context=terms['complete_exchange_progression'],
            localization_note=note,editorial_decision='retain-wording',fresh_retained_wording_justification=note,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            previous_logical_label=r['previous_paragraph'].strip(),inherited_storage_padding_not_authored_alignment=True,source_prose_or_completion_credit_added=0)
        choices.append(r)
    assert len(choices)==2 and [r['english'] for r in choices]==['Buy','Pass']
    save(OUTPUT,{**base,'records':rows,'revised':12,'retained':12,
        'no_authored_line_break_alignment_spaces_or_fit_driven_prose_shortening':True,
        'all_seven_bargaining_values_final100000_hypothetical_free_request_hearsay_power_and_both_decisions_preserved':True,
        'Carlo_oyaji_address_not_translated_as_father_or_invented_age_rank_religion_nationality':True,
        'two_explicit_FI_macros_three_distinct_FE_recipients_and_Charm_Wits_Spirit_plus1_preserved':True,
        'all24_source_speeches_observed_no_offline_only_source_lines':True,
        'existing_Trader_label_contextual_retention_recorded_no_name_bytes_or_global_name_credit':True,
        'spoken_rope_unnamed_existing_Tireless_Hawser_card_not_new_title_or_effect_approval':True,
        'source_stat_item_payment_bodies_preserved_no_earned_affordability_or_natural_event_claim':True,'full_goal_complete':False})
    save(MENU,{**base,'format':'dk4-editorial-typed-choice-manuscript-v1','encoder':'typed-menu-relocatable-v1','records':choices,'revised':0,'retained':2,
        'source_choice_word':0x2100,'source_choice_count':2,'source_command_offset':880,'native_indices_and_both_actual_outcomes_preserved':True,'full_goal_complete':False})
    ROOT.mkdir(parents=True);save(ROOT/'all26_clean_first_contextual_decisions.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        choice_manuscript=str(MENU),choice_manuscript_sha256=sha(MENU.read_bytes()),objects=26,revised=12,retained=14,all14_retentions_individually_justified=True,
        source_context_localization_naturalness_true_formatting_false=True,all24_source_speeches_and_both_choices_observed=True,
        source_names_voice_resource_picture_two_FI_four_relatives_native_price_and_complete_end_bound=True,
        no_name_layer_or_English_ROM_or_registry_or_ledger_change=True,
        evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,Path(comparison['contextual_reconciliation']),Path(prose.__file__),Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B20126 contextual decisions:12 revisions/14 individually justified retentions. Two FI/three FE/two menu labels preserved;native formatting/English scene/release pending. Zero credit.')
