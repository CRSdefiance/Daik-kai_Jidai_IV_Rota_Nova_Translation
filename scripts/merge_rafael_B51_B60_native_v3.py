"""Bind245 native records by exact compiled bytes,with38 refreshed and207 reused."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B51_B60_formatting_20261104')

if __name__=='__main__':
    original=ROOT/'speech_native_v1/compiled_native_pages.json';delta_path=ROOT/'speech_native_delta_v3/compiled_native_pages.json'
    plans_path=ROOT/'automatic_v3/automatic_plans.json';delta_manifest=ROOT/'layout_delta_v3/delta.json'
    out=ROOT/'combined_native_v3.json';assert not out.exists()
    first,fresh,plans,delta=map(load,[original,delta_path,plans_path,delta_manifest])
    assert first['runtime']==fresh['runtime'] and first['font_sha256']==fresh['font_sha256']
    rows={r['id']:deepcopy(r) for r in first['records']}
    updated={r['id']:r for r in fresh['records']}
    assert set(updated)==set(delta['changed_record_IDs'])
    rows.update(updated)
    assert len(rows)==245 and all(rows[r['id']]['compiled_hex']==r['encoded_hex'] for r in plans['records'])
    result=deepcopy(first);result.update(records=[rows[r['id']] for r in plans['records']],
        plan=str(plans_path),plan_sha256=sha(plans_path.read_bytes()),pages=253,
        direct_visual_review_pending=True,two_new_page_boundary_findings_pending=True,
        current_version_fresh_records=38,current_version_exact_reused_records=207,
        source_native_receipts={str(p):sha(p.read_bytes()) for p in [original,delta_path,plans_path,delta_manifest,Path(__file__)]})
    save(out,result);print('Bound245 native records to exact v3 compiled bytes;two visual boundary refinements remain.')
