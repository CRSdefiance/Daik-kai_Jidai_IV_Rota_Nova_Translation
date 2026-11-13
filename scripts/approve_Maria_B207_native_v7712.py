"""Approve18 individual Maria formatting gates after complete native, stored and actual review."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.maria_B207_profile_v1 import contract
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Maria_B207_final_paths_v7712 import *
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    assert not APPROVAL.parent.exists() and all(not p.exists() for p in APPROVED.values())
    actual,view,policy,stored,later=map(read,[ACTUAL,VIEW,POLICY,STORED,LATER]);bindings=contract()['record_bindings']
    assert actual['total_actual_speech_occurrences']==36 and view['all36_complete_source_English_speech_panes_individually_viewed'] and actual['all_jobs_terminal_andreaped']
    assert policy['positive_count']==18 and policy['negative_count']==89 and stored['stored_alignment_cases']==72 and stored['zero_ink_parity_tail_count']==7
    assert view['later_RGB_differences']==104 and view['later_samples']==123 and [g['later_sample_count'] for g in later['groups']]==[123]
    positive={r['id']:r for r in policy['positive_cases']};results=[]
    for route,path in DRAFTS.items():
        old=read(path);doc=deepcopy(old);ag=next(g for g in actual['groups'] if g['route']==route and g['version']=='English')
        assert ag['actual_unique_speeches']==18 and ag['complete_body_holds']==ag['complete_name_holds']=={3:74}[route] and not ag['incomplete_sampled_holds'] and not ag['unidentified_trace_rows']
        panels={r['id']:r for r in ag['speech_observations']}
        for row in doc['records']:
            b=bindings[row['id']];qa=positive[row['id']]['qa'];panel=panels[row['id']]
            assert row['english']==b['planning_record']['english'] and row['source_hex']==b['compiler_source_hex'] and not row['review']['formatting']
            assert qa['native_page_count']==b['native_page_count']==panel['native_page_count']==1 and qa['base_QA_issues']==b['base_QA_issues']
            assert not any(i['severity'] in ['error','warning'] for i in qa['issues'])
            row['historical_formatting_reason']=row['formatting_reason'];row['review']['formatting']=True
            row.update(compiled_hex=b['compiled_hex'],formatted_markup=qa['formatted_markup'],base_QA_report=qa,qa_waivers=b['qa_waivers'],qa_waiver_reason=b['qa_waiver_reason'],row_count_reason=b['row_count_reason'],reviewed_ordinary_boundaries=b['ordinary_wrap_reasons'],native_profile_maximum_total_rows=4,original_physical_native_rows_per_page=4,native_page_count=1,current_complete_native_display_pending=False,actual_record_observed=True,actual_complete_body_holds=len(panel['complete_body_holds']),actual_complete_name_holds=len(panel['complete_name_holds']),registered_integration_pending=True,formatting_reason='Exact file-qualified paragraph uses its own guarded Maria profile andretains one original216x64/four-row page. All logical/compiled/stored native alignments,complete first/internal/final glyphs,bounds,canaries,consumption,pair phase andguards pass. Source/English initialized original-route fixtures observe all18 speeches,complete body/name holds,original commands andnormal returns;all actual panes/sheets were viewed. Seven individual row-count infos andall unmodified base QA remain;there areno warnings orwaivers. R4 keeps three original CP932 ellipses with18 black18 light-gray pixels,not ASCII dark-gray shadows. Carlo Sinat/Trader headers arecomplete;Filippo is a source-bound body alias only. Fixtures explicitly useonlythe existing audited system unlock,earned=false;they prove neither original optional activation/location/earned progress norfull effects/routes/hardware. Preserve all measured command,timing,RNG,actor/component andlater RGB differences without broad equivalence claims. Atomic registered integration,exact patch andown-ROM startup remain pending.')
        assert Counter(r['editorial_decision'] for r in doc['records'])=={'revise':13,'retain-wording':5}
        assert [r['english'] for r in doc['records']]==[r['english'] for r in old['records']]
        doc['historical_all18_formatting_gates_false']=doc.pop('all18_formatting_gates_false')
        doc.update(encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],previous_manuscript=str(path),previous_manuscript_sha256=sha(path.read_bytes()),formatting_review_pending=False,all18_five_individual_gates_true=True,actual_objects=18,actual_pages=18,actual_complete_body_holds=ag['complete_body_holds'],actual_complete_name_holds=ag['complete_name_holds'],offline_only_objects=0,offline_only_object_IDs=[],native_approval=str(APPROVAL),source_prose_or_completion_credit_added=0,atomic_registered_integration_patch_andcurrent_startup_pending=True,status='all18 individual source/prose/native/stored/actual gates approved;reference seal andregistered integration pending')
        for key,p in proofs().items():doc[key]=p;doc[key+'_sha256']=sha(Path(p).read_bytes())
        validate_natural_dialogue_batch(doc);save(APPROVED[route],doc);results.append(dict(route=route,path=str(APPROVED[route]),sha256=sha(APPROVED[route].read_bytes()),revised=13,retained=5,actual_body_holds=ag['complete_body_holds'],actual_header_holds=ag['complete_name_holds']))
    APPROVAL.parent.mkdir(parents=True)
    save(APPROVAL,dict(manuscripts=results,all18_individual_five_gates_approved=True,revision_count=13,retention_count=5,actual_pages=18,paired_source_English_speech_occurrences=36,all36_panes9_sheets_viewed=True,all_native_policy_stored_actual_name_andreference_research_gates_pass=True,all_measured_late_differences_andnatural_activation_limits_preserved=True,no_name_item_asset_orfull207_orother_consumer_approval=True,source_prose_or_completion_credit_added=0,evidence={str(p):sha(p.read_bytes()) for p in [*DRAFTS.values(),*map(Path,proofs().values()),Path(__file__)]},full_goal_complete=False))
    print('18 individual Maria five-gate decisions approved:13 revisions/5 retentions;all native/stored/actual evidence andlater limits bound. Zero credit;reference seal/registered integration pending.')
