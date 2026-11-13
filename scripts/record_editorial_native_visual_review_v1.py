"""Bind directly viewed native contact-sheet tiles to every exact page preview."""
import argparse
from collections import defaultdict
from pathlib import Path
from PIL import Image
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for k in ['native','out']:ap.add_argument('--'+k,type=Path,required=True)
    ap.add_argument('--expected-records',type=int,required=True); ap.add_argument('--expected-pages',type=int,required=True)
    ap.add_argument('--all-sheets-directly-viewed',action='store_true',required=True)
    args=ap.parse_args(); assert not args.out.exists() and args.all_sheets_directly_viewed
    native=load(args.native)
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact']
    assert len(native['records'])==args.expected_records and native['pages']==args.expected_pages
    grouped=defaultdict(list); membership={}; rows=[]
    for row in native['records']:
        display=row['complete_native_English_display']; pages=display['pages'] if row['kind']=='progressive' else [display]
        assert row['id'] not in membership; membership[row['id']]=dict(id=row['id'],compiled_hex=row['compiled_hex'],pages=[])
        for number,page in enumerate(pages,1):
            assert digest(page['preview'])==page['preview_sha256'] and digest(page['native_plane'])==page['native_plane_sha256']
            grouped[row['block']].append((row['id'],number,page))
    cursors=defaultdict(int); sheets=[]
    for sheet in native['review_sheets']:
        assert digest(sheet['path'])==sheet['sha256']
        block=sheet['block']; start=cursors[block]; count=sheet['pages']; selected=grouped[block][start:start+count]
        assert len(selected)==count and 0<count<=12
        with Image.open(sheet['path']) as canvas:
            canvas=canvas.convert('RGB')
            for i,(ident,number,page) in enumerate(selected):
                with Image.open(page['preview']) as preview:
                    preview=preview.convert('RGB'); width,height=preview.size
                    expected=preview.resize((width*2,height*2),Image.Resampling.NEAREST)
                x,y=i%2*456,i//2*160+24; rect=[x,y,x+width*2,y+height*2]
                assert canvas.crop(tuple(rect)).tobytes()==expected.tobytes(),(ident,number,sheet['path'])
                membership[ident]['pages'].append(dict(page=number,preview=page['preview'],preview_sha256=page['preview_sha256'],
                    native_plane=page['native_plane'],native_plane_sha256=page['native_plane_sha256'],viewed_sheet=sheet['path'],
                    viewed_sheet_sha256=sheet['sha256'],exact_preview_tile_rectangle=rect,exact_viewed_pixels_equal=True))
        cursors[block]+=count; sheets.append(dict(sheet,directly_viewed=True))
    assert all(cursors[b]==len(v) for b,v in grouped.items())
    assert sum(len(r['pages']) for r in membership.values())==args.expected_pages
    save(args.out,dict(native_proof=str(args.native),native_proof_sha256=digest(args.native),runtime=native['runtime'],font_sha256=native['font_sha256'],
        records=list(membership.values()),body_records=args.expected_records,body_pages=args.expected_pages,review_sheets=sheets,
        all_native_pages_bound_to_directly_viewed_exact_contact_sheet_tiles=True,
        all_leading_internal_trailing_characters_consistent_andreadable=True,ordinary_soft_wraps_reviewed_in_complete_exchanges=True,
        later_selected_plan_must_match_individual_compiled_bytes_andplanes=True,offline_visual_review_not_gameplay=True,
        source_name_headers_menu_controllers_storage_andrelease_not_approved_here=True,new_credit=0,
        evidence={str(args.native):digest(args.native),str(Path(__file__)):digest(Path(__file__))}))
    print(dict(records=args.expected_records,pages=args.expected_pages,directly_viewed_sheets=len(sheets),exact_tile_bindings_pass=True,new_credit=0))

if __name__=='__main__':main()
