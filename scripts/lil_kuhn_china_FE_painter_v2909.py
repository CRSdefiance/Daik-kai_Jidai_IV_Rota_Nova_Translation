"""Same typed FE painter as the sealed2901b proof, for final parity targets."""
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


BASE=0x02000000
PRIOR=Path('work/analysis/lil_FE_display_v1737/actual_paper_contract_and_all9_reviewed_FE_panels.json')
PROOF=Path('work/analysis/lil_Kuhn_China_FE_v2901b/current_FE_macro_font_and_typed_paper_proof.json')

def make_painter(image):
    arm=image.read_file('/__arm9__.bin');proof=read(PROOF)
    assert sha(arm)==proof['ARM9_sha256'] and proof['all22_complete_native_independent_planes_all_glyphs_and_canaries_equal']
    assert proof['all22_one_native_page_consumes_complete_target']
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
    return paint,dict(source_proof=str(PROOF),source_proof_sha256=sha(PROOF.read_bytes()),current_calibration_matches_complete_historical_ink_and_blank_mask=True,capture=str(capture),capture_sha256=actual['capture_sha256'])
