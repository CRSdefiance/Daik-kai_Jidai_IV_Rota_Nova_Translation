"""Qualify completed native leaves, all318 viewed pages andthe exact84-record reuse."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT

def pages(row):
    value=row['complete_native_English_display'];return value['pages'] if row['kind']=='progressive' else [value]

def main():
    out=ROOT/'initial_complete_native_v1.json';assert not out.exists()
    doc_path=ROOT/'formatting_v1/formatting_input.json';plan_path=ROOT/'plan_v4_FE_guards/automatic_plans.json'
    fresh_path=ROOT/'resume226_native_v1/compiled_native_pages.json'
    doc,plan,fresh=map(load,[doc_path,plan_path,fresh_path]);selection=load(ROOT/'native_resume_selection_v1.json')
    assert fresh['runtime']==doc['runtime'] and (len(fresh['records']),fresh['pages'],fresh['fresh_compiled_alignments'])==(226,230,904)
    assert fresh['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and fresh['complete_consumption_andpagination_exact']
    original={r['id']:r for r in doc['records']};planned={r['id']:r for r in plan['records']}
    leaves={};sources={};old_groups={}
    for block in [51,52,53]:
        path=ROOT/f'initial_native_v1/B{block}_checked.json';group=load(path)['records'];old_groups[block]=group
        for row in group:leaves[row['id']]=row;sources[row['id']]=dict(path=str(path),sha256=digest(path),completed_block_from_later_failed_run=True)
    for binding in selection['bindings']:
        if binding['kind']!='append-only-completed-record':continue
        path=Path(binding['path']);assert digest(path)==binding['sha256']
        proof=load(path);row=proof['record'];assert row['id'] not in leaves
        inputs=load(proof['native_run_inputs']);assert digest(proof['native_run_inputs'])==proof['native_run_inputs_sha256']
        assert inputs['runtime']==fresh['runtime'] and inputs['font_sha256']==fresh['font_sha256']
        leaves[row['id']]=row;sources[row['id']]=dict(path=str(path),sha256=digest(path),completed_individual_journal=True)
    assert len(leaves)==84
    for row in fresh['records']:
        assert row['id'] not in leaves
        leaves[row['id']]=row;sources[row['id']]=dict(path=str(fresh_path),sha256=digest(fresh_path),fresh_complete_scope=True)
    assert leaves.keys()==original.keys()==planned.keys() and len(leaves)==310
    selected=[]
    for expected in doc['records']:
        row=leaves[expected['id']];p=planned[row['id']]
        assert row['source_reference']==expected['source_reference'] and row['current_reference']==expected['current_reference']
        assert row['logical_English']==expected['english'] and row['compiled_hex']==p['encoded_hex']
        assert len(row['native_alignment']['cases'])==4 and len(pages(row))==p['expected_native_pages']
        display=row['complete_native_English_display']
        if row['kind']=='progressive':
            assert display['all_visible_first_internal_final_characters_in_order'] and display['no_blank_or_overlap_page']
            assert display['complete_consumed_bytes']==len(bytes.fromhex(row['expanded_native_hex']))
            assert all(page['native_independent_plane_equal'] and page['all_bitmap_header_input_canaries_exact'] for page in pages(row))
        else:
            assert display['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
            assert display['input_bitmap_header_view_context_canaries_andcomplete_return_exact']
            assert display['all_executed_instructions_exact_current_sections_andpayload']
            assert display['planned_native_row_comparison']['complete_glyph_row_membership_exact']
        for number,page in enumerate(pages(row),1):
            assert digest(page['preview'])==page['preview_sha256'] and digest(page['native_plane'])==page['native_plane_sha256']
            selected.append(dict(id=row['id'],page=number,preview=page['preview'],preview_sha256=page['preview_sha256'],
                native_plane_sha256=page['native_plane_sha256'],native_receipt=sources[row['id']]))
    assert len(selected)==318
    sheets=[];viewed=set()
    groups=[(b,old_groups[b],ROOT/'initial_native_v1',list(range(1,{51:3,52:1,53:4}[b]+1))) for b in [51,52,53]]
    groups += [(b,[r for r in fresh['records'] if r['block']==b],ROOT/'resume226_native_v1',
        list(range(4,8)) if b==54 else list(range(1,{55:5,56:4,57:5}[b]+1))) for b in [54,55,56,57]]
    for block,rows,folder,parts in groups:
        ordered=[(r,index,page) for r in rows for index,page in enumerate(pages(r),1)]
        for part in parts:
            path=folder/f'B{block}_part{part}.png';members=ordered[(part-1)*12:part*12];assert members
            sheets.append(dict(path=str(path),sha256=digest(path),pages=len(members),directly_viewed=True))
            viewed.update((r['id'],index,page['preview_sha256'],page['native_plane_sha256']) for r,index,page in members)
    first19=load(ROOT/'first19_visual_v1/contact_sheet_manifest.json')
    for sheet in first19['review_sheets']:
        assert digest(sheet['path'])==sheet['sha256'];sheets.append({**sheet,'directly_viewed':True})
        viewed.update((m['id'],m['page'],m['preview_sha256'],m['native_plane_sha256']) for m in sheet['members'])
    reuse=load(ROOT/'B54_first36_exact_visual_reuse_v1.json');assert reuse['pages']==36
    for value in reuse['reused_pages']:
        row=leaves[value['id']];page=next(p for p in pages(row) if p['preview']==value['preview'])
        source_id,source_page,receipt,receipt_sha=value['exact_previously_viewed_page']
        assert digest(receipt)==receipt_sha
        assert (source_id,source_page,page['preview_sha256'],page['native_plane_sha256']) in viewed
        number=pages(row).index(page)+1;viewed.add((row['id'],number,page['preview_sha256'],page['native_plane_sha256']))
    assert all((r['id'],r['page'],r['preview_sha256'],r['native_plane_sha256']) in viewed for r in selected)
    assert sum(s['pages'] for s in sheets)==282 and len(sheets)==28
    # Earlier unjournaled B54 previews are byte-identical to the selected pages;
    # their images are visually covered, but their unretained alignments are not reused.
    current_by_name={Path(p['preview']).name:p for row in leaves.values() for p in pages(row)};old_images=[]
    for path in sorted((ROOT/'initial_native_v1').glob('DK4_MES_B54*.png')):
        page=current_by_name[path.name];assert digest(path)==page['preview_sha256']
        old_images.append(dict(path=str(path),sha256=digest(path),selected_preview=page['preview']))
    assert len(old_images)==74
    save(out,{**{k:v for k,v in fresh.items() if k not in ['records','review_sheets']},
        'manuscript':str(doc_path),'manuscript_sha256':digest(doc_path),'plan':str(plan_path),'plan_sha256':digest(plan_path),
        'records':[leaves[r['id']] for r in doc['records']],'pages':318,
        'fresh_compiled_alignments':904,'reused_compiled_alignments':336,'selected_alignment_cases':1240,
        'completed_source_records_reused':84,'fresh_source_records':226,
        'all_records_native_checked_once_or_exact_compiled_dependency_reuse':True,
        'failed_invocations_not_claimed_as_complete_passes':True,
        'selected_native_receipt_per_record':sources,'review_sheets':sheets,
        'directly_reviewed_selected_page_receipts':selected,'direct_visual_review_pending':False,
        'directly_viewed_pages':282,'exact_duplicate_visual_pages_reused':36,
        'earlier_unjournaled_same_RGB_previews_visually_covered':old_images,
        'formatting_gates_still_false':True,'actual_gameplay':False,'new_credit':0,
        'evidence':{str(p):digest(p) for p in [doc_path,plan_path,fresh_path,ROOT/'native_resume_selection_v1.json',
            ROOT/'B54_first36_exact_visual_reuse_v1.json',Path(__file__)]}})
    print('Qualified310 native bodies/318 viewed pages/1240 selected alignments;84 records and36 duplicate visual pages reused;five guards fixed.')
if __name__=='__main__':main()
