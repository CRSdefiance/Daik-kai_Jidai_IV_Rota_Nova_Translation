"""Terminal ordinary navigation audit; no B23 or Bruges arrival credit."""
import json
import struct
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_lil_lessons_research_v1739 import ROM
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save
from scripts.native_lil_Bruges_location_v1752c import apply_fixture,REQUEST

ROOT=Path('work/analysis/lil_failed_approach_v1757')
RUN=Path('work/analysis/lil_crew_lesson_v1753')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_crew_lesson_v1753_RESEARCH_ONLY')

if __name__=='__main__':
    assert not ROOT.exists()
    plan,terminal,report,trace,journal=map(read,(RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',
        CAP/'observer/commands.json',CAP/'navigation_command_journal.json'))
    digest=sha(ROM.read_bytes())
    assert digest==plan['research_ROM_sha256']==terminal['research_ROM_sha256']==report['ROM_sha256']
    assert terminal['terminal'] and terminal['frame']==report['frames']==32021
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert 'battery_save_preloaded' not in report
    synthetic={k:v for k,v in report.items() if k.startswith('synthetic_') and v}
    assert set(synthetic)=={'synthetic_battle_recovery_proximity_fixtures'}
    assert len(synthetic['synthetic_battle_recovery_proximity_fixtures'])==4
    assert not trace['errors'] and trace['mismatches']==0 and not trace['unreturned_at_capture_end']
    assert trace['all_host_slots_restored_and_core_file_exact']
    assert all(r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] for r in trace['rows'])
    commands=[json.loads(s) for s in (RUN/'navigation.jsonl').read_text(encoding='utf-8-sig').splitlines() if s.strip()]
    assert commands==[r['command'] for r in journal['commands_received']]
    assert commands[-1]=={'stop':True} and journal['last_command_frame']==32021
    schedule=list(read(plan['inputs']))
    for row in journal['commands_received']:
        assert row['validation_passed']
        command=row['command']
        if command.get('buttons') or command.get('touch'):
            event={'start':row['frame']+1,'duration':command['duration']}
            event['buttons']=command.get('buttons',[])
            if command.get('touch'): event['touch']=command['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    photos=[]
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
        assert Image.open(row['path']).size==(256,384)
        photos.append({'frame':row['frame'],'path':row['path'],'sha256':row['PNG_sha256']})
    snapshots={}
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
        data=Path(row['path']).read_bytes()
        assert len(data)==row['bytes']==0x400000 and sha(data)==row['sha256'] and row['read_only_export']
        snapshots[row['path']]=row['sha256']
    assert len(trace['rows'])==trace['callbacks']==262
    assert {(r['source'].get('route'),r['source'].get('block')) for r in trace['rows']}=={(2,22),(2,120)}
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin')
    raw=Path(report['read_only_RAM_snapshot']['path']).read_bytes()
    cpu,get=get_machine(arm,raw);ports=[]
    for index,name in [(2,'Amsterdam'),(3,'Bruges')]:
        city=get(0xCD6B8,index);pointer=struct.unpack('<I',cpu.mem_read(city,4))[0]
        actual_name=bytes(cpu.mem_read(pointer,50)).split(b'\0')[0].decode('cp932')
        assert actual_name==name
        ports.append({'index':index,'actual_name':actual_name,'model':city,'name_pointer':pointer,
                      'original_port_point':list(struct.unpack('<2i',cpu.mem_read(city+12,8)))})
    for fixture in synthetic['synthetic_battle_recovery_proximity_fixtures']:
        before=(CAP/f'frame_{fixture["frame"]:06d}_arm9_ram.bin').read_bytes()
        after,replayed=apply_fixture(arm,before,REQUEST)
        assert sha(before)==fixture['before_RAM_sha256'] and sha(after)==fixture['after_RAM_sha256']
        assert {k:v for k,v in fixture.items() if k!='frame'}==json.loads(json.dumps(replayed))
        assert len(fixture['owned_bytes'])==16
    ROOT.mkdir(parents=True)
    save(ROOT/'terminal_navigation_and_nontrigger_findings.json',{
        'research_ROM':str(ROM),'research_ROM_sha256':digest,'terminal_frame':32021,
        'all262_callbacks_zero_errors_mismatches_host_restored_and_no_pending_command':True,
        'normal_Sea_View_Info_Mode_and_Functions_opened_and_visually_viewed':True,
        'no_native_B23_entry_observed':True,'no_Bruges_arrival_or_whole_route_credit':True,
        'only_four_declared16_byte_coordinate_fixtures_and_ordinary_inputs':True,
        'full_input_schedule_capture_hashes_and4MiB_snapshot_hashes_verified':True,
        'known_port_identity_from_original_data_getter':ports,'captures':photos,'RAM_snapshots':snapshots,
        'finding':'The spawn-point-based target is outside the original known-town center radius;1754 source/native scan proves the corrected center. No game text or runtime defect inferred.',
        'proofs':{str(p):sha(p.read_bytes()) for p in (RUN/'run_plan.json',RUN/'terminal.json',RUN/'navigation.jsonl',
            CAP/'capture_report.json',CAP/'observer/commands.json',CAP/'navigation_command_journal.json')},
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Earlier approach terminal32021 audited:4 coordinate-only fixtures replay exactly,262 callbacks clean,no B23 or docking credit;source center correction retained.')

