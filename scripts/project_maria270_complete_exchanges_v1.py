"""Keep thirteen complete exchanges moving while retaining the unresolved full FE exchange."""
from copy import deepcopy
from pathlib import Path
from collections import Counter
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B37_B50_clean_20261109')
OUT=ROOT/'complete_B37_B49_projection_v1'

def main():
    assert not OUT.exists()
    prose_path=Path('translations/maria_B37_B50_contextual_review_v1.json')
    form_path=ROOT/'formatting_v1/formatting_input.json'
    plan_path=ROOT/'refined_plan_v2/automatic_plans.json'
    prose,form,plan=map(load,[prose_path,form_path,plan_path])
    assert plan['manuscript_sha256']==digest(form_path)
    assert {r['id'] for r in plan['failures']}=={'DK4_MES_B50_R0043'}
    blocks=list(range(37,50));selected=[r for r in form['records'] if r['block'] in blocks]
    withheld=[r for r in form['records'] if r['block']==50]
    assert len(selected)==270 and len(withheld)==16
    ids={r['id'] for r in selected};prose_ids={r['id'] for r in prose['records'] if r['block'] in blocks}
    assert ids==prose_ids and len(ids)==270
    for block in blocks:
        assert [r for r in selected if r['block']==block]==[r for r in form['records'] if r['block']==block]
    counts=Counter(r['decision'] for r in selected)
    projected=deepcopy(form);projected.update(records=deepcopy(selected),blocks=blocks,source_objects=270,
        proposed_revisions=counts['revision'],justified_retentions=counts['retention'],physical_speech_objects=266,
        ordinary_speech_objects=266,typed_choice_objects=4,typed_choice_commands=2,
        source_macro_occurrences=sum(sum(r['source_macros'].values()) for r in selected),
        subset_of=str(form_path),subset_of_sha256=digest(form_path),
        complete_exchange_scope_projection_only=True,no_prose_orcontrol_orper_record_gate_changes=True,
        withheld_complete_exchange=50,full_B50_source_prose_anddisplay_risk_preserved=True,new_credit=0)
    assert Counter(r['kind'] for r in selected)=={'progressive':265,'system-FE':1,'typed-choice-label':4}
    assert projected['source_macro_occurrences']==18
    OUT.mkdir();new_form=OUT/'formatting_input.json';save(new_form,projected)
    scoped_plan=deepcopy(plan);scoped_plan.update(manuscript=str(new_form),manuscript_sha256=digest(new_form),
        records=[r for r in plan['records'] if r['id'] in ids],failures=[],
        complete_parent_plan=str(plan_path),complete_parent_plan_sha256=digest(plan_path),
        excluded_failure_belongs_only_to_withheld_complete_B50=True,new_credit=0)
    assert len(scoped_plan['records'])==266
    assert not any(i['severity'] in ['warning','error'] for r in scoped_plan['records'] for i in r['base_QA']['issues'])
    save(OUT/'automatic_plans.json',scoped_plan)
    manuscript=deepcopy(prose);manuscript.update(records=[r for r in prose['records'] if r['id'] in ids],blocks=blocks,
        source_objects=270,proposed_revisions=counts['revision'],justified_retentions=counts['retention'],
        subset_of=str(prose_path),subset_of_sha256=digest(prose_path),complete_exchange_scope_projection_only=True,new_credit=0)
    structural=deepcopy(manuscript);structural['translation_policy']='natural-dialogue-v1';validate_natural_dialogue_batch(structural)
    save(OUT/'contextual_review.json',manuscript)
    initial_rows=[];block_receipts=[];sheets=[]
    for block in blocks:
        path=ROOT/f'initial_native_v1/B{block}_checked.json';receipt=load(path)
        assert receipt['actual_gameplay'] is False and receipt['new_credit']==0
        initial_rows+=receipt['records'];block_receipts.append(dict(path=str(path),sha256=digest(path)))
        for p in sorted((ROOT/'initial_native_v1').glob(f'B{block}_part*.png')):sheets.append(dict(path=str(p),sha256=digest(p)))
    source_byid={r['id']:r for r in selected}
    original_plan=load(ROOT/'format_plan_v1/automatic_plans.json');old={r['id']:r for r in original_plan['records']}
    assert len(initial_rows)==266 and {r['id'] for r in initial_rows}=={r['id'] for r in scoped_plan['records']}
    pages=0
    for r in initial_rows:
        source=source_byid[r['id']]
        assert r['source_reference']==source['source_reference'] and r['current_reference']==source['current_reference']
        assert r['compiled_hex']==old[r['id']]['encoded_hex'] and r['logical_English']==source['english']
        assert len(r['native_alignment']['cases'])==4
        assert all(c['output_hex']==r['expanded_native_hex'] for c in r['native_alignment']['cases'])
        rendered=r['complete_native_English_display']
        actual=rendered['pages'] if r['kind']=='progressive' else [rendered]
        assert len(actual)==old[r['id']]['expected_native_pages']
        for page in actual:
            assert digest(page['preview'])==page['preview_sha256'] and digest(page['native_plane'])==page['native_plane_sha256']
        pages+=len(actual)
    assert pages==276 and len(sheets)==30
    changed=[r['id'] for r in scoped_plan['records'] if r['encoded_hex']!=old[r['id']]['encoded_hex']]
    new_pages=sum(r['expected_native_pages'] for r in scoped_plan['records'])
    retained_counts=Counter(r['decision'] for r in withheld)
    save(OUT/'projection_qualification.json',dict(selected_records=270,complete_exchanges=13,
        revisions=counts['revision'],justified_retentions=counts['retention'],body_records=266,
        progressive=265,system_FE=1,captions=4,source_macro_occurrences=18,
        initial_completed_native_blocks=block_receipts,initial_native_bodies=266,initial_native_pages=276,
        directly_viewed_initial_body_sheets=sheets,all276_initial_selected_pages_directly_viewed=True,
        full_initial_runner_failed_later_in_withheld_B50_not_claimed_full_success=True,
        immutable_completed_block_records=str(OUT/'initial_completed_block_records.json'),
        four_potential_page_reclaims=276-new_pages,proposed_pages=new_pages,
        changed_layout_ids=changed,changed_layouts_need_fresh_native_anddirect_visual_checks=True,
        withheld_records=16,withheld_block=50,withheld_revisions=retained_counts['revision'],
        withheld_retentions=retained_counts['retention'],
        unresolved='B50R43 unchanged139-character FE counterfactual: generic38 layout fails native bounds; validated36/37 guarded plans cannot fit all words. Preserve full prose; separate complete B50 until resolved.',
        FE_R36_blank_row_cause_evidence=str(ROOT/'FE_row_diagnostic_v1.json'),
        all287_generated_initial_images_directly_viewed=False,
        actual_generated_initial_body_images_directly_viewed=283,
        included_initial_B50_completed7_sheet=dict(path=str(ROOT/'B50_initial_completed7.png'),sha256=digest(ROOT/'B50_initial_completed7.png')),
        all42_name_strings_andboth_menu_sheets_directly_viewed=True,
        all_fifth_gates_false=True,registered_integration_andgameplay_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [prose_path,form_path,plan_path,ROOT/'FE_row_diagnostic_v1.json',Path(__file__)]}))
    save(OUT/'initial_completed_block_records.json',dict(records=initial_rows,completed_blocks=blocks,
        runtime=form['runtime'],initial_manuscript=str(form_path),initial_manuscript_sha256=digest(form_path),
        initial_plan=str(ROOT/'format_plan_v1/automatic_plans.json'),
        initial_plan_sha256=digest(ROOT/'format_plan_v1/automatic_plans.json'),
        original_block_receipts=block_receipts,no_full_failed_run_pass_inferred=True,
        source_code='scripts/check_editorial_compiled_pages_static_captain_v1.py',
        source_code_sha256=digest('scripts/check_editorial_compiled_pages_static_captain_v1.py'),
        reused_complete_native_calls=1064,pages=276,direct_visual_review_complete=True,
        changed_compiled_rows_unapproved_until_fresh_checks=True,new_credit=0))
    print('Projected270 records:',dict(counts),'in13 complete exchanges;',len(changed),'changed layouts/',new_pages,'proposed pages;B50’s16 retained as unfinished,zero credit.')

if __name__=='__main__':main()
