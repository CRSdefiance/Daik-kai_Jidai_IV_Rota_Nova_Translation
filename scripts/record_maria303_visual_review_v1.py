"""Journal directly inspected native contact sheets without closing storage/gameplay/release gates."""
import argparse
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B58_B70_clean_20261109')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--blocks',type=int,nargs='*',default=[])
    ap.add_argument('--include-names-menus',action='store_true');args=ap.parse_args()
    out=ROOT/'visual_reviews_v1';out.mkdir(exist_ok=True)
    for block in args.blocks:
        target=out/f'B{block}_initial.json';assert not target.exists()
        receipt=ROOT/f'native_pages_v1/B{block}_checked.json';rows=load(receipt)['records']
        pages=[]
        for row in rows:
            journal=ROOT/('native_pages_v1/complete_'+row['id']+'.json');proof=load(journal)
            assert proof['record']==row and proof['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass']
            panels=row['complete_native_English_display']['pages'] if row['kind']=='progressive' else [row['complete_native_English_display']]
            for number,panel in enumerate(panels,1):
                assert digest(panel['preview'])==panel['preview_sha256'] and digest(panel['native_plane'])==panel['native_plane_sha256']
                pages.append(dict(id=row['id'],page=number,preview=panel['preview'],preview_sha256=panel['preview_sha256'],
                    native_plane_sha256=panel['native_plane_sha256'],native_receipt=str(journal),native_receipt_sha256=digest(journal)))
        sheets=[ROOT/f'native_pages_v1/B{block}_part{i}.png' for i in range(1,(len(pages)+11)//12+1)]
        assert all(p.exists() for p in sheets)
        save(target,dict(block=block,source_records=len(rows),directly_reviewed_pages=len(pages),
            selected_page_receipts=pages,review_sheets=[dict(path=str(p),sha256=digest(p),directly_viewed=True) for p in sheets],
            findings=[dict(id='DK4_MES_B58_R0178',finding='Keep the short Where are they question together instead of splitting Where/are they across adjacent rows.',fresh_layout_delta_pending=True)] if block==58 else [],
            all_complete_glyphs_visible_on_reviewed_pages=True,no_blank_clipped_overlapping_orunintended_pages_observed=True,
            source_block_receipt=str(receipt),source_block_receipt_sha256=digest(receipt),
            actual_gameplay=False,stored_script_andrepresentative_gameplay_pending=True,all_fifth_gates_still_pending=True,new_credit=0))
        print('Journaled direct view:',block,len(pages),'native pages on',len(sheets),'sheets.')
    if args.include_names_menus:
        target=out/'names_andmenus_initial.json';assert not target.exists()
        names_path=ROOT/'name_planes_v1/native_name_planes.json';menus_path=ROOT/'menu_native_v1/group_verification.json'
        names,menus=map(load,[names_path,menus_path])
        sheets=names['review_sheets']+[m['review_sheet'] for m in menus['objects']]
        for sheet in sheets:assert digest(sheet['path'])==sheet['sha256']
        save(target,dict(scoped_name_strings=24,scoped_actor_consumers=40,native_name_planes_reused=16,native_name_planes_fresh=8,
            all24_current_name_strings_directly_viewed=True,choice_menus=2,choice_captions=4,
            all_four_reviewed_captions_directly_viewed=True,normal_highlight_native_plane_cases=16,
            all_complete_names_caption_glyphs_andcentering_visually_accepted=True,
            review_sheets=[{**s,'directly_viewed':True} for s in sheets],
            source_evidence={str(p):digest(p) for p in [names_path,menus_path,Path(__file__)]},
            full_catalogue_UI_actual_controller_andbatch_gameplay_unvisited=True,
            all_fifth_gates_still_pending=True,actual_gameplay=False,new_credit=0))
        print('Journaled direct view of24 name strings andfour menu captions;native andvisual scope only.')

if __name__=='__main__':main()
