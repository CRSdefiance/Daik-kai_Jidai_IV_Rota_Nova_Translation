"""Current22FE complete panels,176null-actor macro cases and typed-paper calibration."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP,UC_ARM_REG_PC
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.lil_kuhn_china_layout_v1 import encode_relocatable_dialogue
from dk4tool.dialogue.lil_kuhn_china_profile import profile_for
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.native_machine_scoped_v764 import machine as cold_machine
from scripts.native_call_abi_v764 import call
from scripts.verify_lil_FE_display_v1737 import OBS,snapshots
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Kuhn_China_FE_v2901b');DOC=Path('translations/lil_kuhn_china_editorial_manuscript_v3.json');BASE=0x02000000
PRIOR=Path('work/analysis/lil_FE_display_v1737/actual_paper_contract_and_all9_reviewed_FE_panels.json')

def expand(arm,common,raw,plan,body):
    cpu,get,provider=machine(arm,common,raw,plan);before=bytes(cpu.mem_read(BASE,0x400000));cases=[]
    hook=cpu.hook_add(UC_HOOK_CODE,lambda u,a,z,d:u.reg_write(UC_ARM_REG_PC,0x027E0000),begin=BASE+0x24314,end=BASE+0x24314)
    try:
        for phase in range(4):
            inp,out=0x02660000+phase,0x02662000;cpu.mem_write(inp-16,b'\xA5'*2080);cpu.mem_write(inp,body+b'\0');input_before=bytes(cpu.mem_read(inp-16,2080));cpu.mem_write(out-16,b'\xA5'*4128)
            call(cpu,0x24310,(out,inp,0),instruction_limit=400000);value=bytes(cpu.mem_read(out,4096)).split(b'\0')[0];assert value==body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
            assert bytes(cpu.mem_read(BASE,0x400000))==before and bytes(cpu.mem_read(inp-16,2080))==input_before
            assert bytes(cpu.mem_read(out-16,16))==b'\xA5'*16 and bytes(cpu.mem_read(out+len(value)+1,4095-len(value)))==b'\xA5'*(4095-len(value))
            cases.append(dict(input_alignment=phase,output_hex=value.hex(),null_source_actor=True,original_macro_ABI_input_output_canaries_and4MiB_exact=True))
    finally:cpu.hook_del(hook)
    return dict(cases=cases,original_24310_macro_and_unexecuted_24314_UI_boundary=True,current_executed_instruction_addresses=len(provider.executed_current),not_FE_through_fallback_actor208=True)

if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4');source=read(doc['source_context'])
    blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    ROOT.mkdir(parents=True);contextpath=ROOT/'historical_source_context.json';save(contextpath,dict(actual_snapshot=source['actual_historical_snapshot'],actual_snapshot_sha256=source['actual_historical_snapshot_sha256']))
    inputpath=ROOT/'current_native_input.json';save(inputpath,dict(current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),native_context_proof=str(contextpath)))
    ctx=CurrentContext(inputpath,source['historical_snapshot_ROM'],ROOT/'current_context')
    prior=read(PRIOR);assert prior['all6_current_FE_native_actual_complete_ink_and_blank_cells_match'] and prior['same_mode1_context_geometry_clip_spacing_and_font_metrics_confirmed_by_readonly_capture']
    observed=read(OBS);captured=next(r for r in observed['rows'] if r.get('complete_readonly_snapshots'));data=snapshots(captured)
    actual_ctx=list(struct.unpack('<19I',bytes.fromhex(captured['context_76_hex'])));actual_view=list(struct.unpack('<25I',bytes.fromhex(captured['bitmap_100_hex'])));actual_font=list(struct.unpack('<6I',bytes.fromhex(captured['font_object_24_hex'])))
    actual_header=list(struct.unpack_from('<5I',data['WRAM'],actual_view[4]-BASE));palette=(actual_view[4]+actual_header[3])&0xffffffff
    assert actual_ctx[1:6]==[0,0,228,48,1] and actual_view[10:16]==[228,48,0,0,228,48] and actual_view[18:20]==[0,0] and actual_font[1:3]==[6,12]
    assert actual_header[:3]==[4,72,48] and data['WRAM'][palette-BASE:palette-BASE+32]==arm[palette-BASE:palette-BASE+32]
    # Copy only the captured,typed graphics descriptors and font parameters.
    # Every object pointer is explicitly rebound;no initialized game RAM,
    # ITCM or DTCM snapshot is installed in the current cold native machine.
    for vt in [actual_ctx[0],actual_view[0],actual_view[20],actual_font[0],actual_font[5]]:
        assert BASE<=vt<BASE+len(arm)-32 and arm[vt-BASE:vt-BASE+32]==data['WRAM'][vt-BASE:vt-BASE+32]
    ascii_font=GameAsciiFont.from_arm9(arm)
    def paint(text):
        cpu=cold_machine(arm);cpu.mem_write(POOL,bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]));header,view,context,string=0x02450000,0x02453000,0x02454000,0x02660000
        hd=actual_header.copy();hd[3]=(palette-header)&0xffffffff;hd[4]=20;vw=actual_view.copy();vw[4]=header;ct=actual_ctx.copy();ct[11]=view
        head=struct.pack('<5I',*hd);size=288*48//2;cpu.mem_write(header-16,b'\xA5'*(20+size+32));cpu.mem_write(header,head+bytes(size));cpu.mem_write(view-16,b'\xA5'*132);cpu.mem_write(view,struct.pack('<25I',*vw));cpu.mem_write(context-16,b'\xA5'*108);cpu.mem_write(context,struct.pack('<19I',*ct))
        font_object=struct.unpack_from('<I',arm,0xD5088)[0];assert font_object==captured['font_metrics_object'];cpu.mem_write(font_object,struct.pack('<6I',*actual_font));cpu.mem_write(struct.unpack_from('<I',arm,0xD19B8)[0],image.read_file('/GRP/KANJI.FNT'))
        cpu.mem_write(string-16,b'\xA5'*(len(text)+33));cpu.mem_write(string,text+b'\0');events=[]
        def observe(u,address,size,unused):
            code,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8));events.append(dict(code=code,style=style,x=u.reg_read(UC_ARM_REG_R2),y=u.reg_read(UC_ARM_REG_R3)))
        hook=cpu.hook_add(UC_HOOK_CODE,observe,begin=BASE+0xD16B4,end=BASE+0xD16B4)
        try:call(cpu,0x01FFCE40-BASE,(context,string),instruction_limit=1000000)
        finally:cpu.hook_del(hook)
        assert cpu.reg_read(UC_ARM_REG_R0)==string+len(text) and bytes(cpu.mem_read(string,len(text)+1))==text+b'\0'
        assert bytes(cpu.mem_read(string-16,16))==bytes(cpu.mem_read(string+len(text)+1,16))==b'\xA5'*16
        assert bytes(cpu.mem_read(header,20))==head and bytes(cpu.mem_read(header-16,16))==bytes(cpu.mem_read(header+20+size,16))==b'\xA5'*16
        assert bytes(cpu.mem_read(view-16,16))==bytes(cpu.mem_read(view+100,16))==b'\xA5'*16 and bytes(cpu.mem_read(context-16,16))==bytes(cpu.mem_read(context+76,16))==b'\xA5'*16
        visible=[e for e in events if e['code']!=32];assert [e['code'] for e in visible]==[v for v in text if v not in [32,10]]
        assert len(visible)==len({(e['x'],e['y']) for e in visible}) and all(0<=e['x']<=222 and e['y']%12==0 and 0<=e['y']<=36 for e in visible)
        native=bytes(n for b in cpu.mem_read(header+20,size) for n in [b&15,b>>4]);expected=bytearray(288*48);physical=bytearray(228*64)
        for e in visible:
            glyph=ascii_font.decode(chr(e['code']))
            for y in range(11):
                for x in range(6):
                    if glyph.getpixel((x,y)):expected[(e['y']+y)*288+e['x']+x]=e['style'];physical[(e['y']//12*16+y)*228+e['x']+x]=1
        assert native==bytes(expected)
        return dict(logical=bytes(native[y*288+x] for y in range(48) for x in range(228)),physical=bytes(physical),events=events,
            object_rebindings=dict(header=header,view=view,context=context,palette=palette,pixels=header+20,font=font_object),complete_return_input_object_canaries_and_native_independent_plane_equal=True)
    calibration=paint(bytes.fromhex(captured['text_hex']));actual=prior['current_actual_checks'][0];capture=Path(actual['capture']);assert sha(capture.read_bytes())==actual['capture_sha256'];rgb=Image.open(capture).convert('RGB')
    wanted={(16+i%228,296+i//228) for i,v in enumerate(calibration['physical']) if v};seen={(x,y) for y in range(296,360) for x in range(16,244) if rgb.getpixel((x,y))==(0,8,0)};assert wanted==seen
    cases=[];pictures=[];macro_calls=0;label_cases=[];FI_cases=[]
    for row in doc['records']:
        if row['kind']!='system-FE':continue
        profile=profile_for(arm,blocks[row['block']],'FE-paper');compiled=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile);assert compiled.encoded[:1]==b'\xfe'
        logical=row['english'].split('}',1)[1].replace('{MACRO:FI}','FI').replace('{MACRO:FA}','FA').replace('{MACRO:FO}','FO').encode('ascii');body=compiled.encoded[1:];pipelines=[]
        for kind,text in [('logical',logical),('compiled-protected',body)]:
            pipelines.append(dict(kind=kind,**ctx.execute(expand,text)));macro_calls+=4;ctx.machines.pop()
        expanded=body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        assert all(c['output_hex']==expanded.hex() for c in pipelines[1]['cases'])
        if b'FI' in body:
            assert row['id']=='DK4_MES_B53_R0006' and b'Lil?' in expanded and b'FI' not in expanded
            FI_cases.append(dict(id=row['id'],source_null_macro_actor_24310=True,complete_expanded_hex=expanded.hex(),all8_current_alignment_outputs_independently_equal=True))
        target=paint(expanded);assert target['complete_return_input_object_canaries_and_native_independent_plane_equal']
        visible=[e for e in target['events'] if e['code']!=32]
        origins={y:min(e['x'] for e in visible if e['y']==y) for y in sorted({e['y'] for e in visible})};assert all(x==0 for x in origins.values())
        label=row.get('English_visible_speaker_label')
        if label:
            assert row['source_visible_label_is_not_an_actor_or_spoken_sentence'] and row['source_visible_speaker_label'] in ['刺客','謎の女']
            assert b' '.join(expanded.split()).startswith((label+': ').encode('ascii')) and body.split(b'\n',1)[0].startswith((label+':').encode('ascii'))
            label_cases.append(dict(id=row['id'],source_label=row['source_visible_speaker_label'],English_label=label,first_row_complete_label_and_colon=True,no_new_actor_or_early_identity=True))
        else:assert row['id']=='DK4_MES_B146_R0031' and expanded==b'Meanwhile, Camille...'
        preview=ROOT/(row['id']+'_complete_physical.png');picture=Image.new('RGB',(228,64));picture.putdata([(0,8,0) if v else (239,232,201) for v in target['physical']]);picture.save(preview);pictures.append((row['id'],picture))
        plane=ROOT/(row['id']+'_complete_logical_228x48.bin');plane.write_bytes(target['logical'])
        cases.append(dict(id=row['id'],encoded_hex=compiled.encoded.hex(),formatted_markup=compiled.formatted_markup,expanded_hex=expanded.hex(),current_native_macro_pipelines=pipelines,
            native_glyphs=target['events'],one_native_page_consumes_complete_target=True,complete_native_independent_plane_and_all_glyphs_and_canaries_equal=True,all_visible_origins_zero_and4rows=True,visible_origins_by_row=origins,
            native_plane=str(plane),native_plane_sha256=sha(target['logical']),whole_physical228x64_plane_sha256=sha(target['physical']),preview=str(preview),preview_sha256=sha(preview.read_bytes()),object_rebindings=target['object_rebindings']))
    assert len(cases)==22 and macro_calls==176 and len(label_cases)==21 and len(FI_cases)==1 and not ctx.machines
    sheets=[]
    for start in range(0,len(pictures),8):
        sheet=Image.new('RGB',(952,640),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,picture) in enumerate(pictures[start:start+8]):
            x,y=i%2*476,i//2*160;draw.text((x+5,y+3),ident+' / FE paper',fill='white');sheet.paste(picture.resize((456,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=ROOT/f'current_FE_sheet{start//8+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    calibration_path=ROOT/'historical_FE_calibration.png';rgb.crop((12,290,248,370)).resize((472,160),Image.Resampling.NEAREST).save(calibration_path)
    save(ROOT/'current_FE_macro_font_and_typed_paper_proof.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),COMMON_sha256=sha(common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),cases=cases,current_original_null_actor_macro_alignment_cases=176,
        logical_geometry=[228,48],physical_geometry=[228,64],physical_rows_advance=16,logical_rows_advance=12,current_cold_typed_graphics_object_construction=True,no_initialized_historical_RAM_ITCM_or_DTCM_overlay_in_painter=True,
        all22_one_native_page_consumes_complete_target=True,all22_complete_native_independent_planes_all_glyphs_and_canaries_equal=True,all21_source_literal_speaker_labels_preserved=label_cases,source_FI_null_actor_cases=FI_cases,
        scoped_profile='dk4tool/dialogue/lil_kuhn_china_profile.py',scoped_profile_sha256=sha(Path('dk4tool/dialogue/lil_kuhn_china_profile.py').read_bytes()),native_formatter_module='dk4tool/dialogue/lil_kuhn_china_layout_v1.py',native_formatter_module_sha256=sha(Path('dk4tool/dialogue/lil_kuhn_china_layout_v1.py').read_bytes()),
        historical_calibration=dict(capture=str(capture),capture_sha256=actual['capture_sha256'],complete_current_native_ink_and_blank_mask_equal=True,preview=str(calibration_path),preview_sha256=sha(calibration_path.read_bytes()),not_selected_or_current_gameplay=True),
        source_captured_context=str(OBS),source_captured_context_sha256=sha(Path(OBS).read_bytes()),prior_actual_FE_rule=str(PRIOR),prior_actual_FE_rule_sha256=sha(PRIOR.read_bytes()),review_sheets=sheets,visual_review_pending=True,
        native_macro_context_plan=str(ctx.proof_path),native_macro_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_selected_Kuhn_China_IDs=[],new_emulator_runs=0,reference_and_release_still_pending=True,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('22FE current complete planes/176null-actor macro cases,including FI. All21literal labels andone caption preserved;historical whole-ink/blank calibration exact. Three sheets need visual review;no selected gameplay claim.')
