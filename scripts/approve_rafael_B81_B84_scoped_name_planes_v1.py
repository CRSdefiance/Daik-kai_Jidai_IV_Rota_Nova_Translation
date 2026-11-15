"""Seal the directly viewed16-name offline planes;retain actual/catalogue/global-review limits."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B81_B84_progressive_name_planes_v2_20261105')
if __name__=='__main__':
    path=ROOT/'native_name_planes.json';out=ROOT/'direct_visual_approval.json';assert not out.exists()
    d=load(path);assert d['scoped_actors']==d['distinct_strings']==16 and (d['fresh_name_planes'],d['exact_reused_name_planes'])==(6,10)
    assert d['current_progressive_names_bound_to_qualified_original_getters'] and d['all_scoped_progressive_names_ASCII_complete_andfit_native216px']
    assert len(d['review_sheets'])==2
    for sheet in d['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    for plane in d['planes']:
        assert sha(Path(plane['native_plane']).read_bytes())==plane['native_plane_sha256']
        assert sha(Path(plane['preview']).read_bytes())==plane['preview_sha256']
        assert plane['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
    save(out,dict(native_proof=str(path),native_proof_sha256=sha(path.read_bytes()),all_two_readable_sheets_directly_viewed=True,
        all16_complete_name_planes_approved=True,fresh_name_planes=6,exact_reused_name_planes=10,sheets=d['review_sheets'],
        name_decisions=d['evidence'],no_name_field_change_ornew_actual_header_capture=True,
        original_failed_v1_six_partial_planes_retained_not_a_complete_pass=True,
        actual_headers_full_catalogue_UI_andglobal207_review_remain_open=True,new_credit=0,guide_photos=False))
    print('Approved16 complete style11 nameplanes on two viewed sheets;no name-field changes/actual-header claim/global207 approval.')
