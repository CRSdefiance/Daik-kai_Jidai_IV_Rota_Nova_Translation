"""Record44 contextual decisions with formatting and every release gate still pending."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import lil_B167_prose_v4128 as prose
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B167_author_v4129')
COMPARISON=Path('work/analysis/lil_B167_comparison_v4127/all29_current_effective_comparison_packet.json')
GLOSS=Path('work/analysis/lil_B167_clean_context_v4117/all29_complete_B167_exchange_and_fresh_glosses.json')
OUTPUTS=[Path('translations/lil_B167_editorial_manuscript_v1.json'),Path('translations/lil_B167_choice_manuscript_v1.json')]
if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS);comparison,gloss=map(read,[COMPARISON,GLOSS]);assert gloss['all29_clean_first_glosses_before_predecessor_English'];source=read(comparison['source_context'])
    assert len(prose.REVISIONS)==16 and len(prose.RETAIN_NOTES)==11 and not set(prose.REVISIONS)&set(prose.RETAIN_NOTES) and set(prose.REVISIONS)|set(prose.RETAIN_NOTES)=={r['source_record_index'] for r in source['records']}
    base=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],source_prose_or_completion_credit_added=0,formatting_review_pending=True,status='source-context-localization-naturalness-reviewed;formatting-native-references-representative-release-pending',whole_exchange_context=gloss['whole_exchange_context'])
    dependencies={'source_context':comparison['source_context'],'control_contract':comparison['control_proof'],'whole_exchange_context_notes':str(GLOSS),'actor_voice_contract':'work/analysis/lil_B167_voices_v4120/current5_static_names_voices_and207_catalog_rebind.json','branch_proof':'work/analysis/lil_B167_branches_v4122/original_relative_skip_operand_proof.json','source_entry_proof':'work/analysis/lil_B167_entry_v4123/source_EV2_B167_action_dependency_and_native_getter_binding.json','source_effect_and_predicate_contract':'work/analysis/lil_B167_controls_v4125/two_Cesare_queries_two_resources_four_paths_and6_leaves.json','actor_terminology_reconciliation':comparison['terms_binding'],'source_nameplate_consumer_proof':'work/analysis/lil_B167_names_v4124b/ten_original_names_owned_scratch_and_readonly_paths.json','effective_current_comparison':str(COMPARISON)}
    for key,p in dependencies.items():base[key]=p;base[key+'_sha256']=sha(Path(p).read_bytes())
    docs=[];allrows=[]
    for choice in [False,True]:
        rows=[]
        for original in comparison['records']:
            if (original['kind']=='typed-choice-label')!=choice:continue
            r=deepcopy(original);old=r['current_effective_paragraph']
            if not choice:
                for macro in ['FI','FA','FO']:old=old.replace(macro,'{MACRO:'+macro+'}')
            if choice:body=old;note=prose.CHOICE_NOTES[r['option_index']]
            else:
                index=r['source_record_index'];body,note=prose.REVISIONS[index] if index in prose.REVISIONS else (old,prose.RETAIN_NOTES[index])
            assert body==body.strip() and '\n' not in body and '  ' not in body and all(ord(c)<128 for c in body) and '%' not in body and not any(tag in body for tag in ['{LB','{PAD','{SPEAKER:'])
            for macro in ['FI','FA','FO']:assert bytes.fromhex(r['source_hex']).count(macro.encode())==body.count('{MACRO:'+macro+'}')
            decision='retain-wording' if body==old else 'revise'
            r.update(source_meaning=r['fresh_source_gloss'],english=body if choice else '{SPEAKER:'+format(r['source_selector'],'02X')+'}'+body,localization_note=note,editorial_decision=decision,current_stored_English=r['current_raw_storage_English'],effective_predecessor_paragraph=old,comparison_basis='Original runtime macro template;NFKC presentation forms andcollapsed legacy whitespace;raw/effective provenance remains distinct.',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),context=gloss['whole_exchange_context'],speaker='Player choice about hearing a sail lecture;not employment or payment' if choice else {2:'Lil',4:'Janus Pasar',13:'Cesare Tony',23:'Manuel Almeida',109:'Shipwright'}[r['source_selector']],prose_author_module=str(Path(prose.__file__)),status=base['status'],editorial_predecessor_English_comparison_pending=False,full_clean_context_precedes_comparison=True,current_macro_dispatch_bound=not choice,current_complete_native_display_pending=True,current_native_UI_body_explicit_unexecuted_boundary=True,current_effective_native_dispatch_proof=comparison['control_proof'])
            if decision=='retain-wording':r['fresh_retained_wording_justification']=note
            if choice:r['choice_consumer_selection_geometry_native_display_pending']=True
            else:r['original_native_display_consumer']='original_progressive_54020'
            rows.append(r);allrows.append(r)
        docs.append({**base,'manuscript_kind':'player-choices' if choice else 'speech','prose_companions':[str(OUTPUTS[0 if choice else 1])],'records':rows,'revised':sum(r['editorial_decision']=='revise' for r in rows),'retained':sum(r['editorial_decision']=='retain-wording' for r in rows)})
    counts=Counter(r['editorial_decision'] for r in allrows);assert len(allrows)==29 and counts=={'revise':16,'retain-wording':13}
    ROOT.mkdir(parents=True)
    for p,d in zip(OUTPUTS,docs,strict=True):save(p,d)
    save(ROOT/'all29_clean_first_contextual_decisions.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in OUTPUTS},decision_counts=dict(counts),source_context=comparison['source_context'],source_context_sha256=comparison['source_context_sha256'],all29_clean_then_current_complete_exchange_and_branches_read=True,source_context_localization_naturalness_gates_true_formatting_false=True,source_no_FI_FA_FO_preserved=True,all13_retentions_individually_justified=True,source_lecture_orientation_wind_types_positions_compatibility_size_mast_and_angle_facts_preserved=True,both_lecture_choices_separate_ends_and_later_Cesare_predicate_result_state_distinguished=True,evidence={str(p):sha(p.read_bytes()) for p in [COMPARISON,GLOSS,Path(prose.__file__),Path(__file__)]},new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(objects=29,speeches=27,choices=2,decisions=dict(counts),FI=0,formatting_pending=True,credit=0))
