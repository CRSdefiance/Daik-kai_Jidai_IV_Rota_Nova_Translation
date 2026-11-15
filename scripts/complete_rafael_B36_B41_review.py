"""Credit175 once after the registered successor passes;keep159 offline-only records explicit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/complete_rafael_B42_B43_review.py').read_text(encoding='utf-8'),{
    'Rafael_early_tutorial_release_verified_20261104':'Rafael_B36_B41_release_verified_20261104',
    'rafael_B42_B43_contextual_final_review_v1.json':'rafael_B36_B41_contextual_final_review_v1.json',
    'Rafael_early_tutorial_B42_B43_checked_20261104/actual_visual_approval.json':'Rafael_B36_B41_checked_20261104/actual_review.json',
    'Rafael_early_tutorial_B42_B43_actual_pixels_20261104/focused_actual_pixels.json':'Rafael_B36_B41_focused_actual_pixels_20261104/focused_actual_pixels.json',
    'Rafael_SC0_B42_B43_early_tutorial_20261104':'Rafael_SC0_B36_B41_contextual_20261104',
    'Rafael_SC0_B42_B43_complete_contextual_release_20261104':'Rafael_SC0_B36_B41_complete_contextual_release_20261104',
    "release['complete_stack_entries']==665":"release['complete_stack_entries']==666",
    "(len(doc['records']),doc['proposed_revisions'],doc['wording_retentions'])==(40,19,21)":
        "(len(doc['records']),doc['proposed_revisions'],doc['wording_retentions'])==(175,76,99)",
    "    assert actual['all42_target_pages_observed_in_order'] and len(actual['all_review_sheets_directly_viewed'])==2\n    assert pixels['all_required_distinct_display_cases_match'] and len(pixels['body_pages'])==92\n    assert [(r['run'],r['calls']) for r in pixels['ordered_linear_scene_sequences']]==[('first_voyage',29),('crew_duties',13)]\n    assert all(r['complete_ordered_calls_match_all_copied_source_speeches'] for r in pixels['ordered_linear_scene_sequences'])":
        "    assert actual['all_three_QA_sheets_directly_viewed'] and (actual['actual_utterances'],actual['actual_pages'],actual['offline_only_utterances'])==(16,18,159)\n    assert pixels['all_selected_pages_observed_in_exact_fixture_order'] and len(pixels['body_pages'])==40\n    assert pixels['all_selected_complete_native_body_planes_andblank_guards_match'] and len(pixels['ordered_selected_source_calls'])==18",
    "assert samples and all(s['complete_native_glyph_plane_andblank_guards_equal'] for s in samples)":
        "assert all(s['complete_native_body_plane_andblank_guards_equal'] for s in samples)",
    'initialized_fixture_runs=2,fixture_frames=25002':'initialized_fixture_runs=1,fixture_frames=10001',
    'captured_body_planes_matched=92':'captured_body_planes_matched=40',
    'native_record_page_observations=42,actual_name_headers=5,reviewed_actual_sheets=2':'native_record_page_observations=18,actual_name_headers=40,reviewed_actual_sheets=3',
    'source00_FI_FE_andboth_two_page_transitions_observed=True,complete_ordered_tutorial_source_calls=True':
        'source00_FU_andboth_two_page_transitions_observed=True,complete_ordered_selected_fixture_source_calls=True,unvisited_utterances=159',
    'records=40':'records=175',
    'ordinary_speeches=40':'ordinary_speeches=175',
    'revised_count=19,retained_count=21,fresh_revisions=19,fresh_retentions=21,layout_findings_resolved=2':
        'revised_count=76,retained_count=99,fresh_revisions=76,fresh_retentions=99,layout_findings_resolved=4,glyph_fixes=2',
    'scoped_name_term_decisions=4,native_name_strings=4':'scoped_name_term_decisions=11,native_name_strings=10',
    'completion_credit_added=40':'completion_credit_added=175',
    "('records_editorially_completed',40),('records_revised_and_integrated',19),('retained_wordings_editorially_completed',21)":
        "('records_editorially_completed',175),('records_revised_and_integrated',76),('retained_wordings_editorially_completed',99)",
    "('records_with_source_and_prose_pass',40),('records_with_source_prose_drafts',40)":
        "('records_with_source_and_prose_pass',175),('records_with_source_prose_drafts',175)",
    "context['fresh_pass_records_explicitly_reread']+=40;context['fresh_pass_records_integrated']+=40":
        "context['fresh_pass_records_explicitly_reread']+=175;context['fresh_pass_records_integrated']+=175",
    'new_revisions=19,justified_retentions=21,new_completed_records=40':'new_revisions=76,justified_retentions=99,new_completed_records=175',
    'new_credit=40':'new_credit=175',
    'session=15896':'session=12117',
    'all40_source_current_final_refs_andfive_gates':'all175_source_current_final_refs_andfive_gates',
    '10306':'10346','10346':'10521','6177':'6253','4169':'4268','10349':'10524',
    "==408":"==583",
    "    ledger['latest_checkpoint']='Rafael B42/B43 tutorials registered andcredited once:40 reviews,19 revisions/21 retentions;10346 integrated completions.665 entries,114 accepted layers,six final stages,exact clean patch andown Rafael startup pass. Next175 prose/native/stored reviews preserved;main/full scope/allROMs unchanged;no guide photos.'":
        "    ledger['latest_checkpoint']='Rafael B36-B41 registered andcredited once:175 reviews,76 revisions/99 retentions;10521 integrated completions.666 entries,114 accepted layers,six final stages,exact clean patch andown Rafael startup pass. Four shared Deck reviews preserved;main/full scope/allROMs unchanged;no guide photos.'",
    '40 tutorials credited once:10346 completions,6177 revisions/4169 retentions;full goal active andmain unchanged.':
        '175 Rafael records credited once:10521 completions,6253 revisions/4268 retentions;159 offline-only utterances explicit;full goal active andmain unchanged.',
})
exec(compile(source,__file__+'::same-once-only-ledger-inverses-complete175-bindings-honest-representative-scope','exec'),globals())
