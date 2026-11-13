"""Audit terminal negative pilots; original selectors never produced the target scene."""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_sighting_follow_v1090 import apply_fixture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_pilots_v1096')
ROM=Path('out/all_routes_combined_v1086_candidate.nds')


def main():
    assert not ROOT.exists()
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin')
    results=[]
    for case in ('closeReady28','closeAttack28'):
        run=Path('work/analysis/sighting_gameplay_v1095_'+case)
        plan=read(run/'run_plan.json');cap=Path(plan['capture_folder'])
        report_path=cap/'capture_report.json';report=read(report_path)
        assert report['frames']==5619 and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and report['ROM_sha256']==sha(ROM.read_bytes())
        assert read(run/'terminal_preservation.json')['source_and_disposable_donors_unchanged']
        for key in ('source_donor','disposable_donor'):
            assert sha(Path(plan[key]).read_bytes())==plan['source_donor_sha256']
        snapshots={}
        for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
            path=Path(row['path']);assert path.stat().st_size==row['bytes']==0x400000
            if row['frame'] in snapshots:assert snapshots[row['frame']]==(path,row['sha256'])
            snapshots[row['frame']]=(path,row['sha256'])
        fixtures=report['synthetic_battle_recovery_proximity_fixtures']
        assert len(fixtures)==109 and fixtures[0]['frame']==5410
        audited=[]
        for index,receipt in enumerate(fixtures):
            frame=receipt['frame'];path,digest=snapshots[frame];raw=path.read_bytes()
            assert sha(raw)==digest==receipt['before_RAM_sha256']
            request=({'sighting_context':case} if index==0 else
                {'sighting_context':'followUnseen28','own_point':receipt['own_point']})
            after,proof=apply_fixture(arm,raw,request)
            assert receipt=={**proof,'frame':frame}
            assert sha(after)==receipt['after_RAM_sha256']
            assert len(receipt['owned_bytes'])==(19 if case=='closeAttack28' else 17) if index==0 else len(receipt['owned_bytes'])==16
            audited.append({'frame':frame,'owned_bytes':len(receipt['owned_bytes']),
                'before_RAM_sha256':digest,'after_RAM_sha256':sha(after),'entire4MiB_reconstruction_exact':True})
            if index%25==0:print(case,'independently replayed',index+1,'/',len(fixtures),flush=True)
        path,digest=snapshots[5619];raw=path.read_bytes();assert sha(raw)==digest
        cpu,get=get_machine(arm,raw);root=get(0xCB1A8)
        owner=struct.unpack_from('<I',arm,0x552A0)[0]
        assert cstring(raw,owner+0x2030)==b'Admiral, city ahead!'
        assert get(0x7F244)==get(0x2E58C)==1 and get(0x35320,root+4+132)==2
        assert not cpu.mem_read(root+4+28*132+0x50,1)[0]&4
        assert list(cpu.mem_read(root+0x2080,16))[0:2]==[1,0]
        assert 28 not in list(cpu.mem_read(root+0x2080,16))[0::4]
        observations=read(run/'bounded_follow_observations.json')
        assert observations['records'][-1]['frame']==5519
        assert bytes.fromhex(observations['records'][-1]['template_hex'])==b'Admiral, city ahead!'
        results.append({'case':case,'terminal_report':str(report_path),'terminal_report_sha256':sha(report_path.read_bytes()),
            'terminal_frame':5619,'all109_fixtures_independently_replayed':audited,
            'target_fleet_first_sighting_flag_still_clear_and_not_loaded':True,
            'actual_terminal_selection':'Admiral, city ahead!','no_target_sighting_attack_or_vicinity_UI_credit':True,
            'no_numeric_message_actor_ownership_health_RNG_or_battle_result_injection':True,
            'original_and_disposable_donors_unchanged':True})
    ROOT.mkdir(parents=True)
    save(ROOT/'terminal_negative_pilot_verification.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'terminal_runs':results,'all218_entire4MiB_fixtures_exact':True,
        'no_new_editorial_completion_credit':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Both terminal pilots audited;original city notice,not target sighting. No completion credit.',flush=True)


if __name__=='__main__':main()
