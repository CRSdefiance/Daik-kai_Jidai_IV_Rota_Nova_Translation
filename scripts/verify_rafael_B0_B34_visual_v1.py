"""Combine the last 15 rerenders and bind their visual approval to prior exact pages."""
from pathlib import Path
import sys
from types import FunctionType
from scripts import verify_rafael_B0_B34_visual_delta_v1 as previous
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_rafael_B0_B34_v1 import FORMATTING, ROOT

PLAN=ROOT/'visual_plan_v3/automatic_plans.json'
FINAL=ROOT/'final_native_pages_v2.json'
APPROVAL=ROOT/'complete_visual_review_v1.json'
DELTA=ROOT/'visual_delta_inputs_v3'
SHEETS=ROOT/'visual_delta_sheets_v3'
env={**previous.env,'__file__':__file__,
    'ORIGINAL':ROOT/'refined_plan_v3/automatic_plans.json','PLAN':PLAN,
    'FIRST_NATIVE':ROOT/'final_native_pages_v1.json','DELTA':DELTA,
    'DELTA_MANUSCRIPT':DELTA/'changed_manuscript.json','DELTA_PLAN':DELTA/'changed_plans.json',
    'FRESH':ROOT/'visual_delta_native_v3/compiled_native_pages.json','FINAL':FINAL,'SHEETS':SHEETS}
env['inputs']=FunctionType(previous.previous.inputs.__code__,env)


def approve():
    assert not APPROVAL.exists()
    old=load(ROOT/'initial_complete_visual_review_v1.json')
    fresh=load(SHEETS/'sheet_index.json'); native=load(FINAL); plan=load(PLAN)
    assert old['all_listed_initial_body_andname_sheets_directly_viewed']
    assert fresh['pages']==15 and len(fresh['sheets'])==1
    assert native['fresh_visual_delta_records']==15 and native['reused_unchanged_visual_records']==268
    assert len(native['records'])==283 and native['pages']==284 and native['plan_sha256']==digest(PLAN)
    assert not plan['failures'] and not any(i['severity'] in ('error','warning') for r in plan['records'] for i in r['base_QA']['issues'])
    all_sheets=old['sheets']+fresh['sheets']
    assert all(digest(r['path'])==r['sha256'] for r in all_sheets)
    save(APPROVAL,dict(runtime=native['runtime'],manuscript=str(FORMATTING),manuscript_sha256=digest(FORMATTING),
        plan=str(PLAN),plan_sha256=digest(PLAN),native=str(FINAL),native_sha256=digest(FINAL),
        body_pages=284,typed_choice_captions=0,source_staged_progressive_pages=0,scoped_names=39,
        all_final_body_caption_and_name_sheets_directly_viewed=True,
        name_sheets_scope='39 unchanged progressive labels and three corrected full-name fields; catalogue UI remains unvisited.',
        sheets=all_sheets,earlier_visual=str(ROOT/'initial_complete_visual_review_v1.json'),
        earlier_visual_sha256=digest(ROOT/'initial_complete_visual_review_v1.json'),
        final_fresh_layouts=15,final_exact_reused_layouts=268,
        total_improved_layouts=19,one_candidate_retained_with_reason='DK4_MES_B21_R0005',
        no_prose_shortening_manual_breaks_or_display_geometry_changes=True,
        display_findings_resolved=True,stored_andactual_checks_pending=True,actual_gameplay=False,new_credit=0))
    print('All 284 final pages and scoped name sheets visually approved; 19 improved layouts, one justified layout retention.')


if __name__=='__main__':
    if sys.argv[1:]==['--approve']:approve()
    else:
        assert not sys.argv[1:]
        FunctionType(previous.previous.combine.__code__,env)()
