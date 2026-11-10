"""Requalify proven pages after six visual preferences; preserve both failed full runs."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')
RELEASE=Path('work/analysis/Rafael_B51_B60_release_verified_20261104/registered_release_verification.json')

if __name__=='__main__':
    output=ROOT/'native_resume_v3';assert not output.exists()
    manuscript=ROOT/'formatting_input_v3.json';plan_path=ROOT/'automatic_v7/automatic_plans.json'
    doc,plans=map(load,[manuscript,plan_path]);targets={r['id']:r for r in plans['records']}
    assert not plans['failures'] and len(targets)==539
    assert not any(i['severity'] in ['error','warning'] for r in plans['records'] for i in r['base_QA']['issues'])
    ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)
    old_path=ROOT/'native_resume_v2/exact_reused_native_records.json';old=load(old_path)
    assert old['runtime']==ctx.receipt() and old['reused_records']==288
    rows={};origins={};retired=[]
    for row in old['records']:
        target=targets[row['id']]
        if row['compiled_hex']!=target['encoded_hex'] or row['logical_English']!=target['logical_English']:
            retired.append(row['id']);continue
        rows[row['id']]=deepcopy(row)
        origins[row['id']]=dict(parent=str(old_path),parent_sha256=sha(old_path.read_bytes()),original=old['origins'][row['id']])
    assert len(rows)==283 and len(retired)==5
    partials=[ROOT/f'speech_native_resume_v2/B{block}_checked.json' for block in [63,64,66,67]]
    fresh=0
    for path in partials:
        for row in load(path)['records']:
            target=targets[row['id']]
            assert row['id'] not in rows and row['compiled_hex']==target['encoded_hex'] and row['logical_English']==target['logical_English']
            assert len(row['native_alignment']['cases'])==4
            assert all(c['output_hex']==row['expanded_native_hex'] for c in row['native_alignment']['cases'])
            rendered=row['complete_native_English_display']
            assert rendered['complete_consumed_bytes']==len(bytes.fromhex(row['expanded_native_hex']))
            assert rendered['all_visible_first_internal_final_characters_in_order'] and rendered['no_blank_or_overlap_page']
            rows[row['id']]=deepcopy(row)
            origins[row['id']]=dict(path=str(path),sha256=sha(path.read_bytes()),completed_block_from_terminal_row_failure_run=True)
            fresh+=1
    assert fresh==6 and len(rows)==289
    assert sum(targets[k]['expected_native_pages'] for k in rows)==294
    output.mkdir()
    save(output/'exact_reused_native_records.json',dict(runtime=ctx.receipt(),records=list(rows.values()),origins=origins,
        reused_records=289,reused_pages=294,retired_due_to_five_fresh_visual_preferences=retired,
        second_run=dict(session=12690,exit_code=1,completed_blocks=[63,64,66,67],
            failure='B69R87 actual FE glyph row mismatch;all macro defaults now correct. Concrete proof andpreview saved.'),
        original_failed_run_andall_complete_compatible_blocks_preserved=True,
        no_whole_failed_run_orunsealed_partial_B69_reuse_claim=True,
        all_compatible_compiled_bytes_prose_controls_font_runtime_andpage_counts_exact=True,
        evidence={str(p):sha(p.read_bytes()) for p in [manuscript,plan_path,old_path,*partials,RELEASE,Path(__file__)]},
        no_new_visual_oractual_gameplay_claim=True,new_credit=0))
    subset=deepcopy(doc);subset['records']=[r for r in doc['records'] if r['id'] not in rows]
    assert len(subset['records'])==250
    subset.update(blocks=sorted({r['block'] for r in subset['records']}),physical_speech_objects=250,
        ordinary_speech_objects=sum(r['kind']=='progressive' for r in subset['records']),
        FE_speech_objects=sum(r['kind']=='system-FE' for r in subset['records']),
        subset_of=str(manuscript),subset_of_sha256=sha(manuscript.read_bytes()))
    sub=output/'remaining_manuscript.json';save(sub,subset)
    plan=deepcopy(plans);plan.update(manuscript=str(sub),manuscript_sha256=sha(sub.read_bytes()),
        records=[r for r in plans['records'] if r['id'] not in rows],subset_of=str(plan_path),subset_of_sha256=sha(plan_path.read_bytes()))
    assert sum(r['expected_native_pages'] for r in plan['records'])==251
    save(output/'remaining_plans.json',plan)
    print('Qualified289 exact native records/294 pages. Fresh250 records/251 pages remain, includingfive phrase refinements andthe scoped FE guard fix.',flush=True)
