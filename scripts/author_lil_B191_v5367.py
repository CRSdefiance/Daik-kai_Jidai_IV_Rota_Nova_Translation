"""Record all13 clean-first contextual decisions; native formatting remains pending."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B191_prose_v5366 as prose
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B191_author_v5367')
COMPARISON=Path('work/analysis/lil_B191_comparison_v5365/all13_complete_clean_and_predecessor_exchange.json')
OUTPUT=Path('translations/lil_B191_editorial_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();comparison=read(COMPARISON);source=read(comparison['source_context'])
    gp=Path(source['whole_exchange_context_notes']);gloss=read(gp);terms=read(comparison['terms'])
    assert gloss['read_no_predecessor_English'] and len(gloss['records'])==13
    assert set(prose.REVISIONS)|set(prose.RETAIN_NOTES)=={r['source_record_index'] for r in source['records']}
    assert not set(prose.REVISIONS)&set(prose.RETAIN_NOTES)
    doc=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],
        current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_prose_or_completion_credit_added=0,formatting_review_pending=True,status='source-context-localization-naturalness-reviewed;native-layout-relocation-actual-release-pending',
        whole_exchange_context=gloss['complete_exchange_progression'],manuscript_kind='speech',prose_companions=[])
    deps=dict(source_context=comparison['source_context'],whole_exchange_context_notes=str(gp),
        actor_voice_contract='work/analysis/lil_B191_voices_v5357/current207_catalog_eight_voices_and_two_source_selectors.json',
        control_contract='work/analysis/lil_B191_dispatches_v5358/all13_source_current_dispatches_no_macros_and9_control_leaves.json',
        branch_proof='work/analysis/lil_B191_branches_v5360/original_relative_skip_operand_proof.json',
        source_entry_proof='work/analysis/lil_B191_entry_v5359/source_EV2_B191_action_dependency_and_native_getter_binding.json',
        source_effect_and_predicate_contract='work/analysis/lil_B191_controls_v5363/three_predicates_four_A000_C200_sixteen_relative_sites_and_single_end.json',
        current_C200_source_ownership_proof='work/analysis/lil_B191_controls_v5363/three_predicates_four_A000_C200_sixteen_relative_sites_and_single_end.json',
        source_nameplate_consumer_proof='work/analysis/lil_B191_names_v5361/four_original_progressive_and_catalogue_name_consumers.json',
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
    counts=Counter(r['editorial_decision'] for r in rows);assert counts=={'revise':5,'retain-wording':8}
    doc.update(records=rows,revised=5,retained=8,
        source_Square_Shopkeeper86_and_Sailor154_catalogue_Retainer_voices0_4_preserved=True,
        source_urgency_competitor_buyout_popularity_speed_conditional_profit_and_explicit_doubt_preserved=True,
        familiar_oyajisan_not_fatherhood_rank_employment_or_joint_profit_partnership=True,
        two_identical_doubts_and_distinct_enthusiastic_insistent_replies_preserved=True,
        delegation_and_sulking_request_not_completed_purchase_or_delivery=True,
        source_category14_Dyes_two_Calicut_aliases_and_tentative_FE_preserved=True,
        source38_commands_three500_700_500_predicates16_relatives_four_A000s_no_effect_paths_C200_end_two_tailzeros_preserved=True,
        no_earlier_location_earned_state_stock_price_or_profit_guarantee_invented=True,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(OUTPUT,doc)
    save(ROOT/'all13_clean_first_contextual_decisions.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),decision_counts=dict(counts),
        all8_retentions_individually_justified=True,all13_records_reviewed_as_one_exchange=True,
        source_context_localization_naturalness_true_formatting_false=True,new_emulator_runs=0,new_review_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,gp,Path(prose.__file__),Path(__file__)]},full_goal_complete=False))
    print('B191:13 whole-exchange decisions,5 revisions/8 justified retentions. Native formatting pending;zero credit.')
