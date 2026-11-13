"""Approve ten source-owned labels after complete native and representative scene review."""
from copy import deepcopy
from pathlib import Path
from PIL import Image
from dk4tool.patch.square_shopkeeper_label_data_v1 import transform
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/square_shopkeeper_approval_v7025')
OLD=Path('translations/square_shopkeeper_label_manuscript_v3.json')
NEW=Path('translations/square_shopkeeper_label_manuscript_v4.json')
NAMES=Path('work/analysis/square_shopkeeper_names_v7021/all_name_field_voice_dynamic_macro_and_complete_native_label_consumers.json')
ACTUAL=Path('work/analysis/square_shopkeeper_actual_v7024b/four_full_scenes_complete_native_bodies_names_commands_and_measured_differences.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists();doc,native,actual=map(read,[OLD,NAMES,ACTUAL])
    assert [r['actor_ID'] for r in doc['records']]==list(range(82,92))
    assert native['all414_parent_and414_target_getters_pass'] and native['all621_parent_and621_target_field_consumers_pass'] and native['macro_alignment_cases']==176
    assert native['only_twenty_name_getters_ten_catalogue_names_ten_primary_fields_change'] and native['all_other197_actors_all207_voices_and_dynamic_CF_D0_assignments_preserved']
    assert actual['target_changed_nameplate_observations']==9 and actual['target_complete_page_observations']==32 and actual['target_speech_observations']==30
    assert actual['all_jobs_terminal_and_reaped'] and actual['no_stale_old_label_ink_wrap_or_nameplate_pagination']
    assert actual['all_native_body_glyphs_black_gray_and_nameplate_first_internal_final_glyphs_and_blank_guards_pass']
    assert [v['actual_complete_body_holds'] for v in actual['versions']]==[67,67,59,59]
    assert [v['actual_complete_name_holds'] for v in actual['versions']]==[63,63,59,59]
    assert [c['normal_exit_frames'] for c in actual['comparisons']]==[[6937,6936],[6693,6693]]
    assert [len(c['command_differences']) for c in actual['comparisons']]==[18,0]
    assert [len(c['RGB_differences']) for c in actual['comparisons']]==[98,19]
    assert [sum(not d['all_differences_within_nameplate_strip'] for d in c['RGB_differences']) for c in actual['comparisons']]==[82,0]
    viewed=[];panes=[]
    for s in actual['review_sheets']:
        p=Path(s['path']);assert sha(p.read_bytes())==s['sha256'];im=Image.open(p).convert('RGB');assert im.size==(768,820)
        viewed.append(dict(path=str(p),sha256=s['sha256']))
        for i,c in enumerate(s['panes']):
            full=Path(c['capture']);assert sha(full.read_bytes())==c['sha256']
            x,y=i%3*256,i//3*410;assert im.crop((x,y+24,x+256,y+408)).tobytes()==Image.open(full).convert('RGB').tobytes()
            panes.append(dict(id=c['id'],page=c['page'],capture=str(full),sha256=c['sha256'],whole_pane_pixel_equal=True))
    assert len(viewed)==6 and len(panes)==32
    for p in [Path(native['review_sheet']),Path(native['native_name_plane']['preview']),
        Path('E:/Rota Nova translations/Generated/work/emulation_v193/square_shopkeeper_v7019/frame_004000_cold_boot.png'),
        Path('E:/Rota Nova translations/Generated/work/emulation_v193/square_shopkeeper_static_target_v7023/frame_003310_cold_boot.png'),
        Path('E:/Rota Nova translations/Generated/work/emulation_v193/square_shopkeeper_staged_target_v7023/frame_003070_cold_boot.png'),
        Path('E:/Rota Nova translations/Generated/work/emulation_v193/square_shopkeeper_static_parent_v7023/frame_002950_cold_boot.png')]:viewed.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    ROOT.mkdir(parents=True);view=ROOT/'all_six_scene_sheets32_exact_panes_and_two_actual_Shopkeeper_headers_viewed.json'
    save(view,dict(viewed_images=viewed,all_six_target_exchange_sheets_individually_returned_and_viewed=True,all32_whole_frame_panes_pixel_equal=panes,
        both_static82_and_staged85_actual_complete_nameplates_viewed=True,native_complete_label_plane_and_unchanged_opening_viewed=True,
        one_row_failed_audit_origin_and_source_locked_correction_preserved=True,all_measured_timing_RNG_UI_RGB_differences_preserved=True,
        no_new_prose_approval_full_catalogue_UI_or_every_conditional_visit_claim=True,visual_review_pending=False,new_review_credit=0,full_goal_complete=False))
    for row in doc['records']:
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        row['historical_formatting_and_shared_consumer_validation_pending']=row['formatting_and_shared_consumer_validation_pending']
        row['formatting_and_shared_consumer_validation_pending']=False;row['review']['formatting']=True
        row['formatting_reason']='Both original progressive/full getters and primary/secondary/additional field consumers retain their pointers and source-owned memory behavior. All ten identical clean occupational labels yield complete60px Shopkeeper in the original style11 row. All207 voices,dynamic CF/D0 assignments,176 macro alignments and every other197 actor output are preserved. Representative complete static82/staged85 exchanges show nine changed headers,32 complete native body page observations and complete leading/internal/final name glyphs without stale old ink. Catalogue UI and individual conditional visits remain unclaimed;all measured timing/RNG/RGB differences stay open. Registered integration and exact clean-input patch remain pending.'
        row['target_reference']={**deepcopy(row['current_reference']),'terminated_hex':b'Shopkeeper\0'.hex()}
        row['new_name_completion_credit']=0
    doc['historical_all_ten_four_prose_gates_true_formatting_false']=doc.pop('all_ten_four_prose_gates_true_formatting_false')
    doc['historical_complete_source_shared_dynamic_pair_macro_native_target_actual_and_registered_release_pending']=doc.pop('complete_source_shared_dynamic_pair_macro_native_target_actual_and_registered_release_pending')
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),
        native_names=str(NAMES),native_names_sha256=sha(NAMES.read_bytes()),actual_scenes=str(ACTUAL),actual_scenes_sha256=sha(ACTUAL.read_bytes()),
        visual_review=str(view),visual_review_sha256=sha(view.read_bytes()),all_five_per_name_review_gates_approved_registered_release_pending=True,
        all207_name_review_scope_remains_open=True,all_other_names_prose_and_prior_completed_label_history_preserved=True,
        no_duplicate_dialogue_or_name_completion_credit=True,mechanical_data_plan_historical_pending_annotations_do_not_replace_native_approval=True,
        status='ten-source-owned-labels-native-and-representative-display-approved-registered-release-pending',full_catalogue_UI_unvisited=True,
        all_measured_later_differences_preserved_for_older_record_technical_reaudit=True,registered_integration_pending=True,full_goal_complete=False)
    source=NdsImage.open(doc['current_ROM']);clean=NdsImage.open('work/clean.nds')
    arm,plan=transform(source.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin'),doc['records'])
    assert plan==doc['data_plan'] and sha(arm)==doc['target_ARM9_sha256'];save(NEW,doc)
    evidence={str(p):sha(p.read_bytes()) for p in [OLD,NEW,NAMES,ACTUAL,view,Path(__file__),Path('work/analysis/square_shopkeeper_origin_v7024b/exact_native_origin_and_source_locked_successor.json')]}
    save(ROOT/'ten_label_approval.json',dict(manuscript=str(NEW),manuscript_sha256=sha(NEW.read_bytes()),source_ARM9_sha256=doc['current_ARM9_sha256'],target_ARM9_sha256=doc['target_ARM9_sha256'],
        source_owned_data_plan=plan,all_ten_source_context_localization_naturalness_and_formatting_gates_true=True,
        all414_name621_field207_voice_consumers176_macro_alignments_and_complete_native_label_pass=True,
        two_storage_behaviors_actual_nine_changed_headers_and32_native_pages_viewed=True,
        all621_pointers_all_other197_names_voices_dynamic_roles_and_unread_old_tails_preserved=True,
        full_catalogue_UI_every_conditional_nameplate_and_full207_editorial_approval_not_claimed=True,
        B189_retrospective_line_breaks_and_all_measured_later_differences_remain_separate_open_leads=True,
        all_earlier_ROMs_translations_failures_proofs_and_history_preserved=True,visual_review_pending=False,
        evidence=evidence,new_name_or_dialogue_completion_credit=0,full_goal_complete=False))
    print('Ten Shopkeeper labels approved through all five gates. Nine actual changed headers and32 complete native pages viewed;registered layer/patch pending.',flush=True)
