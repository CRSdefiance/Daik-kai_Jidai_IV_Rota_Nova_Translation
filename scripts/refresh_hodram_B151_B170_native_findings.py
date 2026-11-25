"""Compile only the 24 revised layouts; bind and retain the other 587 native proofs."""
from copy import deepcopy
from pathlib import Path
import subprocess
import sys
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B151_B170_formatting_20261102')
OUT=ROOT/'ordinary_native_v2'
if __name__=='__main__':
    assert not OUT.exists()
    manuscript=ROOT/'ordinary_formatting_input.json';old_plan_path=ROOT/'ordinary_plans_v2/automatic_plans.json';new_path=ROOT/'visual_replans_v2/automatic_plans.json'
    prior_path=ROOT/'ordinary_native_v1/compiled_native_pages.json'
    doc,old,new,prior=map(load,[manuscript,old_plan_path,new_path,prior_path])
    assert old['manuscript_sha256']==new['manuscript_sha256']==prior['manuscript_sha256']==sha(manuscript.read_bytes())
    assert prior['plan_sha256']==sha(old_plan_path.read_bytes()) and not new['failures']
    originals={r['id']:r for r in old['records']};replacements={r['id']:r for r in new['records']};bound={r['id']:r for r in doc['records']}
    assert len(originals)==611 and len(replacements)==24 and set(replacements)<set(originals)
    assert not any(i['severity'] in ['error','warning'] for r in new['records'] for i in r['base_QA']['issues'])
    for ident,r in replacements.items():
        assert originals[ident]['logical_English']==r['logical_English']==bound[ident]['english']
        assert r['encoded_hex']!=originals[ident]['encoded_hex']
        assert r['planning_record']==originals[ident]['planning_record']
    OUT.mkdir(parents=True)
    subset=deepcopy(doc);subset['records']=[r for r in doc['records'] if r['id'] in replacements]
    subset.update(blocks=sorted({r['block'] for r in subset['records']}),physical_speech_objects=24,typed_choice_objects=0,
        subset_of=str(manuscript),subset_of_sha256=sha(manuscript.read_bytes()))
    subpath=OUT/'changed_manuscript.json';save(subpath,subset)
    subplan={**new,'manuscript':str(subpath),'manuscript_sha256':sha(subpath.read_bytes())};subplan_path=OUT/'changed_plans.json';save(subplan_path,subplan)
    runtime=prior['runtime'];subprocess.run([sys.executable,'scripts/check_hodram_B151_B170_ordinary_native.py',
        '--manuscript',str(subpath),'--plan',str(subplan_path),'--release',runtime['release_proof'],'--startup',runtime['startup_proof'],'--out',str(OUT/'fresh')],check=True)
    fresh_path=OUT/'fresh/compiled_native_pages.json';fresh=load(fresh_path)
    assert fresh['runtime']==runtime and fresh['font_sha256']==prior['font_sha256'] and len(fresh['records'])==24
    revised={r['id']:r for r in fresh['records']};reused=[]
    for record in prior['records']:
        if record['id'] in revised:continue
        planned=originals[record['id']];assert record['compiled_hex']==planned['encoded_hex'] and record['logical_English']==planned['logical_English']
        display=record['complete_native_English_display'];pages=display['pages'] if record['kind']=='progressive' else [display]
        for page in pages:
            assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
            assert sha(Path(page['preview']).read_bytes())==page['preview_sha256']
        reused.append(record['id'])
    assert len(reused)==587
    combined=[revised.get(r['id'],r) for r in prior['records']]
    finalplans={**old,'records':[replacements.get(r['id'],r) for r in old['records']],
        'visual_refinement_plans':str(new_path),'visual_refinement_plans_sha256':sha(new_path.read_bytes()),
        'exact_unchanged_plans_reused_after_visual_review':587,'fresh_visual_replans':24,
        'evidence':{str(p):sha(p.read_bytes()) for p in [manuscript,old_plan_path,new_path,Path(__file__)]}}
    finalplan_path=ROOT/'ordinary_plans_v3/automatic_plans.json';finalplan_path.parent.mkdir();save(finalplan_path,finalplans)
    save(OUT/'compiled_native_pages.json',dict(manuscript=str(manuscript),manuscript_sha256=sha(manuscript.read_bytes()),
        plan=str(finalplan_path),plan_sha256=sha(finalplan_path.read_bytes()),runtime=runtime,font_sha256=fresh['font_sha256'],records=combined,
        pages=sum(r['expected_native_pages'] for r in finalplans['records']),fresh_compiled_alignments=fresh['fresh_compiled_alignments'],
        reused_compiled_alignments=4*len(reused),reused_record_ids=reused,changed_layout_ids=sorted(replacements),
        previous_native=str(prior_path),previous_native_sha256=sha(prior_path.read_bytes()),
        previous_direct_view_sheets=prior['review_sheets'],review_sheets=fresh['review_sheets'],fresh_native=str(fresh_path),fresh_native_sha256=sha(fresh_path.read_bytes()),
        all_records_native_checked_or_exact_same_input_runtime_font_proof_reused=True,
        direct_visual_review_pending=True,formatting_gates_still_false=True,actual_gameplay=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [manuscript,old_plan_path,new_path,prior_path,fresh_path,Path(__file__)]}))
    print('24 revised layouts/37 fresh pages checked;587 exact native records reused. Only the replacement sheets need direct view.')
