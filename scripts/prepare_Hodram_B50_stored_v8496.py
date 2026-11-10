"""Reuse unchanged compiled bodies andfreshly test the one required parity tail."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_B50_stored_tools_v8496')
if __name__=='__main__':
    assert not ROOT.exists();result=derive('scripts/prove_Hodram_B49_stored_v8399.py','scripts/prove_Hodram_B50_stored_v8496.py',{
        'scripts.Hodram_outcomes_registered_route_context_v8380':'scripts.Hodram_B49_registered_route_context_v8478',
        'Hodram_B49_stored_v8399':'Hodram_B50_stored_v8496','Hodram_B49_relocation_v8398':'Hodram_B50_relocation_v8495','Hodram_B49_pages_v8395':'Hodram_B50_pages_v8492b',
        'Hodram_B49_native_review_v8397':'Hodram_B50_native_review_v8493','translations/hodram_B49_editorial_manuscript_v2.json':'translations/hodram_B50_editorial_manuscript_v2.json','current_V8377_Hodram_native_v8380':'current_V8475_Hodram_native_v8478',
        "view['reviewed_body_pages']==14 and view['directly_viewed_native_sheet']==native['review_sheet']":"view['all_three_complete_bodies_visually_read'] and view['directly_viewed_sheet']==native['review_sheet']",
        'IlnkContainer.parse(archive).blocks[49]':'IlnkContainer.parse(archive).blocks[50]','block=49':'block=50',
        'len(rows)==14 and len(fresh)==6 and len(reused)==8':'len(rows)==3 and len(fresh)==1 and len(reused)==2',
        'fresh_native_alignment_cases=24,exact_reused_native_alignment_cases=32':'fresh_native_alignment_cases=4,exact_reused_native_alignment_cases=8',
        'all14_full_first_internal_final_glyphs_bounds_consumption_andsingle_page_checks_pass':'all3_full_first_internal_final_glyphs_bounds_consumption_andsingle_page_checks_pass',
        'all14_ink_planes_exact_to_already_viewed':'all3_ink_planes_exact_to_already_viewed',
        'source_bound_ellipsis_andmixed_ellipsis_English_preserved':'ordinary_source_punctuation_andzero_macros_preserved',
        'menu_UI_full_stored_controls_loaders_actual_policy_andregistered_release_pending':'full_stored_controls_loaders_actual_policy_andregistered_release_pending',
        'All14 stored bodies pass:6 parity tails/24 fresh alignments,8 exact bodies/32 reused alignments. Full viewed ink unchanged;no blank/extra pages.No ROM/credit.':'B50all3storedbodies pass:1paritytail/4freshalignments,2exactbodies/8reusedalignments. Fullviewedink unchanged;no blank/extrapages.No ROM/credit.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'derivation.json',dict(derivation=result,all_original_native_painter_macro_ABI_bounds_parity_andcomplete_ink_checks_preserved=True,all_native_addresses_andmultiplicity_preserved=True,only_one_changed_stored_body_requires_fresh_alignments=True,all_earlier_producers_andproofs_preserved=True,new_credit=0,full_goal_complete=False))
