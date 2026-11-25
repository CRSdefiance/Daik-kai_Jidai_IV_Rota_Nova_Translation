"""Prepare complete source Japanese pages andnine native progressive name masks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B48_source_plane_tools_v8037')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/prove_Rafael_B46_source_planes_v7946.py','scripts/prove_Rafael_B48_source_planes_v8037.py',{
        'Rafael_B46_source_name_planes_v7946':'Rafael_B48_source_name_planes_v8037',
        'Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json':
            'Rafael_B48_current_v8028/all91_complete_source_current_refs_before_new_English_manuscript.json',
        'Rafael_B46_effective_v7928/all24_effective_English_templates48_original_dispatches12_FE.json':
            'Rafael_B48_effective_v8029/all91_effective_English_templates182_original_dispatches4_FE.json',
        'Rafael_B46_names_v7921/three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json':
            'Rafael_B48_names_v8023/nine_static_speakers18_getters_clean_fields36_synthetic_macro_alignments.json',
        'Rafael_B46_pages_v7933/24_complete_native_pages96_compiled_alignments12_FE.json':
            'Rafael_B48_pages_v8036/91_complete_native_paragraphs92_pages364_compiled_alignments4_FE.json',
        'Rafael_B46_logical_v7931/24_logical_paragraphs96_original_native_alignments12_FE.json':
            'Rafael_B48_logical_v8032/91_logical_paragraphs364_original_native_alignments4_FE.json',
        'native_six_progressive_andfull_getters':'native_eighteen_progressive_andfull_getters',
        'block=46':'block=48','len(nameplanes)==3 and len(sourcepages)==24':'len(nameplanes)==9 and len(sourcepages)==91',
        "sum(len(r['pages']) for r in sourcepages)==24":"sum(len(r['pages']) for r in sourcepages)==91",
        '24_complete_source_pages3_names12_literal_alignments12_FE.json':'91_complete_source_pages9_names36_literal_alignments4_FE.json',
        'source_complete_native_pages=24':'source_complete_native_pages=91',
        'current_name_literal_alignment_cases=12':'current_name_literal_alignment_cases=36',
        'all24_original_Japanese_paragraphs_andzero_macros_preserved':'all91_original_Japanese_paragraphs_andoneFI_preserved',
        'Twelve original progressive paragraphs,twelve CP932 FE pages andthree complete nameplates.':
            'Eighty-seven original progressive Japanese paragraphs,four CP932 FE pages andnine complete nameplates.',
        '24 complete clean-source pages,including12 CP932 FE pages,three original-style11 nameplates/12 literal alignments pass. Actual comparisons pending.':
            '91complete clean-source pages/fourCP932FE,nine original-style11 names/36literalalignments pass.Actual comparisons pending.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared91source-page/nine-name complete-font proof;four source FE consumers remain distinct.')
