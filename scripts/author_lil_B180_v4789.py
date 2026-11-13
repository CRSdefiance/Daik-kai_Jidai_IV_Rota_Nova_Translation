"""Record all11 contextual editorial decisions; no formatting approval or credit."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B180_prose_v4788 as prose
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B180_author_v4789')
COMPARISON=Path('work/analysis/lil_B180_comparison_v4786/all11_complete_clean_and_predecessor_exchange.json')
OUTPUT=Path('translations/lil_B180_editorial_manuscript_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    comparison=read(COMPARISON);source=read(comparison['source_context'])
    gloss_path=Path(source['whole_exchange_context_notes']);gloss=read(gloss_path)
    assert gloss['all11_clean_source_read_and_individually_glossed_before_predecessor_English']
    assert set(prose.REVISIONS)|set(prose.RETAIN_NOTES)=={r['source_record_index'] for r in source['records']}
    assert not set(prose.REVISIONS)&set(prose.RETAIN_NOTES)
    doc=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],
        source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_prose_or_completion_credit_added=0,formatting_review_pending=True,
        status='source-context-localization-naturalness-reviewed;native-layout-relocation-actual-release-pending',
        whole_exchange_context=gloss['whole_exchange_context'],manuscript_kind='speech',prose_companions=[])
    dependencies=dict(source_context=comparison['source_context'],whole_exchange_context_notes=str(gloss_path),
        actor_voice_contract='work/analysis/lil_B180_voices_v4775/current207_catalog_eight_voices_and_two_source_selectors.json',
        control_contract='work/analysis/lil_B180_dispatches_v4776/all11_source_current_dispatches_no_macros_and7_control_leaves.json',
        branch_proof='work/analysis/lil_B180_branches_v4777/original_relative_skip_operand_proof.json',
        source_entry_proof='work/analysis/lil_B180_entry_v4778/source_EV2_B180_action_dependency_and_native_getter_binding.json',
        source_effect_and_predicate_contract='work/analysis/lil_B180_controls_v4780c/two_predicates_three_A000_C200_ten_relative_sites_and_single_end.json',
        predicate_RNG_ownership_proof='work/analysis/lil_B180_predicate500_v4782/all16_original500_predicate_RNG_ownership_cases.json',
        current_C200_source_ownership_proof='work/analysis/lil_B180_C200_v4784/source_fleet_descriptor_two_C200_contracts.json',
        source_nameplate_consumer_proof='work/analysis/lil_B180_names_v4779/four_original_Lady_name_consumers.json',
        actor_terminology_reconciliation=comparison['terms'],effective_current_comparison=str(COMPARISON))
    for key,path in dependencies.items():doc[key]=path;doc[key+'_sha256']=sha(Path(path).read_bytes())
    rows=[]
    for original in comparison['records']:
        row=deepcopy(original);i=row['source_record_index'];old=row['previous_paragraph']
        body,note=prose.REVISIONS[i] if i in prose.REVISIONS else (old,prose.RETAIN_NOTES[i])
        assert body.isascii() and body==' '.join(body.split()) and not any(s in body for s in ['%','{LB','{PAD','{MACRO:'])
        decision='revise' if i in prose.REVISIONS else 'retain-wording';assert (body!=old)==(decision=='revise')
        row.update(source_meaning=row['fresh_source_gloss'],english='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body,
            speaker='Impersonal fashion notice' if row['kind']=='system-FE' else 'Lady',
            context=gloss['whole_exchange_context'],localization_note=note,editorial_decision=decision,
            effective_predecessor_paragraph=old,full_clean_context_precedes_comparison=True,
            editorial_predecessor_English_comparison_pending=False,current_macro_dispatch_bound=True,
            current_complete_native_display_pending=True,current_native_UI_body_explicit_unexecuted_boundary=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status=doc['status'],
            prose_author_module=str(Path(prose.__file__)),
            original_native_display_consumer='original_null_actor_24310_then5473C_FE' if row['kind']=='system-FE' else 'original_progressive_54020')
        if decision=='retain-wording':row['fresh_retained_wording_justification']=note
        rows.append(row)
    counts=Counter(r['editorial_decision'] for r in rows);assert counts=={'revise':5,'retain-wording':6}
    doc.update(records=rows,revised=5,retained=6,no_third_person_gender_rank_relationship_brand_or_supplier_invented=True,
        Lady166_Lady167_static_selectors_and_impersonal_FE_preserved=True,source500_predicates_are_three_way_original_RNG_conditions=True,
        source_all28_commands_and_three_opaque_effect_alternatives_preserved=True,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(OUTPUT,doc)
    save(ROOT/'all11_clean_first_contextual_decisions.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),
        decision_counts=dict(counts),all6_retentions_individually_justified=True,
        unsupported_she_her_removed_and_Spices_corrected_to_Scents=True,
        all11_current_source_records_reviewed_as_one_complete_exchange=True,
        source_context_localization_naturalness_true_formatting_false=True,
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_orledger_change=True,
        dependencies={str(p):sha(p.read_bytes()) for p in [COMPARISON,gloss_path,Path(prose.__file__),Path(__file__)]},full_goal_complete=False))
    print(dict(objects=11,progressive=10,FE=1,revised=5,retained=6,native_layout_pending=True,ROM_changed=False,review_credit=0))
