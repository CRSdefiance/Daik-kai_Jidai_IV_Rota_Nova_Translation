"""Bind completed65 outputs; qualify only the existing native continuation guard."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_pages_preparation_v8803b');assert not root.exists()
    old=Path('work/analysis/Hodram_B54_B60_pages_v8803');docpath=Path('translations/hodram_B54_B60_editorial_manuscript_v1.json')
    planpath=Path('work/analysis/Hodram_B54_B60_layout_v8802c/automatic_plans.json');doc,plan=map(read,[docpath,planpath])
    completed=[];files={};sheets=[];blocks=[54,55,56,57,58]
    for block in blocks:
        path=old/f'B{block}_completed_English_rows.json';packet=read(path);assert not packet['actual_gameplay'] and packet['new_credit']==0
        files[str(path)]=sha(path.read_bytes())
        for row in packet['records']:
            original=next(r for r in doc['records'] if r['id']==row['id']);p=next(r for r in plan['records'] if r['id']==row['id'])
            assert row['source_reference']==original['source_reference'] and row['current_reference']==original['current_reference'] and row['compiled_hex']==p['encoded_hex']
            assert len(row['native_alignment']['cases'])==4 and all(c['output_hex']==row['expanded_native_hex'] for c in row['native_alignment']['cases'])
            rendered=row['complete_native_English_display']
            if row['kind']=='system-FE':
                assert rendered['pages']==1
                for key in ['native_physical_plane','native_logical_plane','preview']:files[rendered[key]]=rendered[key+'_sha256']
            else:
                assert len(rendered['pages'])==p['expected_native_pages']==1 and rendered['complete_consumed_bytes']==len(bytes.fromhex(row['expanded_native_hex']))
                assert rendered['all_visible_first_internal_final_characters_in_order'] and rendered['no_blank_or_overlap_page']
                for page in rendered['pages']:
                    assert page['first_visible_origin']==[0,0] and page['native_independent_plane_equal'] and page['all_bitmap_header_input_canaries_exact']
                    for key in ['native_plane','preview']:files[page[key]]=page[key+'_sha256']
            completed.append(row)
        for path in sorted(old.glob(f'B{block}_English_part*.png')):
            files[str(path)]=sha(path.read_bytes());sheets.append(dict(block=block,path=str(path),sha256=files[str(path)],pages=min(12,len(packet['records'])-12*len([s for s in sheets if s['block']==block]))))
    assert len(completed)==65 and len(sheets)==9
    for path,digest in files.items():assert sha(Path(path).read_bytes())==digest
    root.mkdir(parents=True)
    reuse=root/'65_complete_rows_andnine_sheets_exact.json'
    save(reuse,dict(records=completed,sheets=sheets,blocks=blocks,pages=65,reused_alignment_cases=260,files=files,
        manuscript=str(docpath),manuscript_sha256=sha(docpath.read_bytes()),plan=str(planpath),plan_sha256=sha(planpath.read_bytes()),
        source_producer='scripts/prove_Hodram_B54_B60_pages_v8803.py',source_producer_sha256=sha(Path('scripts/prove_Hodram_B54_B60_pages_v8803.py').read_bytes()),
        completed_native_results_reused_not_replayed=True,original_failure_andall_partial_B59_artifacts_preserved=True,new_credit=0,full_goal_complete=False))
    start="ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');rows=[];sheets=[];page_count=0"
    replacement="""ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    reuse_path=Path('work/analysis/Hodram_B54_B60_pages_preparation_v8803b/65_complete_rows_andnine_sheets_exact.json');reuse=read(reuse_path)
    assert reuse['manuscript_sha256']==sha(DOC.read_bytes()) and reuse['plan_sha256']==sha(PLAN.read_bytes())
    for path,digest in reuse['files'].items():assert sha(Path(path).read_bytes())==digest
    rows=list(reuse['records']);sheets=list(reuse['sheets']);page_count=reuse['pages']"""
    result=derive('scripts/prove_Hodram_B54_B60_pages_v8803.py','scripts/prove_Hodram_B54_B60_pages_v8803b.py',{
        'work/analysis/Hodram_B54_B60_pages_v8803':'work/analysis/Hodram_B54_B60_pages_v8803b',start:replacement,
        "for block in doc['blocks']:\n        pictures=[]":"for block in doc['blocks']:\n        if block in reuse['blocks']:continue\n        pictures=[]",
        "assert page['first_visible_origin']==[0,0]":"""segment=expected[page['start']:page['end']]
                    guarded=page['page']>1 and segment.startswith(b' ') and not segment.startswith(b'  ')
                    assert page['first_visible_origin']==([6,0] if guarded else [0,0])
                    if guarded:assert page['events'][0]==dict(kind='ascii',code=32,style=1,x=0,y=0)
                    page['native_continuation_guard_at_zero_andfirst_visible_at_six']=guarded""",
        'fresh_compiled_alignment_cases=328,progressive_alignment_cases=324':'fresh_compiled_alignment_cases=68,reused_compiled_alignment_cases=260,total_bound_compiled_alignment_cases=328,progressive_alignment_cases=324',
        "review_sheets=sheets,direct_view_pending=True":"review_sheets=sheets,completed65_reuse=str(reuse_path),completed65_reuse_sha256=sha(reuse_path.read_bytes()),native_guard_is_not_a_dropped_leading_glyph=True,direct_view_pending=True",
    })
    save(root/'qualified_native_page_guard_successor.json',dict(derivation=result,reuse=str(reuse),reuse_sha256=sha(reuse.read_bytes()),
        reason='The original first-visible-origin assertion wrongly required zero on every page. Focused original rendering of B59R23 shows the next page consumes the encoder-owned space guard at x0 and its first visible b at x6. The established guarded-continuation profile already budgets this cell. Bind that exact prefix/event/origin case only; retain complete code order, independent pixels, bounds, consumption, canaries and all original instructions. No whitespace is authored and no viewport, font or glyph check is changed.',
        fresh_remaining_utterances=17,reused_completed_utterances=65,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
