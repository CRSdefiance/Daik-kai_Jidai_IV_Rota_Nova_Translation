"""Execute original duel text preparation;derive final crops,not backing width."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC,UC_ARM_REG_LR,UC_ARM_REG_SP
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.sighting_grammar_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine as base_machine
from scripts.probe_button_prompt_native import STACK
from scripts.verify_village_wrap_v608 import read,save
from scripts.duel_postmacro_layout_v1134 import layout,trailing_ascii_phase

ROOT=Path('work/analysis/duel_compiled_fonts_v1136')
ROM=Path('out/all_routes_combined_v1105_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/sighting_grammar_v1106b_1105_compassReady8')
BASE=0x02000000


def execute(arm,raw,text,font,kanji):
    cpu,get=get_machine(arm,raw);owner,string=0x02460000,0x02468000
    cpu.mem_write(owner,bytes(0x200));cpu.mem_write(string,text+b'\0')
    get(0xE14C,owner)
    registration=[]
    def register(u,pc,size,data):
        assert u.reg_read(UC_ARM_REG_R0)==owner
        registration.append({'widget':owner,'native_registration_boundary':pc})
        u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    hook=cpu.hook_add(UC_HOOK_CODE,register,begin=BASE+0xD351C,end=BASE+0xD351C)
    try:get(0xDEF4,owner)
    finally:cpu.hook_del(hook)
    view=owner+0x3C;header=struct.unpack('<I',cpu.mem_read(view+16,4))[0]
    h=struct.unpack('<5I',cpu.mem_read(header,20));assert h[:3]==(4,52,36)
    assert struct.unpack('<2I',cpu.mem_read(view+40,8))==(208,36)
    rectangle=struct.unpack('<4i',cpu.mem_read(owner+32,16));assert rectangle==(52,16,204,80)
    pixel_base=(header+h[4])&0xFFFFFFFF;pixel_bytes=208*36//2
    guards=[(pixel_base-16,bytes(cpu.mem_read(pixel_base-16,16))),
        (pixel_base+pixel_bytes,bytes(cpu.mem_read(pixel_base+pixel_bytes,16)))]
    clears=[];draw={};events=[]
    def clear(u,pc,size,data):
        image,color,point,extent=[u.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3)]
        origin=struct.unpack('<2i',u.mem_read(point,8));dimensions=struct.unpack('<2i',u.mem_read(extent,8))
        assert image==header and color==0 and origin==(0,0) and dimensions==(208,36)
        assert tuple(struct.unpack('<5I',u.mem_read(image,20)))==h
        # This SDK graphics routine lies outside the ROM autoload sections in
        # the CPU harness. Model ONLY its observed full-plane zero-fill ABI.
        # Macro processing,measurement,context creation and glyph drawing run.
        u.mem_write(pixel_base,bytes(pixel_bytes));clears.append({'image':image,'origin':list(origin),'dimensions':list(dimensions),'color':color})
        u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    def entry(u,pc,size,data):
        context,pointer=[u.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1)]
        value=bytes(u.mem_read(pointer,512)).split(b'\0')[0]
        output,lines=layout(text)
        assert value==output,'Compiled code output differs at original font entry'
        assert context-pointer==0x400 and len(output)<0x400
        assert struct.unpack('<i',u.mem_read(context+40,4))[0]==(12 if len(lines)==1 else 0)
        # Read-only reference check. Native compiled code already produced all
        # text bytes and the private Y value;Python changes neither.
        draw.update(context=context,string=pointer,expanded_hex=value.hex(),
            generated_postmacro_hex=output.hex(),generated_lines=lines,

            initial_x=struct.unpack('<i',u.mem_read(context+36,4))[0],
            initial_y=struct.unpack('<i',u.mem_read(context+40,4))[0])
    macro=[]
    def before_compiled(u,pc,size,data):
        pointer=u.reg_read(UC_ARM_REG_R1)
        value=bytes(u.mem_read(pointer,128)).split(b'\0')[0]
        assert value==text
        macro.append(value.hex())
    def returned(u,pc,size,data):draw['consumed_bytes']=u.reg_read(UC_ARM_REG_R0)-draw['string']
    def glyph_event(u,pc,size,data):
        code,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8))
        events.append({'kind':'cp932' if pc==0x01FF83AC else 'ascii','code':code,'style':style,'x':u.reg_read(UC_ARM_REG_R2),'y':u.reg_read(UC_ARM_REG_R3)})
        if pc==0x01FF83AC:
            assert struct.unpack('<I',u.mem_read(u.reg_read(UC_ARM_REG_R0)+12,4))[0]==0
    hooks=[cpu.hook_add(UC_HOOK_CODE,before_compiled,begin=THUNK,end=THUNK),
        cpu.hook_add(UC_HOOK_CODE,glyph_event,begin=0x01FF83AC,end=0x01FF83AC),
        cpu.hook_add(UC_HOOK_CODE,glyph_event,begin=BASE+0xD16B4,end=BASE+0xD16B4),
        cpu.hook_add(UC_HOOK_CODE,clear,begin=0x01FFB2DC,end=0x01FFB2DC),
        cpu.hook_add(UC_HOOK_CODE,entry,begin=BASE+0xD5404,end=BASE+0xD5404),
        cpu.hook_add(UC_HOOK_CODE,returned,begin=BASE+0xDAC4,end=BASE+0xDAC4)]
    try:get(0xDA28,owner,string,0,60)
    finally:
        for hook in hooks:cpu.hook_del(hook)
    assert len(clears)==1 and len(registration)==1 and macro==[text.hex()]
    assert bytes(cpu.mem_read(string,len(text)+1))==text+b'\0'
    assert bytes(cpu.mem_read(header,20))==struct.pack('<5I',*h)
    assert all(bytes(cpu.mem_read(at,len(value)))==value for at,value in guards)
    packed=bytes(cpu.mem_read(pixel_base,pixel_bytes));native=bytes((b>>shift)&15 for b in packed for shift in (0,4))
    assert draw['initial_x']==0 and draw['initial_y']==(12 if len(draw['generated_lines'])==1 else 0)
    expected,expected_letters=expected_plane(arm,kanji,font,draw['generated_lines'])
    full_ink=sum(bool(value) for value in expected)
    assert [(e['kind'],e['code'],e['x'],e['y']) for e in events if e['code']!=32]==expected_letters
    assert all(e['style']==15 and 0<=e['x'] and e['x']+(12 if e['kind']=='cp932' else 6)<=144 and 0<=e['y'] and e['y']+12<=36 for e in events)
    assert native==bytes(expected),'Complete native font plane differs from independently laid-out source words'
    source_ink=sum(bool(value) for value in native);visible=bytes(native[y*208+x] for y in range(36) for x in range(144))
    outside_source=[e for e in events if e['x']+(12 if e['kind']=='cp932' else 6)>208 or e['y']+12>36]
    outside_crop=[e for e in events if e['x']+(12 if e['kind']=='cp932' else 6)>144 or e['y']+12>36]
    first=font.decode(chr(text[0]));first_damaged=any(
        native[(draw['initial_y']+y)*208+x]!=15*int(y<11 and bool(first.getpixel((x,y)))) for y in range(12) for x in range(6))
    requests=[]
    def gpu(u,pc,size,data):
        size_pointer,destination_pointer=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8))
        requests.append({'image':u.reg_read(UC_ARM_REG_R1),
            'source':list(struct.unpack('<2i',u.mem_read(u.reg_read(UC_ARM_REG_R3),8))),
            'size':list(struct.unpack('<2i',u.mem_read(size_pointer,8))),
            'destination':list(struct.unpack('<2i',u.mem_read(destination_pointer,8)))})
        u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    point=0x02469000;renderer=0x02469100
    cpu.mem_write(point,struct.pack('<2i',52,16));cpu.mem_write(renderer,struct.pack('<I',0x0215FA94))
    cpu.mem_write(STACK,struct.pack('<3I',0,point,0))
    hook=cpu.hook_add(UC_HOOK_CODE,gpu,begin=0x01FF92D8,end=0x01FF92D8)
    try:get(0xCFC14,renderer,view,0x0211460C,3)
    finally:cpu.hook_del(hook)
    assert requests==[{'image':header,'source':[0,i*12],'size':[144,12],'destination':[56,20+i*20]} for i in range(3)]
    return {'text':text.decode('cp932'),'source_backing_canvas':[208,36],'native_widget_rectangle':list(rectangle),
        'original_macro_output_exact':True,'compiled_native_formatter_executed_before_original_painter':True,'native_draw_context':draw,'SDK_full_plane_clear_boundary_modeled':clears,
        'widget_registration_and_SDK_clear_bridged_GPU_submission_captured_not_rendered':True,
        'whole_source_plane_exact_to_independently_laid_out_complete_words_and_font':True,
        'observed_native_glyphs':events,
        'odd_trailing_ASCII_run_flush_is_one_invisible_space_not_authored_text':bool(trailing_ascii_phase(draw['generated_lines'][-1])),'glyphs_crossing_source_rows':outside_source,
        'glyphs_outside_final_visible_crop':outside_crop,'first_glyph_damaged_by_later_stride_spill':first_damaged,
        'original_renderer_three_final_crop_submissions':requests,'compiled_native_formatter_has_complete_correct_visible_layout':True,
        'full_expected_ink':full_ink,'native_source_ink':source_ink,'actual_final_crop_ink':sum(bool(value) for value in visible),
        'glyph_ink_absent_from_final_crop':full_ink-sum(bool(value) for value in visible),'native_font_consumes_complete_generated_string':draw['consumed_bytes']==len(bytes.fromhex(draw['generated_postmacro_hex'])),
        'all_source_input_header_and_pixel_neighbor_guards_preserved':True},native,visible



def expected_plane(arm,kanji,font,lines):
    mapping=struct.unpack_from('<3340H',arm,0x125EC4)
    plane=bytearray(208*36);letters=[]
    for row,line in enumerate(lines):
        ybase=12 if len(lines)==1 else row*12
        xbase=0
        for character in line:
            raw=character.encode('cp932');width=len(raw)*6
            code=int.from_bytes(raw,'big');kind='ascii' if len(raw)==1 else 'cp932'
            if character!=' ':letters.append((kind,code,xbase,ybase))
            if kind=='ascii':
                glyph=font.decode(character)
                for y in range(12):
                    for x in range(6):
                        plane[(ybase+y)*208+xbase+x]=15*int(y<11 and bool(glyph.getpixel((x,y))))
            else:
                assert code in mapping
                index=mapping.index(code);cell=kanji[index*22:(index+1)*22]
                for y in range(12):
                    for x in range(12):plane[(ybase+y)*208+xbase+x]=0
                for y in range(11):
                    for x in range(11):
                        if cell[y*2+x//8]&(0x80>>(x%8)):
                            plane[(ybase+y)*208+xbase+x]=15
                # Independent original D1898 bottom-to-top lower-right shadow.
                for y in range(11,0,-1):
                    for x in range(11):
                        if plane[(ybase+y-1)*208+xbase+x] and not plane[(ybase+y)*208+xbase+x+1]:
                            plane[(ybase+y)*208+xbase+x+1]=14
            xbase+=width
    return plane,letters



THUNK=0x0247A000
COMPILER_PATH=Path('work/analysis/duel_layout_native_v1133/compiler_provenance.json')


def get_machine(arm,raw):
    from keystone import Ks,KS_ARCH_ARM,KS_MODE_ARM
    compiler=read(COMPILER_PATH);binary=Path(compiler['binary']).read_bytes()
    assert sha(binary)==compiler['binary_sha256']
    cpu,get=base_machine(arm,raw)
    cpu.mem_write(0x02470000,binary)
    assembly=f"""push {{r4-r6,lr}}
mov r4,r0
mov r5,r1
mov r0,r1
ldr r3,formatter
blx r3
cmp r0,#1
mov r1,#0
moveq r1,#12
str r1,[r4,#40]
mov r0,r4
mov r1,r5
bl 0x020d5404
pop {{r4-r6,pc}}
formatter: .word {compiler['entry']}
"""
    ka=Ks(KS_ARCH_ARM,KS_MODE_ARM)
    thunk=bytes(ka.asm(assembly,THUNK)[0])
    cpu.mem_write(THUNK,thunk)
    branch=bytes(ka.asm(f'bl {THUNK}',BASE+0xDAC0)[0])
    cpu.mem_write(BASE+0xDAC0,branch)
    return cpu,get


def main():
    assert not ROOT.exists()
    compiler=read(COMPILER_PATH)
    matrix_path=Path('work/analysis/duel_native_layout_v1134/compiled_native_DP_matrix.json')
    matrix=read(matrix_path)
    assert matrix['all4700_native_outputs_match_independent_physical_phase_DP']
    assert sha(Path(compiler['binary']).read_bytes())==compiler['binary_sha256']
    catalog_path=Path('work/analysis/duel_scope_names_v1117b/source_name_layout_catalogue.json')
    catalog=read(catalog_path)
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');kanji=rom.read_file('/GRP/KANJI.FNT')
    assert sha(ROM.read_bytes())==catalog['candidate_sha256']
    raw=Path(catalog['snapshot']).read_bytes();assert sha(raw)==catalog['snapshot_sha256']
    font_base=struct.unpack_from('<I',arm,0xD19B8)[0]-BASE
    assert raw[font_base:font_base+len(kanji)]==kanji
    assert kanji==NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT')
    selected=[];seen=set()
    for row in matrix['cases']:
        key=(row['message_ID'],row['input_hex'])
        if key in seen:continue
        seen.add(key);selected.append(row)
    assert len(selected)>=2820
    font=GameAsciiFont.from_arm9(arm);results=[];previews=[]
    ROOT.mkdir(parents=True)
    for row in selected:
        text=bytes.fromhex(row['input_hex'])
        case,native,visible=execute(arm,raw,text,font,kanji)
        assert case['native_draw_context']['generated_postmacro_hex']==row['generated_hex']
        assert case['compiled_native_formatter_has_complete_correct_visible_layout']
        assert case['native_font_consumes_complete_generated_string']
        assert case['glyph_ink_absent_from_final_crop']==0
        assert not case['first_glyph_damaged_by_later_stride_spill']
        case.update(message_ID=row['message_ID'],source_kind=row['kind'],
            source_208x36_4bit_SHA256=sha(native),visible_144x36_4bit_SHA256=sha(visible))
        case.pop('SDK_full_plane_clear_boundary_modeled')
        case.pop('original_renderer_three_final_crop_submissions')
        results.append(case)
        if row['message_ID'] in (1931,1933,1938,1944) and len(previews)<12 and (
                row['kind']=='legal-name-stress' and not text.isascii() or
                row['kind']=='source' and (b'Clifford' in text or b'\x82\x65ernando' in text or row['message_ID']==1944)):
            path=ROOT/f'native_compiled_{len(previews):02d}_ID{row["message_ID"]}.png'
            canvas=Image.new('RGB',(864,198),'#263238');draw=ImageDraw.Draw(canvas)
            draw.text((4,4),f'Compiled native formatter + original font/crops; CPU research; ID{row["message_ID"]}',fill='white')
            im=Image.frombytes('L',(144,36),bytes(255-v*17 for v in visible))
            canvas.paste(im.resize((864,144),Image.Resampling.NEAREST),(0,30));canvas.save(path)
            previews.append({'path':str(path),'sha256':sha(path.read_bytes()),'message_ID':row['message_ID']})
        if len(results)%400==0:print(f'Compiled native formatter + complete font/crops:{len(results)}/{len(selected)}',flush=True)
    assert len(results)==len(selected)
    proof=ROOT/'compiled_native_complete_fonts.json'
    save(proof,{'candidate':str(ROM),'candidate_sha256':catalog['candidate_sha256'],
        'compiler_provenance':str(COMPILER_PATH),'native_layout_matrix':str(matrix_path),
        'unique_complete_font_cases':len(results),'all_source_names_and_legal_name_stress_included':True,
        'cases':results,'research_previews':previews,'KANJI_font_sha256':sha(kanji),
        'original_macro_constructor_ASCII_CP932_fonts_and_three_crop_submissions_execute':True,
        'native_compiled_layout_and_private_Y_execute_without_Python_replacement':True,
        'Python_oracle_only_reads_and_compares_output_and_font_pixels':True,
        'CPU_only_trampoline_is_unconditionally_inserted_into_DA28_for_declared_case_inputs':THUNK,
        'production_caller_scope_and_owned_code_placement_not_yet_implemented':True,
        'boundary_models':['SDK clear','UI registration','GPU submission capture'],
        'not_actual_emulator_playback_or_a_playable_ROM_change':True,
        'all33_formatting_gates_still_false':True,'no_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    path=Path('translations/editorial_review_current_v1.json');ledger=read(path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1267
    ledger['duel_prose_v1103'].update(compiled_native_complete_fonts=str(proof),
        formatting_status='compiled-native-layout-and-complete-fonts-pass;production-scope-owned-placement-integration-actual-open')
    save(path,ledger)
    print(f'{len(results)} complete compiled-native font/crop cases pass;production-scope/owned-placement/integration/actual still open.',flush=True)


if __name__=='__main__':main()
