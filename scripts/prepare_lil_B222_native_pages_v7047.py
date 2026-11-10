"""Prepare all16 complete paragraph native checks under the exact current2b6 runtime."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B222_native_page_tools_v7047')
if __name__=='__main__':
    assert not ROOT.exists()
    changes={
        'B221':'B222','editorial_manuscript_v1.json':'editorial_manuscript_v2.json',
        'layout_v6976/fourteen_whole_paragraph_plans_no_macros_no_prose_changes':'layout_v7046b/sixteen_whole_paragraph_plans_no_macros_no_prose_changes',
        'current_V6956_native_v6966':'current_V7029_native_v7033','native_pages_v6980':'native_pages_v7047',
        'Al_Ferid_exact_native_context_v6520':'square_shopkeeper_exact_native_context_v7020',
        'Al_Ferid_font_oracles_v6520':'square_shopkeeper_font_oracles_v7020',
        'aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05':'2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a',
        '[2,17,85]':'[2,16]',"len(plan['records'])==14":"len(plan['records'])==16",'len(cases)==len(pictures)==14':'len(cases)==len(pictures)==16',
        'alignments==112':'alignments==128','all14_paragraphs14_complete_native_pages112_alignments':'all16_paragraphs16_complete_native_pages128_alignments',
        'complete_native_pages=14':'complete_native_pages=16','logical_compiled_input_alignment_cases=112':'logical_compiled_input_alignment_cases=128',
        'all14_single_pages':'all16_single_pages','all14_complete_pages_sheet':'all16_complete_pages_sheet','only_original_static_selectors2_17_85':'only_original_static_selectors2_16',
        'source_owned_AA5_page_adapter':'source_owned_2b6_page_adapter','::AA5-original-pages':'::2b6-original-pages',
        'native_name_planes_actual_headers_controls_reference_and_release_pending':'final_stored_actual_English_reference_and_release_pending',
        'all14_formatting_gates_remain_false':'all16_formatting_gates_remain_false','14 complete single native pages/112 alignments':'16 complete single native pages/128 alignments'}
    tool=derive('scripts/verify_lil_B221_native_pages_v6980.py','scripts/verify_lil_B222_native_pages_v7047.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_exact_native_checker.json',dict(tool=tool,
        all_native_addresses_geometry_pair_phase_guards_and_canaries_preserved=True,exact2b6_helpers_no_relaxed_AA5_guard=True,
        sixteen_logical_and_compiled_paragraphs_all_four_alignments_per_version_required=True,new_review_credit=0,full_goal_complete=False))
