"""Join fresh changed layouts to exact compatible native proofs without rerendering unchanged text."""
import argparse
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.pack_rafael_B201_B220_review_sheets_v1 import body,read_image

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['manuscript','before-plan','after-plan','previous-native','fresh-native','delta','out','sheets']:
        parser.add_argument('--'+name,type=Path,required=True)
    a=parser.parse_args();assert not a.out.exists() and not a.sheets.exists()
    doc,before,after,old,new,delta=map(load,[a.manuscript,a.before_plan,a.after_plan,a.previous_native,a.fresh_native,a.delta])
    assert before['manuscript_sha256']==after['manuscript_sha256']==old['manuscript_sha256']==digest(a.manuscript)
    assert old['plan_sha256']==digest(a.before_plan)
    assert old['runtime']==new['runtime']==doc['runtime'] and old['font_sha256']==new['font_sha256']
    subset=load(new['manuscript']);freshplan=load(new['plan'])
    assert digest(new['manuscript'])==new['manuscript_sha256']==freshplan['manuscript_sha256']
    assert digest(new['plan'])==new['plan_sha256'] and freshplan['subset_of_sha256']==digest(a.after_plan)
    assert subset['subset_of_sha256']==digest(a.manuscript)
    source={r['id']:r for r in doc['records']}
    assert all(r==source[r['id']] for r in subset['records'])
    assert not before['failures'] and not after['failures']
    assert not any(i['severity'] in ['error','warning'] for r in after['records'] for i in r['base_QA']['issues'])
    prior={r['id']:r for r in before['records']};planned={r['id']:r for r in after['records']}
    original={r['id']:r for r in old['records']};fresh={r['id']:r for r in new['records']}
    assert original.keys()==prior.keys()==planned.keys()
    changed={k for k in prior if prior[k]['encoded_hex']!=planned[k]['encoded_hex']}
    assert changed==fresh.keys()==set(delta['changed_record_IDs'])
    assert all(prior[k]['logical_English']==planned[k]['logical_English'] for k in prior)
    for receipt in [old,new]:
        assert receipt['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
        assert receipt['complete_consumption_andpagination_exact'] and not receipt['actual_gameplay']
    records=[]
    for key,plan in planned.items():
        row=deepcopy(fresh.get(key,original[key]))
        assert row['compiled_hex']==plan['encoded_hex'] and row['logical_English']==plan['logical_English']
        assert len(row['native_alignment']['cases'])==4
        display=row['complete_native_English_display']
        pages=[display] if row['kind']=='system-FE' else display['pages']
        assert len(pages)==plan['expected_native_pages']
        assert all(digest(p['native_plane'])==p['native_plane_sha256'] for p in pages)
        records.append(row)
    pages=sum(r['expected_native_pages'] for r in planned.values())
    assert new['pages']==delta['fresh_pages'] and new['fresh_compiled_alignments']==4*len(fresh)
    result={**old,'records':records,'pages':pages,'plan':str(a.after_plan),'plan_sha256':digest(a.after_plan),
        'current_version_fresh_records':len(fresh),'current_version_exact_reused_records':len(records)-len(fresh),
        'current_version_fresh_alignments':4*len(fresh),'current_version_exact_reused_alignments':4*(len(records)-len(fresh)),
        'all_current_placement_alignments':4*len(records),'review_sheets':[],
        'direct_visual_review_pending':True,'previous_native':str(a.previous_native),'previous_native_sha256':digest(a.previous_native),
        'all_unselected_compiled_bytes_andprose_exact':True,'new_credit':0,
        'evidence':{**old['evidence'],**new['evidence'],**{str(p):digest(p) for p in [a.manuscript,a.before_plan,a.after_plan,a.previous_native,a.fresh_native,a.delta,Path(__file__)]}}}
    a.out.parent.mkdir(parents=True,exist_ok=True);save(a.out,result)
    reader=FunctionType(read_image.__code__,{**read_image.__globals__,'digest':digest})
    pack=FunctionType(body.__code__,{**body.__globals__,'read_image':reader})
    pack(a.sheets,a.fresh_native)
    print(dict(final_records=len(records),final_pages=pages,fresh_records=len(fresh),fresh_pages=new['pages'],unchanged_records=len(records)-len(fresh)))

if __name__=='__main__':main()
