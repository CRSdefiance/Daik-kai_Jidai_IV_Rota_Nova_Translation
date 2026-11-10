"""Two contextual refinements after whole actual-scene review; preserve all earlier manuscripts."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_Maria_story_layout_v7733 as layout
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_final_prose_v7756')
PREVIOUS=Path('translations/maria_B34_B108_B35_editorial_manuscript_v2.json')
OUTPUT=Path('translations/maria_B34_B108_B35_editorial_manuscript_v3.json')
VIEW=Path('work/analysis/maria_story_actual_view_v7755/131_actual_panes33_sheets_viewed_named_limits_two_final_prose_refinements.json')
PREVIOUS_PLAN=Path('work/analysis/maria_story_refined_v7735/67_refined_decisions_native_logical_bindings_automatic_plans_QA.json')
CHANGES={
    'DK4_MES_B34_R0042':("It looks like we'll need to act before any harm comes to my homeland.",
        "Clean 祖国 is Maria's homeland. My avoids assigning her companions a shared national origin, while preserving the tentative assessment, protective motive and collective intended action."),
    'DK4_MES_B108_R0111':("I hear the Argot Company's young leader has a strong sense of justice. They say she was furious and would never forgive FO.",
        "The report frame They say scopes both the anger and categorical would never forgive. Preserve the young female leader, strong justice, two hearsay frames, reported indignation and refusal without inventing a sworn vow or direct personal knowledge. Remove the redundant said she'd construction, whose verified v2 layout unnecessarily continued on a short second page."),
}
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();old,view,previous_plan=map(read,[PREVIOUS,VIEW,PREVIOUS_PLAN])
    assert previous_plan['manuscript_sha256']==sha(PREVIOUS.read_bytes()) and {r['id'] for r in view['final_prose_refinements']}==set(CHANGES)
    doc=deepcopy(old);changed=[];plans=[]
    adapter=checked_text(layout.ADAPTER,{'cost[0]+tiny,cost[1]+1,cost[2]+weak':'cost[0]+tiny+weak,cost[1]+1,cost[2]+weak'})
    env=dict(layout.ENV);exec(compile(adapter,__file__+'::same-scoped-full-width-planner','exec'),env)
    for row in doc['records']:
        if row['id'] in CHANGES:
            english,reason=CHANGES[row['id']];previous=deepcopy(row)
            assert row['decision']=='revision'
            for token in ['FI','FA','FO']:assert english.count(token)==row['english'].count(token)
            row.update(english=english,decision_reason=row['decision_reason']+' Final actual-scene review: '+reason,
                previous_v2_English=previous['english'],final_contextual_refinement_reason=reason,previous_v2_prose_fully_preserved=True)
            changed.append(dict(id=row['id'],before=previous['english'],after=english,reason=reason))
        planning=deepcopy(row);body=row['english']
        for token in ['FI','FA','FO']:body=body.replace(token,'{MACRO:'+token+'}')
        planning['english']='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+body;p=env['plan'](planning)
        assert ' '.join(p['lines'])==body
        p.update(file_path=row['file_path'],block=row['block'],source_record_index=row['source_record_index'],source_selector=row['source_selector'],
            logical_English=row['english'],planning_record=planning,base_QA=layout.base_qa(planning,p))
        assert not any(i['severity'] in ['warning','error'] for i in p['base_QA']['issues'])
        if any(i['code']=='line-break-count' and i['severity']=='info' for i in p['base_QA']['issues']):
            p['row_count_reason']=row['decision_reason']+' Complete English uses '+str(len(p['lines']))+' automatically planned rows of '+str(p['line_lengths'])+' cells. All facts, words, punctuation and source macros remain within the original four-row page.'
        if row['id'] not in CHANGES:
            prior=next(v for v in previous_plan['records'] if v['id']==row['id'])
            assert p['encoded_hex']==prior['encoded_hex'] and p['lines']==prior['lines']
        plans.append(p)
    assert len(changed)==2 and len(plans)==67 and sum(p['expected_native_pages'] for p in plans)==67
    doc.update(previous_manuscript=str(PREVIOUS),previous_manuscript_sha256=sha(PREVIOUS.read_bytes()),
        actual_v2_view=str(VIEW),actual_v2_view_sha256=sha(VIEW.read_bytes()),two_after_actual_contextual_refinements=changed,
        all65_unchanged_other_compiled_plans_exact=True,new_two_native_stored_andaffected_English_actual_checks_pending=True,
        no_claim_v2_changed_paragraph_actual_pixels_apply_to_v3=True)
    save(OUTPUT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'67_final_v3_plans_two_refinements65_exact_compiled_retentions.json',dict(
        manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),previous_manuscript=str(PREVIOUS),previous_manuscript_sha256=sha(PREVIOUS.read_bytes()),
        records=plans,changed_records=changed,decisions=dict(revision=48,retention=19),source_owned_automatic_plan_adapter=adapter,
        all67_automatic_plans_single_native_four_row_pages=True,all65_other_compiled_bodies_andlineplans_exact=True,
        prior_v2_successful_two_page_native_andactual_evidence_preserved=True,
        no_manual_break_prose_fact_omission_global_profile_width_macro_orfont_change=True,
        new_two_logical_compiled_stored_glyph_andaffected_English_actual_evidence_pending=True,
        all67_formatting_gates_false=True,no_ROM_orcredit_change=True,
        evidence={str(p):sha(p.read_bytes()) for p in [PREVIOUS,OUTPUT,VIEW,PREVIOUS_PLAN,Path(__file__)]},full_goal_complete=False))
    print('v3:two faithful refinements;48revisions19retentions;67single-page plans;65other compiled bodies exact. New two native/stored/affected English actual checks pending.No ROM orcredit.')
    for p in plans:
        if p['id'] in CHANGES:print(p['id'],p['lines'],p['line_lengths'])
