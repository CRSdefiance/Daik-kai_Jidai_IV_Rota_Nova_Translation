"""Complete terminal20700 location-only replay;optional relaxation remains open."""
from pathlib import Path
from scripts import native_hot_spring_notice_location_v1640 as fixture
from scripts.audit_fatigue_location_runs_v1607 import audit_run
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/hot_spring_notice_first_run_v1643a')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_notice_live_v1641_1637')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=read(CAP/'navigation_command_journal.json')['commands_received'];frames=[r['frame'] for r in rows if 'battle_fixture' in r['command']]
    proof=audit_run('hot_spring_notice_live_v1641',1637,fixture,20700,frames)
    ROOT.mkdir(parents=True);save(ROOT/'terminal_location_only_replay_preservation.json',{'preservation_audit':proof,
        'normal_Sea_View20700_actually_viewed':True,'all100_old_prefix_captures_RGB_exact_proof':'work/analysis/hot_spring_notice_prefix_v1641d/all_original_prefix_frames_RGB_exact.json',
        'optional_relaxation_and_notice310_still_unobserved':True,'no_completion_credit':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('First V1637 replay terminal20700:all48-byte fixtures,otherRAM,inputs,snapshots/PNGs and unchanged saves audited. Optional branch unobserved;no completion credit.')
