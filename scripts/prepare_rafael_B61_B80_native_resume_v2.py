"""Keep completed compatible native blocks and delta results; resume only unproved bytes."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')
RELEASE=Path('work/analysis/Rafael_B51_B60_release_verified_20261104/registered_release_verification.json')

if __name__=='__main__':
    output=ROOT/'native_resume_v2';assert not output.exists()
    manuscript=ROOT/'formatting_input_v3.json';plan_path=ROOT/'automatic_v5/automatic_plans.json'
    old_manuscript=ROOT/'formatting_input_v2.json';old_plan=ROOT/'automatic_v2/automatic_plans.json'
    doc,plans=map(load,[manuscript,plan_path]);targets={r['id']:r for r in plans['records']}
    assert not plans['failures'] and len(targets)==539
    ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)
    assert doc['current_ROM_sha256']==ctx.receipt()['candidate_sha256']
    before=load(old_plan);assert before['manuscript_sha256']==sha(old_manuscript.read_bytes())
    before_byid={r['id']:r for r in before['records']}
    sources=[ROOT/f'speech_native_v1/B{block}_checked.json' for block in range(61,69)]
    assert all(p.is_file() for p in sources)
    delta_path=ROOT/'speech_native_delta_v4/compiled_native_pages.json';delta=load(delta_path)
    assert delta['runtime']==ctx.receipt() and delta['pages']==12 and len(delta['records'])==7
    assert delta['complete_consumption_andpagination_exact'] and delta['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    rows={};origins={};old_records=0;retired=[]
    for path in sources:
        for row in load(path)['records']:
            old_records+=1;target=targets[row['id']]
            assert row['compiled_hex']==before_byid[row['id']]['encoded_hex']
            if row['compiled_hex']!=target['encoded_hex'] or row['logical_English']!=target['logical_English']:
                retired.append(row['id']);continue
            assert len(row['native_alignment']['cases'])==4
            assert all(c['output_hex']==row['expanded_native_hex'] for c in row['native_alignment']['cases'])
            rendered=row['complete_native_English_display']
            if row['kind']=='system-FE':
                assert rendered['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
                assert rendered['planned_native_row_comparison']['complete_glyph_row_membership_exact']
                pages=1
            else:
                assert rendered['all_visible_first_internal_final_characters_in_order'] and rendered['no_blank_or_overlap_page']
                assert rendered['complete_consumed_bytes']==len(bytes.fromhex(row['expanded_native_hex']))
                pages=len(rendered['pages'])
            assert pages==target['expected_native_pages']
            rows[row['id']]=deepcopy(row)
            origins[row['id']]=dict(path=str(path),sha256=sha(path.read_bytes()),
                complete_block_from_terminal_failed_run=True,failed_run_not_claimed_as_whole_batch_pass=True)
    assert old_records==289 and len(rows)==281 and len(retired)==8
    for row in delta['records']:
        target=targets[row['id']]
        assert row['id'] not in rows and row['compiled_hex']==target['encoded_hex'] and row['logical_English']==target['logical_English']
        rows[row['id']]=deepcopy(row)
        origins[row['id']]=dict(path=str(delta_path),sha256=sha(delta_path.read_bytes()),complete_terminal_native_delta_pass=True)
    assert len(rows)==288
    output.mkdir()
    save(output/'exact_reused_native_records.json',dict(runtime=ctx.receipt(),records=list(rows.values()),origins=origins,
        old_full_run=dict(session=91157,exit_code=1,completed_blocks=list(range(61,69)),
            failure='First B69 FE/name call reached a stale Hodram expected-value assertion in the FE harness;not a ROM/default-name defect.',
            original_compiled_page_checker='scripts/check_rafael_early_tutorial_compiled_pages.py',
            original_compiled_page_checker_sha256=sha(Path('scripts/check_rafael_early_tutorial_compiled_pages.py').read_bytes())),
        all_compatible_compiled_bytes_logical_prose_controls_andnative_page_counts_exact=True,
        own_registered_Rafael_snapshot_andunchanged_native_renderer_font_dependencies=True,
        initial14_ellipsis_andseven_boundary_changes_require_their_own_fresh_proofs=True,
        reused_records=288,reused_pages=293,retired_completed_block_records=retired,
        no_new_visual_oractual_gameplay_claim=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [manuscript,plan_path,old_manuscript,old_plan,delta_path,RELEASE,Path(__file__)]}))
    fresh=deepcopy(doc);fresh['records']=[r for r in doc['records'] if r['id'] not in rows]
    assert len(fresh['records'])==251
    for row in fresh['records']:
        for key in ['source_reference','current_reference']:
            assert row[key]
    fresh.update(blocks=sorted({r['block'] for r in fresh['records']}),physical_speech_objects=251,
        ordinary_speech_objects=sum(r['kind']=='progressive' for r in fresh['records']),
        FE_speech_objects=sum(r['kind']=='system-FE' for r in fresh['records']),
        subset_of=str(manuscript),subset_of_sha256=sha(manuscript.read_bytes()))
    sub=output/'remaining_manuscript.json';save(sub,fresh)
    plan=deepcopy(plans);plan.update(manuscript=str(sub),manuscript_sha256=sha(sub.read_bytes()),
        records=[r for r in plans['records'] if r['id'] not in rows],subset_of=str(plan_path),subset_of_sha256=sha(plan_path.read_bytes()))
    assert sum(r['expected_native_pages'] for r in plan['records'])==252
    save(output/'remaining_plans.json',plan)
    print('Qualified288 completed native records/293 pages;resume only251 records/252 pages, including all14 changed ellipses. Old failed full run/partial evidence preserved.',flush=True)
