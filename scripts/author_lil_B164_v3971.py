"""Produce49 individual contextual decisions with formatting explicitly pending."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B164_prose_v3970 as prose
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B164_author_v3971')
COMPARISON=Path('work/analysis/lil_B164_comparison_v3969/all49_current_effective_comparison_packet.json')
GLOSS=Path('work/analysis/lil_B164_clean_context_v3961/all49_complete_B164_exchange_and_fresh_glosses.json')
OUTPUTS=[Path('translations/lil_B164_editorial_manuscript_v1.json'),Path('translations/lil_B164_choice_manuscript_v1.json')]
if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS);comparison,gloss=map(read,[COMPARISON,GLOSS]);assert gloss['all49_clean_first_glosses_before_predecessor_English'];source=read(comparison['source_context']);terms=read(comparison['terms_binding']);assert len(prose.REVISIONS)==29 and len(prose.RETAIN_NOTES)==18 and not set(prose.REVISIONS)&set(prose.RETAIN_NOTES);assert set(prose.REVISIONS)|set(prose.RETAIN_NOTES)=={r['source_record_index'] for r in source['records']};base=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],source_prose_or_completion_credit_added=0,formatting_review_pending=True,status='source-context-localization-naturalness-reviewed;formatting-native-references-representative-release-pending',whole_exchange_context=gloss['whole_exchange_context'])
    dependencies={'source_context':comparison['source_context'],'control_contract':comparison['control_proof'],'whole_exchange_context_notes':str(GLOSS),'actor_voice_contract':'work/analysis/lil_B164_voices_v3963/current3_static_names_voices_and207_catalog_rebind.json','branch_proof':'work/analysis/lil_B164_branches_v3965/original_relative_skip_operand_proof.json','source_entry_proof':'work/analysis/lil_B164_entry_v3966/source_EV2_B164_action_dependency_and_native_getter_binding.json','source_effect_and_predicate_contract':'work/analysis/lil_B164_controls_v3968/four_branches_typed_advice_outcomes_resource_and9_leaves.json','actor_terminology_reconciliation':comparison['terms_binding'],'effective_current_comparison':str(COMPARISON)}
    for key,p in dependencies.items():base[key]=p;base[key+'_sha256']=sha(Path(p).read_bytes())
    docs=[];allrows=[]
    for choice in [False,True]:
        rows=[]
        for original in comparison['records']:
            if (original['kind']=='typed-choice-label')!=choice:continue
            r=deepcopy(original);old=r['current_effective_paragraph']
            if choice:body=old;note=prose.CHOICE_NOTES[r['option_index']]
            else:
                index=r['source_record_index'];body,note=prose.REVISIONS[index] if index in prose.REVISIONS else (old,prose.RETAIN_NOTES[index])
            assert body==body.strip() and '\n' not in body and '  ' not in body and all(ord(c)<128 for c in body) and '%' not in body;assert not any(m in body for m in ['{MACRO:','{LB','{PAD','{SPEAKER:']);decision='retain-wording' if body==old else 'revise';r.update(source_meaning=r['fresh_source_gloss'],english=body if choice else '{SPEAKER:'+format(r['source_selector'],'02X')+'}'+body,localization_note=note,editorial_decision=decision,current_stored_English=r['current_raw_storage_English'],effective_predecessor_paragraph=old,comparison_basis='Original runtime template;NFKC presentation forms and collapsed legacy whitespace;raw/effective provenance preserved.',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),context=gloss['whole_exchange_context'],speaker='Player choice about hearing advice;not employment' if choice else {2:'Lil',9:'Camille',13:'Cesare Tony'}[r['source_selector']],prose_author_module=str(Path(prose.__file__)),status=base['status'],editorial_older_English_comparison_pending=False,full_clean_context_precedes_comparison=True,current_macro_dispatch_bound=not choice,current_complete_native_display_pending=True,current_native_UI_body_explicit_unexecuted_boundary=True,current_effective_native_dispatch_proof=comparison['control_proof'])
            if decision=='retain-wording':r['fresh_retained_wording_justification']=note
            if choice:r['choice_consumer_selection_geometry_native_display_pending']=True
            else:r['original_native_display_consumer']='original_progressive_54020'
            rows.append(r);allrows.append(r)
        docs.append({**base,'manuscript_kind':'player-choices' if choice else 'speech','prose_companions':[str(OUTPUTS[0 if choice else 1])],'records':rows,'revised':sum(r['editorial_decision']=='revise' for r in rows),'retained':sum(r['editorial_decision']=='retain-wording' for r in rows)})
    counts=Counter(r['editorial_decision'] for r in allrows);assert len(allrows)==49 and counts=={'revise':29,'retain-wording':20};ROOT.mkdir(parents=True)
    for p,d in zip(OUTPUTS,docs,strict=True):save(p,d)
    save(ROOT/'all49_clean_first_contextual_decisions.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in OUTPUTS},decision_counts=dict(counts),source_context=comparison['source_context'],source_context_sha256=comparison['source_context_sha256'],all49_clean_then_current_complete_exchange_and_branches_read=True,source_context_localization_naturalness_gates_true_formatting_false=True,source0D_Cesare_Tony_and_current_runtime_Camille_replacement_preserved=True,all_source_numerical_facts_and_advice_choice_after_hiring_preserved=True,all20_retentions_individually_justified=True,evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,GLOSS,Path(prose.__file__),Path(__file__)]},new_emulator_runs=0,source_prose_orcompletion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False));print(dict(objects=49,speeches=47,choices=2,decisions=dict(counts),formatting_pending=True,credit=0))
