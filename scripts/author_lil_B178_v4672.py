"""Record all13 B178 contextual decisions; native/display/release gates stay open."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B178_prose_v4671 as prose
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_B178_author_v4672')
COMPARISON=Path('work/analysis/lil_B178_comparison_v4670/all13_current_effective_comparison_packet.json')
GLOSS=Path('work/analysis/lil_B178_clean_context_v4661/all13_complete_B178_exchange_and_fresh_glosses.json')
OUTPUT=Path('translations/lil_B178_editorial_manuscript_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    comparison,gloss=map(read,[COMPARISON,GLOSS]);source=read(comparison['source_context'])
    assert gloss['all13_clean_source_read_and_individually_glossed_before_predecessor_English']
    assert comparison['source_context_sha256']==sha(Path(comparison['source_context']).read_bytes())
    assert len(prose.REVISIONS)==2 and len(prose.RETAIN_NOTES)==11
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
        'actor_voice_contract':'work/analysis/lil_B178_voices_v4663/current3_static_names_voices_and207_catalog_rebind.json',
        'branch_proof':'work/analysis/lil_B178_branches_v4665/original_relative_skip_operand_proof.json',
        'source_entry_proof':'work/analysis/lil_B178_entry_v4666/source_EV2_B178_action_dependency_and_native_getter_binding.json',
        'source_effect_and_predicate_contract':'work/analysis/lil_B178_controls_v4668/one_A000_C200_single_end_and3_source_leaves.json',
        'actor_terminology_reconciliation':comparison['terms_binding'],
        'source_nameplate_consumer_proof':'work/analysis/lil_B178_names_v4667b/six_original_Lady166_167_168_name_consumers_readonly_paths.json',
        'effective_current_comparison':str(COMPARISON),
    }
    for key,path in dependencies.items():
        doc[key],doc[key+'_sha256']=path,sha(Path(path).read_bytes())
    speakers={166:'Lady',167:'Lady',168:'Lady',254:'Impersonal fashion notice'}
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
    assert counts=={'revise':2,'retain-wording':11}
    assert sum(r['kind']=='system-FE' for r in rows)==1 and len(rows)==13
    doc.update(manuscript_kind='speech',prose_companions=[],records=rows,revised=2,retained=11)
    ROOT.mkdir(parents=True);save(OUTPUT,doc)
    save(ROOT/'all13_clean_first_contextual_decisions.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        decision_counts=dict(counts),source_context=comparison['source_context'],source_context_sha256=comparison['source_context_sha256'],
        all13_clean_then_current_whole_exchange_read=True,all11_retentions_individually_justified=True,
        source_context_localization_naturalness_gates_true_formatting_false=True,
        three_Lady_native_names_bound_and_FE_notice_impersonal=True,
        source_FI0_FA0_FO0_preserved=True,Amsterdam_two_inline_city_spans_and_Wheat_source_current_pointers_bound=True,
        home_baking_enthusiasm_husband_example_curiosity_bakery_boast_offer_pleased_reply_ingredient_question_first_wheat_and_forecast_preserved=True,
        no_added_rank_kinship_recipe_quantities_prices_completed_purchase_or_earned_boom_exact_speaker_assignments_preserved=True,
        evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,GLOSS,Path(prose.__file__),Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(objects=13,progressive=12,FE=1,decisions=dict(counts),FI=0,FA=0,FO=0,formatting_pending=True,credit=0))
