"""Resolve scoped automatic weak-boundary findings without changing prose or prior producers."""
import inspect
from pathlib import Path
from scripts import plan_Maria_story_layout_v7733 as prior
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/maria_story_wrap_v7734')
PRIOR=prior.ROOT/'67_automatic_full_width_plans_all_base_QA_preserved.json'
if __name__=='__main__':
    assert not ROOT.exists();previous=read(PRIOR);doc=read(prior.MANUSCRIPT)
    assert previous['manuscript_sha256']==sha(prior.MANUSCRIPT.read_bytes())
    adapter=checked_text(prior.ADAPTER,{'cost[0]+tiny,cost[1]+1,cost[2]+weak':'cost[0]+tiny+weak,cost[1]+1,cost[2]+weak'})
    env=dict(prior.ENV);exec(compile(adapter,__file__+'::scoped-weak-boundary-priority','exec'),env)
    rows=[];unresolved=[]
    for old in previous['records']:
        planning=old['planning_record'];p=env['plan'](planning)
        assert ' '.join(p['lines'])==' '.join(old['lines']) and p['source_hex']==old['source_hex']
        p.update(file_path=old['file_path'],block=old['block'],source_record_index=old['source_record_index'],source_selector=old['source_selector'],
            logical_English=old['logical_English'],planning_record=planning,base_QA=prior.base_qa(planning,p),
            previous_plan_lines=old['lines'],previous_plan_cost=old['planning_cost'],automatic_wrap_changed=p['lines']!=old['lines'])
        info=[i for i in p['base_QA']['issues'] if i['code']=='line-break-count' and i['severity']=='info']
        if info:
            r=next(r for r in doc['records'] if r['id']==p['id'])
            p['row_count_reason']=r['decision_reason']+' The complete English uses '+str(len(p['lines']))+' automatically planned rows of '+str(p['line_lengths'])+' display cells, within the native four-row page; source Japanese row boundaries are not English dramatic pauses. All words, punctuation, source macros and guards remain.'
        issues=[i for i in p['base_QA']['issues'] if i['severity'] in ['warning','error']]
        if issues:unresolved.append(dict(id=p['id'],issues=issues,lines=p['lines']))
        rows.append(p)
    assert len(rows)==67 and not previous['failures']
    ROOT.mkdir(parents=True);save(ROOT/'67_refined_full_width_plans_no_prose_changes_all_QA_preserved.json',dict(
        manuscript=str(prior.MANUSCRIPT),manuscript_sha256=sha(prior.MANUSCRIPT.read_bytes()),previous_plan=str(PRIOR),previous_plan_sha256=sha(PRIOR.read_bytes()),
        records=rows,unresolved=unresolved,source_owned_successor_adapter=adapter,
        changed_only_local_weak_boundary_cost_before_row_count=True,all_original_other_costs_guards_geometry_macros_andprose_preserved=True,
        prior_five_weak_boundary_warnings_three_records_preserved_not_waived=True,no_global_weak_boundary_orprofile_changes=True,
        row_count_notes_individually_bound_to_prose_decisions=True,physical_native_rows_per_page=4,physical_viewport=[216,64],
        native_font_compiled_stored_actual_controls_production_andrelease_pending=True,all_formatting_gates_remain_false=True,
        new_credit=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [prior.MANUSCRIPT,PRIOR,Path(prior.__file__),Path(__file__)]},full_goal_complete=False))
    print('67refined plans;changed',sum(r['automatic_wrap_changed'] for r in rows),'pages',sum(r['expected_native_pages'] for r in rows),'unresolved',unresolved)
    print('row-count infos',sum('row_count_reason' in r for r in rows))
    if unresolved:raise SystemExit(1)
