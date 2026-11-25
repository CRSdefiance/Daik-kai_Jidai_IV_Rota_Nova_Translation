"""Author all 150 reachable source-bound gloss/prose reviews; no release credit."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import importlib
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B111_B119_author_v3225')
SOURCE=Path('work/analysis/lil_B111_B119_source_v3217b/complete150_reachable_Lil_clean_current_context.json')
COMPARISON=Path('work/analysis/lil_B111_B119_comparison_v3221/all150_current_effective_comparison_packet.json')
CONTROL=Path('work/analysis/lil_B111_B119_controls_v3219/all150_source_current_dispatch_variable_styles_predicates_and_query.json')
CONTEXT=Path('work/analysis/lil_B111_B119_clean_context_v3213b/all182_complete_clean_exchange_context_notes.json')
TERMS=Path('work/analysis/lil_B111_B119_terms_v3220/clean_current_items_and_native_actor_role_reconciliation.json')
VOICES=Path('work/analysis/lil_B111_B119_voices_v3218/current207_catalog_eight_voices_and_CF_D0_D1_D6_D7_DC_roles.json')
BRANCH=Path('work/analysis/lil_B111_B119_branches_v3211/original_relative_skip_operand_proof.json')
CLASSIFICATION=Path('work/analysis/lil_B115_tail_classification_v3216/source_return0_graph_and_canonical_Maria_copy_classification.json')
OUTPUTS=[Path('translations/lil_B111_B119_editorial_manuscript_v1.json'),
         Path('translations/lil_B111_B119_actor_style_manuscript_v1.json')]
MODULES=['scripts.lil_monk_rescue_jade_prose_v3222','scripts.lil_cacao_tablet_Benazir_prose_v3223',
         'scripts.lil_figurehead_tribal_trends_prose_v3224']

if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS)
    source,comparison,control,context,terms,voices=map(read,[SOURCE,COMPARISON,CONTROL,CONTEXT,TERMS,VOICES])
    assert comparison['source_context_sha256']==control['source_context_sha256']==terms['source_context_sha256']==sha(SOURCE.read_bytes())
    assert context['all148speech_and34_actor_style_alternatives_read_in_complete_clean_exchanges']
    assert context['older_English_not_yet_editorially_compared']
    assert len(comparison['records'])==150 and len(control['speech_and_stored_alternative_dispatch_cases'])==300
    speech={};voice={};producers={}
    for name in MODULES:
        m=importlib.import_module(name)
        for label,target in [('SPEECH',speech),('VOICE',voice)]:
            entries=getattr(m,label)
            assert not set(entries)&set(target)
            target.update(entries)
            for key in entries:producers[label,key]=str(Path(m.__file__))
    expected_speech={(r['block'],r['source_record_index']) for r in source['records']}
    expected_voice={(r['block'],r['command_offset'],r['source_reference']['offset']-r['command_offset'])
        for r in source['typed_actor_style_records']}
    assert set(speech)==expected_speech and set(voice)==expected_voice and len(speech)==116 and len(voice)==34
    for f in comparison['comparison_files']:assert sha(Path(f['path']).read_bytes())==f['sha256']
    byid={r['id']:r for r in comparison['records']}
    role_names={int(k):v for k,v in terms['source_speaker_annotation_reconciliation'].items()}
    context_byblock={b['block']:b['context_notes'] for b in context['blocks']}
    context_byblock[113]=("D6 voices callattentiontothejade. Liladmiresitsbeauty. Nativeactorhex13/decimal19isCarlo,not the provisionalManuelannotation. Carlo comparesjade'svalueintheNewWorldandtheEast,andinfersbuildingimportancefromthejadeoffering. Preserve inference,genericjade andnoearneditem.")
    context_byblock[115]=("Onlytheordinary-entry Lilregionisreviewedhere:fiveD0stylebodiescallattentiontothetablet,Lildismissesit,andoptionalJanus4explainslocalabsenceofstone/mosquedriedmudconstruction. Lilinfersnonlocalorigin;Janusagreesprobably. The32Maria speechesaftertheoriginalreturn0areunownedappendedcopies,provedunreachablefromthisentryandqueuedatcanonicalSC3B97;preservetheircurrentbytes. Do notmergecastsoruseMaria'scompanycontextforLil.")
    docs=[]
    base=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path='/data/SC2.DK4',current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],
        source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        control_contract=str(CONTROL),control_contract_sha256=sha(CONTROL.read_bytes()),
        whole_exchange_context_notes=str(CONTEXT),whole_exchange_context_notes_sha256=sha(CONTEXT.read_bytes()),
        branch_proof=str(BRANCH),branch_proof_sha256=sha(BRANCH.read_bytes()),
        item_terminology_reconciliation=str(TERMS),item_terminology_reconciliation_sha256=sha(TERMS.read_bytes()),
        actor_voice_contract=str(VOICES),actor_voice_contract_sha256=sha(VOICES.read_bytes()),
        effective_current_comparison=str(COMPARISON),effective_current_comparison_sha256=sha(COMPARISON.read_bytes()),
        appended_copy_classification=str(CLASSIFICATION),appended_copy_classification_sha256=sha(CLASSIFICATION.read_bytes()),
        unowned_appended32_Maria_copy_must_remain_byte_exact=True,
        canonical32_Maria_SC3_B97_records_remain_in_full_editorial_goal=True,
        source_prose_or_completion_credit_added=0,formatting_review_pending=True,
        status='source-context-localization-naturalness-reviewed;formatting-native-references-representative-release-pending')
    allrows=[]
    for label,records,entries in [('SPEECH',source['records'],speech),('VOICE',source['typed_actor_style_records'],voice)]:
        rows=[]
        for original in records:
            row=deepcopy(byid[original['id']]);isvoice=label=='VOICE'
            key=(row['block'],row['command_offset'],row['source_reference']['offset']-row['command_offset']) if isvoice else (row['block'],row['source_record_index'])
            gloss,body,note=entries[key];prefix=row['source_selector']
            assert gloss.strip() and note.strip() and body.strip()==body
            assert '\n' not in body and '\r' not in body and '%' not in body
            assert not any(t in body for t in ['{LB','{ALIGN','{PAD','{END'])
            raw=bytes.fromhex(row['source_hex'])
            for macro in ['FI','FA','FO']:assert raw.count(macro.encode())==body.count('{MACRO:'+macro+'}'),(row['id'],macro)
            old=row['current_effective_paragraph']
            for macro in ['FI','FA','FO']:old=old.replace(macro,'{MACRO:'+macro+'}')
            decision='retain-wording' if body==old else 'revise'
            row.update(source_meaning=gloss,english='{SPEAKER:'+format(prefix,'02X')+'}'+body,
                localization_note=note,editorial_decision=decision,current_stored_English=row['current_raw_storage_English'],
                effective_predecessor_paragraph=old,
                comparison_basis='Current original runtime macro template;NFKC presentation forms andcollapsedlegacywhitespace. No source orcurrentphysicalrecordisrewrittenhere.',
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
                context='Whole clean exchange read beforeoldEnglishcomparison;currentroles/macros/catalogboundwithoutnewsceneassignment. '+context_byblock[row['block']],
                prose_author_module=producers[label,key],status=base['status'],
                editorial_older_English_comparison_pending=False,full_clean_context_precedes_comparison=True,
                current_macro_dispatch_bound=True,current_complete_native_display_pending=True,
                current_native_UI_body_explicit_unexecuted_boundary=True,
                current_effective_native_dispatch_proof=str(CONTROL))
            if decision=='retain-wording':row['fresh_retained_wording_justification']=note
            else:row.pop('fresh_retained_wording_justification',None)
            if isvoice:
                row.update(speaker='Original '+format(prefix,'02X')+' role'+str(prefix-207)+' speech provider;source actor-style slots '+str(row['style_indices']),
                    virtual_formatter_prefix_hex=format(prefix,'02x'),
                    virtual_formatter_prefix_is_not_part_of_stored_alternative_text=True,
                    original_native_display_consumer='original4100_variable_actor_voice_selection_then2425C_progressive54020')
            else:
                row.update(source_kind=row['kind'],kind='system-FE' if prefix==254 else 'progressive',
                    speaker='Original FE modal presenter;no named speaker' if prefix==254 else
                        role_names[prefix] if prefix<207 else 'Original '+format(prefix,'02X')+' role'+str(prefix-207)+' speech provider',
                    original_native_display_consumer='original_FE_modal_5473C_mode1' if prefix==254 else 'original_progressive_54020')
            rows.append(row);allrows.append(row)
        doc={**base,'manuscript_kind':'speech' if label=='SPEECH' else 'actor-styles','records':rows,
            'prose_companions':[str(OUTPUTS[1] if label=='SPEECH' else OUTPUTS[0])],
            'revised':sum(r['editorial_decision']=='revise' for r in rows),
            'retained':sum(r['editorial_decision']=='retain-wording' for r in rows)}
        docs.append(doc)
    assert len(allrows)==150 and len({r['id'] for r in allrows})==150
    assert sum(len(r['style_indices']) for r in docs[1]['records'])==48
    assert {r['virtual_formatter_prefix_hex'] for r in docs[1]['records']}=={'d0','d1','d6','d7','dc'}
    ROOT.mkdir(parents=True)
    for path,doc in zip(OUTPUTS,docs,strict=True):save(path,doc)
    counts=Counter(r['editorial_decision'] for r in allrows)
    save(ROOT/'all150_gloss_prose_contextual_review_receipt.json',dict(
        manuscripts={str(p):sha(p.read_bytes()) for p in OUTPUTS},
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        current_effective_comparison=str(COMPARISON),current_effective_comparison_sha256=sha(COMPARISON.read_bytes()),
        prose_modules={str(Path(importlib.import_module(n).__file__)):sha(Path(importlib.import_module(n).__file__).read_bytes()) for n in MODULES},
        all150_fresh_glosses_and_individual_localization_or_retention_notes=True,
        all150_current_English_read_after_complete_clean_exchanges_and_current_native_bindings=True,
        proposed_revisions=counts['revise'],justified_retentions=counts['retain-wording'],
        speech_objects=116,actor_style_alternatives=34,actor_style_slots=48,FE_panels=1,
        actual_style_prefixes=['d0','d1','d6','d7','dc'],no_D0_assumption_or_fixed_actor_replacement=True,
        all_three_FI_and_one_FO_source_macros_preserved=True,
        all_four_editorial_gates_true_formatting_native_reference_and_release_still_pending=True,
        appended32_Maria_copy_excluded_from_Lil_credit_and_retained_in_full_goal=True,
        source_prose_or_completion_credit_added=0,new_emulator_runs=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(objects=150,proposed_revisions=counts['revise'],justified_retentions=counts['retain-wording'],
        source_context_localization_naturalness=True,formatting_native_reference_release_pending=True,editorial_credit=0))
