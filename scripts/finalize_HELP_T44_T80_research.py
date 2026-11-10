"""Seal37 five-gate reviews only after17 observed pages andall38 native pages areviewed."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/finalize_town_HELP23_research.py').read_text(encoding='utf-8'),{
 'from dk4tool.dialogue.reviewed_help_pages_v3 import plan_articles':'from dk4tool.dialogue.reviewed_help_pages_v5 import plan_articles',
 'Shared_HELP_T21_T43_formatting_20261104':'Shared_HELP_T44_T80_formatting_20261104',
 'help_town23_contextual_final_review_v1.json':'help_shipyard37_contextual_final_review_v1.json',
 "native_path=ROOT/'refined_native_v2/native_help_pages.json'":"native_path=ROOT/'native_pages_v1/native_help_pages.json'",
 "visual_path=ROOT/'preview_qualification_v2/direct_visual_approval.json'":"visual_path=ROOT/'preview_qualification_v1/direct_visual_approval.json'",
 "native['native_pages']==28 and (native['fresh_pages'],native['exact_reused_pages'])==(10,18)":
 "native['native_pages']==38 and len(native['records'])==38",
 "visual['all28_complete_pages_approved']":"visual['all38_complete_pages_approved']",
 "==(15,10,13)":"==(17,16,21)",
 "==6 and len(actual['readable_actual_sheets'])==4":"==7 and len(actual['readable_actual_sheets'])==5",
 'all_four_actual_sheets_directly_viewed=True,all15_observed_pages_approved=True':
 'all_five_actual_sheets_directly_viewed=True,all17_observed_pages_approved=True',
 'all_five_two_page_cases_two_row_heading_bottom_links_andoriginal_returns_observed=True':
 'fleet_two_page_case_ten_row_bodies_equipment_links_andoriginal_returns_observed=True',
 'Inn_B_phrase_andSquare_Trends_wording_observed_in_Help_not_new_town_command_activation=True':
 'corrected_A_X_instruction_observed_in_Help_not_new_physical_Refit_X_execution=True',
 'Semantic paragraphs keep tips,letter instructions and100-percent exceptions whole.':
 'Source66 definition andoperating-funds paragraphs keep the commander-return sentence onone page;at least150 andnative button phrases remain whole.',
 'Exact-byte/runtime proof reuse isexplicit;all28 pages directly viewed.':
 'All38 pages receive fresh native/full-font checks anddirect visual review;current runtime dependencies arebound explicitly.',
 'len(records)==23 and sum(r[\'offline_only\'] for r in records)==13':
 'len(records)==37 and sum(r[\'offline_only\'] for r in records)==21',
 "format='dk4-town-help23-contextual-final-review-v1',records=records,records_count=23":
 "format='dk4-shipyard-help37-contextual-final-review-v1',records=records,records_count=37",
 'all23_individual_five_gates_pass=True':'all37_individual_five_gates_pass=True',
 'proposed_revisions=19,justified_retentions=4':'proposed_revisions=27,justified_retentions=10',
 'native_andvisually_approved_pages=28,initial_pages29_preserved_after_six_display_refinements=True':
 'native_andvisually_approved_pages=38,initial38_page_plan_preserved_after_source66_paragraph_refinement=True',
 'fresh_native_pages=10,exact_reused_native_pages=18,actual_pages=15,actual_articles=10,offline_only_pages=13,offline_only_articles=13':
 'fresh_native_pages=38,exact_reused_native_pages=0,actual_pages=17,actual_articles=16,offline_only_pages=21,offline_only_articles=21',
 'actual_ordinary_coldboot_frames=31641,all_five_continuation_cases_andL_R_returns_observed=True':
 'actual_ordinary_coldboot_frames=30681,one_continuation_case_andseven_L_R_orforward_back_returns_observed=True',
 '23 town Help reviews sealed:19 revisions/4 retentions,28 native/viewed pages,15 observed/13 offline-only.':
 '37 shipyard-to-ruins Help reviews sealed:27 revisions/10 retentions,38 native/viewed pages,17 observed/21 offline-only.',
})
exec(compile(source,__file__+'::same-individual-full-native-actual-oroffline-binding-andproduction-source-inverse-for37-articles','exec'),globals())
