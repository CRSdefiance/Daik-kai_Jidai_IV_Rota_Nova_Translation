"""Rafael B44 local-profile research: actual macro names, guarded calls and planes.

Does not register a profile or approve any manuscript. FE is a distinct consumer.
"""
from dataclasses import replace
from pathlib import Path
import struct
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_name_catalog_glyphs_v278 import raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/hodram_opening_fonts_v2021')
DOC=Path('translations/hodram_opening_contextual_editorial_manuscript_v1.json')
ROM=Path('out/all_routes_combined_v2013_candidate.nds')
REPORT=Path('work/analysis/hodram_opening_context_v2018/run_plan.json')
INPUT,OUTPUT=0x02660000,0x02662000

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    doc=read(DOC);image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin');report=read(REPORT)
    assert report['candidate_sha256']==sha(ROM.read_bytes()) and report['no_save_savestate_or_fixtures']
    live=read('work/analysis/hodram_opening_context_v2018/live_observer_progress.json');assert not live['errors'] and not live['mismatches']
    snapshot={'path':'E:/Rota Nova translations/Generated/work/emulation_v193/hodram_opening_context_v2018_V2013/frame_004000_arm9_ram.bin'}
    raw=Path(snapshot['path']).read_bytes();assert len(raw)==0x400000;snapshot['sha256']=sha(raw)
    cpu,get=get_machine(arm,raw);assert get(0x7F244)==1 and struct.unpack_from('<I',raw,0x2796B0)[0]==1
    actors=get(0xCB184);captain=actors+0x19E4
    assert [get(0x2434C,i)for i in (1,2,9,16,18,23)]==[1,2,9,16,18,23]
    profile=replace(get_dialogue_profile('hodram-story-live'),name='hodram-opening-editorial-native-v1-RESEARCH-ONLY',leading_speaker_bytes=frozenset({16,18,23}),
        balanced_wrapping=True,literal_prefix_policy='native-guard-v255',
        macro_widths={'FI':36,'FA':54,'FO':90,'I':12},macro_ascii_lengths={'FI':6,'FA':9,'FO':15})
    cases=[];failures=[];pictures=[]
    boundary=cpu.hook_add(UC_HOOK_CODE,lambda u,a,z,d:u.reg_write(UC_ARM_REG_PC,0x027E0000),begin=0x020242CC,end=0x020242CC)
    names={'FI':b'Hodram','FA':b'Bergstrom','FO':b'Bergstrom Fleet'}
    def native(value,actor):
        checks=[]
        expected=value
        for name,name_bytes in names.items():expected=expected.replace(name.encode(),name_bytes)
        for phase in range(4):
            cpu.mem_write(INPUT-16,b'\xa5'*2080);cpu.mem_write(INPUT+phase,value+b'\0')
            before=bytes(cpu.mem_read(INPUT-16,2080));cpu.mem_write(OUTPUT-16,b'\xa5'*4128)
            call(cpu,0x242C8,(OUTPUT,INPUT+phase,actor),instruction_limit=400000)
            result=bytes(cpu.mem_read(OUTPUT,4096)).split(b'\0')[0]
            assert result==expected,(result,expected)
            assert bytes(cpu.mem_read(0x02000000,0x400000))==raw and bytes(cpu.mem_read(INPUT-16,2080))==before
            assert bytes(cpu.mem_read(OUTPUT-16,16))==b'\xa5'*16
            assert bytes(cpu.mem_read(OUTPUT+len(result)+1,4095-len(result)))==b'\xa5'*(4095-len(result))
            checks.append(dict(alignment=phase,output_hex=result.hex(),all4MiB_ABI_input_output_guards_exact=True))
        return expected,checks
    try:
        measured,measurement=native(b'FI FA FO',captain)
        assert measured==b'Hodram Bergstrom Bergstrom Fleet'
        for row in doc['records']:
            if row['source_presentation_prefix_hex']=='fe':continue
            try:
                source=bytes.fromhex(row['current_text_hex']);markup=row['english'].removesuffix('{PAD}')
                zero=row['source_presentation_prefix_hex']=='00'
                if zero:source=source[1:];markup=markup.removeprefix('{SPEAKER:00}')
                result=encode_relocatable_dialogue(source,markup,profile)
                encoded=result.encoded if zero else result.encoded[1:]
                if not zero:assert result.encoded[0]==int(row['source_presentation_prefix_hex'],16)
                actor_ID=get(0x2434C,int(row['source_presentation_prefix_hex'],16));actor=captain if actor_ID==1 else actors+4+actor_ID*32
                logical=markup if zero else markup.split('}',1)[1]
                for name in names:logical=logical.replace('{MACRO:'+name+'}',name)
                logical=logical.encode('ascii')
                expanded,logical_checks=native(logical,actor)
                expanded_wrapped,wrapped_checks=native(encoded,actor)
                pixels,events,font=raster(arm,expanded_wrapped)
                assert pixels==expected_pixels(arm,font,events)
                assert[e['code']for e in events if e['code']!=32]==[ord(c)for c in expanded_wrapped.decode('ascii')if c not in' \n']
                visible=[e for e in events if e['code']!=32]
                assert all(0<=e['x']<=210 and 0<=e['y']<=48 for e in visible)
                assert len(visible)==len({(e['x'],e['y'])for e in visible})
                origins={y:min(e['x']for e in visible if e['y']==y)for y in sorted({e['y']for e in visible})}
                assert all(x==0 for x in origins.values())
                qa=audit_relocatable_dialogue_record(source,markup,profile)
                im=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
                im.putdata([colors[p]for p in pixels]);path=ROOT/(row['id']+'.png');im.save(path)
                pictures.append((row['id'],row['speaker'],im))
                cases.append(dict(id=row['id'],source_preamble_hex=row['source_complete_preamble_hex'],
                    encoded_text_excluding_speaker_hex=encoded.hex(),whole_command_speaker_byte=row['source_presentation_prefix_hex'],
                    formatted_markup=result.formatted_markup,native_expanded_hex=expanded_wrapped.hex(),
                    macro_cases=logical_checks+wrapped_checks,qa=qa,glyphs=events,
                    whole_native_independent_font_plane_exact=True,native_font_plane_sha256=sha(pixels),
                    all_glyphs_complete_in_order_unique_cells_within216x64=True,visible_origins_by_native_row=origins,
                    preview=str(path),preview_sha256=sha(path.read_bytes())))
            except(ValueError,AssertionError)as exc:failures.append(dict(id=row['id'],type=type(exc).__name__,error=str(exc)))
    finally:cpu.hook_del(boundary)
    sheets=[]
    for start in range(0,len(pictures),8):
        sheet=Image.new('RGB',(920,640),'#263238');draw=ImageDraw.Draw(sheet)
        for k,(ident,speaker,im)in enumerate(pictures[start:start+8]):
            x,y=460*(k%2),160*(k//2);draw.text((x+5,y+3),ident+' / '+speaker,fill='white')
            sheet.paste(im.resize((432,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=ROOT/f'review_sheet_{start//8+1:02d}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'all67_progressive_native_macros_and_complete_font_planes.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),
        ARM9_sha256=sha(arm),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_run_plan=str(REPORT),source_run_plan_sha256=sha(REPORT.read_bytes()),original_run_not_claimed_terminal_by_this_native_probe=True,
        snapshot=snapshot,cases=cases,failures=failures,native_macro_calls=4+sum(len(r['macro_cases'])for r in cases),
        actual_measured_FI_FA_FO={'FI':'Hodram','FA':'Bergstrom','FO':'Bergstrom Fleet'},measurement_cases=measurement,
        research_profile_only=True,global_profile_unchanged=True,FE_separate_not_sent_to_progressive_selector=True,
        not_gameplay_whole_GPU_or_hardware_proof=True,visual_review_pending=True,review_sheets=sheets,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(planes=len(cases),native_macro_calls=4+sum(len(r['macro_cases'])for r in cases),failures=failures),flush=True)
