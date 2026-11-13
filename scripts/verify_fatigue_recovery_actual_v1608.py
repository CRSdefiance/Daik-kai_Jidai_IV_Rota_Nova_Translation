"""Original friendly-village -10: full native/RGB glyphs, callstack and return."""
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.fatigue_status_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_fatigue_region2_fixture_v1605 as fixture
from scripts.audit_fatigue_location_runs_v1607 import audit_run
from scripts.probe_fatigue_status_fonts_v1590 import pipeline
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.probe_inspection_status_fonts_v1574 import literal_independent
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
from scripts.verify_dialogue_palette_v628 import PALETTE,resident,captured_rgb

ROOT=Path('work/analysis/fatigue_recovery_verified_v1608')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/fatigue_recovery_live_v1606_1594')
ROM=fixture.ROM

def main_frame(raw):
    positions=[];pos=0
    while True:
        at=raw.find(struct.pack('<I',0x02079E90),pos)
        if at<0:break
        pos=at+1;main=at+4
        if main+0xB0<=len(raw) and struct.unpack_from('<I',raw,main+0xAC)[0]==0x0207B190:positions.append(main)
    assert len(positions)==1
    return positions[0]

if __name__=='__main__':
    assert not ROOT.exists()
    audit=audit_run('fatigue_recovery_live_v1606',1594,fixture,6200,[5000,5650])
    report=read(CAP/'capture_report.json');frames={r['frame']:r for r in report['frames_captured']}
    shots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']}
    rom=NdsImage.open(ROM);arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
    clean_arm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for start,end in [(0x795A4,0x79698),(0x79728,0x79958),(0x79E20,0x79E98),(0x119164,0x119194)]:assert arm[start:end]==clean_arm[start:end]
    assert resident(arm,PALETTE,32)==resident(clean_arm,PALETTE,32)
    assert resident(arm,0x020548C8,4)==bytes.fromhex('0f20a0e3') and resident(arm,0x020548D4,4)==bytes.fromhex('34208de5')
    palette=struct.unpack('<16H',resident(arm,PALETTE,32));rgb={1:captured_rgb(palette[15]),15:captured_rgb(palette[14])}
    assert rgb=={1:(0,8,0),15:(197,198,197)}
    owner,wrapped=[struct.unpack_from('<I',arm,p)[0]-0x02000000 for p in [0x552A0,0x54894]]
    class CurrentFont:
        @staticmethod
        def open(path):return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    before=Path(shots[5900]['path']).read_bytes();cpu,get=get_machine(arm,before);fleet=get(0xCB1A8)+4+132*get(0x2E58C)
    fatigue_before=bytes(cpu.mem_read(fleet+0x3D,1))[0];assert fatigue_before==6
    main=main_frame(before);assert struct.unpack_from('<I',before,main-8)[0]==2
    assert struct.pack('<I',0x020795EC) in before[main-0x80:main]
    point=struct.unpack_from('<2i',before,main+0x14);assert point==struct.unpack_from('<2i',before,main+0x2C)
    temp=0x02470000;cpu.mem_write(temp,struct.pack('<2i',*point));assert get(0x797A0,temp)==2
    holds=[]
    for frame in [6050,6080]:
        raw=Path(shots[frame]['path']).read_bytes();cpu,get=get_machine(arm,raw)
        fatigue_after=bytes(cpu.mem_read(fleet+0x3D,1))[0];assert fatigue_after==0
        main=main_frame(raw);assert struct.unpack_from('<I',raw,main-8)[0]==2
        assert struct.unpack_from('<I',raw,main-0x4C)[0]==0x020795F4
        assert struct.unpack_from('<I',raw,main-0x6C)[0]==0x02079794
        assert struct.unpack_from('<I',raw,main-0x68)[0]==309
        argument=struct.unpack_from('<I',raw,main-0x64)[0]-0x02000000
        digits=raw[argument:argument+16].split(b'\0')[0];assert digits=='１０'.encode('cp932')
        value=raw[owner+0x2030:owner+0x2230].split(b'\0')[0];formatted=raw[wrapped:wrapped+512].split(b'\0')[0]
        assert value==entries[309].text==b'Fatigue decreased by %s.'
        native=pipeline(arm,common,before,{'patches':[]},309,10)
        assert native['formatted_hex']==formatted.hex() and native['loaded_template_hex']==value.hex()
        assert native['fatigue_before']==fatigue_before and native['fatigue_after_original_clamp']==fatigue_after
        assert formatted==b'Fatigue decreased by '+digits+b'.' and b'\n' not in formatted
        events=[];pixels=raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events)
        assert pixels==literal_independent(arm,rom.read_file('/GRP/KANJI.FNT'),formatted.decode('cp932'))
        assert events[0]['code']==ord('F') and any(e['code']==ord('.') for e in events)
        assert all(not p for p in pixels[228*12:])
        assert raw[PALETTE-0x02000000:PALETTE-0x02000000+32]==resident(arm,PALETTE,32)
        with Image.open(frames[frame]['path']) as im:
            picture=im.convert('RGB')
            for index,color in rgb.items():
                expected={(16+i%228,296+i//228) for i,p in enumerate(pixels) if p==index}
                actual={(x,y) for y in range(294,366) for x in range(16,244) if picture.getpixel((x,y))==color}
                assert actual==expected,(frame,index,len(expected-actual),len(actual-expected))
        holds.append({'frame':frame,'message_ID':309,'original_requested_recovery':10,'fatigue_before':6,'fatigue_after_original_clamp':0,
            'saved_friendly_village_return':hex(0x020795F4),'saved_signed_helper_modal_return':hex(0x02079794),
            'actual_original_vararg_hex':digits.hex(),'native_pipeline':native,
            'full_native_independent_actual_ink_and_shadow_RGB_equal':True,'complete_F_fullwidth_digits_period_literal_x0_and_bounds':True,
            'capture':frames[frame]['path'],'capture_sha256':frames[frame]['PNG_sha256']})
    after=Path(shots[6200]['path']).read_bytes();cpu,get=get_machine(arm,after)
    assert bytes(cpu.mem_read(fleet+0x3D,1))[0]==0
    ROOT.mkdir(parents=True)
    save(ROOT/'original_friendly_village_recovery10_verified.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'preservation_audit':audit,
        'before_event_frame':5900,'actual_region':2,'actual_Search_point':list(point),'holds':holds,
        'actual_original_friendly_village_success_and_signed_helper_minus10_observed':True,
        'no_health_fatigue_RNG_actor_or_event_result_writes':True,
        'location_fixture_only_not_earned_travel':True,'all_original_Search_and_dismissal_controls_recorded':True,
        'recovery6080_and_normal_Sea_View6200_actually_viewed':True,
        'normal_return_capture':frames[6200],
        'no_full_route_or_hardware_verification':True,'editorial_completion_requires_separate_coverage_update':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Original friendly-village -10 verified:6 to0 clamp,actual309 vararg and saved calls,full native/independent/RGB F/digits/period,normal Sea View6200;all48-byte fixtures and otherRAM/inputs/saves audited.')
