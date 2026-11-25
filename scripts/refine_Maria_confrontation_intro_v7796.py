"""Preserve the rejected macro-order proposal; keep FO thenFI in natural introductory prose."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_Maria_confrontation_layout_v7793 as layout
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_confrontation_intro_v7796')
PREVIOUS=Path('translations/maria_B36_editorial_manuscript_v1.json')
MANUSCRIPT=Path('translations/maria_B36_editorial_manuscript_v2.json')
OLD_PLAN=Path('work/analysis/maria_confrontation_layout_v7793/16_automatic_full_width_plans_all_base_QA_preserved.json')
if __name__=='__main__':
    assert not ROOT.exists() and not MANUSCRIPT.exists();old,previous_plan=map(read,[PREVIOUS,OLD_PLAN])
    assert previous_plan['manuscript_sha256']==sha(PREVIOUS.read_bytes()) and len(previous_plan['records'])==15
    assert previous_plan['failures']==[dict(id='DK4_MES_B36_R0023',error_type='DialogueEncodingError',error='control-order: runtime macros or controls changed order')]
    doc=deepcopy(old);rows=[];changed=[]
    for row in doc['records']:
        if row['source_record_index']==23:
            before=row['english'];row.update(english="I'm with FO. My name is FI. Surely you've heard of me.",
                previous_v1_English=before,decision_reason=row['decision_reason']+' The first draft reordered FI/FO and was rejected by the unchanged control-order guard. Two natural introductory clauses keep source FO before FI without adding a rank or losing confident recognition.',
                original_FO_before_FI_order_preserved=True)
            row['localization_note']=row['decision_reason']
            assert before.count('FI')==row['english'].count('FI')==1 and before.count('FO')==row['english'].count('FO')==1
            assert row['english'].index('FO')<row['english'].index('FI')
            planning=deepcopy(row);body=row['english']
            for token in ['FI','FA','FO']:body=body.replace(token,'{MACRO:'+token+'}')
            planning['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body
            p=layout.plan(planning)
            p.update(file_path=row['file_path'],block=row['block'],source_record_index=row['source_record_index'],source_selector=row['source_selector'],
                logical_English=row['english'],planning_record=planning,base_QA=layout.base_qa(planning,p))
            if any(i['code']=='line-break-count' for i in p['base_QA']['issues']):
                p['row_count_reason']=row['decision_reason']+' All words and substitutions remain in '+str(len(p['lines']))+' automatically planned rows.'
            changed.append(dict(id=row['id'],before=before,after=row['english'],reason=row['decision_reason']))
        else:
            p=deepcopy(next(p for p in previous_plan['records'] if p['id']==row['id']))
            assert p['logical_English']==row['english']
        assert not any(i['severity'] in ['warning','error'] for i in p['base_QA']['issues'])
        rows.append(p)
    assert len(rows)==16 and len(changed)==1 and all(p['expected_native_pages']==1 for p in rows)
    doc.update(previous_manuscript=str(PREVIOUS),previous_manuscript_sha256=sha(PREVIOUS.read_bytes()),
        original_control_order_failure_preserved=True,final_macro_order_refinement=changed,
        all15_other_logical_paragraphs_andcompiled_plans_unchanged=True)
    save(MANUSCRIPT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'16_complete_automatic_plans_original_macro_order_preserved.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),records=rows,failures=[],
        previous_plan=str(OLD_PLAN),previous_plan_sha256=sha(OLD_PLAN.read_bytes()),changed_records=changed,
        all15_prior_successful_plans_reused_byexact_source_prose_compiled_andQA=True,
        source_owned_plan_adapter=layout.ADAPTER,all_original_base_QA_issues_preserved_no_waivers=True,
        final_single_native_pages=16,row_count_infos=sum(i['code']=='line-break-count' for p in rows for i in p['base_QA']['issues']),
        all16_formatting_gates_false=True,no_control_order_guard_runtime_macro_profile_orfont_change=True,
        evidence={str(p):sha(p.read_bytes()) for p in [PREVIOUS,MANUSCRIPT,OLD_PLAN,Path(layout.__file__),Path(__file__)]},new_credit=0,full_goal_complete=False))
    print('16complete one-page plans;FO-before-FI restored naturally;15successful plans exact reuse;QA infos',sum(i['code']=='line-break-count' for p in rows for i in p['base_QA']['issues']))
