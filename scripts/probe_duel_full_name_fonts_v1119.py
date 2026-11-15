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
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_button_prompt_native import STACK
from scripts.verify_village_wrap_v608 import read,save
from scripts.duel_postmacro_layout_v1119 import layout,trailing_ascii_phase

ROOT=Path('work/analysis/duel_full_name_fonts_v1119')
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
        assert value==text
        output,lines=layout(value)
        assert context-pointer==0x400 and len(output)<0x400
        # Controlled CPU prototype at the post-macro font boundary. Only the
        # callers own expanded-text buffer and its private Y cursor change.
        # This is NOT an assembled runtime fix or an emulator injection.
        u.mem_write(pointer,output+b'\0')
        u.mem_write(context+40,struct.pack('<i',12 if len(lines)==1 else 0))
        draw.update(context=context,string=pointer,expanded_hex=value.hex(),
            generated_postmacro_hex=output.hex(),generated_lines=lines,

            initial_x=struct.unpack('<i',u.mem_read(context+36,4))[0],
            initial_y=struct.unpack('<i',u.mem_read(context+40,4))[0])
    def returned(u,pc,size,data):draw['consumed_bytes']=u.reg_read(UC_ARM_REG_R0)-draw['string']
    def glyph_event(u,pc,size,data):
        code,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8))
        events.append({'kind':'cp932' if pc==0x01FF83AC else 'ascii','code':code,'style':style,'x':u.reg_read(UC_ARM_REG_R2),'y':u.reg_read(UC_ARM_REG_R3)})
        if pc==0x01FF83AC:
            assert struct.unpack('<I',u.mem_read(u.reg_read(UC_ARM_REG_R0)+12,4))[0]==0
    hooks=[cpu.hook_add(UC_HOOK_CODE,glyph_event,begin=0x01FF83AC,end=0x01FF83AC),
        cpu.hook_add(UC_HOOK_CODE,glyph_event,begin=BASE+0xD16B4,end=BASE+0xD16B4),
        cpu.hook_add(UC_HOOK_CODE,clear,begin=0x01FFB2DC,end=0x01FFB2DC),
        cpu.hook_add(UC_HOOK_CODE,entry,begin=BASE+0xD5404,end=BASE+0xD5404),
        cpu.hook_add(UC_HOOK_CODE,returned,begin=BASE+0xDAC4,end=BASE+0xDAC4)]
    try:get(0xDA28,owner,string,0,60)
    finally:
        for hook in hooks:cpu.hook_del(hook)
    assert len(clears)==1 and len(registration)==1
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
        'original_macro_output_exact':True,'native_draw_context':draw,'SDK_full_plane_clear_boundary_modeled':clears,
        'widget_registration_and_SDK_clear_bridged_GPU_submission_captured_not_rendered':True,
        'whole_source_plane_exact_to_independently_laid_out_complete_words_and_font':True,
        'observed_native_glyphs':events,
        'odd_trailing_ASCII_run_flush_is_one_invisible_space_not_authored_text':bool(trailing_ascii_phase(draw['generated_lines'][-1])),'glyphs_crossing_source_rows':outside_source,
        'glyphs_outside_final_visible_crop':outside_crop,'first_glyph_damaged_by_later_stride_spill':first_damaged,
        'original_renderer_three_final_crop_submissions':requests,'CPU_prototype_has_complete_correct_visible_layout':True,
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


def main():
    assert not ROOT.exists()
    names_path=Path('work/analysis/duel_scope_names_v1117b/source_name_layout_catalogue.json')
    catalog=read(names_path)
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');kanji=rom.read_file('/GRP/KANJI.FNT')
    assert sha(ROM.read_bytes())==catalog['candidate_sha256']
    raw=Path(catalog['snapshot']).read_bytes();assert sha(raw)==catalog['snapshot_sha256']
    font_base=struct.unpack_from('<I',arm,0xD19B8)[0]-BASE
    assert raw[font_base:font_base+len(kanji)]==kanji
    assert kanji==NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT')
    names={row['name_hex']:row for row in catalog['names']}
    records=read('translations/duel_editorial_manuscript_v3.json')['records']
    assert len(names)==141
    font=GameAsciiFont.from_arm9(arm);results=[];samples=[]
    ROOT.mkdir(parents=True)
    corrected=[]
    for item in catalog['all4160_complete_word_layouts']:
        paragraph=bytes.fromhex(item['paragraph_hex'])
        output,lines=layout(paragraph)
        assert lines==item['lines']
        corrected.append({**item,'generated_hex':output.hex(),
            'trailing_ASCII_run_parity_after_last_double_byte_glyph':True})
    assert len(corrected)==4160
    save(ROOT/'all4160_source_name_layouts_corrected_phase.json',{
        'original_name_catalogue':str(names_path),'original_name_catalogue_sha256':sha(names_path.read_bytes()),
        'layouts':corrected,'prior_total_byte_parity_encoding_is_superseded_not_a_font_pass':True,
        'complete_words_and_all_name_bytes_preserved':True})
    for index,(name_hex,name) in enumerate(sorted(names.items())):
        argument=bytes.fromhex(name_hex)
        for record in records:
            number=record['message_id']
            if number>=1951:continue
            text=record['english'].encode('ascii').replace(b'%s',argument)
            case,native,visible=execute(arm,raw,text,font,kanji)
            assert case['CPU_prototype_has_complete_correct_visible_layout'] and case['native_font_consumes_complete_generated_string']
            assert case['glyph_ink_absent_from_final_crop']==0 and not case['first_glyph_damaged_by_later_stride_spill']
            case.update(actor_slot=name['actor_slot'],native_actor_ID=name['actor_ID'],name_hex=name_hex,message_ID=number,
                entire_208x36_4bit_plane_SHA256=sha(native),entire_144x36_visible_4bit_plane_SHA256=sha(visible))
            # Compact sufficient evidence retains all glyph requests and line output.
            case.pop('SDK_full_plane_clear_boundary_modeled')
            case.pop('original_renderer_three_final_crop_submissions')
            results.append(case)
            if not argument.isascii() and number in (1931,1938):
                path=ROOT/f'name{ name["actor_slot"] }_message{number}_CPU_research.png'
                canvas=Image.new('RGB',(864,198),'#263238');draw=ImageDraw.Draw(canvas)
                draw.text((4,4),f'CPU research only: native name slot{name["actor_slot"]}, message{number}',fill='white')
                im=Image.frombytes('L',(144,36),bytes(255-v*17 for v in visible))
                canvas.paste(im.resize((864,144),Image.Resampling.NEAREST),(0,30));canvas.save(path)
                samples.append({'path':str(path),'sha256':sha(path.read_bytes())})
        if (index+1)%20==0:print(f'Complete native names:{index+1}/141;full planes:{len(results)}',flush=True)
    assert len(results)==2820 and all(not row['glyphs_crossing_source_rows'] and not row['glyphs_outside_final_visible_crop'] for row in results)
    proof=ROOT/'native_all_source_names_font_proof.json'
    save(proof,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'native_name_catalogue':str(names_path),'native_name_catalogue_sha256':sha(names_path.read_bytes()),
        'source_slots208_unique_actual_IDs207_unique_name_strings141':True,
        'all2820_full_native_ASCII_CP932_planes_match_independent_complete_font_masks_and_shadows':True,
        'all20_duel_drafts_all_source_names_fit_without_truncated_letters_or_authored_indents':True,
        'original_KANJI_font_sha256':sha(kanji),'current_snapshot_contains_exact_original_KANJI_font':True,
        'cases':results,'research_previews':samples,
        'explicit_boundary_models':['SDK clear','widget registration','Python post-macro24x3 layout'],
        'original_constructor_measurement_macro_ASCII_CP932_painters_and_crop_submissions_execute':True,
        'not_assembled_runtime_or_actual_gameplay':True,'all33_formatting_gates_still_pending':True,
        'mixed_phase_counterexample_retained':'work/analysis/duel_full_name_failure_v1118/first_CP932_request_failure.json',
        'phase_uses_trailing_ASCII_run_after_last_double_byte_glyph_not_whole_row_byte_count':True,
        'layout_module_sha256':sha(Path('scripts/duel_postmacro_layout_v1119.py').read_bytes()),
        'no_ROM_registry_runtime_or_completion_credit_change':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    path=Path('translations/editorial_review_current_v1.json');ledger=read(path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1267
    ledger['duel_prose_v1103'].update(native_all_source_name_fonts=str(proof),
        corrected_all4160_source_name_phase_catalogue=str(ROOT/'all4160_source_name_layouts_corrected_phase.json'),
        all2820_CPU_native_font_planes_include_preserved_fullwidth_names=True,
        formatting_status='all-source-name-CPU-prototype-fonts-pass;assembled-runtime-owned-storage-integration-and-actual-still-pending')
    save(path,ledger)
    print('2820 complete native name/font cases pass;runtime/storage/integration/actual gates remain open.',flush=True)


if __name__=='__main__':main()
