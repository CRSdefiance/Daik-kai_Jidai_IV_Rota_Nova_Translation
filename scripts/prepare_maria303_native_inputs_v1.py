"""Project all299 original speech objects for the unchanged native runner; retain four captions separately."""
import runpy
import sys
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B58_B70_clean_20261109')

def main():
    docpath=ROOT/'formatting_v3/formatting_input_complete_indices_v1.json'
    planpath=ROOT/'plan_v5_page_continuity/automatic_plans.json';out=ROOT/'native_inputs_v1'
    doc,plan=map(load,[docpath,planpath]);assert not out.exists()
    assert plan['manuscript_sha256']==digest(docpath) and not plan['failures']
    speech=[r for r in doc['records'] if r['kind'] in ['progressive','system-FE']]
    choices=[r for r in doc['records'] if r['kind']=='typed-choice-label']
    assert len(speech)==len(plan['records'])==299 and len(choices)==4
    assert {r['id'] for r in speech}=={r['id'] for r in plan['records']}
    assert all(r['expected_native_pages']==1 for r in plan['records'])
    assert not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    sys.argv=['prepare_editorial_native_subset_v2','--manuscript',str(docpath),'--plan',str(planpath),
        '--out',str(out),'--ids',*[r['id'] for r in speech]]
    runpy.run_module('scripts.prepare_editorial_native_subset_v2',run_name='__main__')
    subset=load(out/'manuscript.json');assert subset['records']==speech
    save(out/'separate_choice_scope.json',dict(records=choices,choice_captions=4,choice_commands=2,
        unchanged_typed_objects_not_rendered_as_speech=True,all_fifth_gates_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [docpath,planpath,Path(__file__)]}))
    print('Selected all299 exact speech objects;four choice captions retained separately, no review credit.')

if __name__=='__main__':main()
