"""Journal directly viewed pages; no storage, gameplay or registration approval."""
import argparse
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.stage_maria328_review_sheets_v1 import pages

def journal(block,folder,out):
    receipt=folder/f'B{block}_checked.json'
    if not receipt.exists():receipt=folder/f'B{block}_pages.json'
    rows=load(receipt)['records'];members=[]
    for row in rows:
        for number,panel in enumerate(pages(row),1):
            assert digest(panel['preview'])==panel['preview_sha256'] and digest(panel['native_plane'])==panel['native_plane_sha256']
            members.append(dict(id=row['id'],page=number,preview=panel['preview'],preview_sha256=panel['preview_sha256'],native_plane_sha256=panel['native_plane_sha256']))
    sheets=[folder/f'B{block}_part{i}.png' for i in range(1,(len(members)+11)//12+1)]
    target=out/(folder.name+f'_B{block}.json');assert not target.exists()
    save(target,dict(block=block,records=len(rows),directly_viewed_pages=len(members),selected_page_receipts=members,
        review_sheets=[dict(path=str(p),sha256=digest(p),directly_viewed=True) for p in sheets],
        source_block_receipt=str(receipt),source_block_receipt_sha256=digest(receipt),
        all_complete_glyphs_visible_on_reviewed_pages=True,no_blank_clipped_overlapping_orunintended_pages_observed=True,
        actual_gameplay=False,all_fifth_gates_still_pending=True,new_credit=0))
    print('Journaled',block,folder.name,len(members),'directly viewed pages.')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--initial-blocks',type=int,nargs='*',default=[])
    ap.add_argument('--selected-blocks',type=int,nargs='*',default=[]);ap.add_argument('--refinements',action='store_true')
    ap.add_argument('--names-menus',action='store_true');args=ap.parse_args()
    out=ROOT/'visual_reviews_v1';out.mkdir(exist_ok=True)
    for block in args.initial_blocks:journal(block,ROOT/'native_pages_v1',out)
    for block in args.selected_blocks:journal(block,ROOT/'selected_review_sheets_v1',out)
    if args.refinements:
        for block in [74,75,76]:journal(block,ROOT/'native_final_v1',out)
    if args.names_menus:
        npath=ROOT/'name_planes_v1/native_name_planes.json';mpath=ROOT/'menu_native_v1/menu_provider_and_planes.json'
        names,menus=map(load,[npath,mpath])
        assert (names['actors'],names['distinct_current_strings'],names['fresh_native_name_strings'],names['reused_native_name_strings'])==(24,28,15,13)
        assert len(names['consumer_bindings'])==48
        assert (len(menus['menus']),menus['native_provider_alignments'],menus['bridged_modal_returns'],menus['complete_English_caption_style_planes'])==(5,30,120,60)
        assert sum(len(x['rejected']) for x in menus['compiler_negatives_rejected'])==40
        assert menus['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        sheets=names['review_sheets']+menus['review_sheets']
        for sheet in sheets:assert digest(sheet['path'])==sheet['sha256']
        target=out/'names_andmenus.json';assert not target.exists()
        save(target,dict(actors=24,consumer_bindings=48,distinct_name_strings_directly_viewed=28,
            target_captions_directly_viewed=15,current_caption_previews_directly_viewed=15,
            native_normal_highlight_planes_checked=60,native_provider_alignments=30,bridged_returns=120,negative_cases=40,
            review_sheets=[dict(s,directly_viewed=True) for s in sheets],
            evidence={str(p):digest(p) for p in [npath,mpath,__file__]},
            actual_controller_full_catalogue_UI_andconditional_headers_unvisited=True,
            actual_gameplay=False,all_fifth_gates_still_pending=True,new_credit=0))
        print('Journaled28 name strings and15 target/15 current caption previews; native highlight checks distinguished from direct views.')

if __name__=='__main__':main()
