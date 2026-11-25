"""Record direct inspection of the fresh registered-ROM Rafael startup sheet."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_startup_view_v8126')
START=Path('work/analysis/Rafael_B49_context_binding_v8125/own_Rafael_startup_andstrict_captain0_context.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(START)
    assert d['actual_frames']==4001 and d['whole_RGB_pair_count']==6 and d['actual_original_captain_ID']==0
    assert d['all_whole_RGB_actor_andcaptain_controls_equal'] and d['all_strict2b6_COMMON_directory_and123264_payload_guards_pass']
    assert sha(Path(d['review_sheet']['path']).read_bytes())==d['review_sheet']['sha256']
    ROOT.mkdir(parents=True);save(ROOT/'own_Rafael_startup_sheet_viewed.json',dict(
        candidate=d['candidate'],candidate_sha256=d['candidate_sha256'],startup_proof=str(START),startup_proof_sha256=sha(START.read_bytes()),
        viewed=True,viewed_sheet=d['review_sheet'],actual_frames=4001,actual_captain=0,strict_own_ROM_input=d['current_native_input'],
        findings='Captain selection/default Rafael Castor and Castor Co. fields complete; opening portraits, Claudio Manaus header and complete ordinary dialogue visible. Six full RGB/whole-actor/captain controls match V8066.',
        no_new_B49_activation_fullroute_hardware_orincidental_prose_credit=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Fresh own-V8122 Rafael startup sheet directly viewed; no additional prose credit.')
