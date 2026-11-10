"""Record all8 clean-first contextual decisions; native formatting remains pending."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B185_prose_v5095 as prose
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B185_author_v5096')
COMPARISON=Path('work/analysis/lil_B185_comparison_v5094/all8_complete_clean_and_predecessor_exchange.json')
OUTPUT=Path('translations/lil_B185_editorial_manuscript_v1.json')
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
        actor_voice_contract='work/analysis/lil_B185_voices_v5088/current207_catalog_eight_voices_and_two_source_selectors.json',
        control_contract='work/analysis/lil_B185_dispatches_v5089/all8_source_current_dispatches_no_macros_and3_control_leaves.json',
        branch_proof='work/analysis/lil_B185_controls_v5091/A000_C200_single_end_and_no_relative_or_predicate_contract.json',
        source_entry_proof='work/analysis/lil_B185_entry_v5090/source_EV2_B185_action_dependency_and_native_getter_binding.json',
        source_effect_and_predicate_contract='work/analysis/lil_B185_controls_v5091/A000_C200_single_end_and_no_relative_or_predicate_contract.json',
        current_C200_source_ownership_proof='work/analysis/lil_B185_controls_v5091/A000_C200_single_end_and_no_relative_or_predicate_contract.json',
        source_nameplate_consumer_proof='work/analysis/lil_B185_names_v5092/four_original_progressive_and_catalogue_name_consumers.json',
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
    counts=Counter(r['editorial_decision'] for r in rows);assert counts=={'revise':4,'retain-wording':4}
    doc.update(records=rows,revised=4,retained=4,two_clean_couple_roles_without_marriage_age_or_kinship_inference=True,
        source_explicit_reported_sales_prices_and_cold_coat_wish_preserved=True,
        FE_prospective_Furs_Stockholm_notice_distinct_from_reported_current_sales_prices=True,source_all11_linear_commands_A000_C200_and_end_preserved=True,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(OUTPUT,doc)
    save(ROOT/'all8_clean_first_contextual_decisions.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),decision_counts=dict(counts),
        all4_retentions_individually_justified=True,all8_records_reviewed_as_one_exchange=True,
        source_context_localization_naturalness_true_formatting_false=True,new_emulator_runs=0,new_review_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,gp,Path(prose.__file__),Path(__file__)]},full_goal_complete=False))
    print('B185:8 whole-exchange decisions,4 revisions/4 justified retentions. Native formatting pending;zero credit.')
