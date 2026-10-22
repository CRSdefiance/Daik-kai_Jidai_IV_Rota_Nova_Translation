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
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_text_surface_v1112')
ROM=Path('out/all_routes_combined_v1105_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/sighting_grammar_v1106b_1105_compassReady8')
BASE=0x02000000


def execute(arm,raw,text,font):
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
    clears=[];draw={}
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
        draw.update(context=context,string=pointer,expanded_hex=value.hex(),
            initial_x=struct.unpack('<i',u.mem_read(context+36,4))[0],
            initial_y=struct.unpack('<i',u.mem_read(context+40,4))[0])
    def returned(u,pc,size,data):draw['consumed_bytes']=u.reg_read(UC_ARM_REG_R0)-draw['string']
    hooks=[cpu.hook_add(UC_HOOK_CODE,clear,begin=0x01FFB2DC,end=0x01FFB2DC),
        cpu.hook_add(UC_HOOK_CODE,entry,begin=BASE+0xD5404,end=BASE+0xD5404),
        cpu.hook_add(UC_HOOK_CODE,returned,begin=BASE+0xDAC4,end=BASE+0xDAC4)]
    try:get(0xDA28,owner,string,0,60)
    finally:
        for hook in hooks:cpu.hook_del(hook)
    assert len(clears)==1 and len(registration)==1
    assert bytes(cpu.mem_read(string,len(text)+1))==text+b'\0'
    assert bytes(cpu.mem_read(header,20))==struct.pack('<5I',*h)
    assert all(bytes(cpu.mem_read(at,len(value)))==value for at,value in guards)
    packed=bytes(cpu.mem_read(pixel_base,pixel_bytes));native=bytes(1 if (b>>shift)&15 else 0 for b in packed for shift in (0,4))
    assert draw['initial_x']==0 and draw['initial_y']==12
    expected=bytearray(208*36);full_ink=visible_ink=0
    for i,ch in enumerate(text.decode('ascii')):
        glyph=font.decode(ch)
        for y in range(11):
            for x in range(6):
                if glyph.getpixel((x,y)):
                    xx=i*6+x;yy=12+y;full_ink+=1
                    if xx<208:expected[yy*208+xx]=1
                    if xx<144:visible_ink+=1
    assert native==bytes(expected),'Native source plane differs from independent glyphs;do not approve a clipped model'
    source_ink=sum(native);visible=bytes(native[y*208+x] for y in range(36) for x in range(144))
    return {'text':text.decode('ascii'),'source_backing_canvas':[208,36],'native_widget_rectangle':list(rectangle),
        'original_macro_output_exact':True,'native_draw_context':draw,'SDK_full_plane_clear_boundary_modeled':clears,
        'only_widget_registration_and_SDK_clear_boundaries_bridged':True,
        'source_bitmap_matches_independent_full_glyphs_clipped_to_backing_canvas':True,
        'full_expected_ink':full_ink,'native_source_ink':source_ink,'actual_final_crop_ink':sum(visible),
        'ink_outside_final_crop':full_ink-visible_ink,'source_return_consumes_complete_string':draw['consumed_bytes']==len(text),
        'all_source_input_header_and_pixel_neighbor_guards_preserved':True},native,visible


def main():
    assert not ROOT.exists()
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes())=='64b1da09fe0f75007af73b0f44a39ce9d2d3c6dedbb70cf6c0ca20223a7f1c29'
    for lo,hi in ((0xDA28,0xDB5C),(0xDB8C,0xDEBC),(0xDEF4,0xE1B0),(0xCFC14,0xCFD6C),(0xCF2C4,0xCF348)):
        assert arm[lo:hi]==clean[lo:hi]
    table=struct.unpack_from('<I',clean,0xDEB8)[0];assert table==0x0211460C
    crops=[struct.unpack_from('<7i',clean,table-BASE+i*28) for i in range(3)]
    assert crops==[(-1,4,4,0,0,144,12),(-1,4,24,0,12,144,12),(-1,4,44,0,24,144,12)]
    assert arm[table-BASE:table-BASE+84]==clean[table-BASE:table-BASE+84]
    report=read(CAP/'capture_report.json');snapshot=CAP/'frame_005310_arm9_ram.bin';raw=snapshot.read_bytes()
    row=next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame']==5310)
    assert sha(raw)==row['sha256'] and report['ROM_sha256']==sha(ROM.read_bytes())
    cpu,get=get_machine(arm,raw);actors=get(0xCB184);obj=actors+4+28*32;vt=struct.unpack('<I',cpu.mem_read(obj,4))[0]
    assert get(0x7EE08,obj)==28
    getter=struct.unpack('<I',cpu.mem_read(vt+0x24,4))[0];pointer=get(getter-BASE,obj)
    name=bytes(cpu.mem_read(pointer,128)).split(b'\0')[0];assert name and name.isascii()
    current=current_entries(common,arm);doc=read('translations/duel_editorial_manuscript_v2.json')
    source_text=current[1931].text.replace(b'%s',name);texts=[('current1931',source_text)]
    for r in doc['records']:
        if r['message_id'] in (1931,1932,1939,1949):texts.append((f'draft{r["message_id"]}',r['english'].encode('ascii').replace(b'%s',name)))
    font=GameAsciiFont.from_arm9(arm);results=[];pictures=[]
    ROOT.mkdir(parents=True)
    for label,text in texts:
        case,native,visible=execute(arm,raw,text,font);case['case']=label
        path=ROOT/(label+'_source208_and_final144.png')
        canvas=Image.new('RGB',(852,190),'#263238');draw=ImageDraw.Draw(canvas)
        draw.text((4,4),label+' / source208x36',fill='white')
        im=Image.frombytes('L',(208,36),bytes(0 if v else 255 for v in native));canvas.paste(im.resize((832,144),Image.Resampling.NEAREST),(4,22))
        draw.text((4,168),'Visible native crop:144 pixels /24 ASCII cells per row;3 rows',fill='white')
        canvas.save(path);case.update(preview=str(path),preview_sha256=sha(path.read_bytes()))
        results.append(case);pictures.append(path)
    assert results[0]['ink_outside_final_crop']==0
    assert any(r['ink_outside_final_crop']>0 for r in results[1:])
    save(ROOT/'native_duel_surface_proof.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'current_snapshot':str(snapshot),'current_snapshot_sha256':sha(raw),'actual_native_opponent_actor_ID':28,
        'original_name_getter':getter,'original_opponent_name_hex':name.hex(),'source_table':table,
        'final_native_crop_requests':[list(r) for r in crops],'visible_ASCII_columns':24,'visible_rows':3,
        'source_canvas_width_is_not_visible_width':True,'cases':results,
        'native_macro_measurement_constructor_and_glyph_path_execute':True,
        'SDK_graphics_clear_and_widget_registration_are_explicit_boundary_models_not_native_or_GPU_proof':True,
        'current_single_line_y12_centering_would_hide_wrapped_third_row_without_correct_postexpansion_measurement':True,
        'new_33_formatting_gates_remain_false_and_no_ROM_or_gameplay_change':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1267
    ledger['duel_prose_v1103'].update(native_surface_proof=str(ROOT/'native_duel_surface_proof.json'),
        native_duel_visible_columns=24,native_duel_visible_rows=3,
        formatting_status='original backing208x36 is finally cropped to144x36;postexpansion24x3 layout and measured centering required;not approved')
    save(ledger_path,ledger)
    print('Original duel constructor/measurement/glyphs mapped:208x36 backing,144px/24-cell final crops,3 rows. Unwrapped drafts lose visible ink despite full byte consumption;no formatting approval.',flush=True)


if __name__=='__main__':main()
