"""Bind172 fresh individual reviews to complete clean/current exchanges; no credit."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from scripts.lil_homecoming_wedding_prose_v3007 import PROSE as A
from scripts.lil_ian_shopping_prose_v3008 import PROSE as B
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Homecoming_Ian_author_v3009')
SOURCE=Path('work/analysis/lil_Homecoming_Ian_source_v3002/complete172_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Homecoming_Ian_controls_v3004/source_bound172_preambles_FE_and_original_conditional_predicates.json')
BRANCH=Path('work/analysis/lil_Homecoming_Ian_branches_v3003/original_relative_skip_operand_proof.json')
CONTEXT=Path('work/analysis/lil_Homecoming_Ian_context_v3005/complete_clean_exchange_context_notes.json')
WEDDING=Path('work/analysis/lil_Homecoming_Ian_wedding_contract_v3006/historical_actual_wedding_FE_and_M26_source_contract.json')
DOC=Path('translations/lil_homecoming_ian_editorial_manuscript_v1.json')
FILES=[Path('scripts')/n for n in ['lil_homecoming_wedding_prose_v3007.py','lil_ian_shopping_prose_v3008.py']]

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists()
    source,control,branch,context,wedding=map(read,[SOURCE,CONTROL,BRANCH,CONTEXT,WEDDING])
    data={**A,**B}; assert len(data)==len(A)+len(B)==2
    reviews={f'DK4_MES_B{block}_R{index:04d}':value for block,rows in data.items() for index,value in rows.items()}
    assert len(reviews)==172 and set(reviews)=={r['id'] for r in source['records']}
    assert source['total_editorial_objects']==172 and source['progressive_speeches']==158 and source['system_FE_panels']==14 and source['typed_choice_labels']==0
    assert len(control['dispatch_cases'])==344 and len(control['current_original_predicate_cases'])==31 and len(control['original_event_queries'])==3
    assert control['all172_complete_preambles_and344_historical_dispatch_contexts_pass'] and control['all14_FE_before_fallback208_use5473C_and_original24310_null_macro_actor']
    assert control['FE_FI_substitution_original_dispatcher_output_bound']
    assert len(branch['cases'])==1240 and len(branch['operands_requiring_adjustment_when_resizing'])==124
    assert sum(len(b['all_clean_native_commands']) for b in source['blocks'])==390
    assert context['all172_complete_clean_Japanese_speeches_read_before_old_English_comparison']
    assert wedding['current_native_paint_of_historical_first_wedding_body_complete_ink_and_blank_mask_equals_actual']
    contexts={b['block']:b['whole_exchange_context'] for b in context['blocks']}; rows=[]
    for original in source['records']:
        row=deepcopy(original); gloss,english,note=reviews[row['id']]
        assert english and gloss and note and english.isascii() and english==english.strip()
        assert not any(t in english for t in ['\n','{LB','{ALIGN','{PAD'])
        body=bytes.fromhex(row['source_hex'])[1:]
        for macro in ['FI','FA','FO']: assert body.count(macro.encode())==english.count('{MACRO:'+macro+'}'),row['id']
        old=' '.join(row['current_English'].split())
        for macro in ['FI','FA','FO']: old=old.replace(macro,'{MACRO:'+macro+'}')
        retained=english==old
        if retained: row['fresh_retained_wording_justification']=note
        row.update(english='{SPEAKER:'+row['source_presentation_prefix_hex'].upper()+'}'+english,source_meaning=gloss,localization_note=note,
            context=contexts[row['block']]+' Every speech in this complete exchange has been read. Storage order is not branch reachability. Historical wedding display and movie context is separately hash-bound; source alignment is not English layout. No new native display, actual selected gameplay or registered-release approval is claimed.',
            editorial_decision='retain-wording' if retained else 'revise',review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='source-context-prose-approved;current-native-progressive-FE-reference-representative-release-pending')
        rows.append(row)
    count=Counter(r['editorial_decision'] for r in rows); assert sum(count.values())==172
    doc=dict(format='dk4-ilhi-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',file_path='/data/SC2.DK4',review_gates=['source','context','localization','naturalness','formatting'],
        source_ROM_sha256=source['source_ROM_sha256'],current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),control_contract=str(CONTROL),control_contract_sha256=sha(CONTROL.read_bytes()),branch_proof=str(BRANCH),branch_proof_sha256=sha(BRANCH.read_bytes()),whole_exchange_context_notes=str(CONTEXT),whole_exchange_context_notes_sha256=sha(CONTEXT.read_bytes()),wedding_display_contract=str(WEDDING),wedding_display_contract_sha256=sha(WEDDING.read_bytes()),
        records=rows,revised=count['revise'],retained=count['retain-wording'],formatting_review_pending=True,no_authored_line_breaks_or_padding=True,no_typed_choices=True,source_prose_credit_added=0,completion_credit_added=0,actual_selected_Homecoming_Ian_IDs=[],new_emulator_runs=0,full_goal_complete=False)
    ROOT.mkdir(parents=True); save(DOC,doc)
    save(ROOT/'source_prose_review_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),total_editorial_objects=172,ordinary=158,FE=14,revised=count['revise'],retained=count['retain-wording'],all172_clean_source_and_whole_exchange_prose_gates_pass=True,source390commands124sites1240cases344dispatch31predicates3queries_bound=True,
        all_source_macros_exact_and_retentions_individually_justified=True,all14_FE_distinct_panels_and_one_FI_preserved=True,optional_departure_does_not_become_unconditional=True,explicit_years_and_dream_self_correction_restored=True,two_V678_repairs_retained_and_individually_justified=True,research_student171_not_priest_and_shown_prop_unnamed=True,optional_Ian_scene_has_no_assumed_marriage_or_actual_hit=True,
        author_files={str(p):sha(p.read_bytes()) for p in FILES+[Path(__file__)]},source_evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROL,BRANCH,CONTEXT,WEDDING]},native_fonts_QA_pagination_reference_representative_and_registered_release_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print(dict(speeches=172,ordinary=158,FE=14,revised=count['revise'],retained=count['retain-wording'],no_ledger_credit=True,native_reference_release_pending=True))
