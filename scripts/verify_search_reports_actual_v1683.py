"""Actual failure,forage and loss312:original callers,arguments,full RGB and returns."""
import argparse
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.search_reports_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_search_reports_actual_v1682 import audit
from scripts.search_reports_native_consumers_v1662b import speech, loss
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.probe_inspection_status_fonts_v1574 import literal_independent
from scripts.verify_dialogue_palette_v628 import PALETTE, resident, captured_rgb
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/search_reports_actual_v1683')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/search_reports_live_v1680_1676')
ROM=Path('out/all_routes_combined_v1676_candidate.nds')
BASE=0x02000000


def stack_word(raw, word):
    hits=[i for i in range(0x180000,0x1A0000,4) if raw[i:i+4]==struct.pack('<I',word)]
    assert len(hits)==1,(hex(word),hits)
    return hits[0]


def number_at(raw,pointer):
    assert BASE<=pointer<BASE+len(raw)-64
    value=raw[pointer-BASE:pointer-BASE+64].split(b'\0')[0]
    text=value.decode('cp932');assert text and all('０'<=c<='９' for c in text)
    return int(text),value


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cases',required=True);args=p.parse_args();cases_path=Path(args.cases);cases=read(cases_path)
    assert not ROOT.exists() and cases['normal_return_actually_viewed'] and cases['terminal']==cases['normal_return_frame']
    preservation=audit(cases['terminal']);report=read(CAP/'capture_report.json')
    frames={r['frame']:r for r in report['frames_captured']}
    shots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']}
    rom=NdsImage.open(ROM);arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo,hi in [(0x53D44,0x53DCC),(0x546B8,0x54708),(0x795A4,0x79728),(0x79BEC,0x7A000),(0x116E80,0x116EE0)]:assert arm[lo:hi]==clean[lo:hi]
    assert resident(arm,PALETTE,32)==resident(clean,PALETTE,32)
    palette=struct.unpack('<16H',resident(arm,PALETTE,32));colors={1:captured_rgb(palette[15]),15:captured_rgb(palette[14])}
    assert colors=={1:(0,8,0),15:(197,198,197)}
    owner,spoken,modal=[struct.unpack_from('<I',arm,offset)[0]-BASE for offset in [0x552A0,0x54450,0x54894]]
    class CurrentFont:
        @staticmethod
        def open(path):return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)

    def picture(frame,formatted,is_spoken):
        lines=[line.strip().decode('cp932') for line in formatted.split(b'\n')]
        pixels=raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000)
        expected=independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),lines) if is_spoken else literal_independent(arm,rom.read_file('/GRP/KANJI.FNT'),lines[0])
        assert pixels==expected
        raw=Path(shots[frame]['path']).read_bytes();assert raw[PALETTE-BASE:PALETTE-BASE+32]==resident(arm,PALETTE,32)
        with Image.open(frames[frame]['path']) as im:
            image=im.convert('RGB')
            for index,color in colors.items():
                wanted={(16+i%228,296+i//228) for i,v in enumerate(pixels) if v==index}
                actual={(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y))==color}
                assert wanted==actual,(frame,index,len(wanted-actual),len(actual-wanted))
        return {'frame':frame,'capture':frames[frame]['path'],'capture_sha256':frames[frame]['PNG_sha256'],'formatted_hex':formatted.hex(),
                'full_native_independent_actual_ink_shadow_and_complete_letters_quantities_bounds_blank_paper_equal':True}

    assert {g['kind'] for g in cases['spoken_groups']}=={'failure','forage'}
    groups=[]
    for group in cases['spoken_groups']:
        role,table,ret=(1,0x02116EC0,0x02079F9C) if group['kind']=='failure' else (7,0x02116E80,0x02079F60)
        assert len(group['holds'])>=2 and group['normal_return_actually_viewed'] and group['normal_return_frame']>max(group['holds'])
        assert group['normal_return_frame'] in frames
        holds=[]
        for frame in group['holds']:
            raw=Path(shots[frame]['path']).read_bytes();main=stack_word(raw,0x0207B190)-0xAC
            assert struct.unpack_from('<3I',raw,main-0x14)==(ret,role,table)
            amounts,arguments=[],[]
            if role==7:
                for pointer in struct.unpack_from('<2I',raw,main-8):
                    value,text=number_at(raw,pointer);amounts.append(value);arguments.append(text)
                assert 0<=amounts[0]<=4650 and 0<=amounts[1]<=3875 and all(v%5==0 for v in amounts)
            cpu,get=get_machine(arm,raw);identity=get(0x82478,get(0xCB1A8)+0x2090,role);root=get(0xCB184)
            actor=root+0x19E4 if identity==get(0x7F244) else root+4+32*identity
            voice,n=get(0x7E988,actor),get(0x53F4C,actor,table)
            assert n in (range(2217,2222) if role==1 else range(2229,2234))
            value=raw[owner+0x2030:owner+0x2230].split(b'\0')[0];formatted=raw[spoken:spoken+512].split(b'\0')[0]
            native=speech(arm,common,raw,{'patches':[]},role,table,amounts)
            assert value==entries[n].text and native['loaded_template_hex']==value.hex() and native['formatted_hex']==formatted.hex()
            assert native['source_ABF50_argument_hex']==[a.hex() for a in arguments]
            holds.append({**picture(frame,formatted,True),'message_ID':n,'actual_actor_ID':identity,'source_voice':voice,'original_role':role,
                'original_table':table,'original_speech_return':ret,'source_water_food_amounts':amounts,'native_pipeline':native})
        groups.append({'kind':group['kind'],'holds':holds,'normal_return_actually_viewed':frames[group['normal_return_frame']]})
    assert len(cases['loss_holds'])>=2
    losses=[]
    for frame in cases['loss_holds']:
        raw=Path(shots[frame]['path']).read_bytes();ret=stack_word(raw,0x02079720)
        assert struct.unpack_from('<I',raw,ret+4)[0]==312
        pointer=struct.unpack_from('<I',raw,ret+8)[0];amount,argument=number_at(raw,pointer);assert amount>0
        value=raw[owner+0x2030:owner+0x2230].split(b'\0')[0];formatted=raw[modal:modal+512].split(b'\0')[0]
        native=loss(arm,common,raw,{'patches':[]},amount)
        assert value==entries[312].text==b'Sailors lost: %s.'
        assert native['loaded_template_hex']==value.hex() and native['formatted_hex']==formatted.hex()
        assert native['source_ABF50_argument_hex']==[argument.hex()]
        losses.append({**picture(frame,formatted,False),'message_ID':312,'original_source_helper_return':0x02079720,'source_lost_sailors':amount,
            'count_neutral_grammar_complete_S_and_period_and_original_modal_x0':True,'native_pipeline':native})
    assert cases['normal_return_frame']>max(cases['loss_holds']) and cases['normal_return_frame'] in frames
    ROOT.mkdir(parents=True)
    save(ROOT/'original_revised_failure_forage_and_loss312_verified.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'cases':str(cases_path),'cases_sha256':sha(cases_path.read_bytes()),'preservation_audit':preservation,'spoken_groups':groups,'loss_holds':losses,
        'normal_Sea_View_return_actually_viewed':frames[cases['normal_return_frame']],
        'original_Search_failure_forage_and_sailor_loss_callers_and_ordered_arguments_observed':True,
        'no_actor_identity_skill_fatigue_RNG_event_or_outcome_forcing':True,
        'only_individually_activated_message_IDs':sorted({h['message_ID'] for g in groups for h in g['holds']}|{312}),
        'other_voice_alternatives_have_native_font_and_representative_family_coverage_not_individual_activation':True,
        'CPU_reexecution_oracle_distinct_from_actual_emulator_event':True,'no_full_route_or_hardware_verification':True,
        'completion_requires_separate_coverage_review':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Actual revised Search failure,forage and loss312:source callers,arguments,full native/independent/palette RGB and normal returns verified;all fixture/input/RAM/save audits pass.')
