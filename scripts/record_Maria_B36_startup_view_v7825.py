"""Record direct visual inspection ofthe registered Maria startup sheet."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B36_startup_view_v7825')
START=Path('work/analysis/maria_B36_startup_verification_v7824/own_Maria_startup_exact_V7779_andstrict_current_input.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(START);sheet=d['review_sheet']
    assert d['all_current_requested_andfinal_frames_equal_V7779'] and d['actual_original_captain_ID']==3
    assert d['strict2b6_COMMON_directory_andall123264_payload_bytes_verified'] and d['existing_system_only_unlock_earned_false']
    assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    ROOT.mkdir(parents=True);save(ROOT/'own_Maria_startup_sheet_viewed.json',dict(candidate=d['candidate'],candidate_sha256=d['candidate_sha256'],
        startup_proof=str(START),startup_proof_sha256=sha(START.read_bytes()),viewed=True,viewed_sheet=sheet,
        whole_RGB_frame_pairs=d['whole_RGB_frame_pairs'],actual_frames=d['actual_frames'],actual_captain=3,
        full_actor_controls_match_V7779=True,strict_own_registered_input=d['strict_current_native_input'],
        existing_system_only_unlock_earned_false=True,unaffected_routes_not_replayed=True,
        incidental_opening_text_not_editorial_credit=True,not_natural_optional_activation_original_location_fullroute_orhardware=True,
        new_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Own registered Maria startup sheet viewed;whole-frame/actor/captain controls andstrict new-ROM input pass.No incidental prose credit.')
