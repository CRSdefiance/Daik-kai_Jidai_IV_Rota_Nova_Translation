"""Record all14 B179 contextual decisions; native/display/release gates stay open."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B179_prose_v4720 as prose
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_B179_author_v4721')
COMPARISON=Path('work/analysis/lil_B179_comparison_v4719/all14_current_effective_comparison_packet.json')
GLOSS=Path('work/analysis/lil_B179_clean_context_v4707/all14_complete_B179_exchange_and_fresh_glosses.json')
OUTPUT=Path('translations/lil_B179_editorial_manuscript_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    comparison,gloss=map(read,[COMPARISON,GLOSS]);source=read(comparison['source_context'])
    assert gloss['all14_clean_source_read_and_individually_glossed_before_predecessor_English']
    assert comparison['source_context_sha256']==sha(Path(comparison['source_context']).read_bytes())
    assert len(prose.REVISIONS)==8 and len(prose.RETAIN_NOTES)==6
    assert not set(prose.REVISIONS)&set(prose.RETAIN_NOTES)
    assert set(prose.REVISIONS)|set(prose.RETAIN_NOTES)=={r['source_record_index'] for r in source['records']}
    doc=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],
        source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_prose_or_completion_credit_added=0,formatting_review_pending=True,
        status='source-context-localization-naturalness-reviewed;formatting-native-references-representative-release-pending',
        whole_exchange_context=gloss['whole_exchange_context'],clean_first_notes_are_historical_and_precede_current_native_bindings=True)
    dependencies={
        'source_context':comparison['source_context'],'control_contract':comparison['control_proof'],
        'whole_exchange_context_notes':str(GLOSS),
        'actor_voice_contract':'work/analysis/lil_B179_voices_v4709/current3_static_names_voices_and207_catalog_rebind.json',
        'branch_proof':'work/analysis/lil_B179_branches_v4711/original_relative_skip_operand_proof.json',
        'source_entry_proof':'work/analysis/lil_B179_entry_v4712/source_EV2_B179_action_dependency_and_native_getter_binding.json',
        'source_effect_and_predicate_contract':'work/analysis/lil_B179_controls_v4714/one_A000_no_C200_single_end_and2_source_leaves.json',
        'actor_terminology_reconciliation':comparison['terms_binding'],
        'source_nameplate_consumer_proof':'work/analysis/lil_B179_names_v4713b/six_original_Barkeep_Patron_Retainer_name_consumers.json',
        'effective_current_comparison':str(COMPARISON),
    }
    for key,path in dependencies.items():
        doc[key],doc[key+'_sha256']=path,sha(Path(path).read_bytes())
    speakers={92:'Barkeep',96:'Patron',152:'Sailor',254:'Impersonal fashion notice'}
    rows=[]
    for original in comparison['records']:
        row=deepcopy(original);old=row['current_effective_paragraph']
        for macro in ['FI','FA','FO']:
            old=old.replace(macro,'{MACRO:'+macro+'}')
        index=row['source_record_index']
        body,note=prose.REVISIONS[index] if index in prose.REVISIONS else (old,prose.RETAIN_NOTES[index])
        assert body==body.strip() and '\n' not in body and '  ' not in body and all(ord(c)<128 for c in body)
        assert '%' not in body and not any(tag in body for tag in ['{LB','{PAD','{SPEAKER:'])
        for macro in ['FI','FA','FO']:
            assert bytes.fromhex(row['source_hex']).count(macro.encode())==body.count('{MACRO:'+macro+'}')
        decision='retain-wording' if body==old else 'revise'
        assert (decision=='revise')==(index in prose.REVISIONS)
        row.update(source_meaning=row['fresh_source_gloss'],english='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body,
            localization_note=note,editorial_decision=decision,current_stored_English=row['current_raw_storage_English'],
            effective_predecessor_paragraph=old,
            comparison_basis='Original native macro template;NFKC presentation forms and collapsed legacy whitespace;raw/effective provenance remains distinct.',
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            context=gloss['whole_exchange_context'],speaker=speakers[row['source_selector']],prose_author_module=str(Path(prose.__file__)),
            status=doc['status'],editorial_predecessor_English_comparison_pending=False,full_clean_context_precedes_comparison=True,
            current_macro_dispatch_bound=True,current_complete_native_display_pending=True,current_native_UI_body_explicit_unexecuted_boundary=True,
            current_effective_native_dispatch_proof=comparison['control_proof'],
            original_native_display_consumer='original_null_actor_24310_then5473C_FE' if row['kind']=='system-FE' else 'original_progressive_54020')
        if decision=='retain-wording':row['fresh_retained_wording_justification']=note
        rows.append(row)
    counts=Counter(r['editorial_decision'] for r in rows)
    assert counts=={'revise':8,'retain-wording':6}
    assert sum(r['kind']=='system-FE' for r in rows)==1 and len(rows)==14
    terms=read(comparison['terms_binding'])
    doc.update(separate_untranslated_city_alias_lead=terms['separate_untranslated_city_alias_lead'],separate_untranslated_city_alias_lead_sha256=terms['separate_untranslated_city_alias_lead_sha256'])
    doc.update(manuscript_kind='speech',prose_companions=[],records=rows,revised=8,retained=6)
    ROOT.mkdir(parents=True);save(OUTPUT,doc)
    save(ROOT/'all14_clean_first_contextual_decisions.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        decision_counts=dict(counts),source_context=comparison['source_context'],source_context_sha256=comparison['source_context_sha256'],
        all14_clean_then_current_whole_exchange_read=True,all6_retentions_individually_justified=True,
        source_context_localization_naturalness_gates_true_formatting_false=True,
        Barkeep_Patron_Sailor_dialogue_names_bound_distinct_catalogue_Retainer_and_FE_impersonal=True,
        source_FI0_FA0_FO0_preserved=True,Sao_Jorge20_byte_owned_city_span_and_Wine_pointer_bound_separate_Japanese_alias_lead_open=True,
        challenge_concession_repeated_taste_questions_hyperbole_trial_order_service_three_gulps_verdict_repeat_joining_order_and_forecast_preserved=True,
        no_invented_prior_drink_brand_drunkenness_rank_master_relationship_price_completed_sale_or_earned_boom=True,
        evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,GLOSS,Path(prose.__file__),Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(objects=14,progressive=13,FE=1,decisions=dict(counts),FI=0,FA=0,FO=0,formatting_pending=True,credit=0))
