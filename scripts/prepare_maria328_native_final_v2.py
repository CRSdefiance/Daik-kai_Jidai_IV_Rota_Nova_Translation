"""Preserve all completed native records and rerun just one changed proved layout."""
import runpy
import sys
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    out=ROOT/'native_final_selection_v2.json';assert not out.exists()
    docpath=ROOT/'formatting_FE_v1/physical_manuscript.json';planpath=ROOT/'plan_visual_v5/automatic_plans.json'
    doc,plan=map(load,[docpath,planpath]);assert plan['manuscript_sha256']==digest(docpath) and not plan['failures']
    originals={r['id']:r for r in doc['records']};planned={r['id']:r for r in plan['records']}
    candidates=load(ROOT/'native_final_selection_v1.json')['exact_reused_records'][:]
    journals=sorted((ROOT/'native_final_v1').glob('complete_*.json'));assert len(journals)==92
    for path in journals:
        proof=load(path);inputs=load(proof['native_run_inputs'])
        assert digest(proof['native_run_inputs'])==proof['native_run_inputs_sha256']
        assert inputs['runtime']==doc['runtime'] and inputs['all_v1_native_assertions_preserved']
        assert proof['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass']
        candidates.append(dict(id=proof['record']['id'],record=proof['record'],path=str(path),sha256=digest(path)))
    assert len(candidates)==len({r['id'] for r in candidates})==225
    selected=[];changed=[]
    for binding in candidates:
        assert digest(binding['path'])==binding['sha256']
        row=binding['record'];ident=row['id'];original=originals[ident]
        assert row['source_reference']==original['source_reference'] and row['current_reference']==original['current_reference']
        assert row['logical_English']==original['english'] and len(row['native_alignment']['cases'])==4
        if row['compiled_hex']!=planned[ident]['encoded_hex']:changed.append(ident);continue
        panels=row['complete_native_English_display']['pages'] if row['kind']=='progressive' else [row['complete_native_English_display']]
        assert len(panels)==planned[ident]['expected_native_pages']
        for p in panels:assert digest(p['preview'])==p['preview_sha256'] and digest(p['native_plane'])==p['native_plane_sha256']
        selected.append(binding)
    assert changed==['DK4_MES_B88_R0204'] and len(selected)==224
    ids=[r['id'] for r in doc['records'] if r['kind'] in ['progressive','system-FE'] and r['id'] not in {s['id'] for s in selected}]
    assert len(ids)==90
    save(out,dict(exact_reused_records=selected,exact_reused_count=224,reused_alignment_cases=896,
        changed_completed_layouts=changed,fresh_ids=ids,fresh_count=90,all_fifth_gates_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [docpath,planpath,ROOT/'native_final_selection_v1.json',__file__]}))
    sys.argv=['prepare_editorial_native_subset_v2','--manuscript',str(docpath),'--plan',str(planpath),
        '--out',str(ROOT/'native_final_inputs_v2'),'--ids',*ids]
    runpy.run_module('scripts.prepare_editorial_native_subset_v2',run_name='__main__')

if __name__=='__main__':main()
