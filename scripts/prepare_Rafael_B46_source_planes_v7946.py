"""Derive complete source CP932/ASCII pages and three original nameplate planes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_source_plane_tools_v7946');assert not root.exists()
    row=derive('scripts/prove_Rafael_B45_source_planes_v7894.py','scripts/prove_Rafael_B46_source_planes_v7946.py',{
        'Eleven complete original progressive paragraphs, one distinct CP932 FE page and two nameplates.':'Twelve original progressive paragraphs,twelve CP932 FE pages andthree complete nameplates.',
        'Rafael_B45_source_name_planes_v7894':'Rafael_B46_source_name_planes_v7946',
        'Rafael_B45_current_v7871/all12_complete_source_current_refs_before_new_English_manuscript.json':'Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json',
        'Rafael_B45_effective_v7872/all12_effective_English_templates24_original_dispatches_distinct_FE.json':'Rafael_B46_effective_v7928/all24_effective_English_templates48_original_dispatches12_FE.json',
        'Rafael_B45_names_v7869/two_static_speakers_four_getters_clean_fields_eight_macro_alignments.json':'Rafael_B46_names_v7921/three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json',
        'Rafael_B45_native_review_v7883/12_exact_native_pages_rebound_with_individual_row_review.json':'Rafael_B46_pages_v7933/24_complete_native_pages96_compiled_alignments12_FE.json',
        'Rafael_B45_logical_refined_v7876b/12_refined_logical_bindings44_reused4_fresh_alignments.json':'Rafael_B46_logical_v7931/24_logical_paragraphs96_original_native_alignments12_FE.json',
        'native_four_progressive_andfull_getters':'native_six_progressive_andfull_getters',
        'block=45,source_selector':'block=46,source_selector',
        'len(nameplanes)==2 and len(sourcepages)==12':'len(nameplanes)==3 and len(sourcepages)==24',
        "sum(len(r['pages']) for r in sourcepages)==12":"sum(len(r['pages']) for r in sourcepages)==24",
        '12_complete_source_pages2_names8_literal_alignments_distinct_FE.json':'24_complete_source_pages3_names12_literal_alignments12_FE.json',
        'source_complete_native_pages=12':'source_complete_native_pages=24',
        'current_name_literal_alignment_cases=8':'current_name_literal_alignment_cases=12',
        'all12_original_Japanese_paragraphs_andreal_FO_preserved':'all24_original_Japanese_paragraphs_andzero_macros_preserved',
        'Twelve complete clean-source pages,including distinct CP932 FE paper,two original-style11 nameplates/eight literal alignments pass. Actual comparisons pending.':'24 complete clean-source pages,including12 CP932 FE pages,three original-style11 nameplates/12 literal alignments pass. Actual comparisons pending.',
    })
    root.mkdir(parents=True);save(root/'source_locked_derivation.json',row)
