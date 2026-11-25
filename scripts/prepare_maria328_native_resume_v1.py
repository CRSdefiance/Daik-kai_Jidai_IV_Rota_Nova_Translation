"""Reuse completed whole blocks; run only the remaining bodies with durable receipts."""
import runpy
import sys
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    doc_path=ROOT/'native_inputs_v1/manuscript.json'
    plan_path=ROOT/'native_inputs_v1/plans.json'
    receipt=ROOT/'native_resume_selection_v1.json'
    assert not receipt.exists()
    doc, plan=map(load,[doc_path,plan_path])
    assert plan['manuscript_sha256']==digest(doc_path) and not plan['failures']
    originals={r['id']:r for r in doc['records']}
    plans={r['id']:r for r in plan['records']}
    completed=[]; bindings=[]
    for block in [73,74,75,76,77,78,81,82,83,84,85,86]:
        path=ROOT/f'native_pages_v1/B{block}_checked.json'
        proof=load(path)
        assert proof['actual_gameplay'] is False and proof['new_credit']==0
        assert {r['id'] for r in proof['records']}=={r['id'] for r in doc['records'] if r['block']==block}
        for row in proof['records']:
            original=originals[row['id']]
            assert row['source_reference']==original['source_reference'] and row['current_reference']==original['current_reference']
            assert row['compiled_hex']==plans[row['id']]['encoded_hex'] and row['logical_English']==original['english']
            assert len(row['native_alignment']['cases'])==4
            panels=row['complete_native_English_display']['pages'] if row['kind']=='progressive' else [row['complete_native_English_display']]
            for panel in panels:
                assert digest(panel['preview'])==panel['preview_sha256'] and digest(panel['native_plane'])==panel['native_plane_sha256']
            completed.append(row)
            bindings.append(dict(id=row['id'],path=str(path),sha256=digest(path)))
    assert len(completed)==len({r['id'] for r in completed})==121
    ids=[r['id'] for r in doc['records'] if r['id'] not in {c['id'] for c in completed}]
    assert len(ids)==193
    save(receipt,dict(completed_records_reused=121,completed_alignment_cases=484,bindings=bindings,ids=ids,
        unjournaled_partial_B87_not_claimed_as_complete=True,new_credit=0,
        evidence={str(p):digest(p) for p in [doc_path,plan_path,ROOT/'formatting_v1/native_macro_measurements.json',
            ROOT/'formatting_v1/role_bindings.json',__file__]}))
    sys.argv=['prepare_editorial_native_subset_v2','--manuscript',str(doc_path),'--plan',str(plan_path),
        '--out',str(ROOT/'native_resume_inputs_v1'),'--ids',*ids]
    runpy.run_module('scripts.prepare_editorial_native_subset_v2',run_name='__main__')

if __name__=='__main__':main()
