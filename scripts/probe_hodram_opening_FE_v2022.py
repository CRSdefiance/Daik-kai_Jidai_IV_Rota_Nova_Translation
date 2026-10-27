"""Six FE source paragraphs: separate null-actor calls and full modal planes."""
from dataclasses import replace
from pathlib import Path
import struct
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_R0,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_lil_FE_display_v1737 import snapshots,OBS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/hodram_opening_FE_v2022')
DOC=Path('translations/hodram_opening_contextual_editorial_manuscript_v1.json')
SNAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hodram_opening_context_v2018_V2013/frame_004000_arm9_ram.bin')
INPUT,OUTPUT=0x02660000,0x02662000

if __name__=='__main__':
    assert not ROOT.exists()
    doc=read(DOC);arm=NdsImage.open(doc['current_ROM']).read_file('/__arm9__.bin')
    assert sha(arm)==doc['required_runtime_ARM9_sha256']=='500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'
    profile=replace(get_dialogue_profile('hodram-story-live'),name='hodram-opening-FE-RESEARCH-ONLY',leading_speaker_bytes=frozenset({254}),
        balanced_wrapping=True,literal_prefix_policy='native-guard-v255')
    source=read(OBS);captured=next(r for r in source['rows']if r.get('complete_readonly_snapshots'))
    data=snapshots(captured);ctx=captured['context'];bitmap=struct.unpack('<25I',bytes.fromhex(captured['bitmap_100_hex']))
    assert bitmap[10:12]==(228,48)and bitmap[12:16]==(0,0,228,48)
    descriptor=bitmap[4];header=struct.unpack_from('<5I',data['WRAM'],descriptor-0x02000000)
    assert header[0]&255==4 and header[1:3]==(72,48)
    pixels_address=(descriptor+header[4])&0xffffffff;ascii_font=GameAsciiFont.from_arm9(arm)
    raw=SNAP.read_bytes();macro,get=get_machine(arm,raw);assert get(0x7F244)==1
    boundary=macro.hook_add(UC_HOOK_CODE,lambda u,a,z,d:u.reg_write(UC_ARM_REG_PC,0x027E0000),begin=0x02024314,end=0x02024314)
    ROOT.mkdir(parents=True);cases=[];failures=[];pictures=[]
    def render(body):
        cpu=machine(arm);cpu.mem_write(0x02000000,data['WRAM']);cpu.mem_write(0x01FF8000,data['ITCM'])
        cpu.mem_write(captured['DTCM_base'],data['DTCM']);cpu.mem_map(0x06000000,0x800000)
        cpu.mem_write(INPUT-16,b'\xa5'*(len(body)+33));cpu.mem_write(INPUT,body+b'\0');events=[]
        def glyph(u,a,z,d):
            code,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8))
            events.append(dict(code=code,style=style,x=u.reg_read(UC_ARM_REG_R2),y=u.reg_read(UC_ARM_REG_R3)))
        hook=cpu.hook_add(UC_HOOK_CODE,glyph,begin=0x020D16B4,end=0x020D16B4)
        try:call(cpu,0x01FFCE40-0x02000000,(ctx,INPUT),instruction_limit=1000000)
        finally:cpu.hook_del(hook)
        assert cpu.reg_read(UC_ARM_REG_R0)==INPUT+len(body)
        assert bytes(cpu.mem_read(INPUT,len(body)+1))==body+b'\0'
        assert bytes(cpu.mem_read(INPUT-16,16))==bytes(cpu.mem_read(INPUT+len(body)+1,16))==b'\xa5'*16
        visible=[e for e in events if e['code']!=32]
        assert [e['code']for e in visible]==[c for c in body if c not in(32,10)]
        assert len(visible)==len({(e['x'],e['y'])for e in visible})
        assert all(0<=e['x']<=222 and 0<=e['y']<=36 and e['y']%12==0 for e in visible)
        expected=bytearray(288*48);physical=bytearray(228*64)
        for e in visible:
            glyph=ascii_font.decode(chr(e['code']))
            for y in range(11):
                for x in range(6):
                    if glyph.getpixel((x,y)):
                        expected[(e['y']+y)*288+e['x']+x]=e['style']
                        physical[(e['y']//12*16+y)*228+e['x']+x]=1
        native=bytes(n for b in cpu.mem_read(pixels_address,72*2*48)for n in(b&15,b>>4))
        assert native==bytes(expected)
        logical=bytes(native[y*288+x]for y in range(48)for x in range(228))
        return logical,bytes(physical),events
    try:
        for row in doc['records']:
            if row['source_presentation_prefix_hex']!='fe':continue
            try:
                compiled=encode_relocatable_dialogue(bytes.fromhex(row['current_text_hex']),row['english'].removesuffix('{PAD}'),profile)
                assert compiled.encoded[:1]==b'\xfe';body=compiled.encoded[1:]
                logical=row['english'].split('}',1)[1].removesuffix('{PAD}').encode('ascii');checks=[]
                for kind,value in(('logical',logical),('wrapped',body)):
                    for phase in range(4):
                        macro.mem_write(INPUT-16,b'\xa5'*2080);macro.mem_write(INPUT+phase,value+b'\0');before=bytes(macro.mem_read(INPUT-16,2080))
                        macro.mem_write(OUTPUT-16,b'\xa5'*4128);call(macro,0x24310,(OUTPUT,INPUT+phase,0),instruction_limit=400000)
                        output=bytes(macro.mem_read(OUTPUT,4096)).split(b'\0')[0]
                        assert output==value and bytes(macro.mem_read(0x02000000,0x400000))==raw
                        assert bytes(macro.mem_read(INPUT-16,2080))==before and bytes(macro.mem_read(OUTPUT-16,16))==b'\xa5'*16
                        assert bytes(macro.mem_read(OUTPUT+len(output)+1,4095-len(output)))==b'\xa5'*(4095-len(output))
                        checks.append(dict(kind=kind,alignment=phase,output_hex=output.hex(),null_actor_original_FE_caller=True,all4MiB_ABI_input_output_guards_exact=True))
                old_plane,old_mask,old_events=render(bytes.fromhex(row['current_text_hex'])[1:])
                plane,mask,events=render(body)
                preview=Image.new('RGB',(228,64));preview.putdata([(0,8,0)if n else(239,232,201)for n in mask]);path=ROOT/(row['id']+'.png');preview.save(path)
                plane_path=ROOT/(row['id']+'_228x48.bin');plane_path.write_bytes(plane)
                mask_path=ROOT/(row['id']+'_physical_mask.bin');mask_path.write_bytes(mask)
                old_mask_path=ROOT/(row['id']+'_old_physical_mask.bin');old_mask_path.write_bytes(old_mask)
                cases.append(dict(id=row['id'],encoded_hex=compiled.encoded.hex(),formatted_markup=compiled.formatted_markup,macro_cases=checks,glyphs=events,
                    consumer='original_FE_modal_5473C_mode1',one_complete_page_terminal_pointer_input_guards_and_independent_pixels=True,
                    logical_geometry=[228,48],physical_geometry=[228,64],native_plane=str(plane_path),native_plane_sha256=sha(plane),
                    physical_mask=str(mask_path),physical_mask_sha256=sha(mask),old_physical_mask=str(old_mask_path),old_physical_mask_sha256=sha(old_mask),
                    preview=str(path),preview_sha256=sha(path.read_bytes()),diagnostics=[dict(code=d.code,severity=d.severity,message=d.message)for d in compiled.diagnostics]))
                pictures.append((row['id'],preview))
            except(ValueError,AssertionError)as exc:failures.append(dict(id=row['id'],type=type(exc).__name__,error=str(exc)))
    finally:macro.hook_del(boundary)
    sheet=Image.new('RGB',(940,3*156),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(ident,preview)in enumerate(pictures):
        x,y=470*(i%2),156*(i//2);draw.text((x+5,y+3),ident+' / FE mode1',fill='white');sheet.paste(preview.resize((456,128)),(x+5,y+23))
    sheet_path=ROOT/'six_FE_review_sheet.png';sheet.save(sheet_path)
    save(ROOT/'all6_separate_FE_native_planes_and48_macro_calls.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),cases=cases,failures=failures,
        exact_original_null_actor_macro_calls=sum(len(r['macro_cases'])for r in cases),source_snapshot=str(SNAP),source_snapshot_sha256=sha(raw),
        borrowed_actual_FE_mode1_geometry_contract=str(OBS),borrowed_contract_sha256=sha(Path(OBS).read_bytes()),
        no_new_revised_actual_panel_or_terminal_original_run_claim=True,actual_scene_reconciliation_pending=True,
        preview=str(sheet_path),preview_sha256=sha(sheet_path.read_bytes()),visual_review_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(FE_planes=len(cases),macro_calls=sum(len(r['macro_cases'])for r in cases),failures=failures))
