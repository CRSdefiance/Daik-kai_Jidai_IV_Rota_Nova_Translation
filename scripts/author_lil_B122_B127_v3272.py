"""Write all159 fresh gloss/prose reviews; four gates only, no ledger credit."""
from collections import Counter
from copy import deepcopy
import importlib
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B122_B127_author_v3272')
SOURCE=Path('work/analysis/lil_B122_B127_source_v3260c/complete159_clean_current_native_context.json')
COMPARISON=Path('work/analysis/lil_B122_B127_comparison_v3268/all159_current_effective_comparison_packet.json')
CONTEXT=Path('work/analysis/lil_B122_B127_clean_context_v3263/all159_complete_clean_exchange_context_notes.json')
CONTROL=Path('work/analysis/lil_B122_B127_controls_v3266/all155_source_current_dispatch_FE_null_actor_and14_predicates.json')
VOICES=Path('work/analysis/lil_B122_B127_voices_v3264/current_eight_static_names_voices_and207_catalog_rebind.json')
TERMS=Path('work/analysis/lil_B122_B127_terms_v3267/clean_current_items_Spirit_static_actors_and_related_terms.json')
BRANCH=Path('work/analysis/lil_B122_B127_branches_v3261b/original_relative_skip_operand_proof.json')
WAIT=Path('work/analysis/lil_B122_original2000_waits_v3265/original2000_actual_rule_and_current_source_binding.json')
MODULES=['scripts.lil_Clifford_Christina_taverns_prose_v3269','scripts.lil_moral_doubts_Guiding_Staff_prose_v3270','scripts.lil_trade_lesson_Fernando_cards_prose_v3271a']
OUTPUTS=[Path('translations/lil_B122_B127_editorial_manuscript_v1.json'),Path('translations/lil_B122_B127_choice_manuscript_v1.json')]
if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS)
    source,comparison,context,control,voices,terms,wait=map(read,[SOURCE,COMPARISON,CONTEXT,CONTROL,VOICES,TERMS,WAIT])
    assert context['all159_clean_source_objects_read_before_older_English_comparison'] and len(comparison['records'])==159
    assert control['all155_complete_preambles_have310_current_code_source_and_current_dispatch_cases'] and control['all20_FE_cases_dispatch5473C_and24310_null_actor_before_dynamic_fallback']
    assert wait['current_zero_argument_wait_contract_bound_by_exact_original_code_and_actual_Lil_pause_evidence']
    for d in [comparison,control,voices,terms]:assert d['source_context_sha256']==sha(SOURCE.read_bytes())
    speech={};choices={};producers={};modules={}
    for name in MODULES:
        module=importlib.import_module(name);modules[str(Path(module.__file__))]=sha(Path(module.__file__).read_bytes())
        for label,target,entries in [('SPEECH',speech,module.SPEECH),('CHOICES',choices,module.CHOICES)]:
            for key,value in entries.items():
                assert key not in target and len(value)==3 and all(isinstance(v,str) and v.strip() for v in value)
                target[key]=value;producers[label,key]=str(Path(module.__file__))
    expected_speech={(r['block'],r['source_record_index']) for r in source['records']};expected_choices={(r['block'],r['command_offset'],r['option_index']) for r in source['typed_choice_records']}
    assert set(speech)==expected_speech and set(choices)==expected_choices and len(speech)==155 and len(choices)==4
    byid={r['id']:r for r in comparison['records']};contexts={g['block']:g for g in context['groups']}
    speakers={2:'Lil Argot',6:'Julio Erneco;source explicitly Christina\'s grandfather',9:'Camille',20:'Fernando',26:'Julian Lopes',92:'Barkeep',95:'Patron',151:'Retainer;static source151,not dynamicD0 fallback'}
    base=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),control_contract=str(CONTROL),control_contract_sha256=sha(CONTROL.read_bytes()),whole_exchange_context_notes=str(CONTEXT),whole_exchange_context_notes_sha256=sha(CONTEXT.read_bytes()),branch_proof=str(BRANCH),branch_proof_sha256=sha(BRANCH.read_bytes()),item_terminology_reconciliation=str(TERMS),item_terminology_reconciliation_sha256=sha(TERMS.read_bytes()),actor_voice_contract=str(VOICES),actor_voice_contract_sha256=sha(VOICES.read_bytes()),effective_current_comparison=str(COMPARISON),effective_current_comparison_sha256=sha(COMPARISON.read_bytes()),original2000_wait_proof=str(WAIT),original2000_wait_proof_sha256=sha(WAIT.read_bytes()),preserve_two_original2000_nontext_illustration_pauses=True,broad_Proof_terminology_editorial_consistency_lead_still_open=True,source_prose_or_completion_credit_added=0,formatting_review_pending=True,status='source-context-localization-naturalness-reviewed;formatting-native-references-representative-release-pending')
    docs=[];allrows=[]
    for label,originals,entries in [('SPEECH',source['records'],speech),('CHOICES',source['typed_choice_records'],choices)]:
        rows=[]
        for original in originals:
            row=deepcopy(byid[original['id']]);choice=label=='CHOICES';key=(row['block'],row['command_offset'],row['option_index']) if choice else (row['block'],row['source_record_index'])
            gloss,body,note=entries[key];assert body==body.strip() and '  ' not in body and '\n' not in body
            assert not any(tag in body for tag in ['{LB','{ALIGN','{PAD','{SPEAKER:']) and all(ord(c)<128 for c in body)
            for macro in ['FI','FA','FO']:assert bytes.fromhex(row['source_hex']).count(macro.encode())==body.count('{MACRO:'+macro+'}'),(row['id'],macro)
            old=row['current_effective_paragraph']
            if not choice:
                for macro in ['FI','FA','FO']:old=old.replace(macro,'{MACRO:'+macro+'}')
            decision='retain-wording' if body==old else 'revise';g=contexts[row['block']]
            row.update(source_meaning=gloss,english=body if choice else '{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body,localization_note=note,editorial_decision=decision,current_stored_English=row['current_raw_storage_English'],effective_predecessor_paragraph=old,comparison_basis='Current original runtime macro template;NFKC presentation forms andcollapsedlegacywhitespace. Raw/current/effective provenance stays separate.',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),context='Complete clean exchange read before older-English comparison. '+g['scene']+' '+g['progression']+' Source storage order includes alternative paths,not one combined conversation. Exact current actor/item/stat/UI2000 bindings are attached;no selected-scene or earned-progress claim.',prose_author_module=producers[label,key],status=base['status'],editorial_older_English_comparison_pending=False,full_clean_context_precedes_comparison=True,current_macro_dispatch_bound=not choice,current_complete_native_display_pending=True,current_native_UI_body_explicit_unexecuted_boundary=True,current_effective_native_dispatch_proof=str(CONTROL))
            if choice:
                row.update(speaker='Lil Argot;player-selected reply',choice_consumer_selection_geometry_native_display_pending=True)
            else:
                prefix=row['source_selector'];row.update(source_kind=row['kind'],speaker='Original FE modal presenter;Clifford offscreen voice or letter,without displayed speaker label' if prefix==254 and row['block']==122 else 'Original FE modal presenter;unlabeled Spirit stat notice' if prefix==254 else speakers[prefix],original_native_display_consumer='original_FE_modal_5473C_mode1' if prefix==254 else 'original_progressive_54020')
            if decision=='retain-wording':row['fresh_retained_wording_justification']=note
            else:row.pop('fresh_retained_wording_justification',None)
            rows.append(row);allrows.append(row)
        docs.append({**base,'manuscript_kind':'speech' if label=='SPEECH' else 'player-choices','records':rows,'prose_companions':[str(OUTPUTS[1] if label=='SPEECH' else OUTPUTS[0])],'revised':sum(r['editorial_decision']=='revise' for r in rows),'retained':sum(r['editorial_decision']=='retain-wording' for r in rows)})
    assert len(allrows)==len({r['id'] for r in allrows})==159
    assert sum(r['kind']=='system-FE' for r in allrows)==10 and sum(r['registered_runtime_catalog_entry'] is not None for r in allrows)==6
    ROOT.mkdir(parents=True)
    for p,d in zip(OUTPUTS,docs,strict=True):save(p,d)
    counts=Counter(r['editorial_decision'] for r in allrows)
    save(ROOT/'all159_gloss_prose_contextual_review_receipt.json',dict(manuscripts={str(p):sha(p.read_bytes()) for p in OUTPUTS},source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),current_effective_comparison=str(COMPARISON),current_effective_comparison_sha256=sha(COMPARISON.read_bytes()),prose_modules=modules,all159_fresh_glosses_and_individual_localization_or_retention_notes=True,all159_clean_then_current_complete_exchanges_read=True,all6_current_registered_Camille_replacements_preserved_as_effective_provenance=True,source_context_localization_naturalness_gates_true_formatting_false=True,decision_counts=dict(counts),all_original_speaker_macro_and_choice_indices_preserved=True,preserve_source2000_waits=True,broader_Proof_terminology_consistency_open_separate_from_technical_reaudit=True,all_new_prose_has_no_authored_layout=True,no_ROM_registry_ledger_or_editorial_credit_change=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(objects=159,decisions=dict(counts),speech=len(docs[0]['records']),choice_labels=len(docs[1]['records']),source_context_localization_naturalness_approved=True,formatting_pending=True,ledger_credit_added=0))
