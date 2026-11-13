"""Two original hot-spring discovery/-15 visits;relaxation branch still pending."""
import json,struct
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.hot_spring_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_hot_spring_location_v1625 as fixture
from scripts.audit_fatigue_location_runs_v1607 import audit_run
from scripts.verify_fatigue_recovery_actual_v1608 import main_frame
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.probe_fatigue_status_fonts_v1590 import pipeline
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.probe_inspection_status_fonts_v1574 import literal_independent
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_dialogue_palette_v628 import PALETTE,resident,captured_rgb
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/hot_spring_actual_v1628')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_live_v1626_1622')
RUN=Path('work/analysis/hot_spring_live_v1626')
ROM=fixture.ROM
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists()
    journal=read(CAP/'navigation_command_journal.json')['commands_received']
    fixture_frames=[r['frame'] for r in journal if 'battle_fixture' in r['command']]
    audit=audit_run('hot_spring_live_v1626',1622,fixture,13600,fixture_frames)
    report=read(CAP/'capture_report.json');frames={r['frame']:r for r in report['frames_captured']}
    shots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']}
    rom=NdsImage.open(ROM);arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in [(0x7931C,0x793B4),(0x79728,0x79958),(0x79E20,0x79E98),(0x116D60,0x116DA0)]:assert arm[lo:hi]==clean[lo:hi]
    assert resident(arm,PALETTE,32)==resident(clean,PALETTE,32)
    palette=struct.unpack('<16H',resident(arm,PALETTE,32));rgb={1:captured_rgb(palette[15]),15:captured_rgb(palette[14])};assert rgb=={1:(0,8,0),15:(197,198,197)}
    owner,speech,modal=[struct.unpack_from('<I',arm,p)[0]-BASE for p in [0x552A0,0x54450,0x54894]]
    fonts=read('work/analysis/hot_spring_fonts_v1617/native_font_research.json')
    assert fonts['ARM9_sha256']==sha(arm) and fonts['COMMON_sha256']==sha(common)
    class CurrentFont:
        @staticmethod
        def open(path):return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    def pixels_match(frame,formatted,lines,spoken):
        pixels=raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
        expected=independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),lines) if spoken else literal_independent(arm,rom.read_file('/GRP/KANJI.FNT'),lines[0])
        assert pixels==expected
        raw=Path(shots[frame]['path']).read_bytes();assert raw[PALETTE-BASE:PALETTE-BASE+32]==resident(arm,PALETTE,32)
        with Image.open(frames[frame]['path']) as im:
            picture=im.convert('RGB')
            for index,color in rgb.items():
                wanted={(16+i%228,296+i//228) for i,p in enumerate(pixels) if p==index}
                actual={(x,y) for y in range(294,366) for x in range(16,244) if picture.getpixel((x,y))==color}
                assert actual==wanted,(frame,index,len(wanted-actual),len(actual-wanted))
        return {'frame':frame,'capture':frames[frame]['path'],'capture_sha256':frames[frame]['PNG_sha256'],
            'full_native_independent_actual_palette_ink_shadow_complete_letters_bounds_and_blank_paper_pass':True}
    visits=[]
    for first,holds,recovery_holds,returned in [(9600,[9600,9630],[9800,9830],10000),(11300,[11300,11330],[11500,11530],11700)]:
        before=Path(shots[first]['path']).read_bytes();cpu,get=get_machine(arm,before);fleet=get(0xCB1A8)+4+132*get(0x2E58C)
        fatigue_before=bytes(cpu.mem_read(fleet+0x3D,1))[0];discovery=[];recoveries=[]
        for frame in holds:
            raw=Path(shots[frame]['path']).read_bytes();cpu,get=get_machine(arm,raw);main=main_frame(raw)
            assert struct.unpack_from('<I',raw,main-8)[0]==2 and struct.unpack_from('<I',raw,main-0x3C)[0]==0x0207933C
            assert struct.unpack_from('<I',raw,main-0x34)[0]==0x02116D80
            identity=get(0x82478,get(0xCB1A8)+0x2090,1);root=get(0xCB184);captain=get(0x7F244)
            actor=root+0x19E4 if identity==captain else root+4+32*identity;number=get(0x53F4C,actor,0x02116D80);voice=get(0x7E988,actor)
            assert number==2276 and voice==1
            value=raw[owner+0x2030:owner+0x2230].split(b'\0')[0];formatted=raw[speech:speech+512].split(b'\0')[0]
            native=consumer(arm,common,raw,{'patches':[]},0x53D44,1,0x02116D80)
            assert value==entries[number].text and native['input_hex']==value.hex() and native['formatted_hex']==formatted.hex()
            case=next(c for c in fonts['cases'] if c['message_ID']==number and c['source_voice']==voice)
            assert case['native_pipeline']['formatted_hex']==formatted.hex()
            discovery.append({**pixels_match(frame,formatted,case['lines'],True),'message_ID':number,'actual_actor_ID':identity,'original_role':1,'source_voice':voice,
                'original_hot_spring_speech_return':hex(0x0207933C),'native_pipeline':native})
        for frame in recovery_holds:
            raw=Path(shots[frame]['path']).read_bytes();cpu,get=get_machine(arm,raw);main=main_frame(raw)
            assert struct.unpack_from('<I',raw,main-0x2C)[0]==0x02079344 and struct.unpack_from('<I',raw,main-0x4C)[0]==0x02079794
            assert struct.unpack_from('<I',raw,main-0x48)[0]==309
            at=struct.unpack_from('<I',raw,main-0x44)[0]-BASE;digits=raw[at:at+32].split(b'\0')[0];assert digits=='１５'.encode('cp932')
            formatted=raw[modal:modal+512].split(b'\0')[0];assert formatted==b'Fatigue decreased by '+digits+b'.'
            native=pipeline(arm,common,before,{'patches':[]},309,15);assert native['formatted_hex']==formatted.hex()
            assert native['fatigue_before']==fatigue_before and native['fatigue_after_original_clamp']==0 and bytes(cpu.mem_read(fleet+0x3D,1))==b'\0'
            recoveries.append({**pixels_match(frame,formatted,[formatted.decode('cp932')],False),'message_ID':309,'original_requested_recovery':15,
                'fatigue_before':fatigue_before,'fatigue_after_original_clamp':0,'native_pipeline':native})
        visits.append({'discovery_holds':discovery,'recovery_holds':recoveries,'normal_Sea_View_return_frame_actually_viewed':returned,
            'return_capture':frames[returned],'optional_relaxation_not_observed_in_this_visit':True})
    reference=read('E:/Rota Nova translations/Generated/work/emulation_v193/fatigue_recovery_live_v1606_1594/capture_report.json');controls=[]
    for row in reference['frames_captured']:
        frame=row['frame'];assert frame<=6200
        if frame not in frames:continue
        with Image.open(row['path']) as old,Image.open(frames[frame]['path']) as new:assert old.convert('RGB').tobytes()==new.convert('RGB').tobytes(),frame
        controls.append({'frame':frame,'whole256x384_RGB_exact_to_prior_V1594_friendly_village_control':True})
    raw=Path(shots[11530]['path']).read_bytes();cpu,get=get_machine(arm,raw);offset=struct.unpack_from('<I',arm,0x793A8)[0]
    assert offset==0x19E4;ability=get(0x7E788,get(0xCB184)+offset,5);assert ability==51
    ROOT.mkdir(parents=True);save(ROOT/'two_original_hot_spring_discovery_and_minus15_visits.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'preservation_audit':audit,'visits':visits,'whole_prefix_controls':controls,
        'all48_coordinate_byte_fixtures_and_other4MiB_inputs_snapshots_PNGs_and_saves_audited':True,
        'no_actor_health_fatigue_skill_RNG_or_event_outcome_writes':True,'only2276_individually_observed_of13_lines':True,
        'discovery_family_native_representative_scope_verified_relaxation_family_actual_pending':True,
        'original_optional_condition_readonly_query':{'frame':11530,'original_captain_object_offset':offset,'stat_index':5,'value':ability,
            'integer_half_threshold':25,'source_RNG100_accepts_zero_through25':True,'no_live_stat_or_RNG_edit':True},
        'optional_relaxation_and_Experience_notice310_still_pending':True,'normal_final_Sea_View13600_actually_viewed':True,
        'source_prose_reviews_added':0,'completed_entries_added':0,'targeted_headless_not_full_route_or_hardware':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Two original hot-spring visits verified:2276 complete native/independent/palette RGB,-15 with source clamp,normal returns;all fixtures/otherRAM/inputs/saves pass. Relaxation6/notice310 remain pending,no completion credit.')
