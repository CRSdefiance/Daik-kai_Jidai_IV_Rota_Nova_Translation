"""Bind an exact selected native proof to already directly viewed original sheet tiles."""
import argparse
from pathlib import Path
import runpy
import sys
from PIL import Image
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ['selected','sheet-map','projection','out']:ap.add_argument('--'+key,type=Path,required=True)
    ap.add_argument('--all-sheets-directly-viewed',action='store_true',required=True)
    args=ap.parse_args();assert not args.projection.exists() and not args.out.exists() and args.all_sheets_directly_viewed
    selected,mapping=map(load,[args.selected,args.sheet_map])
    assert selected['all_selected_runtime_font_macro_source_current_compiled_glyph_andbounds_receipts_exact']
    selectionpath=Path(selected['source_receipt_selection']);assert digest(selectionpath)==selected['source_receipt_selection_sha256']
    selection=load(selectionpath);assert selection['native_selection_complete'] and selection['remaining_records']==0
    for bound in selection['reused_native_records']:
        assert digest(bound['receipt'])==bound['receipt_sha256'];proof=load(bound['receipt'])
        assert proof['four_native_alignment_cases_pass'] and proof['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass']
    assert len(mapping['sheets'])==len(selected['review_sheets']) and mapping['all_listed_sheets_directly_viewed']
    sheets=[]
    for expected,actual in zip(selected['review_sheets'],mapping['sheets'],strict=True):
        assert expected['block']==actual['block'] and expected['pages']==actual['pages']
        path=Path(actual['path']);assert digest(path)==actual['sha256']
        with Image.open(path) as canvas:
            canvas=canvas.convert('RGB')
            for i,page in enumerate(expected['exact_selected_pages']):
                preview=Path(page['preview']);assert digest(preview)==page['preview_sha256']
                with Image.open(preview) as picture:
                    picture=picture.convert('RGB');scaled=picture.resize((picture.width*2,picture.height*2),Image.Resampling.NEAREST)
                x,y=i%2*456,i//2*160+24
                assert canvas.crop((x,y,x+scaled.width,y+scaled.height)).tobytes()==scaled.tobytes(),(expected['path'],str(path),page['label'])
        sheets.append(dict(block=expected['block'],path=str(path),sha256=actual['sha256'],pages=expected['pages']))
    projection={**selected,'review_sheets':sheets,
        'all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass':True,
        'complete_consumption_andpagination_exact':True,
        'native_assertions_derived_from_every_exact_selected_four_case_receipt':True,
        'exact_prior_viewed_tile_reuse_not_repeated_visual_inspection':True,
        'viewed_sheet_mapping':str(args.sheet_map),'viewed_sheet_mapping_sha256':digest(args.sheet_map)}
    save(args.projection,projection)
    sys.argv=[__file__,'--native',str(args.projection),'--out',str(args.out),
        '--expected-records',str(selected['records_count']),'--expected-pages',str(selected['pages']),'--all-sheets-directly-viewed']
    runpy.run_module('scripts.record_editorial_native_visual_review_v1',run_name='__main__')


if __name__=='__main__':main()
