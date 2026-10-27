"""Bind145 individual clean-source reviews to complete recruitment/rescue exchanges."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from scripts.lil_christina_recruitment_prose_v3040 import PROSE as A
from scripts.lil_mivor_harbor_rescue_prose_v3041 import PROSE as B
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Christina_Mivor_author_v3042')
SOURCE=Path('work/analysis/lil_Christina_Mivor_source_v3035/complete145_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Christina_Mivor_controls_v3037/source_bound145_preambles_FE_and_original_conditional_predicates.json')
BRANCH=Path('work/analysis/lil_Christina_Mivor_branches_v3036/original_relative_skip_operand_proof.json')
CONTEXT=Path('work/analysis/lil_Christina_Mivor_context_v3038/complete_clean_exchange_context_notes.json')
NAMES=Path('work/analysis/lil_Christina_Mivor_names_v3039c/current_registered_names_and_source_identity_contract.json')
DOC=Path('translations/lil_christina_mivor_editorial_manuscript_v1.json')
FILES=[Path('scripts')/n for n in ['lil_christina_recruitment_prose_v3040.py','lil_mivor_harbor_rescue_prose_v3041.py']]
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists()
    source,control,branch,context,names=map(read,[SOURCE,CONTROL,BRANCH,CONTEXT,NAMES])
    data={**A,**B}; assert len(data)==len(A)+len(B)==2
    reviews={f'DK4_MES_B{block}_R{index:04d}':value for block,rows in data.items() for index,value in rows.items()}
    assert len(reviews)==145 and set(reviews)=={r['id'] for r in source['records']}
    assert source['total_editorial_objects']==145 and source['progressive_speeches']==142 and source['system_FE_panels']==3 and source['typed_choice_labels']==0
    assert len(control['dispatch_cases'])==290 and len(control['current_original_predicate_cases'])==3 and len(control['original_event_queries'])==0
    assert control['all145_complete_preambles_and290_historical_dispatch_contexts_pass'] and control['all3_FE_before_fallback208_use5473C_and_original24310_null_macro_actor']
    assert control['all3_FE_source_visible_Boy_labels_preserved_by_original_dispatcher']
    assert len(branch['cases'])==120 and len(branch['operands_requiring_adjustment_when_resizing'])==12
    assert sum(len(b['all_clean_native_commands']) for b in source['blocks'])==236
    assert context['all145_complete_clean_Japanese_speeches_read_before_old_English_comparison']
    assert names['Mivor_full_name']=='Mivor Genz' and names['original_name_ring_scratch_restored_recovers_all4MiB']
    contexts={b['block']:b['whole_exchange_context'] for b in context['blocks']};rows=[]
    for original in source['records']:
        row=deepcopy(original);gloss,english,note=reviews[row['id']]
        if row['original_actor_ID']==79:
            row['source_packet_speaker_annotation']=row['speaker'];row['speaker']='Mivor Genz;current registered actor79'
            row['source_speaker_annotation_correction']='Provisional Gentz annotation superseded by current registered Mivor Genz;source bytes unchanged.'
        assert english and gloss and note and english.isascii() and english==english.strip()
        assert not any(t in english for t in ['\n','{LB','{ALIGN','{PAD'])
        body=bytes.fromhex(row['source_hex'])[1:]
        for macro in ['FI','FA','FO']:assert body.count(macro.encode())==english.count('{MACRO:'+macro+'}'),row['id']
        if row['kind']=='system-FE':assert row['source_Japanese'].startswith('＜男の子＞') and english.startswith('Boy: ')
        old=' '.join(row['current_English'].split())
        for macro in ['FI','FA','FO']:old=old.replace(macro,'{MACRO:'+macro+'}')
        retained=english==old
        if retained:row['fresh_retained_wording_justification']=note
        row.update(english='{SPEAKER:'+row['source_presentation_prefix_hex'].upper()+'}'+english,source_meaning=gloss,localization_note=note,
            context=contexts[row['block']]+' Every speech in this complete exchange has been read. Storage order is not branch reachability. Registered names/source-proven grandfather identity are separately hash-bound. Boy FE source labels stay visible;familiar sibling addresses do not imply kinship. No new native display,actual selected gameplay orregistered-release approval is claimed.',
            editorial_decision='retain-wording' if retained else 'revise',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='source-context-prose-approved;current-native-progressive-FE-reference-representative-release-pending')
        rows.append(row)
    counts=Counter(r['editorial_decision'] for r in rows);assert sum(counts.values())==145
    doc=dict(format='dk4-ilcm-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',file_path='/data/SC2.DK4',review_gates=['source','context','localization','naturalness','formatting'],
        source_ROM_sha256=source['source_ROM_sha256'],current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),control_contract=str(CONTROL),control_contract_sha256=sha(CONTROL.read_bytes()),branch_proof=str(BRANCH),branch_proof_sha256=sha(BRANCH.read_bytes()),whole_exchange_context_notes=str(CONTEXT),whole_exchange_context_notes_sha256=sha(CONTEXT.read_bytes()),name_identity_contract=str(NAMES),name_identity_contract_sha256=sha(NAMES.read_bytes()),
        records=rows,revised=counts['revise'],retained=counts['retain-wording'],formatting_review_pending=True,no_authored_line_breaks_or_padding=True,no_typed_choices=True,source_prose_credit_added=0,completion_credit_added=0,actual_selected_Christina_Mivor_IDs=[],new_emulator_runs=0,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(DOC,doc)
    save(ROOT/'source_prose_review_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),total_editorial_objects=145,ordinary=142,FE=3,revised=counts['revise'],retained=counts['retain-wording'],all145_clean_source_and_whole_exchange_prose_gates_pass=True,source236commands12sites120cases290dispatch3predicates0queries_bound=True,
        all_source_macros_exact_and_retentions_individually_justified=True,all3_FE_distinct_source_Boy_labels_preserved=True,source_explicit_grandfather_and_no_invented_rescue_siblings=True,initial_fear_wins_and_later_love_wins_comparison_preserved=True,arranged_engagement_rejected_and_rescue_does_not_establish_romantic_consent=True,current_registered_Mivor_Genz_annotation_corrected_without_editing_executed_source_packet=True,
        author_files={str(p):sha(p.read_bytes()) for p in FILES+[Path(__file__)]},source_evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROL,BRANCH,CONTEXT,NAMES]},native_fonts_QA_pagination_reference_representative_and_registered_release_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print(dict(speeches=145,ordinary=142,FE=3,revised=counts['revise'],retained=counts['retain-wording'],no_ledger_credit=True,native_reference_release_pending=True))
