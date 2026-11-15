"""Reuse exact completed block records; check only unvisited or newly formatted bodies."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT=Path('work/analysis/Rafael351_native_resume_inputs_v1_20261105')
DOC=Path('translations/rafael_B121_B140_formatting_manuscript_v4.json')
PLAN=Path('work/analysis/Rafael351_automatic_plans_v4_20261105/automatic_plans.json')
PARTIAL=Path('work/analysis/Rafael351_native_v1_20261105')
TERMS=Path('work/analysis/Rafael351_item_UI_terms_v1_20261105/term_bindings.json')
FAILURE=Path('work/analysis/Rafael351_native_gc_v1_20261105/completion.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,plan,terms,failure=map(load,[DOC,PLAN,TERMS,FAILURE])
    assert plan['manuscript_sha256']==sha(DOC.read_bytes()) and not plan['failures']
    assert not failure['completed_without_exception'] and failure['terminal'] and failure['all_locked_sources_unchanged']
    assert not any(i['severity'] in ['error','warning'] for r in plan['records'] for i in r['base_QA']['issues'])
    ctx=RegisteredRuntime(terms['runtime']['release_proof'],terms['runtime']['startup_proof'],captain=0)
    assert ctx.receipt()==terms['runtime'] and doc['current_ROM_sha256']==ctx.receipt()['candidate_sha256']
    originals={r['id']:r for r in doc['records']};target={r['id']:r for r in plan['records']}
    reused={};retired=[];origins={};evidence=[DOC,PLAN,TERMS,FAILURE,Path(__file__)]
    complete=[]
    for block in range(121,128):
        path=PARTIAL/f'B{block}_checked.json';partial=load(path);evidence.append(path)
        expected={r['id'] for r in doc['records'] if r['block']==block and r['kind']!='typed-choice-label'}
        assert {r['id'] for r in partial['records']}==expected
        complete.append(block)
        for row in partial['records']:
            original=originals[row['id']];planned=target[row['id']]
            assert row['source_reference']==original['source_reference'] and row['current_reference']==original['current_reference']
            assert row['logical_English']==original['english']
            if row['compiled_hex']!=planned['encoded_hex']:
                retired.append(row['id']);continue
            assert len(row['native_alignment']['cases'])==4
            assert all(c['output_hex']==row['expanded_native_hex'] and c['original_macro_ABI_input_output_canaries_and_all_unowned4MiB_exact'] for c in row['native_alignment']['cases'])
            rendered=row['complete_native_English_display']
            if row['kind']=='progressive':
                assert rendered['complete_consumed_bytes']==len(bytes.fromhex(row['expanded_native_hex']))
                assert rendered['all_visible_first_internal_final_characters_in_order'] and rendered['no_blank_or_overlap_page']
                pages=rendered['pages']
            else:
                assert rendered['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
                assert rendered['planned_native_row_comparison']['complete_glyph_row_membership_exact']
                pages=[rendered]
            assert len(pages)==planned['expected_native_pages']
            for page in pages:
                for key,digest in [('native_plane','native_plane_sha256'),('preview','preview_sha256')]:
                    assert sha(Path(page[key]).read_bytes())==page[digest]
            reused[row['id']]=deepcopy(row)
            origins[row['id']]=dict(path=str(path),sha256=sha(path.read_bytes()),
                complete_block_from_preserved_failed_run=True,compiled_source_current_prose_andpages_exact=True)
    assert len(reused)==129 and set(retired)=={'DK4_MES_B121_R0100','DK4_MES_B123_R0048','DK4_MES_B123_R0171'}
    fresh=[r for r in doc['records'] if r['kind']!='typed-choice-label' and r['id'] not in reused]
    assert len(fresh)==212
    ROOT.mkdir(parents=True)
    save(ROOT/'exact_reused_native_records.json',dict(runtime=ctx.receipt(),font_sha256=sha(ctx.image.read_file('/GRP/KANJI.FNT')),
        records=list(reused.values()),origins=origins,reused_records=129,reused_pages=129,
        completed_blocks=complete,retired_due_to_fresh_preferences=retired,
        no_unsealed_partial_B128_imported=True,no_new_visual_oractual_gameplay_claim=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in evidence}))
    subset=deepcopy(doc);subset.update(records=fresh,blocks=sorted({r['block'] for r in fresh}),
        physical_speech_objects=212,typed_choice_objects=0,typed_choice_commands=0,
        subset_of=str(DOC),subset_of_sha256=sha(DOC.read_bytes()),
        complete_batch_display_still_pending=True)
    sub=ROOT/'remaining_manuscript.json';save(sub,subset)
    subplan={**plan,'manuscript':str(sub),'manuscript_sha256':sha(sub.read_bytes()),
        'records':[target[r['id']] for r in fresh], 'subset_of':str(PLAN),'subset_of_sha256':sha(PLAN.read_bytes())}
    save(ROOT/'remaining_plans.json',subplan)
    print('Qualified129 exact native records/pages for reuse. Fresh212 bodies/215 pages remain;three refinements retire earlier pages. No unsealed B128 or new gameplay credit.')
