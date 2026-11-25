"""Seal the exact 13-exchange Maria subset after stored and representative QA.

Preserve the complete original source/current binding, five-gate and per-record
final-reference contract. B50 remains a separate, unapproved complete exchange.
"""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/finalize_maria301_research_v1.py').read_text(encoding='utf-8'),{
    'Maria_B0_B32_clean_20261109':'Maria_B37_B50_clean_20261109',
    'maria_B0_B32_final_review_v1.json':'maria_B37_B49_final_review_v1.json',
    'maria_B0_B32_scoped_names_final_v1.json':'maria_B37_B49_scoped_names_final_v1.json',
    "ROOT/'stored_reconstruction_v1/reconstruction.json'":"ROOT/'stored270_reconstruction_v1/reconstruction.json'",
    "ROOT/'stored_v1/stored_native_verification.json'":"ROOT/'stored270_v1/stored_native_verification.json'",
    "ROOT/'stored_catalogue_all_v1/all299_stored_effective_body_bindings.json'":"ROOT/'stored270_catalogue_v1/all266_stored_effective_body_bindings.json'",
    "ROOT/'loaders_v1/verification.json'":"ROOT/'loaders270_v1/verification.json'",
    "ROOT/'offline_display_approval_v1.json'":"ROOT/'offline270_display_approval_v2.json'",
    "ROOT/'gameplay_review_v1.json'":"ROOT/'gameplay270_review_v1.json'",
    "ROOT/'scoped36_name_editorial_review_v2.json'":"ROOT/'scoped28_name_editorial_review_v1.json'",
    "Path('translations/maria_B0_B32_contextual_review_v1.json')":"ROOT/'complete_B37_B49_projection_v1/contextual_review.json'",
    "len(doc['records']) == len(byprose) == 301":"len(doc['records']) == len(byprose) == 270",
    '(178,123)':'(161,109)',
    "data['visual']['every_final_page_directly_viewed_in_readable_sheets']":"data['visual']['all272_selected_body_pages_directly_viewed']",
    "data['visual']['all36_scoped_actors_and44_distinct_name_strings_native_andvisually_checked']":"data['visual']['all42_name_strings_andboth_menu_sheets_directly_viewed']",
    '(303,303,635)':'(272,272,480)',
    "data['catalogue']['all299_ordinary_and_style_bodies_checked']":"data['catalogue']['all266_ordinary_and_style_bodies_checked']",
    '(42683,92,96,207)':'(41924,63,69,203)',
    "actual['all96_broad_pages_andboth_two_page_exit_sheets_directly_viewed'] and actual['all_four_two_page_transitions_observed']":
        "actual['all_selected_pages_directly_viewed'] and actual['all_six_two_page_transitions_observed']",
    "actual['ordinary_default_menu_return_to_next_fixture_speech_observed']":"actual['ordinary_default_menu_returns_to_next_fixture_speech_observed']",
    "actual['complete_original_host_nonspeech_setup_variant_reaches_resupply_andordinary_sailing']":"actual['complete_original_host_nonspeech_setup_reaches_resupply_andordinary_sailing']",
    "actual['reclaimed_one_page_Havana_paragraph_observed'] and actual['corrected_B14_I_glyph_observed']":
        "actual['both_reclaimed_B49_single_pages_andcomplete_question_tag_observed'] and actual['FE_to_named_speaker_transition_observed']",
    "styles['physical_alternatives'] == 7 and styles['native_target_slot_cases'] == 8":"styles['physical_alternatives'] == 0 and styles['native_target_slot_cases'] == 0 and not styles['objects']",
    "sum(len(x['rejected']) for x in styles['compiler_negatives']) == 9":"sum(len(x['rejected']) for x in styles['compiler_negatives']) == 0",
    "len(menus['menus']) == 1 and stored['typed_labels_checked'] == 2":"len(menus['menus']) == 2 and stored['typed_labels_checked'] == 4",
    '(299,2,92)':'(266,4,63)',
    'all301_individual_five_gates_pass=True':'all270_individual_five_gates_pass=True',
    'actual_source_speech_variants=92,actual_body_pages=96,offline_only_source_speech_variants=207':'actual_source_speech_variants=63,actual_body_pages=69,offline_only_source_speech_variants=203',
    'native_body_pages=303':'native_body_pages=272',
    'all36_individual_five_gates_pass_in_scoped_context=True':'all28_individual_five_gates_pass_in_scoped_context=True',
    'records=301,revisions=178,retentions=123':'records=270,revisions=161,retentions=109',
    'body_pages=303,typed_labels=2,scoped_names=36,wrap_improvements=35,layout_retentions=2':'body_pages=272,typed_labels=4,scoped_names=28,wrap_improvements=26,layout_retentions=6',
    'actual_source_variants=92,actual_pages=96,offline_only_source_variants=207':'actual_source_variants=63,actual_pages=69,offline_only_source_variants=203',
    'actual_runs=3,actual_frames=42683,actual_menus=1':'actual_runs=4,actual_frames=41924,actual_menus=2',
    "print('Sealed301 five-gate reviews and36 scoped names;178 revisions/123 retentions. Registered integration andonce-only credit remain.')":
        "print('Sealed270 five-gate reviews and28 scoped names;161 revisions/109 retentions. B50 preserved separately;registered integration andonce-only credit remain.')",
})
exec(compile(source,__file__+'::same-complete-individual-five-gates-exact-Maria270-scope','exec'),globals())
