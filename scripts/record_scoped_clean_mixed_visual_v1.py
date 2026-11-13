"""Record direct name/menu sheet review without claiming gameplay or storage coverage."""
import argparse
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ['names','menus','out']:ap.add_argument('--'+key,type=Path,required=True)
    ap.add_argument('--all-sheets-directly-viewed',action='store_true',required=True)
    args=ap.parse_args();assert not args.out.exists() and args.all_sheets_directly_viewed
    names,menus=map(load,[args.names,args.menus]);assert names['runtime']==menus['runtime']
    assert names['all_name_strings_ASCII_complete_andfit_style11_216px']
    assert menus['all_complete_caption_controls_indices_pixels_centering_bounds_andcanaries_pass']
    for plane in names['planes']:
        assert plane['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
        assert digest(plane['native_plane'])==plane['native_plane_sha256'] and digest(plane['preview'])==plane['preview_sha256']
    sheets=[dict(s,kind='scoped-name',directly_viewed=True) for s in names['review_sheets']]
    for obj in menus['objects']:
        assert digest(obj['proof'])==obj['proof_sha256']
        proof=load(obj['proof']);assert proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        for sheet in obj['review_sheets']:sheets.append(dict(sheet,kind='native-menu-caption',directly_viewed=True))
    for sheet in sheets:assert digest(sheet['path'])==sheet['sha256']
    save(args.out,dict(runtime=names['runtime'],scoped_actors=names['actors'],scoped_name_consumer_bindings=len(names['consumer_bindings']),
        distinct_name_strings=names['distinct_current_strings'],fresh_native_name_strings=names['fresh_native_name_strings'],reused_native_name_strings=names['reused_native_name_strings'],
        menus=menus['menus'],captions=menus['captions'],native_menu_provider_alignments=menus['native_provider_alignments'],
        bridged_modal_returns=menus['bridged_modal_returns'],current_target_normal_highlight_planes=menus['current_andtarget_normal_highlight_planes'],
        target_normal_highlight_planes=menus['target_normal_highlight_planes'],compiler_negative_cases=menus['compiler_negatives'],
        all_names_andcaptions_directly_viewed=True,complete_leading_internal_trailing_names_andcaption_glyphs_visible=True,
        no_font_encoding_clipping_orcentering_defect_observed=True,review_sheets=sheets,
        native_indices_aliases_controls_andforeground_planes_pass=True,
        full_catalogue_UI_actual_headers_controller_paths_andnew_conditional_rosters_unvisited=True,
        actual_gameplay=False,stored_script_andregistered_integration_pending=True,all_fifth_gates_still_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [args.names,args.menus,Path(__file__)]}))
    print(dict(names=names['distinct_current_strings'],captions=menus['captions'],directly_viewed_sheets=len(sheets),actual_gameplay=False,new_credit=0))


if __name__=='__main__':main()
