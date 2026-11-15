"""Prepare all15 clean source pages andfour complete current names with exact current font."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B47_source_plane_tools_v7986')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/prove_Rafael_B46_source_planes_v7946.py','scripts/prove_Rafael_B47_source_planes_v7986.py',{
        'Rafael_B46_source_name_planes_v7946':'Rafael_B47_source_name_planes_v7986',
        'Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json':
            'Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json',
        'Rafael_B46_effective_v7928/all24_effective_English_templates48_original_dispatches12_FE.json':
            'Rafael_B47_effective_v7981/all15_effective_English_templates30_original_progressive_dispatches.json',
        'Rafael_B46_names_v7921/three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json':
            'Rafael_B47_names_v7976/four_static_speakers_eight_getters_clean_fields16_synthetic_macro_alignments.json',
        'Rafael_B46_pages_v7933/24_complete_native_pages96_compiled_alignments12_FE.json':
            'Rafael_B47_pages_v7985/15_complete_native_paragraphs16_pages60_compiled_alignments.json',
        'Rafael_B46_logical_v7931/24_logical_paragraphs96_original_native_alignments12_FE.json':
            'Rafael_B47_logical_v7983/15_logical_paragraphs60_original_native_progressive_alignments.json',
        'native_six_progressive_andfull_getters':'native_eight_progressive_andfull_getters',
        'FE,FE_calibration=make_source_painter(image)':
            "assert font==NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT')\n    assert all(r['source_selector']!=254 for r in current['records'])\n    FE_calibration=dict(unused='B47 has no FE source ornew FE coverage')",
        'block=46':'block=47',
        'len(nameplanes)==3 and len(sourcepages)==24':'len(nameplanes)==4 and len(sourcepages)==15',
        "sum(len(r['pages']) for r in sourcepages)==24":"sum(len(r['pages']) for r in sourcepages)==15",
        '24_complete_source_pages3_names12_literal_alignments12_FE.json':
            '15_complete_source_pages4_names16_literal_alignments_all_progressive.json',
        'source_complete_native_pages=24':'source_complete_native_pages=15',
        'current_name_literal_alignment_cases=12':'current_name_literal_alignment_cases=16',
        'all24_original_Japanese_paragraphs_andzero_macros_preserved':'all15_original_Japanese_paragraphs_andzero_macros_preserved',
        'source_FE_palette_native15_foreground14_shadow_actual_color_binding_pending':
            'no_FE_source_orFE_palette_coverage_claim_B47_all_progressive',
        'actual_source_English_body_header_FE_andtransition_audit_pending':
            'actual_source_English_body_header_andR53_two_page_transition_audit_pending',
        'Twelve original progressive paragraphs,twelve CP932 FE pages andthree complete nameplates.':
            'Fifteen original progressive Japanese paragraphs andfour complete original-style11 names.',
        '24 complete clean-source pages,including12 CP932 FE pages,three original-style11 nameplates/12 literal alignments pass. Actual comparisons pending.':
            '15 complete clean-source progressive pages,four original-style11 names/16 literal alignments pass.Allcurrent glyphs andbounds exact;actual comparisons pending.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared15-source-page/four-name current-font proof;no new FE coverage.')
