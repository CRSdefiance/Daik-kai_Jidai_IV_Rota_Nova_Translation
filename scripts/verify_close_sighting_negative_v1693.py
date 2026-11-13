"""Audit the terminal close-range pilot without awarding sighting UI coverage."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_close_sighting_v1689 import ROM, apply_fixture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/close_sighting_negative_v1693')
RUN=Path('work/analysis/close_sighting_v1690_closeReady8')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/close_sighting_v1690_1676_closeReady8')


if __name__=='__main__':
    assert not ROOT.exists()
    report_path=CAP/'capture_report.json';report=read(report_path);plan=read(RUN/'run_plan.json')
    assert report['frames']==5512 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['ROM_sha256']==plan['candidate_sha256']==sha(ROM.read_bytes())
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');raw={};captures=[]
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        data=Path(row['path']).read_bytes();assert len(data)==row['bytes']==0x400000 and sha(data)==row['sha256']
        if row['frame'] in raw:assert raw[row['frame']]==data
        raw[row['frame']]=data
    fixtures=report['synthetic_battle_recovery_proximity_fixtures']
    assert [r['frame'] for r in fixtures]==[5100,5310,5311]
    replay=[]
    for receipt in fixtures:
        frame=receipt['frame'];after,proof=apply_fixture(arm,raw[frame],{'sighting_context':'closeReady8'})
        assert receipt=={**proof,'frame':frame} and sha(after)==receipt['after_RAM_sha256'] and len(receipt['owned_bytes'])==17
        replay.append({'frame':frame,'all4MiB_exact':True,'owned_bytes':17,'after_RAM_sha256':sha(after)})
    states=[];owner=struct.unpack_from('<I',arm,0x552A0)[0]
    for frame in (5100,5110,5210,5310,5311,5312,5412,5512):
        cpu,get=get_machine(arm,raw[frame]);root=get(0xCB1A8);enemy=root+4+8*132
        assert not cpu.mem_read(enemy+0x50,1)[0]&4
        template=cstring(raw[frame],owner+0x2030)
        if frame in (5312,5412):assert template==b'Dock at %s?'
        states.append({'frame':frame,'own_point':list(struct.unpack('<2i',cpu.mem_read(root+4+132+0x34,8))),
            'enemy8_point':list(struct.unpack('<2i',cpu.mem_read(enemy+0x34,8))),
            'enemy8_unseen':True,'loaded_groups':list(cpu.mem_read(root+0x2080,16)),
            'template_hex':template.hex(),'source_navigation_state':list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))),
            'RAM_sha256':sha(raw[frame])})
        image=CAP/f'frame_{frame:06d}_navigation.png'
        captures.append({'frame':frame,'path':str(image),'sha256':sha(image.read_bytes())})
    assert read(RUN/'terminal_preservation.json')['source_and_disposable_donors_unchanged']
    for key in ('source_donor','disposable_donor'):
        assert sha(Path(plan[key]).read_bytes())==plan['source_donor_sha256']
    ROOT.mkdir(parents=True)
    save(ROOT/'terminal_negative_close_range_proof.json',{'candidate':str(ROM),'candidate_sha256':report['ROM_sha256'],
        'terminal_report':str(report_path),'terminal_report_sha256':sha(report_path.read_bytes()),'terminal_frame':5512,
        'fixture_replay':replay,'states':states,'captures':captures,'all_snapshots_and_source_disposable_saves_exact':True,
        'actual_observation':'Original Dock at Syracuse? prompt;normal B No returns to visually inspected Sea View. No enemy sighting selected.',
        'preflight_erratum':'36C70 null for an unloaded enemy is not evidence that its world fleet is inactive;original fleet vtable+10 eligibility is1 for8 and28. V1691 aborted on the overly strong mobile assertion;V1691b preserves the actual observation.',
        'next_test_requirement':'Use an open-water original fleet context;cached-coordinate placement near Syracuse selected the port prompt. Do not reset seen flags or force sighting/message results.',
        'no_close_range_Armed_Latina_or_editorial_completion_credit':True,'full_goal_complete':False,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Terminal5512 audited:3 exact17-byte fixtures,all RAM/saves,original Syracuse prompt and normal No return. No target or completion credit.')
