"""Record direct inspection ofthe affected registered-ROM Lil startup sheet."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_startup_view_v7861')
START=Path('work/analysis/retrospective_B218_startup_binding_v7860/own_Lil_startup_andstrict_current_context.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(START)
    assert d['actual_frames']==4001 and d['whole_RGB_pair_count']==6 and d['actual_captain']==2
    assert d['all_prior_whole_RGB_actor_andcaptain_controls_equal'] and d['all_strict2b6_COMMON_directory_and123264_payload_guards_pass']
    assert sha(Path(d['review_sheet']['path']).read_bytes())==d['review_sheet']['sha256']
    ROOT.mkdir(parents=True);save(ROOT/'own_registered_Lil_startup_sheet_viewed.json',dict(
        candidate=d['candidate'],candidate_sha256=d['candidate_sha256'],startup_proof=str(START),startup_proof_sha256=sha(START.read_bytes()),
        viewed=True,viewed_sheet=d['review_sheet'],all6_whole_RGB_actor_andcaptain_controls_equal=True,
        strict_own_ROM_input=d['strict_current_native_input'],actual_frames=4001,actual_captain=2,
        only_affected_Lil_startup_repeated_all_unaffected_route_evidence_retained=True,
        no_new_B218_activation_fullroute_hardware_orincidental_prose_credit=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Own registered V7857 Lil startup sheet viewed;6whole-frame pairs/actors/captain2/strict input pass.No new editorial credit.')
