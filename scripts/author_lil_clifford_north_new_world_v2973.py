"""Author all143 complete-exchange speech reviews; no ledger or native credit."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from scripts.lil_clifford_aftermath_homeward_prose_v2970 import PROSE as A
from scripts.lil_bamboo_clifford_strategy_prose_v2971 import PROSE as B
from scripts.lil_maldonado_tavern_prose_v2972 import PROSE as C
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Clifford_North_New_World_author_v2973')
SOURCE=Path('work/analysis/lil_Clifford_North_New_World_source_v2965/complete143_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Clifford_North_New_World_controls_v2968/source_bound143_preambles_FE_and_original_conditional_predicates.json')
BRANCH=Path('work/analysis/lil_Clifford_North_New_World_branches_v2967/original_relative_skip_operand_proof.json')
CONTEXT=Path('work/analysis/lil_Clifford_North_New_World_context_v2966/complete_clean_exchange_context_notes.json')
TERMS=Path('work/analysis/lil_Clifford_North_New_World_item_terms_v2969/clean_current_and_registered_item_names.json')
DOC=Path('translations/lil_clifford_north_new_world_editorial_manuscript_v1.json')
FILES=[Path('scripts')/n for n in ['lil_clifford_aftermath_homeward_prose_v2970.py','lil_bamboo_clifford_strategy_prose_v2971.py','lil_maldonado_tavern_prose_v2972.py']]

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists()
    source,control,branch,context,terms=map(read,[SOURCE,CONTROL,BRANCH,CONTEXT,TERMS])
    data={**A,**B,**C};assert len(data)==len(A)+len(B)+len(C)==6
    reviews={f'DK4_MES_B{block}_R{index:04d}':value for block,rows in data.items() for index,value in rows.items()}
    assert len(reviews)==143 and set(reviews)=={r['id'] for r in source['records']}
    assert source['total_editorial_objects']==143 and source['progressive_speeches']==140 and source['system_FE_panels']==3 and source['typed_choice_labels']==0
    assert len(control['dispatch_cases'])==286 and len(control['current_original_predicate_cases'])==45 and len(control['original_event_queries'])==4
    assert control['all143_complete_preambles_and286_historical_dispatch_contexts_pass'] and control['all3_FE_before_fallback208_use5473C_and_original24310_null_macro_actor']
    assert len(branch['cases'])==1800 and len(branch['operands_requiring_adjustment_when_resizing'])==180
    assert sum(len(b['all_clean_native_commands']) for b in source['blocks'])==453
    assert context['all143_complete_clean_Japanese_speeches_read_before_old_English_comparison'] and terms['all3_current_pointer_strings_equal_registered_names']
    contexts={b['block']:b['whole_exchange_context'] for b in context['blocks']};rows=[]
    for original in source['records']:
        row=deepcopy(original);english,gloss,note=reviews[row['id']]
        assert english and gloss and note and english.isascii() and english==english.strip()
        assert not any(t in english for t in ['\n','{LB','{ALIGN','{PAD'])
        body=bytes.fromhex(row['source_hex'])[1:]
        for macro in ['FI','FA','FO']:assert body.count(macro.encode())==english.count('{MACRO:'+macro+'}'),row['id']
        old=' '.join(row['current_English'].split())
        for macro in ['FI','FA','FO']:old=old.replace(macro,'{MACRO:'+macro+'}')
        retained=english==old
        if retained:row['fresh_retained_wording_justification']=note
        row.update(english='{SPEAKER:'+row['source_presentation_prefix_hex'].upper()+'}'+english,source_meaning=gloss,localization_note=note,
            context=contexts[row['block']].replace('stolen-Prof','stolen-Proof')+' Every speech in this complete exchange has been read. Storage order is not branch reachability. Registered item terminology is separately source-pointer-bound. No new native display,actual selected gameplay or registered-release approval is claimed.',
            editorial_decision='retain-wording' if retained else 'revise',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='source-context-prose-approved;current-native-progressive-FE-reference-representative-release-pending')
        rows.append(row)
    count=Counter(r['editorial_decision'] for r in rows);assert sum(count.values())==143
    doc=dict(format='dk4-ilnk-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',file_path='/data/SC2.DK4',review_gates=['source','context','localization','naturalness','formatting'],
        source_ROM_sha256=source['source_ROM_sha256'],current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),control_contract=str(CONTROL),control_contract_sha256=sha(CONTROL.read_bytes()),branch_proof=str(BRANCH),branch_proof_sha256=sha(BRANCH.read_bytes()),whole_exchange_context_notes=str(CONTEXT),whole_exchange_context_notes_sha256=sha(CONTEXT.read_bytes()),item_terminology_reconciliation=str(TERMS),item_terminology_reconciliation_sha256=sha(TERMS.read_bytes()),
        records=rows,revised=count['revise'],retained=count['retain-wording'],formatting_review_pending=True,no_authored_line_breaks_or_padding=True,no_typed_choices=True,source_prose_credit_added=0,completion_credit_added=0,actual_selected_Clifford_North_New_World_IDs=[],new_emulator_runs=0,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(DOC,doc)
    save(ROOT/'source_prose_review_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),total_editorial_objects=143,ordinary=140,FE=3,revised=count['revise'],retained=count['retain-wording'],all143_clean_source_and_whole_exchange_prose_gates_pass=True,source453commands180sites1800cases286dispatch45predicates4queries_bound=True,
        all_source_macros_exact_and_retentions_individually_justified=True,all3_FE_no_name_macros_or_invented_speaker_labels=True,complete_letters_tavern_location_and_Clifford_signatures_preserved=True,political_independence_and_Crown_permission_and_private_knowledge_qualified=True,bottle_warning_misses_and_no_invented_injury_or_physical_grip=True,source_0D_Cesare_actor_preamble_preserved=True,
        author_files={str(p):sha(p.read_bytes()) for p in FILES+[Path(__file__)]},source_evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROL,BRANCH,CONTEXT,TERMS]},native_fonts_QA_pagination_reference_representative_and_registered_release_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print(dict(speeches=143,ordinary=140,FE=3,revised=count['revise'],retained=count['retain-wording'],no_ledger_credit=True,native_reference_release_pending=True))
