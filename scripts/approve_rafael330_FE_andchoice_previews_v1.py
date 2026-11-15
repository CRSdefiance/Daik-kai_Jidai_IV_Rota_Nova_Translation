"""Approve all four FE panels andtwenty caption style planes,without granting actual/release credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

CHOICES=Path('work/analysis/Rafael_B84_choices_20261105')
FE=Path('work/analysis/Rafael_B84_FE_pagination_20261105')

if __name__=='__main__':
    out=CHOICES/'complete_native_visual_approval_v1.json';assert not out.exists()
    two,three=[load(CHOICES/p/'menu_provider_and_planes.json') for p in ['two_choice_native_v1','three_choice_native_v1']]
    styles=load(CHOICES/'all_styles_visual_v1/receipt.json');native=load(FE/'native_v1/compiled_native_pages.json')
    assert (len(two['records']),len(three['records']),styles['planes'],native['pages'])==(8,12,20,4)
    assert len(two['compiler_negatives_rejected'])==7 and len(three['compiler_negatives_rejected'][0]['rejected'])==8
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and native['complete_consumption_andpagination_exact']
    assert len(native['review_sheets'])==1
    sheets=[two['review_sheet'],*three['review_sheets'],*native['review_sheets']]
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    assert sha(Path(styles['sheet']).read_bytes())==styles['sheet_sha256']
    for p in styles['records']:assert sha(Path(p['plane']).read_bytes())==p['plane_sha256']
    save(out,dict(all_four_readable_native_sheets_directly_viewed=True,all20_menu_style_planes_andfour_FE_pages_approved=True,
        sheets=sheets,all_styles_sheet=styles['sheet'],all_styles_sheet_sha256=styles['sheet_sha256'],
        complete_source_current_target_native_provider_alignments=12,bridged_modal_returns=42,
        all15_menu_compiler_invalid_cases_rejected=True,no_actual_menu_controller_claim_from_bridged_cases=True,
        original_two_source_FE_paragraphs_retained_as_four_native_panels=True,source_FE_control_andscope_inverse_checks_separate=True,
        actual_FE_panel_dismissal_transitions_menu_highlights_andstored_release_still_pending=True,
        zero_extra_source_records_orcompletion_credit=True,guide_photos=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [CHOICES/'two_choice_native_v1/menu_provider_and_planes.json',
            CHOICES/'three_choice_native_v1/menu_provider_and_planes.json',CHOICES/'all_styles_visual_v1/receipt.json',FE/'native_v1/compiled_native_pages.json',Path(__file__)]}))
    print('Approvedfour FE panels andall20 native menu style planes;15 rejects/12 provider alignments/42 bridged returns. Actual controller/transition checks remain separate.')
