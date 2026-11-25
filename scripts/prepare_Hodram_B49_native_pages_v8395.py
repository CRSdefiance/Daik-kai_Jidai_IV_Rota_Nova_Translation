"""Source-lock fourteen compiled native pages and56 guarded alignments to the own current Hodram context."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_native_tools_v8395');assert not root.exists()
    d=derive('scripts/prove_Hodram_B47_B48_pages_v8324.py','scripts/prove_Hodram_B49_pages_v8395.py',{
        'scripts.Hodram_registered_route_context_v8303':'scripts.Hodram_outcomes_registered_route_context_v8380',
        'Hodram_B47_B48_pages_v8324':'Hodram_B49_pages_v8395','translations/hodram_B47_B48_editorial_manuscript_v1.json':'translations/hodram_B49_editorial_manuscript_v1.json',
        'work/analysis/Hodram_B47_B48_layout_v8323/six_automatic_plans_original_usable_width_distinct_FE_all_QA_preserved.json':'work/analysis/Hodram_B49_layout_v8394/automatic_plans.json',
        'work/analysis/Hodram_B47_B48_logical_v8320/six_logical_paragraphs24_guarded_alignments_distinct_FE_one_FI.json':'work/analysis/Hodram_B49_logical_v8389/logical_prose_and_choice_table.json',
        'work/analysis/Hodram_B47_B48_source_display_v8316b/six_source_dispatches24_macro_alignments_five_progressive_one_FE_pages_Lil_identity_reuse.json':'work/analysis/Hodram_B49_source_display_v8386b/source_display.json',
        'current_V8300_Hodram_native_v8303':'current_V8377_Hodram_native_v8380',
        "len(plan['records'])==6":"len(plan['records'])==14","len(rows)==6":"len(rows)==14","len(pictures)==6":"len(pictures)==14",
        '(1368,320)':'(1368,800)','six_complete_English_native_pages.png':'fourteen_English_native_pages.png','six_complete_native_pages24_compiled_alignments_distinct_FE.json':'compiled_native_pages.json',
        'fresh_compiled_alignment_cases=24':'fresh_compiled_alignment_cases=56','progressive_alignment_cases=20':'progressive_alignment_cases=52','complete_progressive_pages=5':'complete_progressive_pages=13',
        'all_six_single_pages':'all14_single_pages','all_six_formatting_gates_still_false':'all16_formatting_gates_still_false','one_source_FI_preserved_no_shortening_orprose_manual_wrap':'zero_source_macros_preserved_no_shortening_orprose_manual_wrap',
        'Six complete one-page English displays/24compiled alignments:fiveprogressive+oneoriginalFE':'Fourteen complete one-page English displays/56compiled alignments:13progressive+oneoriginalFE',
    })
    root.mkdir(parents=True);save(root/'compiled_native_page_derivation.json',dict(derivation=d,all_native_high_constants_andmultiplicity_preserved=True,own_V8377_context_original_FE_andsource_bound_ellipsis_glyphs=True,no_ROM_font_profile_viewport_orcredit_change=True,new_credit=0,full_goal_complete=False))
