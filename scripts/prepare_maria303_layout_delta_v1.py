"""Bind the final full plan to the unchanged299-body native scope, then select exactly five changed layouts."""
from copy import deepcopy
from pathlib import Path
import runpy
import sys
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B58_B70_clean_20261109')

def main():
    fullpath=ROOT/'plan_v6_visual/automatic_plans.json';afterpath=ROOT/'plan_v6_visual/body_plans.json'
    bodypath=ROOT/'native_inputs_v1/manuscript.json';beforepath=ROOT/'native_inputs_v1/plans.json'
    nativepath=ROOT/'native_pages_v1/compiled_native_pages.json';out=ROOT/'native_delta_v1'
    assert not afterpath.exists() and not out.exists()
    full,body,before,native=map(load,[fullpath,bodypath,beforepath,nativepath])
    assert native['manuscript_sha256']==digest(bodypath) and native['plan_sha256']==digest(beforepath)
    assert len(body['records'])==len(full['records'])==len(before['records'])==len(native['records'])==299
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact']
    assert full['manuscript_sha256']==body['subset_of_sha256'] and digest(body['subset_of'])==body['subset_of_sha256']
    expected={r['id']:r for r in before['records']};updated={r['id']:r for r in full['records']}
    assert expected.keys()==updated.keys()
    changed={k for k in expected if expected[k]['encoded_hex']!=updated[k]['encoded_hex']}
    assert changed=={'DK4_MES_B58_R0178','DK4_MES_B61_R0050','DK4_MES_B62_R0093','DK4_MES_B62_R0099','DK4_MES_B64_R0092'}
    assert all(expected[k]['logical_English']==updated[k]['logical_English'] for k in expected)
    after=deepcopy(full);after.update(manuscript=str(bodypath),manuscript_sha256=digest(bodypath),
        complete_parent_plan=str(fullpath),complete_parent_plan_sha256=digest(fullpath),
        all299_plan_objects_exact_full_manuscript_projection=True,new_credit=0)
    save(afterpath,after)
    old_argv=sys.argv[:]
    try:
        sys.argv=[__file__,'--manuscript',str(bodypath),'--before-plan',str(beforepath),'--after-plan',str(afterpath),'--out',str(out)]
        runpy.run_module('scripts.prepare_editorial_native_layout_delta_v1',run_name='__main__')
    finally:sys.argv=old_argv
    assert set(load(out/'delta.json')['changed_record_IDs'])==changed
    print('Five byte-changed layouts selected;294 completed native records remain exact for reuse.')

if __name__=='__main__':main()
