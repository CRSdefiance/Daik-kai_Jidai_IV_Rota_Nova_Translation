"""Select every planned body,including both FE children,whilekeeping all15 captions separate."""
import runpy
import sys
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    doc_path = ROOT/'formatting_FE_v1/physical_manuscript.json'
    plan_path = ROOT/'plan_continuity_v2/automatic_plans.json'
    out = ROOT/'native_inputs_v1'
    assert not out.exists()
    doc, plan = map(load,[doc_path,plan_path])
    assert plan['manuscript_sha256'] == digest(doc_path) and not plan['failures']
    speech = [r for r in doc['records'] if r['kind'] in ['progressive','system-FE']]
    choices = [r for r in doc['records'] if r['kind']=='typed-choice-label']
    assert len(speech) == len(plan['records']) == 314 and len(choices) == 15
    assert {r['id'] for r in speech} == {r['id'] for r in plan['records']}
    assert not any(i['severity'] in ['warning','error'] for r in plan['records'] for i in r['base_QA']['issues'])
    sys.argv = ['prepare_editorial_native_subset_v2','--manuscript',str(doc_path),'--plan',str(plan_path),
        '--out',str(out),'--ids',*[r['id'] for r in speech]]
    runpy.run_module('scripts.prepare_editorial_native_subset_v2',run_name='__main__')
    subset = load(out/'manuscript.json')
    assert subset['records'] == speech
    save(out/'separate_choice_scope.json',dict(records=choices,choice_captions=15,choice_commands=5,
        source_editorial_objects=328,physical_body_candidates=314,one_source_riddle_has_two_native_children=True,
        unchanged_typed_objects_not_rendered_as_speech=True,all_fifth_gates_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [doc_path,plan_path,Path(__file__)]}))
    print('Selected all314 body candidates;15 captions remain separate;no new source credit ordisplay approval.')


if __name__ == '__main__':
    main()
