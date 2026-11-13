"""Bind every final body page to an actually viewed sheet with exact native-pixel tile comparisons."""
from pathlib import Path
from PIL import Image
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

VIEWED_BASE_BLOCKS=[96,98,99,100,101,102,103,104,105,106,107,110,111,112,113,114,115]

def main():
    out=ROOT/'body_visual_review_v1.json';assert not out.exists()
    final_path=ROOT/'selected_native_sheets_v2/selected_native_pages.json';final=load(final_path)
    assert final['records_count']==330 and final['pages']==338 and final['selected_completed_alignment_cases']==1320
    selection_path=ROOT/'native_final_selection_v2/resume_selection.json';selection=load(selection_path)
    assert selection['native_selection_complete'] and selection['remaining_records']==0
    views={};sources={}
    def tile(sheetpath,index,preview,expected_hash,label):
        sheetpath=Path(sheetpath);preview=Path(preview)
        assert digest(preview)==expected_hash
        picture=Image.open(preview).convert('RGB');sheet=Image.open(sheetpath).convert('RGB')
        x,y=index%2*456,index//2*160+24
        crop=sheet.crop((x,y,x+picture.width*2,y+128))
        assert crop.tobytes()==picture.resize((picture.width*2,128),Image.Resampling.NEAREST).tobytes(),(sheetpath,label)
        views[str(sheetpath)]=digest(sheetpath)
        sources[(str(preview.resolve()),expected_hash)]=dict(sheet=str(sheetpath),sheet_sha256=views[str(sheetpath)],label=label,
            exact_viewed_sheet_tile_matches_complete_native_preview=True)
    def native_block(directory,block):
        proof=load(directory/f'B{block}_checked.json');pictures=[]
        for row in proof['records']:
            display=row['complete_native_English_display'];pages=display['pages'] if row['kind']=='progressive' else [display]
            for i,page in enumerate(pages,1):pictures.append((row['id']+f' p{i}',page))
        for i,(label,page) in enumerate(pictures):
            tile(directory/f'B{block}_part{i//12+1}.png',i%12,page['preview'],page['preview_sha256'],label)
    for block in VIEWED_BASE_BLOCKS:native_block(ROOT/'native_pages_v1',block)
    for directory,blocks in [('native_B98_fix_v1',[98]),('native_B105_fix_v1',[105]),('native_late_fix_v1',[106,110,115]),('native_B116_fix_v1',[116])]:
        for block in blocks:native_block(ROOT/directory,block)
    selected_old=load(ROOT/'selected_native_sheets_v1/selected_native_pages.json')
    for sheet in selected_old['review_sheets']:
        if sheet['block']<116:continue
        assert digest(sheet['path'])==sheet['sha256']
        for i,page in enumerate(sheet['exact_selected_pages']):tile(sheet['path'],i,page['preview'],page['preview_sha256'],page['label'])
    assert len(views)==48,len(views)
    records=[];total=0
    for row in final['records']:
        display=row['complete_native_English_display'];pages=display['pages'] if row['kind']=='progressive' else [display];bound=[]
        for i,page in enumerate(pages,1):
            key=(str(Path(page['preview']).resolve()),page['preview_sha256']);assert key in sources,(row['id'],i)
            bound.append(dict(page=i,preview=page['preview'],preview_sha256=page['preview_sha256'],**sources[key]));total+=1
        records.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],compiled_hex=row['compiled_hex'],
            logical_English=row['logical_English'],pages=bound,complete_final_native_body_pages_directly_viewed=True))
    assert total==338 and len(records)==330
    save(out,dict(source_editorial_objects=330,source_body_objects=328,physical_body_candidates=330,body_pages=338,records=records,
        viewed_sheets=views,sheets_actually_viewed_including_superseded_layout_findings=48,
        all_final_body_pages_bound_to_directly_viewed_exact_native_pixels=True,
        selected_native_proof=str(final_path),selected_native_proof_sha256=digest(final_path),native_selection=str(selection_path),native_selection_sha256=digest(selection_path),
        selected_plan=str(ROOT/'plan_continuity_v10/automatic_plans.json'),selected_plan_sha256=digest(ROOT/'plan_continuity_v10/automatic_plans.json'),
        page_reclamation_without_shortened_prose=['DK4_MES_B98_R0013','DK4_MES_B106_R0016','DK4_MES_B115_R0004'],
        complete_closing_clause_boundary_fixes=['DK4_MES_B105_R0101','DK4_MES_B105_R0106','DK4_MES_B105_R0132','DK4_MES_B106_R0013','DK4_MES_B110_R0011','DK4_MES_B116_R0024','DK4_MES_B116_R0110'],
        orphan_See_fixed='SC3_B99_STYLE_446_366',
        justified_complete_question_andordinary_with_soft_boundaries=['DK4_MES_B115_R0035','DK4_MES_B115_R0004'],
        justified_other_layout_retentions={
            'DK4_MES_B112_R0004':'Readable full-width regional-name soft boundary; full Proof term intact, no sparse extra rows.',
            'DK4_MES_B123_R0035':'Whole interpretive coda follows a complete hypothesis; no phrase fragment crosses the page.',
            'DK4_MES_B124_R0004':'Ordinary complete-word North/Sea soft boundary in a clear full-width paragraph.',
            'DK4_MES_B116_R0024':'Source-specific shorter setup rows preserve the complete main characterization on page two without rewriting.',
            'DK4_MES_B116_R0110':'Source-specific shorter explanatory rows preserve Richard\'s interrupted lofty-ideals clause and live company token together.'},
        mixed_fullwidth_Latin_repairs_visually_checked=['DK4_MES_B105_R0023','DK4_MES_B110_R0011','DK4_MES_B121_R0019'],
        former_Japanese_grant_now_native_English='DK4_MES_B118_R0008',
        FE_pagination_owners=['DK4_MES_B116_R0041','DK4_MES_B116_R0051'],FE_source_scoped_guard_reserve_36_not_global=True,physical_FE_width_228_unchanged=True,
        all_body_structural_native_alignment_glyph_bounds_consumption_andpagination_pass=True,
        two_caption_pages_six_style_object_integrity_name_planes_storage_gameplay_andregistered_integration_pending=True,
        all_fifth_gates_still_false=True,actual_gameplay=False,new_credit=0,full_goal_complete=False,producer_sha256=digest(__file__)))
    print('Bound all338 final body pages/330 physical bodies to48 actually viewed sheets; no source credit or gameplay claim.')

if __name__=='__main__':main()
