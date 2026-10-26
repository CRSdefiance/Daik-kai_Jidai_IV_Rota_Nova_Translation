"""Prepare B171 positive/negative contracts and full cumulative registration."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B171_registration_tools_v4352')
if __name__=='__main__':
    assert not ROOT.exists()
    old=Path('scripts/register_lil_B170_v4302b.py').read_text(encoding='utf-8')
    a=old.index('    profile.update(status=');b=old.index("    registry['profiles'][PROFILE]",a)
    profile='''    profile.update(status='experimental', lil_B171_editorial=owned.CONFIG,
        description='Full V4303 cumulative stack plus37 complete B171 Sanghyeon visitation/morning reviews:24 revisions/13 retentions,37 progressive speeches,45 commands,eight leaves,four presentations,one resource,C200 and both ends;no source A000,pause,predicate or relative sites. Two complete-content boots cover all37 panels,original dream/morning transitions,first end and normal return;two focused repeats bind persistent state and later PRNG/timing scope. No natural eligibility,earned flag,full-route or hardware claim.', note='B171 source/native/reference/representative approved;registered build,exact patch and fresh startup pending.')
'''
    changes={
        old[a:b]:profile,
        'B170':'B171','lil_B170':'lil_B171',
        'registration_v4302b':'registration_v4352','all-routes-unified-v4303':'all-routes-unified-v4353',
        'all_routes_combined_v4251':'all_routes_combined_v4303','editorial_manuscript_v6':'editorial_manuscript_v5',
        'reference_checkpoint_v4299':'reference_checkpoint_v4347','all-routes-unified-v4251':'all-routes-unified-v4303',
        'lil_B170_layout_v2':'lil_B171_layout_v1','reference_approval_v4298':'reference_approval_v4346',
        'loader_v4285':'loader_v4336',
        "len(proof['changed_records']) == 33":"len(proof['changed_records']) == 37",
        'transition_review_v4297/all6_sheets_figure_pause_effect_C200_and_paired_return_review':'transition_review_v4345/all7_sheets_dream_morning_C200_and_paired_return_review',
        "visual['later_diagnostic_full_screen_views']":"visual['later_sailing_views']",
        "('missing_pause', 'reference_map', lambda value: value['blocks'][0]['original2000_pause_and_resume_maps'].pop())":"('invented_pause', 'reference_map', lambda value: value['blocks'][0]['original2000_pause_and_resume_maps'].append({}))",
        "('wrong_pause_resume', 'reference_map', lambda value: value['blocks'][0]['original2000_pause_and_resume_maps'][0].update(target_resume=36))":"('invented_A000', 'reference_map', lambda value: value['blocks'][0]['mapped_native_commands'].append(dict(word=0xA000)))",
        "('wrong_A000_raw_word', 'reference_map', lambda value: value.update(source_A000_raw_hex_words=['0029', '0001']))":"('wrong_4500_extent', 'reference_map', lambda value: value['blocks'][0]['mapped_native_commands'][1].update(old_native_extent=4))",
        'Yifa_selector_as_text':'Sanghyeon_selector_as_text',
        'source_resource20_boundary_cases_reused_only_by_exact_words_and_runtime':'source_resource10_boundary_cases_reused_only_by_exact_word_and_runtime',
        'all12_source_current_target_nonrelative_nonspeech_leaves':'all8_source_current_target_nonrelative_nonspeech_leaves',
        'native_four_consumer_cases':'native_six_consumer_cases',
        'first_end1852_actual_second1856_native_decoder_only':'first_end2112_actual_second2116_native_decoder_only',
        'source_A000_packed_semantics_or_earned_recruitment_not_inferred':'no_natural_event_eligibility_earned_flags_full_route_or_hardware_claim',
        'later67_SeaView_differences_preserved_with_explicit_inference_and_state_scope':'later59_sailing_differences_preserved_with_explicit_inference_and_state_scope',
        'paired_post_B170_town11290_whole1A04_actor_models_and_captain2_equal':'paired_town11770_whole1A04_actor_models_and_captain2_equal',
        'cross_language_speech_timing_differences':'cross_language_command_timing_differences',
        "for macro in ['FI', 'FO']:":"for macro in ['FI']:",
        'actual_all33_pause_resources_A000_C200_and_first_end':'actual_all37_dream_morning_presentations_resource_C200_and_first_end',
        "if label == 'wrong_actual_effect':":"if label == 'wrong_actual_presentation':",
        "actual['versions'][0]['actual_source_A000_hex1019_2001']['result_words'] = [3, 1]":"actual['versions'][0]['actual_presentation_commands'][0]['word'] = 0x6001",
        "actual['versions'][0]['source_first_end_offset'] = 1856":"actual['versions'][0]['source_first_end_offset'] = 2116",
        "elif label == 'wrong_actual_pause':":"elif label == 'wrong_actual_resource':",
        "actual['versions'][0]['actual_pause_and_resume'][0]['returned'] = 3333":"actual['versions'][0]['actual_resources'][0]['word'] = 0x6326",
        "['wrong_actual_effect', 'wrong_actual_end', 'wrong_actual_C200', 'wrong_actual_pause', 'missing_actual_version']":"['wrong_actual_presentation', 'wrong_actual_end', 'wrong_actual_C200', 'wrong_actual_resource', 'missing_actual_version']",
        'V4251':'V4303','after_full_V4251':'after_full_V4303',
        'build_integrated_release_v4302b.tmp':'build_integrated_release_v4352.tmp',
        'expected_manifest_batches=546':'expected_manifest_batches=547',
        'positive_records=33':'positive_records=37','expected_batches=546':'expected_batches=547',
        "        ('wrong_command', 'reference_map', lambda value: value['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),":"        ('wrong_command', 'reference_map', lambda value: value['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),\n        ('wrong_command_word', 'reference_map', lambda value: value['blocks'][0]['mapped_native_commands'][0].update(word=0x6001)),",
        "        'work/analysis/lil_B170_loader_v4285/whole_SC2_and_B170_initial_entry_proof.json'}":"        'work/analysis/lil_B171_loader_v4336/whole_SC2_and_B171_initial_entry_proof.json',\n        'work/analysis/lil_B171_timing_count_amendment_v4349/amendment_receipt.json',\n        'work/analysis/editorial_handoff_verification_v4350/verified_handoff.json'}",
    }
    tool=derive('scripts/register_lil_B170_v4302b.py','scripts/register_lil_B171_v4352.py',changes)
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,expected_manifest_batches=547,accepted_layers=114,
        no_registration_or_ROM_created_yet=True,full_goal_complete=False))
    print('Prepared B171 registration and source/proof negatives after full V4303;547 cumulative manuscript batches expected.')
