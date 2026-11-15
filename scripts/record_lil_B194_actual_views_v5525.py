"""Record four returned sheet views and24 paired full screens across two unforced paths."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B194_actual_views_v5525')
INPUTS = [
    Path('work/analysis/lil_B194_default_actual_review_v5522/paired_all115_samples24_selected_commands9_planes_and_final_state_analysis.json'),
    Path('work/analysis/lil_B194_available_actual_review_v5524/paired_all115_samples30_selected_commands11_planes_and_final_state_analysis.json'),
]

if __name__ == '__main__':
    assert not ROOT.exists()
    versions, evidence = [], {str(Path(__file__)): sha(Path(__file__).read_bytes())}
    all_ids = set()
    for index, path in enumerate(INPUTS):
        d = read(path)
        actual = read(d['actual_proof'])
        expected, selected, exit_frame, outcome = [(9, 24, 5017, 0), (11, 30, 5737, 1)][index]
        assert d['visual_review_pending'] and d['nontext_equal_samples'] == 115 and not d['nontext_difference_samples']
        assert d['fixture_return_frames'] == [exit_frame, exit_frame]
        assert d['exact_timing_difference_counts'] == dict(total=0, speech=0, control_or_end=0)
        assert d['whole_RGB_final9001_equal'] and d['all_sampled_postscene_whole_RGB_equal']
        assert not d['sampled_postscene_whole_RGB_differences_unmasked']
        assert all(d['postscene9001_native_component_equality'].values())
        assert d['postscene9001_whole1A04_actor_models_and_captain2_equal']
        assert d['PRNG_equality'] and d['postscene9001_PRNG_seeds'] == [3723009301, 3723009301]
        assert actual['fresh_actual_unique_speech_panels'] == actual['complete_matching_observations'] == expected
        assert not actual['failures'] and not actual['paired_region_differences']
        assert len(actual['actual_panels']) == expected
        assert [len(v['selected_B22_command_pairs']) for v in actual['versions']] == [selected, selected]
        assert [v['actual_predicate_transitions'][0]['result'] for v in actual['versions']] == [outcome, outcome]
        assert all(v['selected_B22_command_pairs'][-1]['result_words'] == [0, outcome] for v in actual['versions'])
        for p, h in d['evidence'].items():
            assert sha(Path(p).read_bytes()) == h
        views = []
        for sheet in d['actual_consumer_sheets'] + d['paired_full_screen_sheets']:
            assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
            views.append({**sheet, 'viewed_after_image_return': True, 'visual_review_pending': False})
        assert len(d['actual_consumer_sheets']) == 2 and len(d['paired_full_screen_sheets']) == 3
        assert sum(len(s['frames']) * 2 for s in d['paired_full_screen_sheets']) == 12
        for terminal in d['terminal_reports']:
            assert terminal['receipt']['terminal'] and terminal['receipt']['observer_host_slots_restored']
        ids = [r['id'] for r in actual['actual_panels']]
        all_ids.update(ids)
        if index == 0:
            review = ('Viewed all nine selected panels and twelve paired full screens. Sailor and Port Worker portraits/names match source. '
                      'R26 uses two substantial rows and retains the complete immediate invitation. Short complete replies stay intact. '
                      'The prospective Sake/Hangzhou FE clears name and portrait. Julio/resource42/conditional C200 are skipped by the original false predicate. '
                      'Amsterdam return and later tutorial remain intact;later text adds no credit. No glyph,bounds,pagination or premature-wrap finding.')
        else:
            assert d['observed_original_join_actor6_company_and_availability'] == [dict(company=1, availability=1)] * 2
            assert d['disclosed_original_recruitment_setup_is_not_earned_story_progress']
            assert all([r['original_source_offset'] for r in v['source_C200']] == [494, 534] for v in actual['versions'])
            review = ('Viewed all eleven panels and twelve paired full screens after the disclosed original B165 actor6 recruitment initializer. '
                      'Julio Erneco portrait and complete name,including initial J,match source. R46 retains the stammer,fabled-drink belief,Admiral Lil address and complete question in three readable rows. '
                      'R49 retains restless personal purchase intention and final right-away phrase in three rows. First rows use the verified width;ordinary phrase wrapping is justified. '
                      'The FE clears Julio name/portrait;both source C200 sites,resource42 command and normal return execute. '
                      'Opaque runtime UI fields3/4 remain recorded rather than assumed zero or assigned invented meaning. '
                      'No clipping,missing glyph,blank page,portrait/name or premature-wrap finding. Original resource command execution does not establish audible output.')
        versions.append(dict(label='default' if index == 0 else 'original-recruitment-setup',
            visual_analysis=str(path), visual_analysis_sha256=sha(path.read_bytes()), actual_proof=d['actual_proof'],
            actual_proof_sha256=sha(Path(d['actual_proof']).read_bytes()), viewed_sheets=views,
            actual_display_IDs=ids, complete_native_holds=sum(len(r['holds']) for r in actual['actual_panels']),
            sampled_nontext_pairs=115, actual_selected_fixture_commands=selected,
            stored_fixture_commands=30 if index == 0 else 31, predicate_result=outcome,
            return_frames=d['fixture_return_frames'], timing_differences=d['exact_timing_difference_counts'],
            sampled_postscene_and_final_RGB_equal=True, all_five_native_groups_and_whole1A04_actor_and_captain2_equal=True,
            final_PRNG_seeds=d['postscene9001_PRNG_seeds'], review=review,
            original_event194_not_naturally_selected=True, no_earned_recruitment_or_fashion_earlier_location_full_route_or_hardware_claim=True))
        evidence[str(path)] = sha(path.read_bytes())
        evidence[d['actual_proof']] = sha(Path(d['actual_proof']).read_bytes())
        evidence.update({s['path']: s['sha256'] for s in views})
    doc = read('translations/lil_B194_editorial_manuscript_v3.json')
    assert all_ids == {r['id'] for r in doc['records']} and len(all_ids) == 11
    ROOT.mkdir(parents=True)
    save(ROOT / 'both_unforced_paths_all11_panels24_fullscreens_and_normal_returns_viewed.json', dict(
        versions=versions, evidence=evidence, actual_sampled_display_IDs=[r['id'] for r in doc['records']],
        offline_only_display_IDs=[], unique_actual_display_objects=11, actual_panel_observations_across_setups=20,
        all_four_actual_consumer_sheets_and_six_paired_fullscreen_sheets_viewed=True,
        total_paired_fullscreen_views=24, sampled_nontext_pairs=230,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
        no_open_translation_specific_display_or_control_finding=True,
        all_source_commands_FI_predicate_relatives_resource_two_C200_and_end_preserved=True,
        default_name_Lil_actual_FI_display_verified_all_custom_name_lengths_not_claimed=True,
        no_PRNG_causal_future_world_full_RAM_or_hardware_equivalence_claim=True,
        original_recruitment_setup_disclosed_not_earned_story_progress=True,
        all_content_jobs_terminal_and_reaped=True, reaped_tool_sessions=[24892, 24384, 26178, 54812],
        actual_new_cold_boot_runs=4, total_frames=36004, visual_review_pending=False,
        registered_integration_and_current_startup_pending=True, new_editorial_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print(dict(unique_actual_objects=11, panel_observations=20, full_screen_views=24, paired_nontext_samples=230,
               complete_native_holds=[v['complete_native_holds'] for v in versions], cold_boots=4, frames=36004, credit=0))
