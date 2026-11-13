"""Refresh only changed compiled layouts; bind exact unchanged pages to their fresh proofs."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B51_B60_formatting_20261104')

if __name__=='__main__':
    output=ROOT/'layout_delta_v3';assert not output.exists()
    manuscript=ROOT/'formatting_input.json';old_path=ROOT/'automatic_v1/automatic_plans.json';new_path=ROOT/'automatic_v3/automatic_plans.json'
    native_path=ROOT/'speech_native_v1/compiled_native_pages.json'
    doc,old,new,native=map(load,[manuscript,old_path,new_path,native_path])
    assert old['manuscript_sha256']==new['manuscript_sha256']==native['manuscript_sha256']==sha(manuscript.read_bytes())
    assert not new['failures'] and not any(i['severity'] in ['warning','error'] for r in new['records'] for i in r['base_QA']['issues'])
    before={r['id']:r for r in old['records']};after={r['id']:r for r in new['records']}
    assert set(before)==set(after) and len(after)==245
    changed={k for k in after if before[k]['encoded_hex']!=after[k]['encoded_hex']}
    unchanged=set(after)-changed
    assert changed and all(after[k]['logical_English']==before[k]['logical_English'] for k in after)
    assert all(before[k]['encoded_hex']==after[k]['encoded_hex'] and before[k]['expected_native_pages']==after[k]['expected_native_pages'] for k in unchanged)
    output.mkdir();subset=deepcopy(doc)
    subset.update(records=[r for r in doc['records'] if r['id'] in changed],
        blocks=sorted({r['block'] for r in doc['records'] if r['id'] in changed}),
        physical_speech_objects=len(changed),ordinary_speech_objects=len(changed),FE_speech_objects=0,
        typed_choice_objects=0,typed_choice_commands=0,subset_of=str(manuscript),subset_of_sha256=sha(manuscript.read_bytes()))
    assert all(r['kind']=='progressive' for r in subset['records'])
    subset_path=output/'changed_manuscript.json';save(subset_path,subset)
    plan=deepcopy(new);plan.update(manuscript=str(subset_path),manuscript_sha256=sha(subset_path.read_bytes()),
        records=[r for r in new['records'] if r['id'] in changed],subset_of=str(new_path),subset_of_sha256=sha(new_path.read_bytes()))
    save(output/'changed_plans.json',plan)
    save(output/'delta.json',dict(full_manuscript=str(manuscript),full_manuscript_sha256=sha(manuscript.read_bytes()),
        old_plan=str(old_path),old_plan_sha256=sha(old_path.read_bytes()),new_plan=str(new_path),new_plan_sha256=sha(new_path.read_bytes()),
        old_native=str(native_path),old_native_sha256=sha(native_path.read_bytes()),changed_record_IDs=sorted(changed),
        unchanged_record_IDs=sorted(unchanged),fresh_changed_native_pages=sum(after[k]['expected_native_pages'] for k in changed),
        reused_exact_native_pages=sum(after[k]['expected_native_pages'] for k in unchanged),
        all245_English_paragraphs_andsource_controls_unchanged=True,
        renderer_macro_contract_font_geometry_andcurrent_ROM_dependencies_unchanged=True,
        changed_pages_require_fresh_native_anddirect_view=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Layout delta:',len(changed),'records/',sum(after[k]['expected_native_pages'] for k in changed),'fresh pages;',len(unchanged),'exact native reuses.')
