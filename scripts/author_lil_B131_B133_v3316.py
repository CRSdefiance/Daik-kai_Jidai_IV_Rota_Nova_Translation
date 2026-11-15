"""Author63 contextual reviews from earlier fresh glosses; formatting pending."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.lil_map_Rafael_share_trade_prose_v3315 import SPEECH,CHOICES
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B131_B133_author_v3316')
SOURCE=Path('work/analysis/lil_remaining_B131_B140_source_v3306b/next63_B131_B133_clean_current_context.json')
COMPARISON=Path('work/analysis/lil_B131_B133_comparison_v3314b/all63_current_effective_comparison_packet.json')
CONTEXT=Path('work/analysis/lil_B131_B133_clean_context_v3312/all63_complete_clean_context_and_fresh_glosses.json')
CONTROL=Path('work/analysis/lil_B131_B133_controls_v3308b/all61_source_current_dispatch_selector00_FE_and5_predicates.json')
VOICE=Path('work/analysis/lil_B131_B133_voices_v3307b/current_five_static_names_voices_selector00_and207_catalog_rebind.json')
TERMS=Path('work/analysis/lil_B131_B133_terms_v3313/clean_current_items_names_and_share_ratio_reconciliation.json')
BRANCH=Path('work/analysis/lil_B131_B133_branches_v3309b/original_relative_skip_operand_proof.json')
PROSE=Path('scripts/lil_map_Rafael_share_trade_prose_v3315.py')
OUTPUTS=[Path('translations/lil_B131_B133_editorial_manuscript_v1.json'),Path('translations/lil_B131_B133_choice_manuscript_v1.json')]
if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS);source,comparison,context,control,voices,terms=map(read,[SOURCE,COMPARISON,CONTEXT,CONTROL,VOICE,TERMS])
    assert context['all63_complete_clean_source_objects_read_before_older_English_comparison'] and context['all63_fresh_source_glosses_precede_localized_English'] and len(comparison['records'])==63 and comparison['registered_runtime_catalog_replacement_count']==0
    assert len(control['speech_dispatch_cases'])==122 and len(control['current_original_predicate_cases'])==5 and control['source00_is_static_actor0_Rafael_Castor_without_role_assignment']
    assert {(r['block'],r['source_record_index']) for r in source['records']}==set(SPEECH) and {(r['block'],r['command_offset'],r['option_index']) for r in source['typed_choice_records']}==set(CHOICES)
    for d in [comparison,control,terms,voices]:assert d['source_context_sha256']==sha(SOURCE.read_bytes())
    byid={r['id']:r for r in comparison['records']};gloss={r['id']:r for r in context['records']};groups={r['block']:r for r in context['groups']};speakers={0:'Rafael Castor;static actor0 in Lil exchange',2:'Lil Argot',5:'Claudio Manaus',9:'Camille',20:'Fernando',254:'Original FE modal presenter;unlabeled market-share exchange notice'}
    base=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),control_contract=str(CONTROL),control_contract_sha256=sha(CONTROL.read_bytes()),whole_exchange_context_notes=str(CONTEXT),whole_exchange_context_notes_sha256=sha(CONTEXT.read_bytes()),branch_proof=str(BRANCH),branch_proof_sha256=sha(BRANCH.read_bytes()),item_terminology_reconciliation=str(TERMS),item_terminology_reconciliation_sha256=sha(TERMS.read_bytes()),actor_voice_contract=str(VOICE),actor_voice_contract_sha256=sha(VOICE.read_bytes()),effective_current_comparison=str(COMPARISON),effective_current_comparison_sha256=sha(COMPARISON.read_bytes()),source00_is_actual_static_Rafael_not_empty_or_dynamic=True,fresh_source_glosses_precede_current_comparison_and_localized_English=True,broad_Proof_terminology_editorial_consistency_lead_still_open=True,source_prose_or_completion_credit_added=0,formatting_review_pending=True,status='source-context-localization-naturalness-reviewed;native-format-references-representative-release-pending')
    docs=[];allrows=[]
    for originals,entries,choice in [(source['records'],SPEECH,False),(source['typed_choice_records'],CHOICES,True)]:
        rows=[]
        for original in originals:
            row=deepcopy(byid[original['id']]);key=(row['block'],row['command_offset'],row['option_index']) if choice else (row['block'],row['source_record_index']);body,note=entries[key];assert body==body.strip() and '  ' not in body and '\n' not in body and all(32<=ord(c)<127 for c in body)
            assert not any(tag in body for tag in ['{LB','{ALIGN','{PAD','{SPEAKER:'])
            for m in ['FI','FA','FO']:assert bytes.fromhex(row['source_hex']).count(m.encode())==body.count('{MACRO:'+m+'}'),(row['id'],m)
            old=row['current_effective_paragraph']
            if not choice:
                for m in ['FI','FA','FO']:old=old.replace(m,'{MACRO:'+m+'}')
            decision='retain-wording' if body==old else 'revise';group=groups[row['block']]
            row.update(source_meaning=gloss[row['id']]['source_meaning'],english=body if choice else '{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body,localization_note=note,editorial_decision=decision,current_stored_English=row['current_raw_storage_English'],effective_predecessor_paragraph=old,comparison_basis='Exact current native template,NFKC presentation forms andcollapsed legacy whitespace;raw storage/effective provenance separate.',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),speaker='Lil Argot;player-selected reply' if choice else speakers[row['source_selector']],context='Complete clean exchange andfresh source glosses read/written before older-English comparison. '+group['scene']+' '+group['progression']+' '+group['facts']+' Native actor0/Rafael in Lil captain2 context andsource FI/FO are bound;no selected-scene or earned-progress claim.',prose_author_module=str(PROSE),prose_author_module_sha256=sha(PROSE.read_bytes()),status=base['status'],editorial_older_English_comparison_pending=False,full_clean_context_precedes_comparison=True,current_complete_native_display_pending=True)
            if not choice:row.update(source_kind=row['kind'],current_macro_dispatch_bound=True,original_native_display_consumer='original_FE_modal_5473C_mode1' if row['source_selector']==254 else 'original_progressive_54020')
            else:row['choice_consumer_selection_geometry_native_display_pending']=True
            if decision=='retain-wording':row['fresh_retained_wording_justification']=note
            else:row.pop('fresh_retained_wording_justification',None)
            rows.append(row);allrows.append(row)
        docs.append({**base,'manuscript_kind':'player-choices' if choice else 'speech','records':rows,'prose_companions':[str(OUTPUTS[0] if choice else OUTPUTS[1])],'revised':sum(r['editorial_decision']=='revise' for r in rows),'retained':sum(r['editorial_decision']=='retain-wording' for r in rows)})
    assert len(allrows)==len({r['id'] for r in allrows})==63 and sum(r.get('source_selector')==0 for r in allrows)==18 and sum(r['kind']=='system-FE' for r in allrows)==1
    ROOT.mkdir(parents=True)
    for p,d in zip(OUTPUTS,docs,strict=True):save(p,d)
    save(ROOT/'all63_contextual_prose_or_retention_receipt.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in OUTPUTS},source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),fresh_clean_context_glosses=str(CONTEXT),fresh_clean_context_glosses_sha256=sha(CONTEXT.read_bytes()),current_effective_comparison=str(COMPARISON),current_effective_comparison_sha256=sha(COMPARISON.read_bytes()),prose_module=str(PROSE),prose_module_sha256=sha(PROSE.read_bytes()),all63_clean_then_current_complete_exchanges_read=True,all63_fresh_glosses_precede_localized_English=True,all63_individual_revision_or_retention_notes=True,source_context_localization_naturalness_gates_true_formatting_false=True,decision_counts=dict(Counter(r['editorial_decision'] for r in allrows)),all18_source00_Rafael_selectors_and_macro_counts_preserved=True,source_choice_indices01_and_two_Nantes_for_one_Lisbon_terms_preserved=True,no_authored_layout=True,Proof_terminology_consistency_still_open_separate_from_later_technical_reaudit=True,no_ROM_registry_ledger_or_editorial_credit_change=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(objects=63,decisions=dict(Counter(r['editorial_decision'] for r in allrows)),formatting=False,credit=0))
