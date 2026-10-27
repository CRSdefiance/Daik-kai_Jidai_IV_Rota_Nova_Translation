"""Audit the fixture-free original Search failure and naturally displayed fatigue+3."""
import json,struct
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.inspection_status_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_fatigue_status_fonts_v1590 import pipeline
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.probe_inspection_status_fonts_v1574 import literal_independent
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
from scripts.verify_dialogue_palette_v628 import PALETTE,resident,captured_rgb
ROOT=Path('work/analysis/fatigue_search_control_verified_v1587g')
RUN=Path('work/analysis/fatigue_search_pilot_v1587b')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/fatigue_search_pilot_v1587b_1578')
ROM=Path('out/all_routes_combined_v1578_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists()
    report,plan,terminal=[read(p) for p in [CAP/'capture_report.json',RUN/'run_plan.json',RUN/'terminal_preservation.json']]
    digest=sha(ROM.read_bytes());assert report['ROM_sha256']==plan['candidate_sha256']==digest
    assert report['frames']==5900 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['hardware_device_verification'] and not report['goal_complete'] and not any(v for k,v in report.items() if k.startswith('synthetic_'))
    assert terminal['source_and_disposable_donors_unchanged']
    assert sha(Path(plan['source_donor']).read_bytes())==sha(Path(plan['disposable_donor']).read_bytes())==terminal['source_donor_sha256']
    assert sha((RUN/'navigation.jsonl').read_bytes())==terminal['navigation_sha256']
    assert sha(Path('scripts/headless_desmume_v193.py').read_bytes())==plan['harness_sha256']
    snapshots={}
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        body=Path(row['path']).read_bytes();assert len(body)==row['bytes']==0x400000 and sha(body)==row['sha256']
        if row['frame'] in snapshots:assert snapshots[row['frame']]['sha256']==row['sha256']
        snapshots[row['frame']]=row
    for row in report['frames_captured']:assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    commands=[json.loads(line) for line in (RUN/'navigation.jsonl').read_text(encoding='utf-8').splitlines()]
    journal=read(CAP/'navigation_command_journal.json')['commands_received'];assert commands==[r['command'] for r in journal]
    assert journal[-1]['frame']==5900 and journal[-1]['command']=={'stop':True}
    schedule=read(RUN/'original_departure_inputs.json')
    for item in journal:
        assert item['validation_passed'];c=item['command']
        assert 'battle_fixture' not in c
        if c.get('stop'):continue
        assert c['until'] in snapshots and c['until']>item['frame']
        if c.get('buttons') or c.get('touch') is not None:
            event={'start':item['frame']+1,'duration':c.get('duration',12),'buttons':c.get('buttons',[])}
            if c.get('touch') is not None:event['touch']=c['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    rom=NdsImage.open(ROM);arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
    clean_arm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert resident(arm,PALETTE,32)==resident(clean_arm,PALETTE,32)
    assert resident(arm,0x020548C8,4)==bytes.fromhex('0f20a0e3') and resident(arm,0x020548D4,4)==bytes.fromhex('34208de5')
    palette=struct.unpack('<16H',resident(arm,PALETTE,32))
    rgb={1:captured_rgb(palette[15]),15:captured_rgb(palette[14])}
    assert rgb=={1:(0,8,0),15:(197,198,197)}
    owner,wrapped=[struct.unpack_from('<I',arm,p)[0]-0x02000000 for p in [0x552A0,0x54894]]
    class CurrentFont:
        @staticmethod
        def open(path):return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    raw_before=Path(snapshots[5500]['path']).read_bytes();cpu,get=get_machine(arm,raw_before);fleet=get(0xCB1A8)+4+132*get(0x2E58C)
    fatigue_before=bytes(cpu.mem_read(fleet+0x3D,1))[0];holds=[]
    frames={r['frame']:r for r in report['frames_captured']}
    for frame in [5700,5730]:
        raw=Path(snapshots[frame]['path']).read_bytes();cpu,get=get_machine(arm,raw)
        fatigue_after=bytes(cpu.mem_read(fleet+0x3D,1))[0];assert fatigue_after==fatigue_before+3
        value=raw[owner+0x2030:owner+0x2230].split(b'\0')[0];formatted=raw[wrapped:wrapped+512].split(b'\0')[0]
        assert value==entries[308].text
        native=pipeline(arm,common,raw_before,{'patches':[]},308,3)
        assert native['formatted_hex']==formatted.hex() and native['loaded_template_hex']==value.hex()
        assert native['fatigue_before']==fatigue_before and native['fatigue_after_original_clamp']==fatigue_after
        pixels=raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000)
        lines=formatted.split(b'\n');assert all(not line.strip() for line in lines[1:])
        assert pixels==literal_independent(arm,rom.read_file('/GRP/KANJI.FNT'),lines[0].decode('cp932'))
        assert raw[PALETTE-0x02000000:PALETTE-0x02000000+32]==resident(arm,PALETTE,32)
        with Image.open(frames[frame]['path']) as im:
            picture=im.convert('RGB')
            for index,color in rgb.items():
                expected={(16+i%228,296+i//228) for i,p in enumerate(pixels) if p==index}
                actual={(x,y) for y in range(294,366) for x in range(16,244) if picture.getpixel((x,y))==color}
                assert actual==expected,(frame,index,len(expected-actual),len(actual-expected))
        holds.append({'frame':frame,'message_ID':308,'actual_change':3,'fatigue_before':fatigue_before,'fatigue_after':fatigue_after,
            'native_pipeline':native,'full_native_independent_actual_ink_and_shadow_RGB_equal':True,'source_palette_and_foreground15_setup_exact':True,'capture':frames[frame]['path'],'capture_sha256':frames[frame]['PNG_sha256']})
    ROOT.mkdir(parents=True);save(ROOT/'fixture_free_Search_failure_original_plus3_verified.json',{'candidate':str(ROM),'candidate_sha256':digest,
        'terminal_report':str(CAP/'capture_report.json'),'terminal_report_sha256':sha((CAP/'capture_report.json').read_bytes()),
        'terminal_frame':5900,'all_inputs_RAM_PNG_and_unchanged_saves_audited':True,'no_fixture_or_RNG_state_event_or_message_injection':True,
        'original_Search_and_nothing_found_then_actual308_plus3_observed':True,'holds':holds,
        'source_disposable_saves_unchanged':True,'revised_text_and_recovery309_not_yet_verified':True,
        'V1587f_binary_mask_erratum':'The first audit counted native shadow15 as black. Source palette625/628 mapping proves it is gray;verify both full masks and exact colors without changing game bytes.',
        'no_editorial_completion_credit':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Fixture-free original Search/+3 audited:two full native/independent/actual RGB holds,unchanged saves;revised text/recovery still pending.')
