"""Seal303 decisions using the unchanged individual-gate and exact-reference contract."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/finalize_maria301_research_v1.py').read_text(encoding='utf-8'), {
    'Maria_B0_B32_clean_20261109': 'Maria_B58_B70_clean_20261109',
    'maria_B0_B32_final_review_v1.json': 'maria_B58_B70_final_review_v1.json',
    'maria_B0_B32_scoped_names_final_v1.json': 'maria_B58_B70_scoped_names_final_v1.json',
    "ROOT/'stored_reconstruction_v1/reconstruction.json'": "ROOT/'reconstruction_v2/reconstruction.json'",
    "ROOT/'scoped36_name_editorial_review_v2.json'": "ROOT/'scoped20_names_editorial_review_v3.json'",
    "ROOT/'formatting_v1/role_bindings.json'": "ROOT/'formatting_v3/role_bindings.json'",
    "ROOT/'scoped_terms_v1.json'": "ROOT/'scoped_terms_reference_v1.json'",
    'maria_B0_B32_contextual_review_v1.json': 'maria_B58_B70_contextual_review_v2.json',
    "len(doc['records']) == len(byprose) == 301": "len(doc['records']) == len(byprose) == 303",
    '(178,123)': '(181,122)',
    "data['visual']['every_final_page_directly_viewed_in_readable_sheets']": "data['visual']['all299_final_pages_directly_viewed_or_exact_visual_dependency_reuse']",
    "data['visual']['all36_scoped_actors_and44_distinct_name_strings_native_andvisually_checked']": "data['visual']['all24_names_andfour_captions_directly_viewed']",
    '(303,303,635)': '(299,299,120)',
    '(42683,92,96,207)': '(48322,116,116,183)',
    "actual['all96_broad_pages_andboth_two_page_exit_sheets_directly_viewed']": "actual['all116_selected_pages_directly_viewed']",
    "actual['all_four_two_page_transitions_observed']": "actual['both_reclaimed_single_page_paragraphs_andnext_source_returns_observed']",
    "actual['complete_original_host_nonspeech_setup_variant_reaches_resupply_andordinary_sailing']": "actual['complete_original_host_nonspeech_setup_reaches_resupply_andordinary_sailing']",
    "actual['reclaimed_one_page_Havana_paragraph_observed'] and actual['corrected_B14_I_glyph_observed']": "actual['inline_FE_boy_andnamed_portrait_return_observed'] and actual['corrected_B59_ASCII_I_andB61_normal_F_glyphs_observed']",
    "assert styles['physical_alternatives'] == 7 and styles['native_target_slot_cases'] == 8\n    assert sum(len(x['rejected']) for x in styles['compiler_negatives']) == 9": "assert not styles['objects'] and not stored['style_records'] and styles['physical_alternatives'] == styles['native_target_slot_cases'] == 0",
    "assert len(menus['menus']) == 1 and stored['typed_labels_checked'] == 2": "assert len(menus['menus']) == 2 and stored['typed_labels_checked'] == 4",
    '(299,2,92)': '(299,4,116)',
    'all301_individual_five_gates_pass=True': 'all303_individual_five_gates_pass=True',
    'actual_source_speech_variants=92,actual_body_pages=96,offline_only_source_speech_variants=207': 'actual_source_speech_variants=116,actual_body_pages=116,offline_only_source_speech_variants=183',
    'native_body_pages=303': 'native_body_pages=299',
    'all36_individual_five_gates_pass_in_scoped_context=True': 'all20_individual_five_gates_pass_in_scoped_context=True',
    "context='Source-bound name/role in the reviewed SC3 references: '+', '.join(row['context_record_ids'])": "context=row['context']",
    'records=301,revisions=178,retentions=123': 'records=303,revisions=181,retentions=122',
    'body_pages=303,typed_labels=2,scoped_names=36,wrap_improvements=35,layout_retentions=2': 'body_pages=299,typed_labels=4,scoped_names=20,wrap_improvements=7,layout_retentions=4,pages_reclaimed=2',
    'actual_source_variants=92,actual_pages=96,offline_only_source_variants=207': 'actual_source_variants=116,actual_pages=116,offline_only_source_variants=183',
    'actual_runs=3,actual_frames=42683,actual_menus=1': 'actual_runs=2,actual_frames=48322,actual_menus=2',
    'Sealed301 five-gate reviews and36 scoped names;178 revisions/123 retentions.': 'Sealed303 five-gate reviews and20 scoped names;181 revisions/122 retentions.',
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-individual-gates-andexact-stored-references303', 'exec'), globals())
