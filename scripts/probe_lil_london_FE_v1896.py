"""Three London FE paragraphs through the proven mode1 native paper consumer."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.lil_london_profile import profile_for
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_lil_FE_display_v1737 import snapshots, OBS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_London_FE_v1896')
DOC=Path('translations/lil_london_editorial_manuscript_v3.json')
PRIOR=Path('work/analysis/lil_FE_display_v1737/actual_paper_contract_and_all9_reviewed_FE_panels.json')
NAV=Path('work/analysis/lil_London_context_navigation_v1891/closed_original_B26_context.json')
INPUT=0x02660000

if __name__=='__main__':
    assert not ROOT.exists()
    doc,prior,nav=map(read,(DOC,PRIOR,NAV))
    assert prior['all6_current_FE_native_actual_complete_ink_and_blank_cells_match']
    assert prior['same_mode1_context_geometry_clip_spacing_and_font_metrics_confirmed_by_readonly_capture']
    im=NdsImage.open(doc['current_ROM'])
    arm=im.read_file('/__arm9__.bin')
    assert sha(arm)== '500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'
    profile=profile_for(arm,IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[26],'FE-paper')
    font=GameAsciiFont.from_arm9(arm)
    observed=read(OBS)
    captured=next(r for r in observed['rows'] if r.get('complete_readonly_snapshots'))
    data=snapshots(captured)
    ctx=captured['context']
    bitmap=struct.unpack('<25I',bytes.fromhex(captured['bitmap_100_hex']))
    assert list(bitmap[10:12])==[228,48] and list(bitmap[12:16])==[0,0,228,48]
    assert struct.unpack('<19I',bytes.fromhex(captured['context_76_hex']))[1:5]==(0,0,228,48)
    descriptor=bitmap[4]
    header=struct.unpack_from('<5I',data['WRAM'],descriptor-0x02000000)
    assert header[0]&255==4 and header[1:3]==(72,48)
    pixels_address=(descriptor+header[4])&0xffffffff
    width=header[1]*4
    assert width==288
    actuals={r['id']:r for r in nav['old_text_observations']}
    cases,old_checks,pictures=[],[],[]

    def render(body):
        cpu=machine(arm)
        cpu.mem_write(0x02000000,data['WRAM'])
        cpu.mem_write(0x01FF8000,data['ITCM'])
        cpu.mem_write(captured['DTCM_base'],data['DTCM'])
        cpu.mem_map(0x06000000,0x800000)
        cpu.mem_write(INPUT-16,b'\xa5'*(len(body)+33))
        cpu.mem_write(INPUT,body+b'\0')
        events=[]
        def glyph(u,address,size,_):
            code,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8))
            events.append(dict(code=code,style=style,x=u.reg_read(UC_ARM_REG_R2),y=u.reg_read(UC_ARM_REG_R3)))
        hook=cpu.hook_add(UC_HOOK_CODE,glyph,begin=0x020D16B4,end=0x020D16B4)
        try:call(cpu,0x01FFCE40-0x02000000,(ctx,INPUT),instruction_limit=1000000)
        finally:cpu.hook_del(hook)
        assert cpu.reg_read(UC_ARM_REG_R0)==INPUT+len(body)
        assert bytes(cpu.mem_read(INPUT,len(body)+1))==body+b'\0'
        assert bytes(cpu.mem_read(INPUT-16,16))==bytes(cpu.mem_read(INPUT+len(body)+1,16))==b'\xa5'*16
        visible=[e for e in events if e['code']!=32]
        assert [e['code'] for e in visible]==[c for c in body if c not in (32,10)]
        assert len(visible)==len({(e['x'],e['y']) for e in visible})
        assert all(0<=e['x']<=222 and e['y']%12==0 and 0<=e['y']<=36 for e in visible)
        native=bytes(n for b in cpu.mem_read(pixels_address,header[1]*2*48) for n in (b&15,b>>4))
        expected=bytearray(width*48)
        physical=bytearray(228*64)
        for e in visible:
            g=font.decode(chr(e['code']))
            for y in range(11):
                for x in range(6):
                    if g.getpixel((x,y)):
                        expected[(e['y']+y)*width+e['x']+x]=e['style']
                        physical[(e['y']//12*16+y)*228+e['x']+x]=1
        assert native==bytes(expected)
        return bytes(native[y*width+x] for y in range(48) for x in range(228)),bytes(physical),events

    ROOT.mkdir(parents=True)
    for row in doc['records']:
        if row['source_presentation_prefix_hex']!='fe':continue
        # First reconcile the actual London old text against the independent
        # existing mode1 paper renderer,not merely a same-shaped host bitmap.
        old=bytes.fromhex(row['current_text_hex'])[1:]
        logical,physical,events=render(old)
        wanted={(16+x,296+y) for y in range(64) for x in range(228) if physical[y*228+x]}
        checks=[]
        for hold in actuals[row['id']]['holds']:
            actual=Image.open(hold['capture']).convert('RGB')
            ink={(x,y) for y in range(296,360) for x in range(16,244) if actual.getpixel((x,y))==(0,8,0)}
            assert ink==wanted,(row['id'],hold['frame'],len(wanted-ink),len(ink-wanted))
            checks.append(dict(frame=hold['frame'],capture=hold['capture'],capture_sha256=hold['capture_sha256'],
                complete_mode1_native_independent_actual_ink_equal=True))
        old_checks.append(dict(id=row['id'],holds=checks))
        compiled=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'].removesuffix('{PAD}'),profile)
        assert compiled.encoded[:1]==b'\xfe'
        body=compiled.encoded[1:]
        assert b'FI' not in body and b'FA' not in body and b'FO' not in body
        logical,physical,events=render(body)
        path=ROOT/(row['id']+'_display.png')
        preview=Image.new('RGB',(228,64))
        preview.putdata([(0,8,0) if v else (239,232,201) for v in physical])
        preview.save(path)
        native=ROOT/(row['id']+'_native_228x48.bin')
        native.write_bytes(logical)
        cases.append(dict(id=row['id'],consumer='original_FE_modal_5473C_mode1',encoded_hex=compiled.encoded.hex(),
            formatted_markup=compiled.formatted_markup,glyphs=events,
            diagnostics=[dict(code=d.code,severity=d.severity,message=d.message) for d in compiled.diagnostics],
            one_native_page_consumes_complete_target=True,logical_geometry=[228,48],physical_row_advance=16,
            complete_first_last_glyphs_bounds_independent_plane_and_input_guards=True,
            preview=str(path),preview_sha256=sha(path.read_bytes()),native_plane=str(native),native_plane_sha256=sha(logical)))
        pictures.append((row['id'],preview))
    assert len(cases)==3 and len(old_checks)==3
    sheet=Image.new('RGB',(470,3*156),'#263238')
    draw=ImageDraw.Draw(sheet)
    for i,(ident,p) in enumerate(pictures):
        draw.text((5,i*156+3),ident+' / FE paper',fill='white')
        sheet.paste(p.resize((456,128),Image.Resampling.NEAREST),(5,i*156+23))
    sheet_path=ROOT/'three_FE_native_review.png'
    sheet.save(sheet_path)
    save(ROOT/'all3_FE_native_planes_and_actual_mode_reconciliation.json',dict(manuscript=str(DOC),
        manuscript_sha256=sha(DOC.read_bytes()),candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],
        ARM9_sha256=sha(arm),cases=cases,old_text_actual_checks=old_checks,
        all6_original_London_FE_holds_match_complete_native_mode1_ink=True,
        all3_new_FE_targets_fit_one_page_complete_in228x48=True,
        prior_actual_paper_contract=str(PRIOR),prior_contract_sha256=sha(PRIOR.read_bytes()),
        exact_actual_context_source=str(OBS),exact_actual_context_source_sha256=sha(OBS.read_bytes()),
        review_sheet=str(sheet_path),review_sheet_sha256=sha(sheet_path.read_bytes()),visual_review_pending=True,
        physical_mapping_inherits_independent_prior_actual_screen_contract_not_new_GPU_trace=True,
        revised_actual_gameplay_relocation_andregistered_release_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(FE_new_native_planes=3,original_actual_matching_holds=6,all_complete_targets_one_native_page=True))
