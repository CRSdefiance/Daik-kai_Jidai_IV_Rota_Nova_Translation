"""Record the viewed complete source exchange and approve two contextual name retentions."""
from copy import deepcopy
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B222_source_view_v7044b')
ACTUAL=Path('work/analysis/lil_B222_source_actual_v7044/all16_Japanese_speeches27_commands_complete_masks_headers_and_normal_return.json')
NAMES=Path('work/analysis/lil_B222_name_planes_v7041/two_actors_four_getters_six_name_component_planes48_alignments.json')
OLD=Path('translations/lil_B222_speaker_name_review_v1.json')
NEW=Path('translations/lil_B222_speaker_name_review_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists();a,n,doc=map(read,[ACTUAL,NAMES,OLD])
    assert a['actual_unique_source_speeches']==16 and a['actual_complete_source_body_holds']==a['actual_complete_name_holds']==63
    assert a['incomplete_sampled_body_holds']==0 and a['all27_stored_commands_executed'] and a['normal_terminal_result']==[0,0]
    assert a['all_jobs_terminal_and_reaped'] and n['name_literal_alignment_count']==48 and n['complete_name_component_plane_count']==6
    viewed=[];panes=[]
    for s in a['review_sheets']:
        p=Path(s['path']);assert sha(p.read_bytes())==s['sha256'];viewed.append(dict(path=str(p),sha256=s['sha256']))
        if 'panes' not in s:continue
        im=Image.open(p).convert('RGB');assert im.size==(768,820)
        for i,photo in enumerate(s['panes']):
            path=Path(photo['path']);assert sha(path.read_bytes())==photo['PNG_sha256'];x,y=i%3*256,i//3*410
            assert im.crop((x,y+24,x+256,y+408)).tobytes()==Image.open(path).convert('RGB').tobytes()
            panes.append(dict(frame=photo['frame'],capture=str(path),sha256=photo['PNG_sha256'],whole_pane_pixel_equal=True))
    assert len(viewed)==4 and len(panes)==16
    assert sha(Path(n['review_sheet']).read_bytes())==n['review_sheet_sha256'];viewed.append(dict(path=n['review_sheet'],sha256=n['review_sheet_sha256']))
    ROOT.mkdir(parents=True);view=ROOT/'all16_source_speeches_four_source_sheets_and_six_name_planes_viewed.json'
    save(view,dict(actual_source=str(ACTUAL),actual_source_sha256=sha(ACTUAL.read_bytes()),native_names=str(NAMES),native_names_sha256=sha(NAMES.read_bytes()),
        viewed_images=viewed,all_four_source_sheets_and_six_name_plane_sheet_individually_returned_and_viewed=True,all16_whole_frame_source_panes_pixel_equal=panes,
        silent_opening_hero_story_private_parentheses_armor_echo_and_normal_return_read_as_complete_exchange=True,
        actual_source_body_black_and_current_name_masks_complete_Japanese_gray_untested=True,
        first_and_final_source_frames_viewed_normal_Amsterdam_then_Sea_View_Sailor_Food_has_run_out=True,
        original_Japan_event222_requires89_unforced_and_not_naturally_selected=True,not_full_effects_full_route_or_hardware_verification=True,
        English_body_native_and_actual_pass_still_pending=True,visual_review_pending=False,new_review_credit=0,full_goal_complete=False))
    revised=deepcopy(doc);revised.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),actual_source_proof=str(ACTUAL),actual_source_proof_sha256=sha(ACTUAL.read_bytes()),
        source_and_name_visual_review=str(view),source_and_name_visual_review_sha256=sha(view.read_bytes()),
        all_two_contextual_name_retentions_five_gates_true_no_asset_change=True,actual_English_headers_will_be_rechecked_with_new_body=True)
    for row in revised['records']:
        assert all(row['review'][k] for k in ['source','context','localization','naturalness']) and not row['review']['formatting']
        row['historical_pre_source_view_formatting_reason']=row['formatting_reason'];row['review']['formatting']=True
        row['formatting_reason']='Four original progressive/full getters,six complete component/returned style11 planes and48 literal alignments pass under exact2b6 guards. All sixteen actual clean-source speeches have complete original current headers;63 independent name masks include both names,all first/internal/final glyphs and blank guards. Full catalogue UI is unvisited;component planes are not its field-layout approval. English-body captures remain independently pending;no name asset,global207 approval or duplicate credit is added.'
    save(NEW,revised);print('Source exchange and all six name planes viewed;two contextual name retentions approved.No name asset or duplicate credit;English body pending.',flush=True)
