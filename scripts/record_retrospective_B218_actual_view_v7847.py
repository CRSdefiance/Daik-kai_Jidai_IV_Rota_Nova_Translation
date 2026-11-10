"""Record direct inspection of all26 actual panes/eight sheets without implying full-route coverage."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_actual_view_v7847')
ACTUAL=Path('work/analysis/retrospective_B218_actual_v7846/two_English_scenes_complete_masks_commands_andall_measured_late_limits.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(ACTUAL)
    assert d['both_jobs_terminal_andreaped'] and d['total_actual_pages']==26
    assert d['total_actual_complete_body_andheader_holds']==102 and d['total_incomplete_sampled_holds']==0
    assert d['all24_original_command_results_andUI_equal'] and d['duration_difference_rows']==0
    assert d['later_RGB_differences']==0 and len(d['later_sampled_whole_frame_comparisons'])==167
    assert all(d['five_native_component_equality'].values()) and d['final_whole_actor_equal']
    assert d['final_PRNG_seeds']==[3000421369,3000421369]
    checks=[];images=[]
    for g in d['groups']:
        assert g['exit_frame']==5975 and g['normal_terminal_result']==[0,0] and not g['unreturned_at_capture_end']
        images.extend([*g['review_sheets'],g['transition_sheet']])
        for i,p in enumerate(g['panels']):
            selected=p['selected_capture'];full=Image.open(selected['capture']).convert('RGB')
            assert sha(Path(selected['capture']).read_bytes())==selected['sha256']
            sheet=Image.open(g['review_sheets'][i//6]['path']).convert('RGB');slot=i%6
            tile=full.crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST)
            x,y=slot%3*520+4,slot//3*416+24
            assert sheet.crop((x,y,x+512,y+384)).tobytes()==tile.tobytes()
            checks.append(dict(case=g['case'],id=p['id'],capture=selected['capture'],capture_sha256=selected['sha256'],
                entire_body_andheader_overview_pane_exact=True))
    assert len(images)==8 and len(checks)==26
    for im in images:assert sha(Path(im['path']).read_bytes())==im['sha256']
    assert all(set(c['differing_fields'])<=set(['decoded_length','fixture_offset']) for c in d['command_comparisons'])
    ROOT.mkdir(parents=True);save(ROOT/'26_actual_panes_eight_sheets_andall_measured_limits_viewed.json',dict(
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),viewed_images=images,
        all_eight_sheets_directly_viewed=True,all26_overview_panes_exact=checks,
        all13_previous_andproposed_body_pages_andLil_Ian_headers_viewed=True,
        target_private_aside_readable_as_two_complete_sentences_without_changed_words=True,
        complete_characters_bounds_pagination_andnormal_transitions_observed=True,
        all_measured_offset_anddecoded_length_differences_retained=True,
        eight_command_difference_rows_are_only_offsets_orlengths=True,
        both_exits5975_zero_timing_results_UI_lateRGB167_components_actors_andseed_differences=True,
        no_fullRAM_everyframe_future_causal_fullmechanics_natural_event_orroute_claim=True,
        source_Japanese_not_recaptured_historical_proof_preserved=True,
        full_catalogue_UI_unvisited=True,incidental_following_text_no_editorial_credit=True,
        frozen_policy_atomic_registered_release_andcompletion_metadata_pending=True,
        new_credit=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('All26 actual panes/eight sheets viewed;102complete body/header holds. Only8 offset/length rows differ;all measured timing/RNG/components/lateRGB match.Policy/release pending.')
