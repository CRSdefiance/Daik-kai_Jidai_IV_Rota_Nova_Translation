"""Record all17 clean-first contextual decisions; native formatting remains pending."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B190_prose_v5322b as prose
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B190_author_v5323b')
COMPARISON=Path('work/analysis/lil_B190_comparison_v5321/all17_complete_clean_and_predecessor_exchange.json')
OUTPUT=Path('translations/lil_B190_editorial_manuscript_v1b.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();comparison=read(COMPARISON);source=read(comparison['source_context'])
    gp=Path(source['whole_exchange_context_notes']);gloss=read(gp);terms=read(comparison['terms'])
    assert gloss['read_no_predecessor_English'] and len(gloss['records'])==17
    assert set(prose.REVISIONS)|set(prose.RETAIN_NOTES)=={r['source_record_index'] for r in source['records']}
    assert not set(prose.REVISIONS)&set(prose.RETAIN_NOTES)
    doc=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],
        current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_prose_or_completion_credit_added=0,formatting_review_pending=True,status='source-context-localization-naturalness-reviewed;native-layout-relocation-actual-release-pending',
        whole_exchange_context=gloss['complete_exchange_progression'],manuscript_kind='speech',prose_companions=[])
    deps=dict(source_context=comparison['source_context'],whole_exchange_context_notes=str(gp),
        actor_voice_contract='work/analysis/lil_B190_voices_v5315/current207_catalog_eight_voices_and_two_source_selectors.json',
        control_contract='work/analysis/lil_B190_dispatches_v5316/all17_source_current_dispatches_no_macros_and6_control_leaves.json',
        branch_proof='work/analysis/lil_B190_branches_v5318/original_relative_skip_operand_proof.json',
        source_entry_proof='work/analysis/lil_B190_entry_v5317/source_EV2_B190_action_dependency_and_native_getter_binding.json',
        source_effect_and_predicate_contract='work/analysis/lil_B190_controls_v5318/one_predicate_three_A000_C200_six_relative_sites_and_single_end.json',
        current_C200_source_ownership_proof='work/analysis/lil_B190_controls_v5318/one_predicate_three_A000_C200_six_relative_sites_and_single_end.json',
        source_nameplate_consumer_proof='work/analysis/lil_B190_names_v5319/four_original_progressive_and_catalogue_name_consumers.json',
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
    counts=Counter(r['editorial_decision'] for r in rows);assert counts=={'revise':10,'retain-wording':7}
    doc.update(records=rows,revised=10,retained=7,
        source_Port_Worker119_and_progressive_Sailor159_catalogue_Retainer159_voices0_4_preserved=True,
        source_unknown_cause_retail_medicine_reported_one_go_cure_explicit_doubt_and_panacea_reputation_preserved=True,
        source_owner_not_invented_rank_kinship_or_employment_and_wish_not_joint_recommendation=True,
        source_common_knowledge_hyperbole_and_apparent_truth_are_character_claims=True,
        source_shopping_proposal_not_completed_purchase_use_or_recovery=True,
        source_Medicine13_full_and_compact_Med_Havana_binding_preserved=True,
        source29_commands_one500_predicate_six_relatives_three_A000_C200_end_and_two_tailzeros_preserved=True,
        FE_prospective_Medicine_Havana_notice_distinct_from_reported_efficacy_and_earlier_location=True,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(OUTPUT,doc)
    save(ROOT/'all17_clean_first_contextual_decisions.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),decision_counts=dict(counts),
        all7_retentions_individually_justified=True,all17_records_reviewed_as_one_exchange=True,
        source_context_localization_naturalness_true_formatting_false=True,new_emulator_runs=0,new_review_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,gp,Path(prose.__file__),Path(__file__)]},full_goal_complete=False))
    print('B190:17 whole-exchange decisions,10 revisions/7 justified retentions. Native formatting pending;zero credit.')
