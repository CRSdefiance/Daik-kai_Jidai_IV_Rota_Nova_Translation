"""Review24 speeches and12 choice labels as one complete bargaining exchange."""
import re
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B196_prose_v5604 as prose
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B196_author_v5605')
COMPARISON=Path('work/analysis/lil_B196_comparison_v5603/all36_complete_clean_and_predecessor_exchange_with_six_choices.json')
OUTPUTS=[Path('translations/lil_B196_editorial_manuscript_v1.json'),Path('translations/lil_B196_choice_manuscript_v1.json')]
PRICES={218:200000,582:100000,832:70000,1156:50000,1370:40000,1588:30000}
if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS)
    comparison=read(COMPARISON);source=read(comparison['source_context']);terms=read(comparison['terms'])
    gp=Path(source['whole_exchange_context_notes']);gloss=read(gp)
    assert gloss['read_no_predecessor_English'] and len(gloss['records'])==24 and len(gloss['choices'])==6
    assert len(prose.REVISIONS)==15 and len(prose.RETAIN_NOTES)==9 and not set(prose.REVISIONS)&set(prose.RETAIN_NOTES)
    assert set(prose.REVISIONS)|set(prose.RETAIN_NOTES)=={r['source_record_index'] for r in source['records']}
    base=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],
        current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_prose_or_completion_credit_added=0,formatting_review_pending=True,
        status='source-context-localization-naturalness-reviewed;native-format-choice-reference-actual-release-pending',
        whole_exchange_context=gloss['complete_exchange_progression'],complete_contextual_review_includes_six_prices_all_branches_and_twelve_labels=True,
        total_editorial_objects_across_speech_and_choice_companions=36)
    deps=dict(source_context=comparison['source_context'],whole_exchange_context_notes=str(gp),
        actor_voice_contract='work/analysis/lil_B196_voices_v5591/current207_catalog_eight_voices_and_six_source_selectors.json',
        control_contract='work/analysis/lil_B196_dispatches_v5592/all24_source_current_dispatches_FI1_and37_control_leaves.json',
        branch_proof='work/analysis/lil_B196_branches_v5595/original_relative_skip_operand_proof.json',
        source_entry_proof='work/analysis/lil_B196_entry_v5593/source_EV2_B196_action_dependency_and_native_getter_binding.json',
        source_effect_and_predicate_contract='work/analysis/lil_B196_controls_v5596/seven_unforced_predicates_six_picture_pairs_twenty_resource_cases_fourteen_opaque_effect_pairs.json',
        source6003_and_end_contract='work/analysis/lil_B196_6003_ends_v5597/source6003_ten_boundary_cases_and_seventy_guarded_end_cases.json',
        source_nameplate_consumer_proof='work/analysis/lil_B196_names_v5594/twelve_original_progressive_and_catalogue_name_consumers.json',
        source_name_literal_scope_proof='work/analysis/lil_B196_source_names_v5598/six_source_name_fields_twelve_current_consumers_and_literal_scope.json',
        source_financial_context=terms['source_financial_context'],actor_terminology_reconciliation=comparison['terms'],effective_current_comparison=str(COMPARISON))
    for key,path in deps.items():base[key]=path;base[key+'_sha256']=sha(Path(path).read_bytes())
    groups={'speech':[],'player-choices':[]};all_decisions=[]
    for original in comparison['records']:
        r=deepcopy(original);choice=r['kind']=='typed-choice-label';old=r['previous_macro_template_paragraph']
        if choice:
            expected=['Buy','Pass'][r['option_index']];assert old==expected
            body=old;decision='retain-wording';price=PRICES[r['command_offset']]
            if r['option_index']==0:
                note=f'At the{price:,}-gold offer,Buy is the natural American menu verb for source買う. Keep it as acceptance of this current offer,not a new item description,proof of funds,discount promise or global purchase instruction. The same wording works independently at this exact source menu.'
            else:
                note=f'At the{price:,}-gold offer,Pass is a natural concise refusal of the current offer and preserves source買わない. It does not relabel refusal as Haggle,promise another discount,or certify a final exit. Keep this existing wording at this menu;the original branch controls determine the outcome.'
            speaker='Player choice at the current asking price';english=body
        else:
            index=r['source_record_index'];decision='revise' if index in prose.REVISIONS else 'retain-wording'
            body,note=prose.REVISIONS[index] if index in prose.REVISIONS else (old,prose.RETAIN_NOTES[index])
            speaker='Impersonal branch-specific Charm notice' if r['source_selector']==254 else terms['approved_prose_names'][str(r['source_selector'])]
            english='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+body
        assert body.isascii() and body==' '.join(body.split()) and not any(v in body for v in ['%','{LB','{PAD'])
        assert (body!=old)==(decision=='revise'),r['id']
        source_macros=re.findall(rb'FI|FA|FO',bytes.fromhex(r['source_hex']))
        target_macros=[m.encode('ascii') for m in re.findall(r'\{MACRO:(FI|FA|FO)\}',english)]
        assert source_macros==target_macros,r['id']
        r.update(english=english,speaker=speaker,source_meaning=r['fresh_source_gloss'],context=gloss['complete_exchange_progression'],
            localization_note=note,editorial_decision=decision,effective_predecessor_paragraph=old,
            full_clean_context_precedes_comparison=True,editorial_predecessor_English_comparison_pending=False,
            current_macro_dispatch_bound=not choice,current_complete_native_display_pending=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            status=base['status'],prose_author_module=str(Path(prose.__file__)),source_prose_or_completion_credit_added=0)
        if choice:r['current_native_typed_choice_font_reference_and_outcome_binding_pending']=True
        else:
            r.update(record_index=r['current_record_index'],current_native_UI_body_explicit_unexecuted_boundary=True,
                original_native_display_consumer='original_null_actor_24310_then5473C_FE' if r['kind']=='system-FE' else 'original_progressive_54020')
        if decision=='retain-wording':r['fresh_retained_wording_justification']=note
        groups['player-choices' if choice else 'speech'].append(r);all_decisions.append(r)
    manifests=[]
    for path,kind in zip(OUTPUTS,['speech','player-choices'],strict=True):
        rows=groups[kind];counts=Counter(r['editorial_decision'] for r in rows)
        assert counts==({'revise':15,'retain-wording':9} if kind=='speech' else {'retain-wording':12})
        doc={**deepcopy(base),'manuscript_kind':kind,'prose_companions':[str(p) for p in OUTPUTS if p!=path],
            'records':rows,'revised':counts.get('revise',0),'retained':counts['retain-wording'],
            'source_six_asking_prices_exact_and_currency_gold_bound':True,
            'source_six_actor_voices_gender_neutral_seller_and_no_invented_relationships':True,
            'source_personal_tentative_advice_halving_at_least_two_more_pleading_regret_and_future_sale_intent_preserved':True,
            'source_R302_elliptical_judgment_retained_without_assigning_an_explicit_you_or_I':True,
            'source_early_FI_Charm_plus1_branch_and_all_twelve_literal_choice_meanings_preserved':True,
            'no_authored_line_break_alignment_spaces_or_fit_driven_prose_shortening':True,
            'actual_B196_scene_and_custom_player_name_behavior_not_claimed':True,'full_goal_complete':False}
        save(path,doc);manifests.append(dict(path=str(path),sha256=sha(path.read_bytes()),kind=kind,records=len(rows),counts=dict(counts)))
    assert len(all_decisions)==36 and Counter(r['editorial_decision'] for r in all_decisions)=={'revise':15,'retain-wording':21}
    ROOT.mkdir(parents=True);save(ROOT/'all36_clean_first_contextual_decisions_with_two_companions.json',dict(manuscripts=manifests,
        whole_exchange_objects=36,source_speeches=24,source_choice_labels=12,revised=15,retained=21,
        retained_speeches=9,retained_choice_labels=12,all21_retentions_individually_justified=True,
        all36_records_reviewed_as_one_exchange_with_distinct_price_branches=True,source_context_localization_naturalness_true_formatting_false=True,
        evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,gp,Path(prose.__file__),Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B196 authored:24 speeches/12 labels,15 revisions/21 individually justified retentions. All six price branches and FI notice retained;native display/choices/release pending;zero credit.')
