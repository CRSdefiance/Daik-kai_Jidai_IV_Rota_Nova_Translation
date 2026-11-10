"""Reuse exact completed planes and select only unproved or changed layouts."""
import runpy
import sys
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    manuscript=ROOT/'formatting_FE_v1/physical_manuscript.json'
    plan_path=ROOT/'plan_visual_v4/automatic_plans.json'
    out=ROOT/'native_final_selection_v1.json'
    assert not out.exists()
    doc,plan=map(load,[manuscript,plan_path])
    assert plan['manuscript_sha256']==digest(manuscript) and not plan['failures']
    originals={r['id']:r for r in doc['records']}
    plans={r['id']:r for r in plan['records']}
    candidates=[]
    initial=load(ROOT/'native_resume_selection_v1.json')
    for binding in initial['bindings']:
        path=binding['path']; assert digest(path)==binding['sha256']
        record=next(r for r in load(path)['records'] if r['id']==binding['id'])
        candidates.append((record,path))
    journals=sorted((ROOT/'native_resume_v1').glob('complete_*.json'))
    assert len(journals)==15
    for path in journals:
        proof=load(path);inputs=load(proof['native_run_inputs'])
        assert digest(proof['native_run_inputs'])==proof['native_run_inputs_sha256']
        assert inputs['runtime']==doc['runtime'] and inputs['all_v1_native_assertions_preserved']
        assert proof['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass']
        candidates.append((proof['record'],str(path)))
    assert len(candidates)==len({r['id'] for r,p in candidates})==136
    reused=[];changed=[]
    for row,path in candidates:
        ident=row['id']; original=originals[ident]
        assert row['source_reference']==original['source_reference'] and row['current_reference']==original['current_reference']
        assert row['logical_English']==original['english'] and len(row['native_alignment']['cases'])==4
        if row['compiled_hex']!=plans[ident]['encoded_hex']:
            changed.append(ident);continue
        panels=row['complete_native_English_display']['pages'] if row['kind']=='progressive' else [row['complete_native_English_display']]
        assert len(panels)==plans[ident]['expected_native_pages']
        for panel in panels:
            assert digest(panel['preview'])==panel['preview_sha256'] and digest(panel['native_plane'])==panel['native_plane_sha256']
        reused.append(dict(id=ident,path=str(path),sha256=digest(path),record=row))
    assert sorted(changed)==['DK4_MES_B74_R0070','DK4_MES_B75_R0012','DK4_MES_B76_R0038']
    assert len(reused)==133
    ids=[r['id'] for r in doc['records'] if r['kind'] in ['progressive','system-FE'] and r['id'] not in {r['id'] for r in reused}]
    assert len(ids)==181
    save(out,dict(exact_reused_records=reused,exact_reused_count=133,reused_alignment_cases=532,
        changed_completed_layouts=changed,fresh_ids=ids,fresh_count=181,
        FE_failure_not_accepted_orwaived=True,all_fifth_gates_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [manuscript,plan_path,ROOT/'native_resume_selection_v1.json',__file__]}))
    sys.argv=['prepare_editorial_native_subset_v2','--manuscript',str(manuscript),'--plan',str(plan_path),
        '--out',str(ROOT/'native_final_inputs_v1'),'--ids',*ids]
    runpy.run_module('scripts.prepare_editorial_native_subset_v2',run_name='__main__')

if __name__=='__main__':main()
