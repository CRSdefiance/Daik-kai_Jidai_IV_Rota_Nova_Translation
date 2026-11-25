"""Verify actual discovery,optional relaxation,notice310 and original dismissal."""
import argparse,struct
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.hot_spring_notice_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_hot_spring_resilient_v1645c import audit
from scripts.verify_fatigue_recovery_actual_v1608 import main_frame
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.probe_inspection_status_fonts_v1574 import pipeline,literal_independent
from scripts.probe_fatigue_status_fonts_v1590 import pipeline as fatigue_pipeline
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_dialogue_palette_v628 import PALETTE,resident,captured_rgb
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/hot_spring_notice_actual_v1646')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_notice_resilient_v1645_1637')
ROM=Path('out/all_routes_combined_v1637_candidate.nds')
BASE=0x02000000

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--cases',required=True);args=parser.parse_args();cases_path=Path(args.cases);cases=read(cases_path)
    assert not ROOT.exists() and cases['normal_return_actually_viewed'] and cases['terminal']==cases['normal_return_frame']
    preservation=audit(cases['terminal']);report=read(CAP/'capture_report.json')
    frames={r['frame']:r for r in report['frames_captured']};shots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']}
    rom=NdsImage.open(ROM);arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
    old=NdsImage.open('out/all_routes_combined_v1622_candidate.nds');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert rom.read_file('/GRP/KANJI.FNT')==old.read_file('/GRP/KANJI.FNT')
    spans=[(0x7931C,0x793B4),(0x79728,0x79958),(0x79E20,0x79E98),(0x116D60,0x116DA0)]
    for lo,hi in spans:assert arm[lo:hi]==clean[lo:hi]
    assert resident(arm,PALETTE,32)==resident(clean,PALETTE,32)
    palette=struct.unpack('<16H',resident(arm,PALETTE,32));colors={1:captured_rgb(palette[15]),15:captured_rgb(palette[14])}
    assert colors=={1:(0,8,0),15:(197,198,197)}
    owner,speech,modal=[struct.unpack_from('<I',arm,p)[0]-BASE for p in [0x552A0,0x54450,0x54894]]
    class CurrentFont:
        @staticmethod
        def open(path):return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    fonts=read('work/analysis/hot_spring_fonts_v1617/native_font_research.json');notice_fonts=read('work/analysis/hot_spring_notice_fonts_v1633/native_font_proof.json')
    assert notice_fonts['ARM9_sha256']==sha(arm) and notice_fonts['COMMON_sha256']==sha(common)
    def picture_check(frame,formatted,spoken):
        lines=[line.strip().decode('cp932') for line in formatted.split(b'\n')]
        pixels=raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
        expected=independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),lines) if spoken else literal_independent(arm,rom.read_file('/GRP/KANJI.FNT'),lines[0])
        assert pixels==expected
        raw=Path(shots[frame]['path']).read_bytes();assert raw[PALETTE-BASE:PALETTE-BASE+32]==resident(arm,PALETTE,32)
        with Image.open(frames[frame]['path']) as im:
            image=im.convert('RGB')
            for index,color in colors.items():
                wanted={(16+i%228,296+i//228) for i,p in enumerate(pixels) if p==index}
                actual={(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y))==color}
                assert wanted==actual,(frame,index,len(wanted-actual),len(actual-wanted))
        return {'frame':frame,'capture':frames[frame]['path'],'capture_sha256':frames[frame]['PNG_sha256'],
            'full_native_independent_actual_ink_shadow_and_complete_letters_bounds_blank_paper_equal':True,'formatted_hex':formatted.hex()}
    assert {g['message_ID'] for g in cases['spoken_groups']}=={2276,2283}
    spoken_groups=[]
    for group in cases['spoken_groups']:
        n=group['message_ID'];table=0x02116D80 if n==2276 else 0x02116D60;ret=0x0207933C if n==2276 else 0x02079380
        assert len(group['holds'])>=2
        holds=[]
        for frame in group['holds']:
            raw=Path(shots[frame]['path']).read_bytes()
            for lo,hi in spans:assert raw[lo:hi]==arm[lo:hi]
            cpu,get=get_machine(arm,raw);main=main_frame(raw)
            assert struct.unpack_from('<I',raw,main-0x3C)[0]==ret and struct.unpack_from('<I',raw,main-0x34)[0]==table
            identity=get(0x82478,get(0xCB1A8)+0x2090,1);root=get(0xCB184);captain=get(0x7F244)
            actor=root+0x19E4 if identity==captain else root+4+32*identity
            assert get(0x53F4C,actor,table)==n and get(0x7E988,actor)==1
            value=raw[owner+0x2030:owner+0x2230].split(b'\0')[0];formatted=raw[speech:speech+512].split(b'\0')[0]
            native=consumer(arm,common,raw,{'patches':[]},0x53D44,1,table)
            assert value==entries[n].text and native['input_hex']==value.hex() and native['formatted_hex']==formatted.hex()
            old_case=next(c for c in fonts['cases'] if c['message_ID']==n and c['source_voice']==1)
            assert old_case['native_pipeline']['formatted_hex']==formatted.hex()
            holds.append({**picture_check(frame,formatted,True),'message_ID':n,'actual_actor_ID':identity,'source_voice':1,'original_role':1,
                'source_table':table,'original_speech_return':ret,'native_pipeline':native})
        spoken_groups.append({'message_ID':n,'holds':holds})
    notice=[];assert len(cases['notice310_holds'])>=2
    for frame in cases['notice310_holds']:
        raw=Path(shots[frame]['path']).read_bytes();main=main_frame(raw)
        assert struct.unpack_from('<I',raw,main-0x3C)[0]==0x02079394 and struct.unpack_from('<I',raw,main-0x38)[0]==310
        value=raw[owner+0x2030:owner+0x2230].split(b'\0')[0];formatted=raw[modal:modal+512].split(b'\0')[0]
        native=pipeline(arm,common,raw,{'patches':[]},310)
        assert value==entries[310].text==b'The hot spring boosted Experience.' and native['loaded_template_hex']==native['formatted_hex']==formatted.hex()==value.hex()
        assert notice_fonts['cases'][0]['compiled_hex']==value.hex()
        notice.append({**picture_check(frame,formatted,False),'message_ID':310,'original_optional_notice_return':0x02079394,'native_pipeline':native,
            'no_argument_no_authored_indent_no_LF_complete_T_Experience_period':True})
    before=Path(shots[cases['recovery_before_frame']]['path']).read_bytes();cpu,get=get_machine(arm,before);fleet=get(0xCB1A8)+4+132*get(0x2E58C)
    fatigue_before=bytes(cpu.mem_read(fleet+0x3D,1))[0];recovery=[];assert len(cases['recovery15_holds'])>=2
    for frame in cases['recovery15_holds']:
        raw=Path(shots[frame]['path']).read_bytes();main=main_frame(raw);cpu,get=get_machine(arm,raw)
        assert struct.unpack_from('<I',raw,main-0x2C)[0]==0x02079344 and struct.unpack_from('<I',raw,main-0x4C)[0]==0x02079794
        native=fatigue_pipeline(arm,common,before,{'patches':[]},309,15);formatted=raw[modal:modal+512].split(b'\0')[0]
        assert native['formatted_hex']==formatted.hex() and bytes(cpu.mem_read(fleet+0x3D,1))[0]==native['fatigue_after_original_clamp']
        recovery.append({**picture_check(frame,formatted,False),'message_ID':309,'source_requested_recovery':15,'fatigue_before':fatigue_before,
            'fatigue_after_original_clamp':native['fatigue_after_original_clamp'],'native_pipeline':native})
    returned=cases['normal_return_frame'];assert returned in frames and returned>max(cases['notice310_holds'])
    ROOT.mkdir(parents=True);save(ROOT/'original_optional_hot_spring_and_Experience_notice_verified.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'cases':str(cases_path),'cases_sha256':sha(cases_path.read_bytes()),'preservation_audit':preservation,'spoken_groups':spoken_groups,'notice310_holds':notice,'recovery15_holds':recovery,
        'original_Search_discovery_recovery_optional_relaxation_effect_notice_and_dismissal_observed':True,
        'original_optional_branch_passed_without_actor_skill_RNG_or_event_outcome_edits':True,
        'normal_Sea_View_return_actually_viewed':frames[returned],
        'artificial_locations_and_single_original_supply_refill_not_earned_travel_or_resupply':True,
        'individually_activated_hot_spring_IDs':[2276,2283,310],'other11_alternative_voice_lines_native_and_representative_family_coverage_only':True,
        'no_full_route_or_hardware_verification':True,'completion_requires_separate_coverage_review':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Original optional hot-spring sequence verified:discovery2276,-15,relaxation2283,new310,normal return;full native/independent/palette pixels and all fixture/input/RAM/save audits pass.')
