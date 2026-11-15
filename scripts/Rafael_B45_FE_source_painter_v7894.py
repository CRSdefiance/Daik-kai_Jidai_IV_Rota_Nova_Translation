"""Current FE typed-paper CP932 painter; complete original code, objects, font and guards."""
import struct
from pathlib import Path
from types import SimpleNamespace
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from scripts.square_shopkeeper_font_oracles_v7020 import make_painter as ASCII_painter,PROGRESSIVE_ORACLE_SOURCE,CURRENT_ARM9
from scripts.verify_name_catalog_glyphs_v278 import expected_pixels as old_expected
from scripts.prove_lil_B208_name_planes_v6405 import codes

def make_source_painter(image):
    prior,calibration=ASCII_painter(image)
    fields=dict(zip(prior.__code__.co_freevars,(c.cell_contents for c in prior.__closure__),strict=True))
    arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT')
    assert sha(arm)==CURRENT_ARM9 and fields['arm']==arm and fields['image'].read_file('/GRP/KANJI.FNT')==font
    context0,view0,header0,font0,palette=[fields[k] for k in ['actual_ctx','actual_view','actual_header','actual_font','palette']]
    assert context0[1:6]==[0,0,228,48,1] and view0[10:16]==[228,48,0,0,228,48]
    assert font0[1:3]==[6,12] and header0[:3]==[4,72,48]
    cold_machine,call=prior.__globals__['cold_machine'],prior.__globals__['call']
    env={**old_expected.__globals__,'WIDTH':288,'HEIGHT':48}
    exec(compile(PROGRESSIVE_ORACLE_SOURCE,__file__+'::same-current-font-ink-on-original288-stride','exec'),env)
    expected=env['expected_pixels']
    sections=MainCodeFile(arm,BASE).sections;payload=bytes(sections[3].data[:-48]);assert len(payload)==123264
    executable=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)]
    def paint(text):
        assert text and b'\0' not in text
        cpu=cold_machine(arm);cpu.mem_write(POOL,payload);executed=set()
        def exact(u,pc,size,unused):
            owners=[s for s in executable if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
            assert len(owners)==1,hex(pc)
            s=owners[0];at=pc-s.ramAddress
            assert bytes(u.mem_read(pc,size))==bytes(s.data[at:at+size]),hex(pc)
            executed.add(pc)
        ch=cpu.hook_add(UC_HOOK_CODE,exact)
        header,view,context,string=0x02450000,0x02453000,0x02454000,0x02660000
        hd=header0.copy();hd[3]=(palette-header)&0xFFFFFFFF;hd[4]=20
        vw=view0.copy();vw[4]=header;ct=context0.copy();ct[11]=view
        head=struct.pack('<5I',*hd);size=288*48//2
        cpu.mem_write(header-16,b'\xA5'*(20+size+32));cpu.mem_write(header,head+bytes(size))
        cpu.mem_write(view-16,b'\xA5'*132);cpu.mem_write(view,struct.pack('<25I',*vw))
        cpu.mem_write(context-16,b'\xA5'*108);cpu.mem_write(context,struct.pack('<19I',*ct))
        font_object=struct.unpack_from('<I',arm,0xD5088)[0]
        assert font_object==fields['captured']['font_metrics_object']
        cpu.mem_write(font_object,struct.pack('<6I',*font0))
        cpu.mem_write(struct.unpack_from('<I',arm,0xD19B8)[0],font)
        cpu.mem_write(string-16,b'\xA5'*(len(text)+33));cpu.mem_write(string,text+b'\0')
        events=[]
        def observe(u,pc,size,unused):
            if pc not in [BASE+0xD16B4,0x01FF83AC]:return
            code,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8))
            events.append(dict(kind='ascii' if pc==BASE+0xD16B4 else 'cp932',code=code,style=style,
                x=u.reg_read(UC_ARM_REG_R2),y=u.reg_read(UC_ARM_REG_R3)))
        gh=cpu.hook_add(UC_HOOK_CODE,observe)
        try:call(cpu,0x01FFCE40-BASE,(context,string),instruction_limit=1000000)
        finally:cpu.hook_del(gh);cpu.hook_del(ch)
        assert cpu.reg_read(UC_ARM_REG_R0)==string+len(text) and bytes(cpu.mem_read(string,len(text)+1))==text+b'\0'
        assert bytes(cpu.mem_read(string-16,16))==bytes(cpu.mem_read(string+len(text)+1,16))==b'\xA5'*16
        assert bytes(cpu.mem_read(header,20))==head and bytes(cpu.mem_read(header-16,16))==bytes(cpu.mem_read(header+20+size,16))==b'\xA5'*16
        assert bytes(cpu.mem_read(view-16,16))==bytes(cpu.mem_read(view+100,16))==b'\xA5'*16
        assert bytes(cpu.mem_read(context-16,16))==bytes(cpu.mem_read(context+76,16))==b'\xA5'*16
        visible=[e for e in events if e['code']!=32]
        assert [e['code'] for e in visible]==[c for c in codes(text) if c not in [32,10]]
        assert len(visible)==len({(e['x'],e['y']) for e in visible})
        assert all(0<=e['x'] and e['x']+(6 if e['kind']=='ascii' else 12)<=228 and e['y'] in [0,12,24,36] for e in visible)
        native=bytes(n for b in cpu.mem_read(header+20,size) for n in [b&15,b>>4])
        assert native==expected(arm,font,events,canvas_height=48)
        logical=bytes(native[y*288+x] for y in range(48) for x in range(228));physical=bytearray(228*64)
        for y in range(48):
            for x in range(228):physical[(y//12*16+y%12)*228+x]=logical[y*228+x]
        return dict(logical=logical,physical=bytes(physical),events=events,complete_consumed_bytes=len(text),
            all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact=True,
            original228x48_bitmap_288stride_6x12_metrics_16physical_pitch_preserved=True,
            input_bitmap_header_view_context_canaries_andcomplete_return_exact=True,
            all_executed_instructions_exact_current_sections_andpayload=True,current_executed_instruction_addresses=len(executed),
            object_rebindings=dict(header=header,view=view,context=context,palette=palette,pixels=header+20,font=font_object))
    return paint,dict(current_ASCII_painter_calibration=calibration,
        source_typed_descriptors_from_same_current_validated_factory=True,
        current_font_mapping_andCP932_shadow_model_preserved_on_native288_stride=True,
        source_helper_sha256=sha(Path(__file__).read_bytes()),actual_source_FE_palette_andscene_comparison_pending=True)
